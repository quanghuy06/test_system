# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      25/06/2018
# Description:      This script define class for a virtual machine that build
#                   PHOcr on linux platform.
import os
from abc import ABCMeta, abstractmethod
from baseapi.linux_file_access import linux_tar_file_tgz
from baseapi.file_access import remove_paths
from configs.command import CommandConfig, BuildConfiguration
from configs.common import Platform
from configs.linux import linux_cmd_getter
from configs.projects.phocr import PhocrProject
from configs.projects.hanoi import HanoiProject
from configs.timeout import TimeOut
from manager.lib_vm.vm_build import VirtualMachineBuild

from handlers.parameters_handler import ParameterHandler


class VmBuildPHOcrLinux(VirtualMachineBuild):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        """
        This is an abstract class which define process on a build virtual machine on linux platform.
        Currently, we have different build modes:
        - Build release package using ICC for normal testing
        - Build release package using GCC for memory leak checking
        For each mode we'll have different build command which need to be executed on virtual
        machine. Also, name of generated build packages also different. So we should have derive
        classes to clarify these information to be enough information for build processes can be
        done.

        """
        super(VmBuildPHOcrLinux, self).__init__(**kwargs)
        self.final_build_folder = None
        self.vm_home_dir = os.path.join("/home", self.username)

    def get_platform(self):
        """
        Operating system of virtual machine. Because this class stand for a virtual machine on
        linux then the platform of course is linux.

        Returns
        -------
        str
            Operating system of virtual machine

        """
        return Platform.LINUX

    @abstractmethod
    def get_build_mode(self):
        """
        For linux platform, we also need some build packages for different purpose with different
        build command. So this is an abstract method and require derive class to clarify this
        information to get the right build command.

        Returns
        -------
        str
            Build mode which is define in BuildConfiguration

        """
        pass

    def get_hanoi_source_working_dir(self):
        """
        Get working directory for Hanoi build where the build command should be run.

        Returns
        -------
        str
            Working directory for Hanoi build on virtual machine or where build command should be
            run

        """
        hanoi_build_config = self.configuration[self.get_platform()][BuildConfiguration.HANOI]
        working_dir = hanoi_build_config[BuildConfiguration.info.WORKINGDIR]
        return working_dir

    def checkout_source(self):
        """
        Check out source to target change which need to check. This information is defined in
        parameters.json by refspec. Also change will be merged to original master to be sure no
        conflict of source code.

        Returns
        -------
        None

        """
        # Get git checkout command to be run
        if self.is_release_build:
            checkout_cmd = CommandConfig.py_checkout(self.info_handler.get_project(),
                                                     self.platform)
        else:
            checkout_cmd = CommandConfig.py_checkout(self.info_handler.get_project(),
                                                     self.platform,
                                                     self.info_handler.get_ref_spec())
        # Get time out depend on job
        if self.info_handler.get_project() == PhocrProject.NAME:
            timeout = TimeOut.execute.CHECKOUT_PHOCR
        else:
            timeout = TimeOut.execute.CHECKOUT_HANOI
        # Checkout to target change and refspec
        self.exec_command(checkout_cmd, timeout=timeout)
        # Merge source code to origin master to make sure there is no source conflict
        merge_cmd = linux_cmd_getter.git_merge(self.info_handler.get_project())
        self.exec_command(merge_cmd, TimeOut.execute.GIT_MERGE)

    def checkout_hanoi_source(self):
        """
        Checkout source code of Hanoiworkflow on platform linux

        Returns
        -------
        None

        """
        checkout_cmd = CommandConfig.py_checkout(
            HanoiProject.NAME,
            self.platform)
        self.exec_command(checkout_cmd, timeout=TimeOut.execute.CHECKOUT_HANOI)
        self.checkout_custom_hanoi_change()

    def copy_package_for_hanoi(self):
        """
        Current, we only need copy package for build Hanoi on windows so this function will do
        nothing.

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def get_build_command(self):
        """
        This is an abstract method and need to be implemented on derive classes. For a linux
        build virtual machine, we can have different build modes and for each mode we also have
        different build command to be run on the virtual machine.

        Returns
        -------
        None

        """
        pass

    def run_build_command(self):
        """
        Execute build command on virtual machine over ssh connection.

        Returns
        -------
        None

        """
        build_command = self.get_build_command()
        self.logger.log_and_print("Build command line: {0}".format(build_command))
        self.exec_command(cmd=build_command,
                          timeout=TimeOut.execute.BUILD_PHOCR_LINUX)

    def run_build_hanoi_command(self):
        """
        Run build Hanoiworkflow on linux.

        Returns
        -------
        None

        """
        build_hn_command = CommandConfig.build_hanoi_linux(
            self.configuration,
            BuildConfiguration.HANOI
        )
        self.exec_command(cmd=build_hn_command,
                          timeout=TimeOut.execute.BUILD_HANOI_LINUX)

    def get_hanoi_installer(self):
        """
        Get Hanoi installer from virtual machine to node.

        Returns
        -------
        None

        """
        hanoi_config = self.configuration[Platform.LINUX][
            BuildConfiguration.HANOI]
        hanoi_cwd = hanoi_config[BuildConfiguration.info.WORKINGDIR]
        remote_log_path = \
            os.path.join(hanoi_cwd,
                         hanoi_config[BuildConfiguration.info.PACKAGING])
        local_log_path = os.path.join(os.getcwd(),
                                      self.get_final_hanoi_installer_name())
        self.put(remote_log_path, local_log_path)

    def get_phocr_build_log(self):
        """
        Currently, linux build log can be gotten from node so this function will do nothing.

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def build_result_path_on_vm(self):
        """
        This is an abstract class and need to be implemented on derived classes. Depend on build
        mode we should have different name of build package then this should be clarified by the
        derive classes.

        Returns
        -------
        str
            Path to build package on virtual machine

        """
        pass

    def post_process(self):
        """
        Copy build results from virtual machine to node then compress build folder to final build
        package

        Returns
        -------
        None

        """
        # Get build package
        self.logger.start_step("Copy build results to node")
        self.final_build_folder = self.get_final_build_folder_name()
        local_path = os.path.join(os.getcwd(), self.final_build_folder)
        if os.path.isdir(local_path):
            remove_paths(local_path)
        self.put(self.build_result_path_on_vm(), local_path,
                 timeout=TimeOut.ssh.GET_PHOCR_BUILD_LINUX)
        self.logger.end_step(True)

        # Archive build package
        self.logger.start_step("Compress build package")
        self.archive_build_package()
        self.logger.end_step(True)

        # All processes done. It's time to generate execution time for processes to json file.
        self.logger.end(write_to_file=False)

    def get_final_phocr_build_package_name(self):
        """
        Generate name of final build package. This will be suffixed by name of the platform of
        virtual machine

        Returns
        -------
        str
            Name of final build package

        """
        return self.get_final_build_folder_name() + ".tgz"

    def get_final_hanoi_installer_name(self):
        """
        Get final Hanoi installer name in platform linux.

        Returns
        -------
        str:
            Hanoi installer name.

        """
        return self.info_handler.get_hanoi_package_release(Platform.LINUX)

    def archive_build_package(self):
        """
        Compress build folder to compressed build package to reduce size of build result

        Returns
        -------
        None

        """
        linux_tar_file_tgz(src_folder=self.get_final_build_folder_name(),
                           des_file=self.get_final_phocr_build_package_name())


