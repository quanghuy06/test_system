# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      19/09/2019
# Description:      This define derive class to support manage build processes on virtual machine
#                   to build a release version on linux platform using GCC for memory leak
#                   checking by valgrind
import os
from baseapi.file_access import remove_paths
from configs.command import CommandConfig, BuildConfiguration
from configs.common import Platform
from configs.timeout import TimeOut
from manager.lib_vm.vm_build_phocr_linux import VmBuildPHOcrLinux


class VmBuildPHOcrLinuxMemory(VmBuildPHOcrLinux):

    def get_build_mode(self):
        """
        Define build mode for build job. This will be a virtual machine to build a release
        version using GCC for memory leak checking by valgrind

        Returns
        -------
        None

        """
        return BuildConfiguration.info.MEMORY

    def get_build_command(self):
        """
        Generate command to build a release package using GCC for memory leak checking by valgrind

        Returns
        -------
        str
            Command to run build on build virtual machine

        """
        build_command = CommandConfig.build_phocr_linux(
            self.configuration,
            BuildConfiguration.info.MEMORY,
            BuildConfiguration.PHOCR
        )
        return build_command

    def build_result_path_on_vm(self):
        """
        Define path to build results folder on virtual machine which build release version using
        GCC for memory leak checking by valgrind. This will be used to copy build results to node.

        Returns
        -------
        str
            Path to build results folder on virtual machine.

        """
        phocr_cwd = self.configuration[Platform.LINUX][BuildConfiguration.PHOCR][
            BuildConfiguration.info.MEMORY][BuildConfiguration.info.WORKINGDIR]
        phocr_build = self.configuration[Platform.LINUX][BuildConfiguration.PHOCR][
            BuildConfiguration.info.MEMORY][BuildConfiguration.info.RESULT]
        return os.path.join(phocr_cwd, phocr_build)
