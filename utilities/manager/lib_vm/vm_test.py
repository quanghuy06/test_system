# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      26/06/2018
# Description:      This script define class for a virtual machine that test
#                   PHOcr on linux platform.
import os
import sys
import pexpect
import traceback
from abc import ABCMeta, abstractmethod
from multiprocessing import Process, Queue
from configs.command import VirtualBox, BuildConfiguration
from configs.compare_result import CompareResultConfig
from configs.database import TestcaseConfig, SpecKeys
from configs.test_result import TestResultConfig, FinalTestResult
from configs.timeout import TimeOut
from manager.lib_vm.virtual_machine import VirtualMachine
from handlers.test_result_handler import TestResultHandler
from handlers.test_spec_handler import TestSpecHandler
from handlers.compare_handlers.compare_result_handler import CompareResultHandler
from baseapi.file_access import copy_paths, copy_globs, copy_ignore_exists,\
    get_test_set, remove_a_path, read_json, write_json, remove_globs
from baseapi.common import get_unique_list
from tests.compare_all import CompareAll
from configs.projects.mekong import MekongProject
from tests.combine_all_mem_peak import MemPeakCombination
from tests.lib_comparison.compare_runner import CompareRunner
import shutil

def execute_compare(platform, test_result, test_folder, output_file, output_folder,
                    exception_queue):
    """
    Execute compare test results on the thread which control processes on virtual machine over
    ssh connection. This comparison will run on node environment after we receive test results
    from virtual machine.

    Parameters
    ----------
    platform: str
        Platform for comparison linux/windows
    test_result: str
        Path to test result json file
    test_folder: str
        Path to folder which includes test cases/ specification of test cases
    output_file: str
        Path to output file of compare result in json format
    output_folder: str
        Path to folder which storage output of comparison
    exception_queue: Queue
        Queue of exception which is raised when executing comparison

    Returns
    -------
    None

    """
    try:
        # Initial comparison executor
        cmp_executor = CompareAll(test_folder=test_folder,
                                  platform=platform,
                                  test_result=test_result,
                                  output_file=output_file,
                                  output_folder=output_folder)
        # Run comparison processes
        cmp_executor.do_work()
    except:
        # Collect exception/errors from executing comparison
        var = traceback.format_exc()
        exception_queue.put(var)


def execute_combine_mem_peak(platform, test_folder, test_file, output_file, exception_queue):
    """
    Combine memory peak data from test results of virtual machine

    Parameters
    ----------
    platform: str
        Platform of virtual machine
    test_folder: str
        Path to test folder which includes test cases/ specification of test cases
    test_file: str
        Path to test result json file
    output_file: str
        Path to output of memory peak report for this virtual machine
    exception_queue: Queue
        List of exception which is raised when executing memory peak data combination

    Returns
    -------
    None

    """
    try:
        # Initial memory peak data combinator
        combine_executor = MemPeakCombination(test_folder=test_folder,
                                              platform=platform,
                                              test_result=test_file,
                                              output_file=output_file)
        # Run data combination
        combine_executor.do_work()
    except:
        # Collect exception/errors when something wrong
        var = traceback.format_exc()
        exception_queue.put(var)


