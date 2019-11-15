# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      13/12/2018
# Description:      This script define class for a virtual machine that build
#                   PHOcr on windows with mode: debug

import os
from abc import ABCMeta
from configs.command import CommandConfig, BuildConfiguration
from manager.lib_vm.vm_build_phocr_windows import VmBuildPHOcrWindows
from configs.common import Platform
from manager.lib_vm.defines import VBLogFile


class VmBuildPHOcrWindowsDebug(VmBuildPHOcrWindows):

    __metaclass__ = ABCMeta

    def get_build_mode(self):
        return BuildConfiguration.info.DEBUG

    def __init__(self, **kwargs):
        self.configuration = None
        super(VmBuildPHOcrWindowsDebug, self).__init__(**kwargs)

    def get_build_command(self):
        """
        Get PHOcr build command on windows in correspond with build mode.

        Returns
        -------
        str
            Command to run build PHOcr in debug mode.
        """
        build_command = \
            CommandConfig.build_windows(self.configuration,
                                        BuildConfiguration.info.DEBUG,
                                        BuildConfiguration.PHOCR)
        return build_command

    def get_build_mode_info(self, project_config):
        """
        Get configuration which corresponding with build mode.

        Parameters
        ----------
        project_config: dict
            Configuration of project read from configure_build.json file.

        Returns
        -------
        dict
            Build node information for build mode.
        """
        return project_config[BuildConfiguration.info.DEBUG]

    def get_build_result_path(self, cwd):
        """
        Get path where will stores build which is gotten from build machine.

        Parameters
        ----------
        cwd: str
            Current working directory.

        Returns
        -------
        str
            Path on local where store build which gotten from build machine.
        """
        build_folder = os.path.join(cwd,
                                    self.get_final_build_folder_name())
        if not os.path.isdir(build_folder):
            os.mkdir(build_folder)
        return os.path.join(build_folder, BuildConfiguration.info.DEBUG)

    def get_phocr_build_log(self):
        """
        Get PHOcr build log from virtual machine.

        """
        phocr_config = self.configuration[Platform.WINDOWS][
            BuildConfiguration.PHOCR]
        build_info = self.get_build_mode_info(project_config=phocr_config)
        phocr_cwd = build_info[BuildConfiguration.info.WORKINGDIR]
        self.logger.start_step("Get log from virtual machine!")
        remote_log_path = os.path.join(phocr_cwd, VBLogFile.LOG_BUILD)
        local_log_path = os.path.join(os.getcwd(), VBLogFile.LOG_BUILD_DEBUG)
        self.put(remote_log_path, local_log_path)
        self.logger.end_step(True)

    def run_build_hanoi_command(self):
        """
        Current, we only check build Hanoi on vm which build PHOcr with mode
        release so this function will do nothing here.

        """
        pass

    def checkout_hanoi_source(self):
        """
        Current, we only check build Hanoi on vm which build PHOcr with mode
        release so this function will do nothing here.

        """
        pass

    def copy_package_for_hanoi(self):
        """
        Current, we only check build Hanoi on vm which build PHOcr with mode
        release so this function will do nothing here.

        """
        pass

    def get_hanoi_installer(self):
        """
        Current, we only check build Hanoi on vm which build PHOcr with mode
        release so this function will do nothing here.

        """
        pass
