# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      13/02/2018
# Description:      This script define class for testing on platform linux
import os
import paramiko
from abc import ABCMeta
from manager.lib_vm.vm_test import VirtualMachineTest
from configs.command import CommandConfig
from configs.timeout import TimeOut


class TestOnLinux(VirtualMachineTest):
    __metaclass__ = ABCMeta

    # Folder on virtual machine which will store static data required by PHOcr for testing on
    # virtual machine. Base directory is home directory on test virtual machine.
    # Currently, these data include:
    # - Trained data
    # - Python portable for PHOcr office
    PHOCR_DATA_DIR = "PHOcr-Data"

    # Folder on virtual machine which will store trained data for PHOcr testing
    # Relative path with phocr data directory: <phocr data dir>/<trained data dir>/phocrdata
    PHOCR_TRAINED_DATA_DIR = "phocr_trained_data"

    # Folde on virtual machine which will store python package for PHOcr office testing
    # Relative path with phocr data directory:
    # <phocr data dir>/<python portable dir>/<python package>
    PYTHON_PORTABLE_DIR = "python_portable"

    # Folder on virtual machine which will store static data required by Mekong for testing on
    # virtual machine. Base directory is home directory on test virtual machine.
    # Currently, these data include:
    # - Valgrind for memory checking
    MEKONG_DATA_DIR = "Mekong-Data"

    def __init__(self, **kwargs):
        super(TestOnLinux, self).__init__(**kwargs)
        self.home_dir = os.path.join("/storage/Jenkins")
        if self.info_handler:
            hanoi_package_name = os.path.splitext(self.hanoi_package)[0]
            self.hanoi_target_dir = os.path.join(self.home_dir,
                                                 hanoi_package_name)
            self.phocr_target_dir = os.path.join(self.home_dir,
                                                 self.build_folder)

    def prepare_shared_folder(self):
        pass

    def install_packages(self):
        # [20190903] Temporary disable Install HaNoi and testing with Hanoi test cases.
        # # Install Hanoi
        # self.logger.log_and_print("+ Install Hanoi")
        # # Change mode
        # des_path = os.path.join(self.hanoi_target_dir, self.hanoi_package)
        # self.exec_command(linux_cmd_getter.chmod_x(des_path))
        # # Run script to install Hanoi
        # self.exec_cmd_install_hanoi()
        #
        # self.copy_hanoi_package_to_pho_build()
        pass

    def copy_hanoi_package_to_pho_build(self):
        """
        Copy hanoi package to phocr build.

        """
        pass

    # Execute interactive command to install HanoiWorkflow
    def exec_cmd_install_hanoi(self):
        cmd = CommandConfig.install_hanoi(self.hanoi_target_dir,
                                          self.hanoi_package,
                                          self.platform)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.ip,
                    username=self.username,
                    timeout=TimeOut.ssh.CONNECT)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        stdin.write('\n')
        stdin.flush()
        stdin.write('\n')
        stdin.flush()
        log = stdout.read()
        log += stderr.read()
        self.logger.log_and_print(log)
        ssh.close()

    def put_test_output(self):
        pass

    def get_run_test_command(self):
        pass

    def prepare_build_packages(self):
        pass
