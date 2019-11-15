# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      25/06/2018
# Description:      This script define class for a virtual machine that
#                   build PHOcr on windows platform.
import os

from baseapi.file_access import remove_paths
from configs.command import CommandConfig, BuildConfiguration
from configs.common import Platform
from configs.timeout import TimeOut
from manager.lib_vm.vm_build import VirtualMachineBuild
from configs.projects.phocr import PhocrProject
from configs.projects.hanoi import HanoiProject
from configs.windows import WindowsCmd
from handlers.parameters_handler import ParameterHandler


class VmBuildPHOcrWindows(VirtualMachineBuild):

    def get_platform(self):
        return Platform.WINDOWS

    def get_hanoi_source_working_dir(self):
        hanoi_build_config = self.configuration[self.get_platform()][BuildConfiguration.HANOI]
        hanoi_build_config_release = hanoi_build_config[self.get_build_mode()]
        working_dir = hanoi_build_config_release[BuildConfiguration.info.WORKINGDIR]
        return working_dir

    def __init__(self, **kwargs):
        self.configuration = None
        super(VmBuildPHOcrWindows, self).__init__(**kwargs)
        self.vm_home_dir = os.path.join("C:/Users", self.username)

    def checkout_source(self):
        if self.is_release_build:
            checkout_cmd = \
                CommandConfig.py_checkout(self.info_handler.get_project(),
                                          self.platform)
        else:
            checkout_cmd = \
                CommandConfig.py_checkout(self.info_handler.get_project(),
                                          self.platform,
                                          self.info_handler.get_ref_spec())
        if self.info_handler.get_project() == PhocrProject.NAME:
            timeout = TimeOut.execute.CHECKOUT_PHOCR
        else:
            timeout = TimeOut.execute.CHECKOUT_HANOI
        self.exec_command(checkout_cmd, timeout=timeout)
        merge_cmd = WindowsCmd.git_merge(self.info_handler.get_project())
        self.exec_command(merge_cmd, TimeOut.execute.GIT_MERGE)
        self.logger.end_step(True)

    def run_build_command(self):
        build_command = self.get_build_command()
        self.exec_command(cmd=build_command,
                          timeout=TimeOut.execute.BUILD_PHOCR_WINDOWS)

    def post_process(self):
        self.logger.start_step("Get build result from build worker")
        platform_config = self.configuration[Platform.WINDOWS][
            BuildConfiguration.PHOCR]
        build_info = self.get_build_mode_info(project_config=platform_config)
        phocr_cwd = build_info[BuildConfiguration.info.WORKINGDIR]
        phocr_build = build_info[BuildConfiguration.info.RESULT]
        remote_build_path = os.path.join(phocr_cwd, phocr_build)
        local_build_path = self.get_build_result_path(os.getcwd())
        if os.path.isdir(local_build_path):
            remove_paths(local_build_path)
        self.put(remote_build_path, local_build_path,
                 timeout=TimeOut.ssh.GET_PHOCR_BUILD_WINDOWS)
        self.logger.end_step(True)

    def get_build_command(self):
        """
        This is abstract function use to generate build command.
        Detail implementation refer to corresponding subclass.

        """
        pass

    def get_build_mode_info(self, project_config):
        """
        This is abstract function use to get configuration which corresponding
        with build mode.
        Detail implementation refer to corresponding subclass.

        Parameters
        ----------
        project_config: dict
            Configuration for project read from configure_build.json

        """
        pass

    def get_build_result_path(self, cwd):
        """
        This is abstract function use to get path where will stores build
        (which is gotten from build machine).
        Detail implementation refer to corresponding subclass.

        """
        pass

    def get_final_phocr_build_package_name(self):
        return self.get_final_build_folder_name()

    def mount_shared_folder_on_vm(self):
        # Implement in the future to shared with build VM
        pass

    def get_final_hanoi_installer_name(self):
        """
        Get final Hanoi installer name in platform windows.

        Returns
        -------
        str
           Hanoi installer name.

        """
        return self.info_handler.get_hanoi_package_release(Platform.WINDOWS)

# TODO: (ThanhLT) This code is used for debug and current it is not used.
# TODO: So it should be deleted.
def main():
    parameter_file = "/media/huanlv/data/test-system/parameters.json"
    parameters_handler = ParameterHandler(input_file=parameter_file)
    node_name = "Windows8.1-32bit-build-1"
    vm_build_windows = VmBuildPHOcrWindows(name= node_name, ip="10.116.41.54",
                               username="build", platform="windows",
                               password="1",
                               log_level=1, info_handler=parameters_handler)
    vm_build_windows.start()
    vm_build_windows.do_work()

if __name__ == '__main__':
    main()
