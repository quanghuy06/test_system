# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      13/02/2018
# Description:      This script define class for board testing on platform linux
import os
import paramiko

from configs.board import Board
from manager.lib_vm.test_on_linux import TestOnLinux
from configs.command import CommandConfig
from configs.projects.phocr import PhocrProject
from configs.timeout import TimeOut
from configs.test_result import FinalTestResult
from configs.database import TestcaseConfig
from configs.projects.mekong import ValGrind
from configs.svn_resource import DataPathSVN
from configs.projects.mekong import TestSystem
from configs.projects.mekong import MekongProject
from configs.test_result import TestResultConfig


class TestOnBoardLinux(TestOnLinux):
    def __init__(self, **kwargs):
        super(TestOnBoardLinux, self).__init__(**kwargs)
        self.home_folder = os.path.join("/storage/Jenkins")
        hanoi_package_name = os.path.splitext(self.hanoi_package)[0]
        self.hanoi_target_dir = os.path.join(self.home_folder,
                                             hanoi_package_name)
        self.phocr_target_dir = os.path.join(self.home_folder,
                                             self.build_folder)

    def prepare_shared_folder(self):
        """
        This class implement for testing on board so this function will do nothing

        """
        pass

    def mount_shared_folder_on_vm(self):
        """
        This class implement for testing on board so this function will do nothing

        """
        pass

    def clean_test_machine(self):
        """
        Delete all old test data on board

        """
        cmd = "rm -rf {2}/*".format(self.username,
                                    self.ip,
                                    self.home_folder)

        self.exec_command(cmd=cmd, timeout=TimeOut.ssh.DELETE_DATA_ON_BOARD)

    def prepare_build_packages(self):
        # Get PHOcr build package
        self.logger.start_step("Get PHOcr build package")
        self.get(self.build_folder,
                 os.path.join(self.home_folder, self.build_folder),
                 timeout=TimeOut.ssh.GET_PHOCR_BUILD_LINUX)
        self.logger.end_step(True)

        # Get Hanoi build release package
        self.logger.start_step("Get Hanoi build release package")

        # Create Hanoi installed dir on VM
        hanoi_package_name = os.path.splitext(self.hanoi_package)[0]
        hanoi_installed_dir = os.path.join(self.home_folder, hanoi_package_name)
        make_hanoi_dir_cmd = "mkdir {0}".format(hanoi_installed_dir)
        self.exec_command(make_hanoi_dir_cmd)

        hanoi_installer_path = os.path.join(hanoi_package_name,
                                            self.hanoi_package)
        self.get(self.hanoi_package,
                 os.path.join(self.home_folder, hanoi_installer_path),
                 timeout=TimeOut.ssh.GET_HANOI_BUILD_LINUX)
        self.logger.end_step(True)

        # Get Mekong 3rd party using for run test
        self.get_mekong_3rd_using_for_test()

    def get_mekong_utilities(self):
        """
        Get Mekong utilities from node to test machine.

        """
        self.get(MekongProject.NAME,
                 os.path.join(self.home_folder, MekongProject.NAME))

    def send_test_cases_to_worker(self):
        """
        Send test case from node to worker.

        """
        self.logger.start_step("Send test cases to worker")
        des_path = os.path.join(self.home_folder, TestcaseConfig.FOLDER_DEFAULT)
        self.get(local_path=self.test_set_worker,
                 client_path=des_path,
                 timeout=TimeOut.ssh.WORKER_GET_TEST_SET)
        self.logger.end_step(True)

    def copy_hanoi_package_to_pho_build(self):
        self.logger.start_step("Copy Hanoi to phocr build dir")
        copy_hanoi_cmd = "cp -rn {0}/* {1}".format(self.hanoi_target_dir,
                                                   self.phocr_target_dir)
        self.exec_command(copy_hanoi_cmd)
        self.logger.end_step(True)

    def get_mekong_3rd_using_for_test(self):
        self.logger.start_step("Get valgrind for memory leak check")
        # Copy valgrind build package to worker
        valgrind_dir = os.path.join(self.svn_dir,
                                    DataPathSVN.MEKONG_3RD_PARTY_DIR,
                                    ValGrind.VALGRIND_PACKAGE)
        self.get(local_path=valgrind_dir,
                 client_path=os.path.join(self.home_folder,
                                          TestSystem.Paths.EXECUTABLES_DIR),
                 timeout=TimeOut.ssh.COPY_FILE)
        # Extract build package on worker
        extract_cmd = "tar xzf {0}".format(ValGrind.VALGRIND_PACKAGE)
        self.exec_command(cmd=extract_cmd,
                          cwd=os.path.join(self.home_folder,
                                           TestSystem.Paths.EXECUTABLES_DIR),
                          timeout=TimeOut.Default.EXTRACT_FILE)
        self.logger.end_step(True)

    def get_run_test_command(self):
        cmd = CommandConfig.set_phocr_env_for_board(self.phocr_target_dir,
                                                    Board.PYTHON_3_5_PATH)
        bin_folder = os.path.join(self.phocr_target_dir, PhocrProject.build.BIN)
        cmd += CommandConfig.py_run_all(os.path.join(self.home_folder,
                                                     FinalTestResult.Test.TESTSET_PREFIX),
                                        bin_folder,
                                        self.platform,
                                        self.home_folder)
        return cmd

    def put_test_output(self):
        # Send test output to node
        self.logger.start_step("Send output test to node")
        self.put(client_path=os.path.join(self.home_folder,
                                          TestcaseConfig.FOLDER_DEFAULT),
                 local_path=self.test_result_worker)
        self.logger.end_step(True)

    def send_test_result_json_to_node(self):
        """
        Send test result json file from test machine to node.

        """
        self.put(client_path=os.path.join(self.home_folder,
                                          TestResultConfig.FILE_DEFAULT),
                 local_path=self.test_result_worker)

    def start(self):
        pass

    def stop(self):
        pass
