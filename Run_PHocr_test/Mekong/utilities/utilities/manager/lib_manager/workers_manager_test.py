# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      25/06/2018
# Description:      This script define class for a virtual machine that build PHOcr on linux
#                   platform.
import os
import pexpect
import sys
import configs.common
from abc import ABCMeta
from baseapi.file_access import write_json, move_paths, remove_paths, \
    copy_paths, read_json
from baseapi.linux_file_access import linux_extract_tgz_file
from configs.command import CommandConfig, BuildConfiguration
from configs.common import Platform
from configs.compare_result import CompareResultConfig
from configs.database import TestcaseConfig
from configs.projects.phocr import PhocrProject
from configs.test_result import TestResultConfig, FinalTestResult
from configs.timeout import TimeOut
from handlers.compare_handlers.compare_result_handler import CompareResultHandler
from handlers.distribution_handler import DistributionHandler
from handlers.test_result_handler import TestResultHandler
from manager.lib_manager.workers_manager_class import WorkersManager
from utils.svn_helper import SVNHelper
from configs.svn_resource import DataPathSVN
from handlers.test_spec_handler import TestSpecHandler
from configs.common import Machines


class WorkersTestManager(WorkersManager):
    __metaclass__ = ABCMeta

    # Error code for missing test distribution file
    ERR_NO_MISSING_TEST_DISTRIBUTION = 2

    def __init__(self, distribution_file, **kwargs):
        """
        Constructor for workers management of testing.

        Parameters
        ----------
        distribution_file : str
            Test distribution file. This is information defines which test cases will be tested
            on which virtual machines. This is required for testing.
        """
        super(WorkersTestManager, self).__init__(**kwargs)
        # Parameters information is required for testing
        if not self.info_handler:
            self.logger.log_and_print("ERROR: Missing parameters information for testing")
            sys.exit(self.ERR_NO_MISSING_PARAMETERS)
        # Initial handler for test distribution information
        if not distribution_file:
            self.logger.log_and_print("ERROR: Missing distribution file")
            sys.exit(self.ERR_NO_MISSING_TEST_DISTRIBUTION)
        self.distribution = DistributionHandler(input_file=distribution_file)
        self.result_node_folder = os.path.join(os.getcwd(), "test_results_" + self.name)
        self.is_force_spec = False
        if os.path.isfile(TestcaseConfig.FORCE_SPEC_FILE):
            self.is_force_spec = True

    # Prepare for work by cleaning workspace
    def prepare_work(self):
        # Clean test result folder
        self.logger.start_step("Clean old results on working directory")
        if os.path.isdir(self.result_node_folder):
            remove_paths(self.result_node_folder)
        for platform in configs.common.SupportedPlatform:
            platform_folder = platform + "_results"
            if os.path.isdir(platform_folder):
                remove_paths(platform_folder)
        self.logger.end_step(True)

        # Update data svn on node
        self.logger.start_step("Update data for build packages on node")
        self.init_shared_folder()
        self.init_svn_folder()

        # Update for Hanoi old release
        self.update_hanoi_releases_svn()

        # Prepare build package for sending to test virtual machine
        self.prepare_build_dependencies_packages()
        self.logger.end_step(True)

        # Get test cases
        self.logger.start_step("Prepare test cases on node")
        if os.path.isdir(TestcaseConfig.FOLDER_DEFAULT):
            remove_paths(TestcaseConfig.FOLDER_DEFAULT)

        # Prepare test cases for workers
        self.logger.start_step("Distribute test cases to workers folder")
        total_tc = 0
        print("self.workers in worker_manager_test.py: {0}".format(self.workers))
        for worker in self.workers:
            print("worker in worker_manager_test.py: {0}".format(worker))
            platform_folder = worker.platform + "_results"
            print("platform_folder in worker_manager_test.py:{0}".format(platform_folder))
            if not os.path.isdir(platform_folder):
                os.makedirs(platform_folder)
            worker_tests_folder = os.path.join(platform_folder, worker.name,
                                               TestcaseConfig.FOLDER_DEFAULT)
            if not os.path.isdir(worker_tests_folder):
                os.makedirs(worker_tests_folder)
            test_list_db = self.distribution.get_test_set_worker_db(self.name, worker.name)
            print("test_list_db in worker_manager_test.py: {0}".format(test_list_db))
            print("woker_test_folder in worker_manager_test.py: {0}".format(worker_tests_folder))
            total_tc += len(test_list_db)
            count = 0
            for test_name in test_list_db:
                print("test_name in test_list_db: {0}".format(test_name))
                count += 1
                self.logger.log_and_print("[{0}][{1}/{2}] {3}".format(worker.name, count,
                                                                      len(test_list_db), test_name))
                if self.name == Machines.MASTER_MACHINE[Machines.NAME]:
                    directory_tc_of_node = Machines.MASTER_MACHINE[Machines.TC_FOLDER]
                else:
                    directory_tc_of_node = Machines.NODE_MACHINES[self.name][Machines.TC_FOLDER]
                src_path = os.path.join(directory_tc_of_node, test_name)
                print("src_path in worker:{0}".format(src_path))
                copy_paths(src_path, worker_tests_folder)
        self.logger.log_and_print("\nTotal test case in {0}: {1}".format(self.name, total_tc))
        self.logger.end_step(True)

    def prepare_build_dependencies_packages(self):
        if self.info_handler.get_project() == PhocrProject.NAME:
            if Platform.LINUX in configs.common.SupportedPlatform:
                self.prepare_work_for_phocr_linux()

    def prepare_work_for_phocr_linux(self):
        # NamLD: disable for ICC build
        # if self.info_handler.is_et() and not self.info_handler.is_build_hanoi():
        if True:
            self.logger.start_step("Get release build packages for testing")
            hanoi_release_dir = os.path.join(self.svn_dir,
                                             DataPathSVN.HANOI_RELEASE)
            hanoi_package = \
                self.info_handler.get_hanoi_package_release(self.platform)
            hanoi_build_path_linux = os.path.join(hanoi_release_dir,
                                                  Platform.LINUX,
                                                  hanoi_package)
            # Copy hanoi build package to current working directory
            copy_paths(hanoi_build_path_linux, os.getcwd())

        # Extract build package for release
        release_build_package = \
            self.info_handler.get_folder_specific() \
            + "_" \
            + Platform.LINUX \
            + "_" \
            + BuildConfiguration.info.RELEASE \
            + ".tgz"
        linux_extract_tgz_file(src_file=release_build_package)

        # Extract build package for memory
        memory_build_package = \
            self.info_handler.get_folder_specific() \
            + "_" \
            + Platform.LINUX \
            + "_" \
            + BuildConfiguration.info.MEMORY \
            + ".tgz"
        linux_extract_tgz_file(src_file=memory_build_package)

    def update_hanoi_releases_svn(self):
        self.logger.start_step("Update hanoi release packages on test node")
        # Update svn to get the newest Hanoi release
        hanoi_release_dir = os.path.join(self.svn_dir,
                                         DataPathSVN.HANOI_RELEASE)
        hanoi_releases_url = self.svn_resource.get_url(DataPathSVN.HANOI_RELEASE)
        svn_helper = SVNHelper(hanoi_releases_url,
                               hanoi_release_dir)
        if not svn_helper.is_checkouted():
            svn_helper.checkout()
        svn_helper.update()
        self.logger.end_step(True)

    # Get log and arrange final results folder
    def post_process(self):
        self.logger.start_step("Arrange test results from test virtual machines")
        # Create final test result folder
        move_paths(TestResultConfig.FOLDER_DEFAULT, self.result_node_folder)
        move_paths(FinalTestResult.SPEC, self.result_node_folder)
        self.workers = self.get_workers()
        total = len(self.workers)
        count = 1
        # Combine results from all workers
        for platform in configs.common.SupportedPlatform:
            final_test_result = {}
            final_test_file = os.path.join(self.result_node_folder,
                                           platform,
                                           TestResultConfig.FILE_DEFAULT)
            final_compare_result = {}
            final_compare_file = os.path.join(self.result_node_folder,
                                              platform,
                                              CompareResultConfig.FILE_DEFAULT)
            platform_folder = os.path.join(self.result_node_folder, platform)
            if not os.path.isdir(platform_folder):
                os.makedirs(platform_folder)
            for worker in self.workers:
                # Only combine results of success workers
                if worker.platform == platform and worker.name not in self.workers_not_done:
                    self.logger.log_and_print("[{0}/{1}] Combine results of {2}"
                                              "".format(count, total, worker.name))
                    result_folder_worker = os.path.join(worker.platform + "_results", worker.name)
                    test_file = os.path.join(result_folder_worker, TestResultConfig.FILE_DEFAULT)
                    test_result_handler = TestResultHandler(input_file=test_file)
                    for test_name in test_result_handler.data:
                        # Combine test result
                        final_test_result[test_name] = test_result_handler.data[test_name]
                    compare_file = os.path.join(result_folder_worker,
                                                CompareResultConfig.FILE_DEFAULT)
                    compare_result_handler = CompareResultHandler(input_file=compare_file)
                    for test_name in compare_result_handler.data:
                        final_compare_result[test_name] = \
                            compare_result_handler.data[test_name]
                    count += 1
            write_json(obj=final_test_result, file_name=final_test_file)
            write_json(obj=final_compare_result, file_name=final_compare_file)

            if self.info_handler.is_check_memory_peak():
                self.combine_mem_peak_info_on_node(platform)

        self.logger.end_step(True)

        # All work done. Generate execution time logging.
        self.generate_execution_time_data()

    def combine_mem_peak_info_on_node(self, platform):
        """
        Combine memory peak information on node by result sent from board.

        """
        final_combine_result = {}
        final_combine_file = os.path.join(self.result_node_folder,
                                          platform,
                                          TestResultConfig.MEM_PEAK_FILE)
        for worker in self.workers:
            # Only combine results of success workers
            count = 1
            if worker.platform == platform \
                    and worker.name not in self.workers_not_done:
                self.logger.log_and_print(
                    "Combine results of {0}".format(worker.name))
                result_folder_worker = os.path.join(
                    worker.platform + "_results", worker.name)
                mem_peak_file = os.path.join(result_folder_worker,
                                             TestResultConfig.MEM_PEAK_FILE)
                mem_peak_result = read_json(mem_peak_file)
                for test_name in mem_peak_result:
                    # Combine test result
                    final_combine_result[test_name] = mem_peak_result[test_name]
                count += 1
        write_json(obj=final_combine_result, file_name=final_combine_file)

    def get_workers(self):
        return self.distribution.get_testers_of_node(node_name=self.name,
                                                     profile_handler=self.profile_handler)

    @staticmethod
    def get_version_of_hanoi_from_name(installer_name):
        delta = [int(s) for s in installer_name.split() if s.isdigit()]
        if len(delta) == 1:
            return delta[0]
        elif len(delta) == 0:
            return 0
        error_msg = "Hanoi installer file name {0} does not correct!".format(installer_name)
        raise Exception(error_msg)

    # Combine results of success workers
    def combine_results_when_worker_not_done_exception(self):
        self.post_process()

    def force_spec_for_all_test_case(self, force_spec_info, test_folder):
        self.logger.start_step("Force specification")
        for test_id in os.listdir(test_folder):
            spec_file = os.path.join(TestcaseConfig.FOLDER_DEFAULT, test_id, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            spec_handler.force_spec(force_spec_info)
            if self.info_handler.is_checking_for_memory():
                spec_handler.update_execute_time_for_test_case(Platform.LINUX,
                                                               TimeOut.execute.RATIO_TIMEOUT_RUN_MEMORY_LEAK)
        self.logger.end_step(True)
