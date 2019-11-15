# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      19/09/2019
# Description:      This define derive class to support manage build processes on virtual machine
#                   to build a release version on linux platform using ICC for normal testing
import os
from configs.command import CommandConfig, BuildConfiguration
from configs.common import Platform
from manager.lib_vm.vm_build_phocr_linux import VmBuildPHOcrLinux


class VmBuildPHOcrLinuxRelease(VmBuildPHOcrLinux):

    def get_build_mode(self):
        """
        Define build mode for build job. This will be a virtual machine to build a release
        version using ICC for normal testing

        Returns
        -------
        None

        """
        return BuildConfiguration.info.RELEASE

    def get_build_command(self):
        """
        Generate command to build a release package using ICC for normal testing

        Returns
        -------
        str
            Command to run build on build virtual machine

        """
        build_command = CommandConfig.build_phocr_linux(
            self.configuration,
            BuildConfiguration.info.RELEASE,
            BuildConfiguration.PHOCR
        )
        return build_command

    def build_result_path_on_vm(self):
        """
        Define path to build results folder on virtual machine which build release version using
        ICC for normal testing. This will be used to copy build results to node.

        Returns
        -------
        str
            Path to build results folder on virtual machine.

        """
        phocr_cwd = self.configuration[Platform.LINUX][BuildConfiguration.PHOCR][
            BuildConfiguration.info.RELEASE][BuildConfiguration.info.WORKINGDIR]
        phocr_build = self.configuration[Platform.LINUX][BuildConfiguration.PHOCR][
            BuildConfiguration.info.RELEASE][BuildConfiguration.info.RESULT]
        return os.path.join(phocr_cwd, phocr_build)