class VirtualMachineTest(VirtualMachine):
    __metaclass__ = ABCMeta

    # Name of snapshot which will be used for testing
    SNAPSHOT_TEST = "Clean-State"

    # Name of snapshot which will used as backup when we create new snapshot for updating data on
    # test virtual machine. This prevents we lost clean state when something happen on updating
    # data out of control
    SNAPSHOT_BACKUP = "Clean-State-Backup"

    def __init__(self, **kwargs):
        """
        This is a abstract class which help to manage processes on virtual machine for test job
        over ssh connection.

        """
        super(VirtualMachineTest, self).__init__(working_state=VirtualBox.snapshot.STATE_TEST,
                                                 **kwargs)
        self.configuration = None
        if self.info_handler:
            # Build package
            self.hanoi_package = \
                self.info_handler.get_hanoi_package_release(self.platform)
            self.build_folder = \
                self.info_handler.get_folder_specific() + "_" + self.platform
        # Test result folder of worker
        self.test_result_worker = \
            os.path.join(self.platform + "_results", self.name)
        self.test_set_worker = os.path.join(self.test_result_worker,
                                            TestcaseConfig.FOLDER_DEFAULT)

    @abstractmethod
    def prepare_shared_folder(self):
        """
        Make shared folder between node and virtual machine for a faster way to transfer data
        between node and virtual machine than using ssh copy.

        Returns
        -------
        None

        """
        pass

    def prepare_work(self):
        """
        Transfer data from node to virtual machine which are necessary for testing on virtual
        machine

        Returns
        -------
        None

        """
        # Add shared folder transient
        self.prepare_shared_folder()

        # Get Mekong utilities
        self.logger.start_step("Get Mekong utilities")
        self.get_mekong_utilities()
        self.logger.end_step(True)

        # Prepare build packages
        self.prepare_build_packages()

        # Install packages
        self.logger.start_step("Install packages")
        self.install_packages()
        self.logger.end_step(True)

        # Worker get test cases
        self.logger.start_step("Send test cases to worker")
        self.send_test_cases_to_worker()
        self.logger.end_step(True)

    def run_test(self):
        """
        Execute command which calls to run_all.py to run test on virtual machine over ssh connection

        Returns
        -------
        None

        """
        name_folder_mem = TestcaseConfig.FOLDER_DEFAULT + "_" + BuildConfiguration.info.MEMORY
        name_folder_rel = TestcaseConfig.FOLDER_DEFAULT + "_" + BuildConfiguration.info.RELEASE
        path_test_folder_test_mem = os.path.join(self.test_set_worker + "_" +
                                                 BuildConfiguration.info.MEMORY)
        path_test_folder_test_rel = os.path.join(self.test_set_worker + "_" +
                                                        BuildConfiguration.info.RELEASE)
        test_set_mem = sorted(get_test_set(path_test_folder_test_mem))
        test_set_rel = sorted(get_test_set(path_test_folder_test_rel))
        for test_id in test_set_rel:
            self.logger.start_step("Run test memory on worker")
            cmd = self.get_run_test_one_testcase_for_rel(test_id)
            self.exec_command(cmd, 1800000)
            self.send_result_to_test_case(test_id, name_folder_rel)
            self.compare_test_case(test_id)

        for test_id in test_set_mem:
            cmd = self.get_run_test_one_testcase_for_mem(test_id)
            self.logger.start_step("Run test release on worker")
            self.exec_command(cmd, 1800000)
            self.send_result_to_test_case(test_id, name_folder_mem)
            self.compare_test_case(test_id)
        self.logger.end_step(True)

    @abstractmethod
    def send_result_to_test_case(self, test_id, test_name):
        pass

    def get_mekong_utilities(self):
        """
        Copy Mekong utilities from node to test machine.

        Returns
        -------
        None

        """
        self.get(MekongProject.NAME, MekongProject.NAME)

    def send_test_cases_to_worker(self):
        """
        Copy test cases from node to virtual machine. Currently, we have 2 different test sets
        for different mode of build package:
        - Test set for normal testing which will use PHOcr build of ICC
        - Test set for memory leak checking which will use PHOcr build of GCC

        Returns
        -------
        None

        """
        test_set = sorted(get_test_set(self.test_set_worker))
        # Create test folder for release
        release_folder = self.test_set_worker + "_" + BuildConfiguration.info.RELEASE
        if os.path.exists(os.path.abspath(release_folder)):
            remove_a_path(os.path.abspath(release_folder))
        create_test_folder_for_release_cmd = "mkdir -p {0}".format(
            os.path.abspath(release_folder))
        pexpect.run(create_test_folder_for_release_cmd)
        # Create test folder for memory testing
        memcheck_folder = self.test_set_worker + "_" + BuildConfiguration.info.MEMORY
        if os.path.exists(os.path.abspath(memcheck_folder)):
            remove_a_path(os.path.abspath(memcheck_folder))
        create_test_folder_for_memory_cmd = "mkdir -p {0}".format(
            os.path.abspath(memcheck_folder))
        pexpect.run(create_test_folder_for_memory_cmd)
        # Move test cases need to check memory or accuracy to matched folders
        for test_id in test_set:
            spec_file = os.path.join(os.path.abspath(self.test_set_worker),
                                     test_id, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            is_check_memory_leak = spec_handler.get_tag(
                SpecKeys.Tags.IS_MEMCHECK)
            is_check_memory_peak = False
            if spec_handler.has_tag(SpecKeys.Tags.IS_MEMCHECK_PEAK):
                is_check_memory_peak = spec_handler.get_tag(
                    SpecKeys.Tags.IS_MEMCHECK_PEAK)
            # Separate test case base on tag is memory testing or not
            if is_check_memory_leak or is_check_memory_peak:
                copy_ignore_exists(
                    os.path.join(os.path.abspath(self.test_set_worker),
                                 test_id), os.path.abspath(memcheck_folder))
            else:
                copy_ignore_exists(
                    os.path.join(os.path.abspath(self.test_set_worker),
                                 test_id), os.path.abspath(release_folder))
        des_path = TestcaseConfig.FOLDER_DEFAULT
        self.get(local_path=release_folder,
                 client_path=des_path + "_" + BuildConfiguration.info.RELEASE,
                 timeout=TimeOut.ssh.WORKER_GET_TEST_SET)
        self.get(local_path=memcheck_folder,
                 client_path=des_path + "_" + BuildConfiguration.info.MEMORY,
                 timeout=TimeOut.ssh.WORKER_GET_TEST_SET)

    def do_work(self):
        """
        This is the main method which execute every things from prepare data for testing,
        run testing and get test results from a virtual machine. After execute this one,
        we'll have test results from virtual machine if everything is good.

        Returns
        -------
        None

        """
        try:
            # Prepare for testing
            self.prepare_work()

            # Run test on workers
            self.run_test()

            # Get test results from workers
            self.post_process()
        except:
            var = traceback.format_exc()
            if self.log_level >= 0:
                self.logger.log_and_print(var)
            self.work_done = False
        finally:
            # Finally remember to stop the worker to release resource
            self.logger.start_step("Stop virtual machine")
            self.stop()
            self.logger.end_step(True)

    def post_process(self):
        """
        Copy test results from virtual machine to node then combine results to final folder on node

        Returns
        -------
        None

        """
        # Send test result json to node
        self.logger.start_step("Send test result json file to node")
        self.send_test_result_json_to_node(BuildConfiguration.info.RELEASE)
        self.send_test_result_json_to_node(BuildConfiguration.info.MEMORY)
        self.logger.end_step(True)

        # After that, we need to combine into one
        self.logger.start_step("Combine test result json file on node")
        self.combine_test_result_json()
        self.logger.end_step(True)

        # Put output test result to node
        self.logger.start_step("Copy test output from to node")
        self.put_test_output()
        self.logger.end_step(True)

        # After that, we need to copy test cases to TESTS folder
        self.logger.start_step("Combine test cases to final folder")
        self.combine_test_cases()
        self.logger.end_step(True)

        # Compare test result
        self.logger.start_step("Compare test output results")
        self.compare_result()
        self.logger.end_step(True)

        # Combine memory peak data into a report
        if self.info_handler.is_check_memory_peak():
            self.logger.start_step("Combine memory peak data")
            self.combine_mem_peak_data()
            self.logger.end_step(True)

        # Collect changed and error test cases
        self.logger.start_step("Collect changed and error test cases")
        self.collect_output()
        self.logger.end_step(True)

        # All processes done. Generate data for detail execution time of processes to json file
        self.logger.end(write_to_file=False)

    def combine_test_cases(self):
        """
        Copy all test cases on test result folder to a final place on node

        Returns
        -------
        None

        """
        # Because copy_globs can not override, so we need to delete sub-folders
        # in TESTS before
        test_folder = os.path.join(os.path.abspath(self.test_result_worker),
                                   TestcaseConfig.FOLDER_DEFAULT)
        remove_globs(globs=os.path.join(test_folder, "*"))
        # Copy test cases from TESTS_release folder into TESTS
        release_test_cases = os.path.join(os.path.abspath(self.test_result_worker),
                                          TestcaseConfig.FOLDER_DEFAULT +
                                          "_" + BuildConfiguration.info.RELEASE, "*")
        copy_globs(globs=release_test_cases, des=test_folder)
        # Copy test cases from TESTS_memory folder into TESTS
        memory_test_cases = os.path.join(os.path.abspath(self.test_result_worker),
                                         TestcaseConfig.FOLDER_DEFAULT +
                                         "_" + BuildConfiguration.info.MEMORY, "*")
        copy_globs(globs=memory_test_cases, des=test_folder)

    def combine_test_result_json(self):
        """
        Collect test results json data from virtual machine and write them to the final test
        results json file for all virtual machines of node. Currently, we need to collect data of
        both normal testing mode and memory testing mode

        Returns
        -------
        None

        """
        final_combine_result = {}
        # Combine test result of release
        release_test_result_json = os.path.join(self.test_result_worker,
                                                BuildConfiguration.info.RELEASE +
                                                "_" + TestResultConfig.FILE_DEFAULT)
        release_result = read_json(release_test_result_json)
        for test_name in release_result:
            final_combine_result[test_name] = release_result[test_name]
        # Combine test result of memory
        memory_test_result_json = os.path.join(self.test_result_worker,
                                               BuildConfiguration.info.MEMORY +
                                               "_" + TestResultConfig.FILE_DEFAULT)
        memory_result = read_json(memory_test_result_json)
        for test_name in memory_result:
            final_combine_result[test_name] = memory_result[test_name]
        write_json(obj=final_combine_result,
                   file_name=os.path.join(self.test_result_worker,
                                          TestResultConfig.FILE_DEFAULT))

    def send_test_result_json_to_node(self, build_mode):
        """
        Send test result json file from test machine to node.

        Returns
        -------
        None

        """
        self.put(client_path=build_mode + "_" + TestResultConfig.FILE_DEFAULT,
                 local_path=self.test_result_worker)

    @abstractmethod
    def put_test_output(self):
        """
        Currently, we use different mechanism to copy test output from virtual machine to node
        between a linux machine and a windows machine. Then this method is defined as abstract
        class and need to be implemented on derive classes

        Returns
        -------
        None

        """
        pass

    def compare_result(self):
        """
        Execute comparison for test output results which are received from virtual machine. This
        comparison is executed on node's environment.

        Returns
        -------
        None

        """
        output_file = os.path.join(self.test_result_worker,
                                   CompareResultConfig.FILE_DEFAULT)
        output_folder = os.path.join(self.test_result_worker,
                                     CompareResultConfig.FOLDER_DEFAULT)
        test_file = os.path.join(self.test_result_worker,
                                 TestResultConfig.FILE_DEFAULT)
        exception_queue = Queue()
        # Need to create a new process to execute comparison. This prevent
        # conflict of using os.chdir() of CompareRunner
        processes = [Process(target=execute_compare,
                             args=(self.platform,
                                   test_file,
                                   self.test_set_worker,
                                   output_file,
                                   output_folder, exception_queue))]
        for p in processes:
            p.start()

        for p in processes:
            p.join()

        if exception_queue.qsize() > 0:
            raise Exception(exception_queue.get())

    def compare_test_case(self, test_id):
        output_file = os.path.join(self.test_set_worker + "_Stream", test_id,
                                   CompareResultConfig.FILE_DEFAULT)
        output_folder = os.path.join(self.test_set_worker + "_Stream", test_id,
                                     CompareResultConfig.FOLDER_DEFAULT)
        os.makedirs(output_folder)
        test_folder = os.path.join(self.test_set_worker + "_Stream", test_id)
        platform = self.platform
        runner = CompareRunner()
        results = {}
        try:
            run_infor = runner.run(test_folder, test_id,
                                   platform, output_folder)
            results[test_id] = run_infor
        except Exception as e:
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)
        write_json(results, output_file)

    def combine_mem_peak_data(self):
        """
        Combine memory peak information in the case testing to check memory peak

        Returns
        -------
        None

        """
        output_file = os.path.join(self.test_result_worker,
                                   TestResultConfig.MEM_PEAK_FILE)
        test_file = os.path.join(self.test_result_worker,
                                 TestResultConfig.FILE_DEFAULT)
        exception_queue = Queue()
        # Need to create a new process to execute comparison. This prevent
        # conflict of using os.chdir() of CompareRunner
        processes = [Process(target=execute_combine_mem_peak,
                             args=(self.platform,
                                   self.test_set_worker,
                                   test_file,
                                   output_file,
                                   exception_queue))]
        for p in processes:
            p.start()

        for p in processes:
            p.join()

        if exception_queue.qsize() > 0:
            raise Exception(exception_queue.get())

    @abstractmethod
    def get_run_test_command(self):
        """
        Generate command which uses run_all.py to run test on virtual machine. Currently,
        we are using different path of python between linux machine and windows machine. Then
        this method need to be implemented on derive classes

        Returns
        -------
        str
            Command to run test on virtual machine

        """
        pass

    @abstractmethod
    def get_run_test_one_testcase_for_rel(self, test_id):
        pass

    @abstractmethod
    def get_run_test_one_testcase_for_mem(self, test_id):
        pass

    @abstractmethod
    def install_packages(self):
        """
        Execute processes to install build packages to be ready for testing

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def prepare_build_packages(self):
        """
        Prepare build packages to be ready for testing normally.

        Returns
        -------
        None

        """
        pass

    def collect_output(self):
        """
        After we receive test output results from virtual machine, currently, we only need to get
        changed or error test cases output and no need to get test cases which not changed to
        reduce time.

        Returns
        -------
        None

        """
        test_file = os.path.join(self.test_result_worker,
                                 TestResultConfig.FILE_DEFAULT)
        compare_file = os.path.join(self.test_result_worker,
                                    CompareResultConfig.FILE_DEFAULT)
        test_result_handler = TestResultHandler(input_file=test_file,
                                                test_folder=self.test_set_worker)
        compare_result_handler = \
            CompareResultHandler(input_file=compare_file,
                                 test_folder=self.test_set_worker)
        platform_folder = os.path.join(TestResultConfig.FOLDER_DEFAULT,
                                       self.platform)
        # Copy changed test cases
        changed_folder = os.path.join(platform_folder, FinalTestResult.CHANGE)
        changed_by_compare_list = compare_result_handler.get_list_changed_tests()
        changed_by_compare_list = get_unique_list(changed_by_compare_list)

        # Copy spec
        self.copy_tests_spec(test_list=test_result_handler.get_list_tests())

        # Collect error test cases
        error_folder = os.path.join(platform_folder, FinalTestResult.ERROR)
        error_list = test_result_handler.get_list_error_tests() + \
            compare_result_handler.get_list_error_compare() + \
            compare_result_handler.get_list_failed_tests() + \
            test_result_handler.get_list_output_0B(None, self.platform) + \
            test_result_handler.get_list_test_cases_missing_output(None,
                                                                   self.platform)
        error_list = get_unique_list(error_list)
        changed_list = []
        for test_case in changed_by_compare_list:
            if test_case not in error_list:
                changed_list.append(test_case)

        # Get output of comparison
        self.copy_output_compare(list_tests=changed_list,
                                 des_path=changed_folder)
        self.copy_output_tests(list_tests=changed_list, des_path=changed_folder)
        self.copy_output_tests(list_tests=error_list, des_path=error_folder)

    # Copy output of run test
    def copy_output_tests(self, list_tests, des_path):
        """
        By collecting changed/error test cases, we only need their test output, other data is not
        necessary.

        Parameters
        ----------
        list_tests: list
            List of test cases which need to be collected test output
        des_path: str
            Path to directory which will storage test output of changed/error test cases on node.
            This directory should be ready to send from node to master.

        Returns
        -------
        None

        """
        if not os.path.isdir(des_path):
            try:
                os.makedirs(des_path)
            except:
                pass
        for test_name in list_tests:
            test_case_folder = os.path.join(des_path, test_name)
            if not os.path.isdir(test_name) and not os.path.exists(
                    test_case_folder):
                os.makedirs(test_case_folder)
            need_copy = [TestcaseConfig.OUTPUT_FOLDER,
                         TestcaseConfig.REF_DATA_DIR,
                         TestcaseConfig.GROUND_TRUTH_DATA_DIR]
            for f in need_copy:
                src_path = os.path.join(self.test_set_worker, test_name, f)
                if os.path.exists(src_path):
                    copy_paths(src_path, test_case_folder)

    def copy_output_compare(self, list_tests, des_path):
        """
        Collect output of compare results. Same as test output, we only need to collect compare
        result of changed/error test cases.

        Parameters
        ----------
        list_tests: list
            List of test cases which need to be collected compare output
        des_path: str
            Path to directory which will store compare output for changed/error test cases. This
            directory should be ready for node to transfer to master.

        Returns
        -------
        None

        """
        if not os.path.isdir(des_path):
            try:
                os.makedirs(des_path)
            except:
                pass
        compare_folder = os.path.join(self.test_result_worker,
                                      CompareResultConfig.FOLDER_DEFAULT)
        for test_name in list_tests:
            final_compare_result = \
                os.path.join(des_path,
                             test_name,
                             CompareResultConfig.FOLDER_DEFAULT)
            try:
                os.makedirs(final_compare_result)
            except:
                pass
            compare_result_glob = os.path.join(compare_folder, test_name, "*")
            copy_globs(globs=compare_result_glob, des=final_compare_result)

    def copy_tests_spec(self, test_list):
        """
        We need to collect specification of all tested test cases. This information will be used
        for making reports on master.

        Parameters
        ----------
        test_list: list
            List of test cases need to be collected specification

        Returns
        -------
        None

        """
        for test_name in test_list:
            test_case_folder = os.path.join(self.test_set_worker, test_name)
            spec_file = os.path.join(test_case_folder, TestcaseConfig.SPEC_FILE)
            spec_folder = os.path.join(FinalTestResult.SPEC, test_name)
            if not os.path.isdir(spec_folder):
                try:
                    os.makedirs(spec_folder)
                except:
                    pass
            copy_paths(spec_file, spec_folder)
