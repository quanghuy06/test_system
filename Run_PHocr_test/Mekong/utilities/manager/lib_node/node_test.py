# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      26/06/2018
# Description:      This script define base class for a test node.
import os
from manager.lib_node.node import Node
from configs.command import CommandConfig
import configs.common
from configs.test_result import FinalTestResult, FinalResult
from baseapi.file_access import copy_globs, copy_paths
from configs.database import TestcaseConfig
from configs.timeout import TimeOut
from configs.projects.hanoi import HanoiProject


class NodeTest(Node):

    def __init__(self, distribution_file, **kwargs):
        """
        Constructor for object which help control management a remote node over ssh connection
        from master

        Parameters
        ----------
        distribution_file: str
            Path to test distribution file which defines list of test cases that will be tested
            on which virtual machine.
        """
        self.distribution_path = distribution_file
        super(NodeTest, self).__init__(**kwargs)
        self.result_folder = "test_results_" + self.name
        self.final_changed_folder = None
        self.final_error_folder = None
        self.final_spec_folder = None

    def prepare_private_data(self):
        """
        Prepare data for testing. Some data need to be transfer from master to test nodes to
        provide information of work for node to manage it's virtual machines on testing.
        Currently, this includes:
        - Parameters json file
        - Test distribution file

        Returns
        -------
        None

        """
        # Get parameters json file
        self.logger.start_step("Get parameters file")
        self.get(local_path=self.info_handler.input_file,
                 client_path=self.working_dir)
        self.logger.end_step(True)

        # Get distribution file
        self.logger.start_step("Get distribution file")
        self.get(self.distribution_path, self.working_dir)
        self.logger.end_step(True)

        if self.info_handler.is_force_specification():
            if not os.path.isfile(TestcaseConfig.FORCE_SPEC_FILE):
                # Raise here because we expect file force spec is generated.
                raise Exception("File {0} to force specification doesn't exit!"
                                "".format(TestcaseConfig.FORCE_SPEC_FILE))
            else:
                self.logger.start_step("Get edited specification file")
                self.get(TestcaseConfig.FORCE_SPEC_FILE, self.working_dir)
                self.logger.end_step(True)

        # Get build packages
        for platform in configs.common.SupportedPlatform:
            # Get PHOcr build package
            build_folder = os.path.join(platform, FinalTestResult.BUILD)
            if os.path.isdir(build_folder):
                for f_name in os.listdir(build_folder):
                    if not HanoiProject.is_hanoi_installer(f_name):
                        # Get PHOcr build package
                        self.logger.start_step("Get {0} from master"
                                               .format(f_name))
                        build_path = os.path.join(build_folder, f_name)
                        self.get(local_path=build_path,
                                 client_path=self.working_dir)
                        self.logger.end_step(True)
                    else:
                        pass

                        # NamLD: Disable build Hanoi because ICC compiler
                        # Get Hanoi installer
                        # if self.info_handler.is_build_hanoi() \
                        #         or not self.info_handler.is_et():
                        #     self.get_hanoi_installer_from_master(platform)

    def get_hanoi_installer_from_master(self, platform):
        """
        Get Hanoi installer from master to node.

        Parameters
        ----------
        platform: str
            Platform supported.

        """
        hanoi_installer = \
            os.path.join(platform,
                         FinalTestResult.BUILD,
                         self.info_handler.get_hanoi_package_release(platform))
        self.logger.start_step("Get {0} from master".format(hanoi_installer))
        self.get(local_path=hanoi_installer,
                 client_path=self.working_dir)
        self.logger.end_step(True)

    def set_final_paths(self, platform):
        """
        Set up final result folders for a test platform

        Parameters
        ----------
        platform: str
            Tested platform on node

        Returns
        -------
        None

        """
        # Directory to storage changed test cases
        self.final_changed_folder = \
            FinalResult.FINAL_CHANGED_FOLDER.format(platform)
        # Directory to storage error test cases
        self.final_error_folder = \
            FinalResult.FINAL_ERROR_FOLDER.format(platform)
        # Directory to storage spec of test cases for making reports
        self.final_spec_folder = FinalResult.FINAL_SPEC_FOLDER

    # Send build result to master
    def post_process(self):
        """
        Copy test results folder from node to master then combine result of node to final folders
        on master

        Returns
        -------
        None

        """
        # copy test results from node to master
        self.logger.start_step("Copy test results from node to master")
        self.get_result_from_node()
        self.logger.end_step(True)

        # Combine test results of node to final folders on master
        self.logger.start_step("Combine test results to final folders on master")
        for platform in configs.common.SupportedPlatform:
            self.set_final_paths(platform=platform)
            platform_test_result = os.path.join(self.result_folder, platform)
            # Combine change folder
            if not os.path.isdir(self.final_changed_folder):
                os.makedirs(self.final_changed_folder)
            change_folder = os.path.join(platform_test_result,
                                         FinalTestResult.CHANGE)
            if os.path.isdir(change_folder):
                glob_f = os.path.join(change_folder, "*")
                copy_globs(glob_f, self.final_changed_folder)
            # Combine error folder
            if not os.path.isdir(self.final_error_folder):
                os.makedirs(self.final_error_folder)
            error_folder = os.path.join(platform_test_result,
                                        FinalTestResult.ERROR)
            if os.path.isdir(error_folder):
                glob_f = os.path.join(error_folder, "*")
                copy_globs(glob_f, self.final_error_folder)
            # Prepare spec of test cases for reporting
            if not os.path.isdir(self.final_spec_folder):
                os.makedirs(self.final_spec_folder)
            spec_folder = os.path.join(self.result_folder, FinalTestResult.SPEC)
            if os.path.isdir(spec_folder):
                for f in os.listdir(spec_folder):
                    f_path = os.path.join(spec_folder, f)
                    des_path = os.path.join(self.final_spec_folder, f)
                    if not os.path.isdir(des_path):
                        copy_paths(f_path, self.final_spec_folder)
        self.logger.end_step(True)

        # End of logging on node thread
        self.logger.end(write_to_file=False)

    def get_result_from_node(self):
        """
        This method will get all result from test node include: test case (include output),
        test_result.json, compare_result.json and log files.

        Returns
        -------
        None

        """
        node_test_result = os.path.join(self.working_dir,
                                        "test_results_" + self.name)
        self.put(client_path=node_test_result, local_path=os.getcwd())

    def get_run_command(self):
        """
        Generate command which use workers_manager.py to manage virtual machines on remote node
        to execute testing.

        Returns
        -------
        str
            Command which will be run on remote node to manage virtual machines to execute testing

        """
        return CommandConfig.node_test_command(node_name=self.name,
                                               distribution=self.distribution_path)

    def timeout(self):
        """
        Define time out of processes base on which is testing

        Returns
        -------
        int
            Time out of testing on remote node

        """
        if self.info_handler.is_test_on_board():
            # Testing on board
            if self.info_handler.is_check_memory_leak():
                # Memory leak checking on board
                return TimeOut.execute.NODE_TEST_MEMORY_LEAK_ONBOARD
            elif self.info_handler.is_check_memory_peak():
                # Memory peak checking on board
                return TimeOut.execute.NODE_TEST_MEMORY_PEAK_ONBOARD
            else:
                return TimeOut.execute.NODE_TEST_ON_BOARD
        else:
            if self.info_handler.is_check_memory_leak():
                # Memory leak checking
                return TimeOut.execute.NODE_TEST_MEMORY_LEAK
            elif self.info_handler.is_check_memory_peak():
                # Memory peak checking
                return TimeOut.execute.NODE_TEST_MEMORY_PEAK
            else:
                # Normal testing
                return TimeOut.execute.NODE_TEST
