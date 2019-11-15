# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      25/06/2018
# Description:      This script define class for a virtual machine that test PHOcr on linux
# platform.
import os
from manager.lib_vm.vm_test import VirtualMachineTest
from configs.command import CommandConfig, BuildConfiguration
from configs.timeout import TimeOut
from configs.windows import WindowsPath, WindowsCmd, WindowsUtils
from configs.common import Platform
from configs.database import TestcaseConfig
from manager.lib_vm.defines import VBShareFolder
from baseapi.file_access import copy_paths, remove_files_with_ext
from baseapi.linux_file_access import linux_copy_ignore_exist
from configs.command import ScriptPath
from configs.projects.phocr import PhocrProject
from configs.svn_resource import DataPathSVN
from configs.projects.hanoi import HanoiProject


class VmTestWindows(VirtualMachineTest):

    def __init__(self, **kwargs):
        super(VmTestWindows, self).__init__(**kwargs)
        self.bin_folders = []
        self.vm_home_folder = os.path.join(WindowsPath.USERS_PATH, self.username)
        self.vm_shared_folder = os.path.join(WindowsPath.SHARED_DRIVE, self.name)
        self.hanoi_installer_name = \
            self.info_handler.get_hanoi_package_release(self.platform)

    def prepare_shared_folder(self):
        self.add_shared_folder_to_vm()
        self.mount_shared_folder_on_vm()

    def prepare_build_packages(self):
        # Prepare PHOcr build
        self.logger.start_step("Get PHOcr build package")
        final_build_path = os.path.join(self.build_folder,
                                        BuildConfiguration.info.RELEASE)
        self.get(final_build_path, self.build_folder,
                 timeout=TimeOut.ssh.GET_PHOCR_BUILD_WINDOWS)
        self.logger.end_step(True)
        # Prepare Hanoi build
        self.logger.start_step("Get Hanoi build package")
        if self.info_handler.is_et() and not self.info_handler.is_build_hanoi():
            hanoi_release_window = os.path.join(self.svn_dir,
                                                DataPathSVN.HANOI_RELEASE,
                                                Platform.WINDOWS)
        else:
            hanoi_release_window = os.getcwd()

        hanoi_installer_path = os.path.join(hanoi_release_window,
                                            self.hanoi_installer_name)
        self.get(hanoi_installer_path,
                 HanoiProject.Windows.VM_HANOI_TEMP_DIR,
                 timeout=TimeOut.ssh.GET_HANOI_BUILD_WINDOWS)
        self.logger.end_step(True)

        # Get run script
        self.logger.start_step("Get run_test.bat script")
        run_script_path = ScriptPath.RUN_TEST_BAT_PATH
        self.get(run_script_path, "")
        self.logger.end_step(True)

    def install_packages(self):

        # Install PHOcr
        self.install_phocr()

        # [20190903] Temporary disable Install HaNoi and testing with Hanoi test cases.
        # # Install HanoiWorkflow
        # self.install_hanoi()

        self.get_trainingdata()

    def get_run_test_command(self):
        return CommandConfig.get_run_test_cmd_by_batch_script()

    def install_phocr(self):
        # self.bin_folders.append(self.build_folder)
        final_build_folder = self.info_handler.get_folder_specific() + \
                             "_" + \
                             Platform.WINDOWS
        install_phocr_cmd = CommandConfig.install_phocr(final_build_folder,
                                                        PhocrProject.build.Windows.RESULT,
                                                        self.platform)
        self.exec_command(install_phocr_cmd, timeout=TimeOut.install.PHOCR_WINDOWS)

        # WANING(Huan) Currently, I install PHOcr into Hanoi folder for test purpose
        # Because I can not find the way to set PATH env to PHOcr folder
        # Then we do not use this code any more
        # self.bin_folders.append('C:/Program\ Files/PHOcr/')

    # Execute interactive command to install HanoiWorkflow
    def install_hanoi(self):
        # Install Hanoi on Windows
        install_cmd = CommandConfig.install_hanoi(HanoiProject.Windows.VM_HANOI_TEMP_DIR,
                                                  self.hanoi_installer_name,
                                                  self.platform)
        self.exec_command(install_cmd, timeout=TimeOut.install.HANOI_WINDOWS)
        self.bin_folders.append(HanoiProject.Windows.INSTALL_DIR)

    def get_trainingdata(self):
        vm_trainingdata_dir = os.path.join(WindowsPath.PROGRAMDATA_PATH,
                                           PhocrProject.NAME)
        svn_trainingdata_dir = os.path.join(self.svn_dir,
                                            DataPathSVN.TRAINING_DATA_DIR,
                                            DataPathSVN.PHOCRDATA_DIR)

        self.get(svn_trainingdata_dir, vm_trainingdata_dir)

    def put_test_output(self):
        # Send test output to node
        self.logger.start_step("Send output test to node")
        test_list = os.listdir(self.test_set_worker)
        total = len(test_list)
        count = 1
        for test_name in test_list:
            if self.log_level > 0:
                self.logger.log_and_print("[{0}/{1}] Get output of {2}".format(count, total,
                                                                               test_name))
            src_path = os.path.join(TestcaseConfig.FOLDER_DEFAULT, test_name,
                                    TestcaseConfig.OUTPUT_FOLDER)
            des_path = os.path.join(self.test_set_worker, test_name)
            self.put(client_path=src_path, local_path=des_path)
            count += 1
        self.logger.end_step(True)

    def get_test_cases(self):
        self.logger.start_step("Send test cases to worker")
        des_path = TestcaseConfig.FOLDER_DEFAULT
        self.get(local_path=self.test_set_worker, client_path=des_path,
                 timeout=TimeOut.ssh.WORKER_GET_TEST_SET)
        self.logger.end_step(True)

    def get(self, local_path, client_path, timeout=TimeOut.Default.SEND_FILE):
        # Check if shared folder of the machine is existed or not
        if not os.path.isdir(self.shared_on_host):
            os.makedirs(self.shared_on_host)
        f_name = os.path.basename(local_path)
        # Copy local path to shared folder
        self.logger.add_line("Copy from {0} to {1}".format(local_path, self.shared_on_host))
        copy_paths(local_path, self.shared_on_host)
        # Copy from shared folder to destination of virtual machine
        src_dir = os.path.join(self.vm_shared_folder, f_name)

        if WindowsUtils.is_windows_absolute_path(client_path):
            des_dir = client_path
        else:
            des_dir = os.path.join(self.vm_home_folder, client_path)

        # Because file "*.pyc" can not copy to Windows evn
        # So need to delete it first
        remove_files_with_ext(self.shared_on_host, ".pyc")

        cmd = "cp -r {0} {1}".format(src_dir, des_dir)
        self.exec_command(cmd=cmd, timeout=timeout)

    def put(self, client_path, local_path, timeout=TimeOut.Default.SEND_FILE):
        # Copy from client path to share folder
        vm_src_dir = os.path.join(self.vm_home_folder, client_path)
        vm_des_share = os.path.join(self.vm_shared_folder, client_path)
        node_src_folder = os.path.join(self.shared_on_host, client_path)

        cmd = "cp -r {0} {1}".format(vm_src_dir, vm_des_share)
        self.exec_command(cmd=cmd, timeout=timeout)

        # Copy from shared folder to local path
        self.logger.add_line("Copy from {0} to {1}".format(node_src_folder, local_path))
        linux_copy_ignore_exist(src=node_src_folder, des=local_path)

    def mount_shared_folder_on_vm(self):
        self.logger.start_step("mount shared folder")
        cmd = WindowsCmd.MOUNT_SHARE_FOLDER.format(WindowsPath.SHARED_DRIVE,
                                                   VBShareFolder.NAME)
        self.exec_command(cmd=cmd, timeout=TimeOut.VirtualMachine.ADD_SHARED_FOLDER)
        self.logger.end_step(True)


