# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      25/06/2018
# Description:      This script define class for a virtual machine that build
#                   PHOcr on linux platform.
import traceback
from abc import ABCMeta, abstractmethod

from configs.command import VirtualBox
from configs.projects.mekong import MekongProject
from manager.lib_vm.virtual_machine import VirtualMachine
from configs.projects.mekong import TestSystem
from baseapi.file_access import read_json
from configs.projects.hanoi import HanoiProject
from configs.timeout import TimeOut


class VirtualMachineBuild(VirtualMachine):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        """
        Constructor for class which help manage processes on build virtual machine over ssh
        connection. This is an abstract class and there are some abstract methods need to be
        implemented.

        """
        super(VirtualMachineBuild, self).__init__(working_state=VirtualBox.snapshot.STATE_BUILD,
                                                  **kwargs)
        self.configuration = None
        self.is_release_build = False
        self.build_configure_path = TestSystem.Paths.BUILD_CONFIGURE
        self.configuration = read_json(self.build_configure_path)

    @abstractmethod
    def get_platform(self):
        """
        This is an abstract method and need to implemented in derive classes. This define which
        platform we are working on the virtual machine or operating system of the virtual machine.

        Returns
        -------
        str
            Operating system of the virtual machine

        """
        pass

    @abstractmethod
    def get_build_mode(self):
        """
        Currently, there are two modes for build are supported:
        - Build release with ICC
        - Build release with GCC which is used for memory leak checking

        This is an abstract method and need to be implemented on the derive classes to define
        which build mode we are working/target.

        Returns
        -------
        str
            Mode of build package on virtual machine

        """
        pass

    def prepare_work(self):
        """
        Copy necessary data from node to virtual machine to be ready for run build

        Returns
        -------
        None

        """
        # Get Mekong utilities
        self.logger.start_step("Get Mekong utilities")
        self.get(MekongProject.NAME, MekongProject.NAME)
        self.logger.end_step(True)

    def do_work(self):
        """
        Connect to virtual machine over ssh connection and manage build processes on it. After
        this done, we will have build packages as expected. This function control all processes
        on an online virtual machines from node to get expected build packages: send
        data/requirements to virtual machine, execute source code check out and build command
        over ssh connection then get build packages.

        Returns
        -------
        None

        """
        try:
            # Prepare for work
            self.prepare_work()
            # Checkout source code
            self.logger.start_step("Checkout source code")
            self.checkout_source()
            self.logger.end_step(True)

            # Run build
            self.logger.start_step("Run build command".format(
                self.info_handler.get_project()))
            self.run_build_command()
            self.logger.end_step(True)

            # Build Hanoi as default on IT
            # ET support option in commit message for build Hanoi or not.
            if (not self.info_handler.is_et() and not self.is_release_build) \
                    or self.info_handler.is_build_hanoi():
                pass
                # NamLD: Don't build Hanoi when use running with ICC compiler
                # This issue will be fixed later.
                # self.build_and_get_hanoi_installer()

            # Send build result to node.
            self.post_process()
        except:
            var = traceback.format_exc()
            if self.log_level >= 0:
                self.logger.log_and_print(var)
            else:
                print(var)
            self.work_done = False
        finally:
            # Get build log from virtual machine.
            self.get_phocr_build_log()
            # Finally, always remember to stop the virtual machine
            self.stop()

    @abstractmethod
    def checkout_source(self):
        """
        This is an abstract method and base on which environment we should have different steps
        to checkout target change for build. This need to be implemented on derive classes.

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def checkout_hanoi_source(self):
        """
        This is abstract function used for running build Hanoi. Detail implementation refer to
        corresponding subclass.

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def get_hanoi_source_working_dir(self):
        """
        Get Hanoi source

        Returns
        -------
        None

        """
        pass

    def checkout_custom_hanoi_change(self):
        """
        Checkout the custom Hanoi change which gerrit committer want to test with

        Returns
        -------

        """
        try:
            working_dir = self.get_hanoi_source_working_dir()
        except KeyError as e:
            error_message = \
                "Search key error {0}".format(
                    str(e)
                )
            raise Exception(error_message)

        hanoi_custom_checkout_command = \
            self.info_handler.hanoi_checkout_command()

        if hanoi_custom_checkout_command:
            self.exec_command(hanoi_custom_checkout_command,
                              timeout=TimeOut.execute.CHECKOUT_HANOI,
                              cwd=working_dir)

    @abstractmethod
    def copy_package_for_hanoi(self):
        """
        This is abstract function used for copy package for build Hanoi. Detail implementation
        refer to corresponding subclass.

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def run_build_command(self):
        """
        This is an abstract method and need to be implemented on derive classes. Base on
        platforms or build modes, we will have different commands to run build on virtual machines.

        Returns
        -------
        str
            Command to run build on virtual machine

        """
        pass

    @abstractmethod
    def run_build_hanoi_command(self):
        """
        This is abstract function used for checkout source code of HanoiWorkflow. Detail
        implementation refer to corresponding subclass.

        Returns
        -------
        str
            Command to build Hanoi project on virtual machine

        """
        pass

    @abstractmethod
    def get_hanoi_installer(self):
        """
        This is abstract function used for checkout source code of HanoiWorkflow. Detail
        implementation refer to corresponding subclass.

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def get_phocr_build_log(self):
        """
        This is abstract function used for get PHOcr build log from virtual machine. Detail
        implementation refer to corresponding subclass.

        Returns
        -------
        None

        """
        pass

    def get_final_build_folder_name(self):
        """
        Get name of final build folder base on build mode

        Returns
        -------
        str
            Name of final build folder

        """
        if self.is_release_build:
            # Prefix for release build package by build mode
            return self.info_handler.get_build_folder_release() +\
                   "_" + self.platform + "_" + self.get_build_mode()
        else:
            # Prefix build package by build mode
            return self.info_handler.get_folder_specific() +\
                   "_" + self.platform + "_" + self.get_build_mode()

    @abstractmethod
    def get_final_phocr_build_package_name(self):
        """
        Get final name of build package which is generated from build job on virtual machine.
        Base on platforms, build modes we can have different name of phocr build package.

        Returns
        -------
        str
            Name of phocr build package on virtual machine

        """
        pass

    @abstractmethod
    def get_final_hanoi_installer_name(self):
        """
        Get final Hanoi installer name. This is an abstract function.
        Detail implementation refer to corresponding subclass.

        Returns
        -------
        str
            Name of hanoi installer package on virtual machine

        """
        pass

    def build_and_get_hanoi_installer(self):
        """
        Checkout source code and build Hanoiworkflow to get Hanoi_Installer.

        Returns
        -------
        None

        """
        # Checkout source code of HanoiWorkflow
        self.logger.start_step("Checkout source code of HanoiWorkflow")
        self.checkout_hanoi_source()
        self.logger.end_step(True)

        # Checkout source code of HanoiWorkflow
        self.logger.start_step("Copy package for Hanoi")
        self.copy_package_for_hanoi()
        self.logger.end_step(True)

        # Run build HanoiWorkflow
        self.logger.start_step("Build HanoiWorkflow")
        self.run_build_hanoi_command()
        self.logger.end_step(True)

        # Get Hanoi installer from Virtual machine
        self.logger.start_step("Get Hanoi installer from Virtual machine")
        self.get_hanoi_installer()
        self.logger.end_step(True)