# TODO: (ThanhLT) This code is used for debug and current it is not used.
# TODO: So it should be deleted.
def main():
    parameter_data = r"""
    {
        "job_name": "PHOcr-EngineeringTest",
        "project": "PHOcr",
        "refspec": "refs/changes/15/1615/40",
        "windows_disable": true,
        "email": "phuc.hoangminh@toshiba-tsdv.com",
        "is_et": true,
        "build_number": "4953",
        "branch": "master",
        "phocr_delta": 384,
        "hanoi_delta": 32,
        "reviewer": "Hoang Minh Phuc",
        "gerrit": {
            "commit_message": "[PHOcr] Config output formatting with embedded Python3.5.2\n\nProject \\\"PHOcr\\\"\n\nChange details                              18 December 2018\n\nNAME\n    Project \\\"PHOcr\\\"\n\nSUMMARY\n    Config output formatting with embedded Python3.5.2\n\nDESCRIPTION\n    This change aims to upgrade Python to 3.5.2 on Ubuntu 10.04.\n    instead of old version 2.6.5 as before.\n    Because we must build a portable Python,\n    so we'll use a flexible setting for python environment\n    (PHOCR_PYTHON_EXECUTABLE_PATH).\n    It means that user need to add PHOCR_PYTHON_EXECUTABLE_PATH to\n    matched python environment. And to do this, please follow\n    step by step:\n    +) Download python (linux or windows) depend on current OS from svn:\n    http://vc1.tsdv.com.vn/2018A/phocr/trunk/src/phocr-3rd/Python-3.5.2/\n    +) Export LD_LIBRARY_PATH=/path-to-python-lib:$LD_LIBRARY_PATH\n\nARCHITECTURE\n    Linux and Windows platform testing required.\n\nAUTOMATION TEST INFORMATION\nWorkspace:\nTestcase ID:\nFunctionalities: export_word|export_excel|export_pptx\nProducts:\nComponents:\nTags:\nHanoi version:\nHanoi Checkout Command:git fetch http://phuchm@10.116.41.96:9090/a/HanoiWorkflow refs/changes/37/1837/1 && git checkout FETCH_HEAD\n\nChange-Id: Ic4e9b3c8ba6b79917d58ae2fafd83e6d7c90b992\n",
            "comment": ""
        }
    }
    """
    parameter_file_path = "tmp-20190220.json"

    with open(parameter_file_path, 'w') as parameter_file:
        parameter_file.write(parameter_data)

    parameters_handler = ParameterHandler(input_file=parameter_file_path)
    node_name = "Ubuntu10.04-32bit-build"
    vm_build_windows = VmBuildPHOcrLinux(name=node_name, ip="10.116.41.82",
                                         username="ocrdev", platform="linux",
                                         password="1",
                                         log_level=1, info_handler=parameters_handler)
    tmp = vm_build_windows.get_build_mode()
    assert tmp == 'release'
    tmp = vm_build_windows.get_platform()
    assert tmp == 'linux'
    tmp = vm_build_windows.info_handler.hanoi_checkout_command()
    assert tmp == 'git fetch ssh://namld@10.116.41.96:29418/HanoiWorkflow refs/changes/37/1837/1' \
                  ' && git checkout FETCH_HEAD'

    # vm_build_windows.checkout_custom_hanoi_change()
    # vm_build_windows.start()
    # vm_build_windows.do_work()

    os.remove(parameter_file_path)


if __name__ == '__main__':
    main()
