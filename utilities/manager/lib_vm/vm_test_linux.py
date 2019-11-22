# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      25/06/2018
# Description:      This script define class for a virtual machine that test
#                   PHOcr on linux platform.
import os
from abc import ABCMeta
from manager.lib_vm.test_on_linux import TestOnLinux
from configs.command import CommandConfig, BuildConfiguration
from configs.projects.phocr import PhocrProject
from configs.timeout import TimeOut
from configs.test_result import FinalTestResult
from configs.database import TestcaseConfig
from manager.lib_vm.defines import VBShareFolder
from baseapi.file_access import copy_paths
from baseapi.linux_file_access import linux_copy_ignore_exist
from configs.projects.mekong import ValGrind
from configs.svn_resource import DataPathSVN
from configs.projects.mekong import TestSystem, TestSystemPaths

CMD_MOUNT_SHARE_FOLDER_ON_VM = 'sudo -S mount -t vboxsf -o uid={0},gid={1} {2} {3}'


class VmTestLinux(TestOnLinux):

    def __init__(self, **kwargs):
        """
        Constructor for class which help control thread to manage running test on a virtual machine

        Returns
        ----------
        None

        """
        super(VmTestLinux, self).__init__(**kwargs)
        # Home directory of user test on virtual machine
        self.home_dir = os.path.join("/home", self.username)
        # Directory to mount shared folder on virtual machine with node
        self.shared_folder = os.path.join(self.home_dir, VBShareFolder.NAME, self.name)
        # Get hanoi and phocr target directory on virtual machine
        hanoi_package_name = os.path.splitext(self.hanoi_package)[0]
        self.hanoi_target_dir = os.path.join(self.home_dir, hanoi_package_name)
        self.phocr_target_dir = os.path.join(self.home_dir, self.build_folder)

    def prepare_shared_folder(self):
        """
        Prepare shared folder between node and virtual machine for transferring data.

        Returns
        -------
        None

        """
        self.add_shared_folder_to_vm()
        self.mount_shared_folder_on_vm()

    def prepare_build_packages(self):
        """
        Prepare build packages to be ready for running test such as copying build packages
        to virtual machine, copying 3rd party to right location.

        Returns
        -------
        None

        """
        # Get PHOcr build package
        self.logger.start_step("Get PHOcr build package")
        # We need to copy 2 build versions of PHOcr
        release_build_folder = self.build_folder + "_" + BuildConfiguration.info.RELEASE
        memory_build_folder = self.build_folder + "_" + BuildConfiguration.info.MEMORY
        # Copy release build package of PHOcr to virtual machine
        self.get(release_build_folder, release_build_folder,
                 timeout=TimeOut.ssh.GET_PHOCR_BUILD_LINUX)
        # Copy build package for memory leak checking to virtual machine
        self.get(memory_build_folder,
                 memory_build_folder,
                 timeout=TimeOut.ssh.GET_PHOCR_BUILD_LINUX)
        self.logger.end_step(True)

        # Get Hanoi build release package
        self.logger.start_step("Get Hanoi build release package")

        # Create Hanoi installed directory on VM
        hanoi_folder = os.path.splitext(self.hanoi_package)[0]
        hanoi_installed_dir = os.path.join(self.home_dir, hanoi_folder)
        # make_hanoi_dir_cmd = "mkdir {0}".format(hanoi_installed_dir)
        # self.exec_command(make_hanoi_dir_cmd)
        self.make_directory(hanoi_installed_dir)
        # Copy hanoi build package to virtual machine
        hanoi_installer_path = os.path.join(hanoi_folder, self.hanoi_package)
        self.get(self.hanoi_package, hanoi_installer_path,
                 timeout=TimeOut.ssh.GET_HANOI_BUILD_LINUX)
        self.logger.end_step(True)

        # Get Mekong 3rd party using for run test
        self.prepare_mekong_3rd_on_vm()

    def copy_hanoi_package_to_pho_build(self):
        """
        Copy Hanoi build to build packages (using ICC and GCC).

        Returns
        -------
        None

        """
        self.logger.start_step("Copy Hanoi to phocr build dir")
        # Copy Hanoi to virtual machine in release build folder
        release_build_folder = \
            self.build_folder + "_" + BuildConfiguration.info.RELEASE
        copy_hanoi_for_release_cmd = "cp -rn {0}/* {1}".format(self.hanoi_target_dir,
                                                               release_build_folder)
        self.exec_command(copy_hanoi_for_release_cmd)
        # Copy Hanoi to virtual machine into build folder using GCC for memory leak checking
        memory_build_folder = self.build_folder +\
                              "_" +\
                              BuildConfiguration.info.MEMORY
        copy_hanoi_for_memory_cmd = "cp -rn {0}/* {1}".format(self.hanoi_target_dir,
                                                              memory_build_folder)
        self.exec_command(copy_hanoi_for_memory_cmd)
        self.logger.end_step(True)

    def prepare_mekong_3rd_on_vm(self):
        """
        Currently, these are mekong 3rd-party:
        - Valgrind utility for memory leak checking

        We already have extracted valgrind on virtual machine in Mekong data folder. All we need
        is to copy valgrind folder to executable path inside Mekong to make it work correctly.

        Returns
        -------
        None

        """
        # Prepare valgrind for Mekong memory leak checking
        self.logger.start_step("Prepare for memory leak check")
        src_valgrind_dir_on_vm =\
            os.path.join(self.home_dir, self.MEKONG_DATA_DIR, ValGrind.VALGRIND_FOLDER)
        des_executable_dir_mekong_on_vm =\
            os.path.join(self.home_dir, TestSystemPaths.EXECUTABLES_DIR)
        # Use virtual box native FS to copy valgrind utility to Mekong
        self.copy(client_src=src_valgrind_dir_on_vm, client_des=des_executable_dir_mekong_on_vm)
        self.logger.end_step(True)

    def get_run_test_command(self):
        """
        Generate linux command line to run test on virtual machines using run.py of Mekong. This
        command already include setting up environment variables.

        Returns
        -------
        str:
            Linux command to run test on virtual machine

        """
        # Environment variables for python
        python_dir_on_vm = os.path.join(self.home_dir, self.PHOCR_DATA_DIR,
                                        self.PYTHON_PORTABLE_DIR, DataPathSVN.PYTHON_FOLDER)
        # Path to training data on virtual machine for setting environment variables
        phocr_trained_data_dir_on_vm = os.path.join(self.home_dir,
                                                    self.PHOCR_DATA_DIR,
                                                    self.PHOCR_TRAINED_DATA_DIR)
        # Call run_all.py for FUNCTIONAL and PERFORMANCE TESTING
        phocr_target_dir_for_release = self.phocr_target_dir + "_" + BuildConfiguration.info.RELEASE
        # Set up environment variables
        cmd = CommandConfig.set_phocr_env(phocr_target_dir_for_release,
                                          phocr_trained_data_dir_on_vm, python_dir_on_vm)
        release_bin_folder = os.path.join(phocr_target_dir_for_release, PhocrProject.build.BIN)
        # Run command
        cmd += CommandConfig.py_run_all(FinalTestResult.Test.TESTSET_PREFIX +
                                        "_" + BuildConfiguration.info.RELEASE,
                                        release_bin_folder,
                                        self.platform,
                                        BuildConfiguration.info.RELEASE + "_")

        # Call run_all.py for MEMORY TESTING
        phocr_target_dir_for_memory = self.phocr_target_dir + "_" + BuildConfiguration.info.MEMORY
        # Set up environment variables
        cmd += " && " + CommandConfig.set_phocr_env(phocr_target_dir_for_memory,
                                                    phocr_trained_data_dir_on_vm, python_dir_on_vm)
        memory_bin_folder = os.path.join(phocr_target_dir_for_memory, PhocrProject.build.BIN)
        # Run command
        cmd += CommandConfig.py_run_all(FinalTestResult.Test.TESTSET_PREFIX +
                                        "_" + BuildConfiguration.info.MEMORY,
                                        memory_bin_folder,
                                        self.platform,
                                        BuildConfiguration.info.MEMORY + "_")
        return cmd

    def get_run_test_one_testcase_for_rel(self, test_id):
        """
        Get command set up environment variable for test release and run script run_one.py for one
        test case.

        Returns: cmd
        -------

        """
        # Environment variables for python
        python_dir_on_vm = os.path.join(self.home_dir, self.PHOCR_DATA_DIR,
                                        self.PYTHON_PORTABLE_DIR,
                                        DataPathSVN.PYTHON_FOLDER)
        # Path to training data on virtual machine for setting environment variables
        phocr_trained_data_dir_on_vm = os.path.join(self.home_dir,
                                                    self.PHOCR_DATA_DIR,
                                                    self.PHOCR_TRAINED_DATA_DIR)
        phocr_target_dir_for_release = self.phocr_target_dir + "_" + BuildConfiguration.info.RELEASE
        # Set up environment variables
        cmd = CommandConfig.set_phocr_env(phocr_target_dir_for_release,
                                          phocr_trained_data_dir_on_vm, python_dir_on_vm)
        release_bin_folder = os.path.join(phocr_target_dir_for_release, PhocrProject.build.BIN)
        # Run command
        cmd += CommandConfig.py_run_one(FinalTestResult.Test.TESTSET_PREFIX + "_" +
                                        BuildConfiguration.info.RELEASE,
                                        test_id,
                                        release_bin_folder,
                                        self.platform)

        return cmd

    def get_run_test_one_testcase_for_mem(self, test_id):
        """
        Get command set up environment variable for test memory and run script run_one.py for one
        test case

        Returns: cmd
        -------

        """
        # Environment variables for python
        python_dir_on_vm = os.path.join(self.home_dir, self.PHOCR_DATA_DIR,
                                        self.PYTHON_PORTABLE_DIR,
                                        DataPathSVN.PYTHON_FOLDER)
        # Path to training data on virtual machine for setting environment variables
        phocr_trained_data_dir_on_vm = os.path.join(self.home_dir,
                                                    self.PHOCR_DATA_DIR,
                                                    self.PHOCR_TRAINED_DATA_DIR)
        phocr_target_dir_for_memory = self.phocr_target_dir + \
                                      "_" + BuildConfiguration.info.MEMORY
        # Set up environment variables
        cmd = CommandConfig.set_phocr_env(phocr_target_dir_for_memory,
                                          phocr_trained_data_dir_on_vm, python_dir_on_vm)
        memory_bin_folder = os.path.join(phocr_target_dir_for_memory, PhocrProject.build.BIN)
        # Run command
        cmd += CommandConfig.py_run_one(FinalTestResult.Test.TESTSET_PREFIX + "_" +
                                        BuildConfiguration.info.MEMORY,
                                        test_id,
                                        memory_bin_folder,
                                        self.platform)
        return cmd

    def put_test_output(self):
        """
        Copy test output result from virtual machine to node

        Returns
        -------
        None

        """
        # Send test output to node
        self.put(client_path=TestcaseConfig.FOLDER_DEFAULT + "_" + BuildConfiguration.info.RELEASE,
                 local_path=self.test_result_worker)
        self.put(client_path=TestcaseConfig.FOLDER_DEFAULT + "_" + BuildConfiguration.info.MEMORY,
                 local_path=self.test_result_worker)

    def get(self, local_path, client_path,
            timeout=TimeOut.Default.SEND_FILE,
            copy_to_shared_folder=True):
        """
        For transferring data we can use shared folder which provided by virtual box for a faster
        speed than using ssh copy. Then we need to override get() method to apply using shared
        folder to copy data from node to virtual machine

        Parameters
        ----------
        local_path: str
            Path to file/directory on node or source data need to be copy
        client_path: str
            Path to file/directory on virtual machine or destination of copy
        timeout: int
            Timeout for copy. When it's over this limit then process is broken up.
        copy_to_shared_folder: bool
            Flag to request copy to shared folder only, no need to copy right into directory
            inside virtual machine

        Returns
        -------
        None

        """
        # Check if shared folder of the machine is existed or not
        if not os.path.isdir(self.shared_on_host):
            os.makedirs(self.shared_on_host)
        f_name = os.path.basename(local_path)
        if copy_to_shared_folder:
            # Copy local path to shared folder
            copy_paths(local_path, self.shared_on_host)
        # Copy from shared folder to destination of virtual machine
        src_dir = os.path.join(self.shared_folder, f_name)
        des_dir = os.path.join("/home", self.username, client_path)
        cmd = "cp -rn {src} {des}".format(src=src_dir, des=des_dir)
        self.exec_command(cmd=cmd, timeout=timeout)

    def put(self, client_path, local_path, timeout=TimeOut.Default.SEND_FILE):
        """
        For transferring data we can use shared folder which provided by virtual box for a faster
        speed than using ssh copy. Then we need to override put() method to apply using shared
        folder to copy data from virtual machine to node

        Parameters
        ----------
        client_path: str
            Path to file/directory on virtual machine or source data to copy
        local_path: str
            Path to file/directory on node or destination of copy
        timeout: int
            Timeout for copying data. When it's over this limit then process is broken up

        Returns
        -------
        None

        """
        # Copy from client path to share folder
        f_name = os.path.basename(client_path)
        vm_src_dir = os.path.join("/home", self.username, client_path)
        vm_des_share = os.path.join(self.shared_folder, f_name)
        node_src_folder = os.path.join(self.shared_on_host, f_name)
        if os.path.isdir(node_src_folder):
            vm_des_share = self.shared_folder
        cmd = "cp -rn {src} {des}".format(src=vm_src_dir, des=vm_des_share)
        self.exec_command(cmd=cmd, timeout=timeout)

        # Copy from shared folder to local path
        linux_copy_ignore_exist(src=node_src_folder, des=local_path)

    def put_one_test_case(self, client_path, local_path, timeout=TimeOut.Default.SEND_FILE):
        vm_src_dir = os.path.join("/home", self.username, client_path)
        vm_des_share = os.path.join(self.shared_folder, "TESTS_Stream")
        if not os.path.isdir(os.path.join(self.shared_on_host, "TESTS_Stream")):
            cmd = "mkdir {folder_shared}".format(folder_shared=vm_des_share)
            self.exec_command(cmd=cmd, timeout=timeout)
            print"maked dir TESTS_Stream"

        node_src_folder = os.path.join(self.shared_on_host, "TESTS_Stream")
        cmd = "cp -rn {src} {des}".format(src=vm_src_dir, des=vm_des_share)
        print"***command copy to folder shared:{0}".format(cmd)
        self.exec_command(cmd=cmd, timeout=timeout)
        print"done copy to folder shared"

        # Copy from shared folder to local path
        # cmd = "cp -r {src} {des}".format(src=node_src_folder, des=local_path)
        # self.exec_command(cmd=cmd, timeout=timeout)
        linux_copy_ignore_exist(src=node_src_folder, des=local_path)

    def mount_shared_folder_on_vm(self):
        """
        Currently, we can use shared folder between node and virtual machine to reduce time of
        transferring data compare with using ssh copy. This function will execute mount command
        on virtual machine to mount shared folder with node.

        Returns
        -------
        None

        """
        # Create directory for shared directory with node
        self.logger.start_step("Mount shared folder on virtual machine")
        mount_path = os.path.join('/home/', self.username, VBShareFolder.NAME)
        self.make_directory(mount_path)
        # Execute command to mount shared folder
        cmd = CMD_MOUNT_SHARE_FOLDER_ON_VM.format(1000, 1000, VBShareFolder.NAME, mount_path)
        self.logger.log_and_print(cmd)
        self.exec_sudo_command(cmd=cmd, timeout=TimeOut.VirtualMachine.ADD_SHARED_FOLDER)
        self.logger.end_step(True)

    def send_result_to_test_case(self, test_id, folder_test):
        """
        Change structure of test case:
        <TestCase1>
            <origin_test_case>
                ground_truth_data  output  ref_data  spec.json  test_data
            <compare_result>
            test_result.json
            compare_result.json

        Send file json which generate by run_one.py to folder test cases
        Returns
        -------
        """
        path_folder_test = os.path.join('/home', self.username, folder_test)
        cmd = "mkdir {folder_test}/{test_id}/{test_id}"\
            .format(folder_test=path_folder_test, test_id=test_id)
        print"***command mkdir:{0}".format(cmd)
        self.exec_command(cmd, TimeOut.execute.TEST)
        cmd = "mv {folder_test}/{test_id}/* {folder_test}/{test_id}/{test_id}"\
            .format(folder_test=path_folder_test, test_id=test_id)
        print"***command mv:{0}".format(cmd)
        self.exec_command_without_err(cmd=cmd, timeout=180000)
        copy_test_result = "mv {test_result} {folder_test}/{test_id}"\
            .format(test_result="test_result.json", folder_test=path_folder_test,
                    test_id=test_id)
        print"***command copy test result:{0}".format(copy_test_result)
        self.exec_command(copy_test_result, TimeOut.execute.TEST)
        path_test_case = os.path.join(path_folder_test, test_id)
        path_results_stream = os.path.join(self.test_result_worker, "TESTS_Stream")
        if not os.path.isdir(path_results_stream):
            os.makedirs(path_results_stream)
        self.put_one_test_case(client_path=path_test_case, local_path=self.test_result_worker)