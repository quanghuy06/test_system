# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created:     07/07/2017
# Last update:      07/07/2017
# Updated by:
# Description:      This script define class to configure command lines that used in automated test
#                   system management

import os
import pexpect
from configs.linux import LinuxCmd
from configs.windows import WindowsCmd
from configs.projects.mekong import ScriptPath, TestSystem, UsedScript
from configs.json_key import ParametersJson
from configs.test_result import FinalTestResult, TestResultConfig
from configs.compare_result import CompareResultConfig
from configs.projects.phocr import PhocrProject
from configs.common import Platform, Machines
from configs.system_data_updater import DataUpdatesAvailable, get_update_option


class VirtualBox:
    CHECK_RUN = "vboxmanage list runningvms"
    class start:
        CMD = "vboxmanage startvm"
        TYPE = "--type headless"
        EXPECT = pexpect.EOF
        EXCEPTION = "start"
    class stop:
        CMD = "vboxmanage controlvm"
        TYPE = "poweroff"
        EXPECT = pexpect.EOF
        EXCEPTION = "stop"
    class snapshot:
        CMD = "vboxmanage snapshot"
        RESTORE = "restore"
        EXPECT = pexpect.EOF
        RESTORE_EXCEPTION = "restore snapshot"
        STATE_BUILD = "Build-Environment"
        STATE_TEST = "Clean-State"


# Build configuration
class BuildConfiguration:
    PHOCR = "PHOcr"
    HANOI = "Hanoi"
    class info:
        WORKINGDIR = "cwd"
        CMD = "command"
        RESULT = "build_result"
        PACKAGING = "packaging"
        RELEASE = "release"
        MEMORY = "memory"
        DEBUG = "debug"


class CommandConfigClass:
    @staticmethod
    def node_build_command(node_name):
        cmd = "{0} {1} -n {2} -p {3} --build" \
              "".format(LinuxCmd.PYTHON, ScriptPath.WORKERS_MANAGER,
                        node_name, ParametersJson.DEFAULT_NAME)
        return cmd

    @staticmethod
    def node_build_release_command(node_name):
        cmd = "{0} {1} -n {2} -p {3} --build-release" \
              "".format(LinuxCmd.PYTHON, ScriptPath.WORKERS_MANAGER,
                        node_name, ParametersJson.DEFAULT_NAME)
        return cmd

    @staticmethod
    def node_test_command(node_name, distribution):
        cmd = "{0} {1} -n {2} -p {3} --test -d {4}".format(LinuxCmd.PYTHON,
                                                           ScriptPath.WORKERS_MANAGER,
                                                           node_name,
                                                           ParametersJson.DEFAULT_NAME,
                                                           distribution)
        return cmd

    @staticmethod
    def node_update_data_command(node_name, update_list, reset_backup):
        """
        Get command line to run updating data for test virtual machine on a node

        Parameters
        ----------
        node_name : str
            Name of node to run command udpate data
        update_list : list
            List of data packages which will be updated
        reset_backup : bool
            Request to reset all virtual machines to backup state for testing. Currently,
            this state is really clean and have no testing data on them.

        Returns
        -------
        str
            Command line to run updating data for test virtual machines on a specific node

        """
        cmd = "{python} {script} -n {node_name} -p {parameters}" \
              "".format(python=LinuxCmd.PYTHON,
                        script=ScriptPath.WORKERS_MANAGER,
                        node_name=node_name,
                        parameters=ParametersJson.DEFAULT_NAME)
        update_options = ""
        if DataUpdatesAvailable.PHOCR_TRAINED_DATA in update_list:
            update_options += " " + get_update_option(DataUpdatesAvailable.PHOCR_TRAINED_DATA)
        if DataUpdatesAvailable.PYTHON_PORTABLE in update_list:
            update_options += " " + get_update_option(DataUpdatesAvailable.PYTHON_PORTABLE)
        if DataUpdatesAvailable.VALGRIND_MEKONG in update_list:
            update_options += " " + get_update_option(DataUpdatesAvailable.VALGRIND_MEKONG)

        reset_option = ""
        if reset_backup:
            reset_option = " --reset-backup"

        # No data to be updated
        if not update_options and not reset_option:
            return ""

        cmd += update_options
        cmd += reset_option
        return cmd

    @staticmethod
    def node_update_test_cases_folder(node_name):
        """

        Parameters
        ----------
        node_name: str
            Name of  node to update test case folder

        Returns
        -------
        str
            Command to run on node (through ssh) to update test cases folder on it.

        """
        if node_name == Machines.MASTER_MACHINE[Machines.NAME]:
            test_folder = Machines.MASTER_MACHINE[Machines.TC_FOLDER]
        elif node_name not in Machines.NODE_MACHINES:
            print("ERR: Can not find configuration for node {node_name} to update test cases "
                  "folders!".format(node_name=node_name))
            return ""
        else:
            test_folder = Machines.NODE_MACHINES[node_name][Machines.TC_FOLDER]

        # Construct command line to run on node to update test cases folder of it.
        cmd = "{python} {run_script} -f {test_folder}".format(
            python=LinuxCmd.PYTHON,
            run_script=ScriptPath.UPDATE_TEST_CASE_FOLDER,
            test_folder=test_folder)

        return cmd

    def node_distribute_test(self, profile=None):
        cmd = "{0} {1} -p {2}".format(LinuxCmd.PYTHON, ScriptPath.DISTRIBUTE_TESTSET,
                                      ParametersJson.DEFAULT_NAME)
        if profile is not None:
            cmd += " -pf {0}".format(TestSystem.ConfigureFiles.PROFILE)
        return cmd

    def export_junit_xml(self):
        test_file = os.path.join(FinalTestResult.TEST, FinalTestResult.Test.FILE)
        cmp_file = os.path.join(FinalTestResult.TEST, CompareResultConfig.FILE_DEFAULT)
        xml_out_file = os.path.join(FinalTestResult.TEST, FinalTestResult.FILE_XML)
        return "{0} {1} -ri {2} -ci {3} -o {4}".format(LinuxCmd.PYTHON,
                                                       ScriptPath.JUNIT_EXPORT,
                                                       test_file,cmp_file, xml_out_file)

    def vm_start_headless(self, vm_name):
        return "{0} \"{1}\" {2}".format(VirtualBox.start.CMD, vm_name, VirtualBox.start.TYPE)

    def vm_stop(self, vm_name):
        return "{0} \"{1}\" {2}".format(VirtualBox.stop.CMD, vm_name, VirtualBox.stop.TYPE)

    def vm_restore(self, vm_name, snap_name):
        return "{0} \"{1}\" {2} \"{3}\"".format(VirtualBox.snapshot.CMD, vm_name,
                                                VirtualBox.snapshot.RESTORE, snap_name)

    def py_checkout(self, project, platform, refs=None):
        if platform == Platform.LINUX:
            python = LinuxCmd.PYTHON
        else:
            python = WindowsCmd.PYTHON
        cmd = "{0} {1} -p {2} -o {2}".format(python, ScriptPath.CHECKOUT_REL, project)
        if refs:
            cmd += " --refs {0}".format(refs)
        return cmd

    def build_phocr_linux(self, configuration, build_mode, project):
        working_dir = configuration[Platform.LINUX][project][build_mode][BuildConfiguration.info.WORKINGDIR]
        command = configuration[Platform.LINUX][project][build_mode][BuildConfiguration.info.CMD]
        return "cd {0} && {1}".format(working_dir, command)

    def build_hanoi_linux(self, configuration, project):
        working_dir = configuration[Platform.LINUX][project][BuildConfiguration.info.WORKINGDIR]
        command = configuration[Platform.LINUX][project][BuildConfiguration.info.CMD]
        return "cd {0} && {1}".format(working_dir, command)

    def build_windows(self, configuration, build_mode, project):
        build_info = configuration[Platform.WINDOWS][project][build_mode]
        working_dir = build_info[BuildConfiguration.info.WORKINGDIR]
        command = build_info[BuildConfiguration.info.CMD]
        return "cd {0} && {1}".format(working_dir, command)

    def install_hanoi(self, folder, package, platform):
        if platform == Platform.LINUX:
            return "cd {0} && ./{1}".format(folder, package)
        else:
            return "cd {0} && ./{1} /quiet".format(folder, package)

    def install_phocr(self, folder, package, platform):
        if platform != Platform.WINDOWS:
            error_msg = "Not implemented install_phocr for {0} platform"
            error_msg = error_msg.format(platform)
            raise Exception(error_msg)
        else:
            return "cd {0} && msiexec /i {1} /quiet".format(folder, package)

    @staticmethod
    def set_ld_library(build_folder, python_portable_lib_dir):
        """
        Generate linux command which set LD_LIBRARY_PATH for PHOcr to run on virtual machine

        Parameters
        ----------
        build_folder : str
            Path to build folder of PHOcr on virtual machine
        python_portable_lib_dir : str
            Path to python portable lib on virtual machine. Currently, we put python portable
            package for PHOcr directly on virtual machine to reduce TAT of test system.

        Returns
        -------
        str
            Linux command set up LD_LIBRARY_PATH environment variable

        """
        phocr_lib_dir = os.path.join(build_folder, PhocrProject.build.LIB)
        return "export LD_LIBRARY_PATH={0}:{1}".format(phocr_lib_dir, python_portable_lib_dir)

    @staticmethod
    def set_phocrdata_path(phocr_trained_data_dir):
        """
        Generate linux command to set up environment variable for trained data directory of PHOcr

        Parameters
        ----------
        phocr_trained_data_dir : str
            Path to PHOcr trained data directory. The parent directory of phocrdata folder.

        Returns
        -------
        str
            Linux command line to set up variable for trained data of PHOcr

        """
        return "export PHOCRDATA_PREFIX={0}".format(phocr_trained_data_dir)

    @staticmethod
    def set_python_portable_path(python_portable_bin_on_vm):
        """
        Chmod +x for python portable path and setting up for environment variable
        PHOCR_PYTHON_EXECUTABLE_PATH to python portable path in vm.

        Parameters
        ----------
        python_portable_bin_on_vm : str
            Path to python binary on virtual machine

        Returns
        -------
        str
            Linux command to set up python executable for PHOcr

        """
        return "chmod +x {0} && export PHOCR_PYTHON_EXECUTABLE_PATH={1}" \
               "".format(python_portable_bin_on_vm, python_portable_bin_on_vm)

    def set_phocr_env(self, build_folder, phocr_trained_data_dir, python_portable_dir):
        """
        Generate linux command to setup environment variable to run test on virtual machine

        Parameters
        ----------
        build_folder : str
            Path to build folder on virtual machine
        phocr_trained_data_dir : str
            Path to PHOcr trained data on virtual machine
        python_portable_dir : str
            Path to python portable on virtual machine

        Returns
        -------

        """
        python_portable_lib_on_vm = os.path.join(python_portable_dir, "lib")
        python_portable_bin_on_vm = os.path.join(python_portable_dir, "bin", "python3.5")
        cmd = \
            self.set_ld_library(build_folder, python_portable_lib_on_vm) + " && "\
            + self.set_phocrdata_path(phocr_trained_data_dir) + " && " \
            + self.set_python_portable_path(python_portable_bin_on_vm) + " && "
        return cmd

    # TODO(Huan) refactor this code
    def set_phocr_env_for_board(self, build_folder, python_bin_on_board):
        """
        Generate linux command to setup environment variable on board

        Parameters
        ----------
        build_folder : str
            Path to build folder on board
        python_bin_on_board : str
            Path to python portable binary on board

        Returns
        -------
        str
            Linux command line to set up environment variable to run test on board

        """
        python_portable_dir_on_board = os.path.dirname(os.path.dirname(python_bin_on_board))
        python_portable_lib_on_board = os.path.join(python_portable_dir_on_board, "lib")
        cmd = \
            self.set_ld_library(build_folder, python_portable_lib_on_board) + " && " \
            + self.set_phocrdata_path(build_folder) + " && " \
            + self.set_python_portable_path_for_board(python_bin_on_board) + " && "
        return cmd

    @staticmethod
    def set_python_portable_path_for_board(python_portable_bin_on_vm):
        """
        Setup environment variable PHOCR_PYTHON_EXECUTABLE_PATH on board to run test. For BOARD
        Sing16. Python3.5 located at: /home/SYSROM_SRC/build/release/bin/python3.5

        Parameters
        ----------
        python_portable_bin_on_vm : str
            Path to binary of python portable on virtual machine

        Returns
        -------
        str
            Linux command to execute set up environment variable for python portable binary

        """
        return "export PHOCR_PYTHON_EXECUTABLE_PATH={0}".format(python_portable_bin_on_vm)


    def set_phocr_env_on_windows(self, train_data_dir):
        return "export PHOCRDATA_PREFIX={0}".format(train_data_dir)

    def get_splitted_command(self):
        return " && "

    def py_run_all(self, test_folder, bin_folders, plf, prefix="", vm_home_dir=""):
        python_path = "python"
        if plf == Platform.LINUX:
            python_path = LinuxCmd.PYTHON
        elif plf == Platform.WINDOWS:
            python_path = WindowsCmd.PYTHON
        return "{python} {run_script} -t {test_folder} " \
               "-b {bin_folders} " \
               "-o {output_file} -p {platform}" \
               "".format(python=python_path,
                         run_script=os.path.join(vm_home_dir,
                                                 ScriptPath.RUN_ALL),
                         test_folder=test_folder,
                         bin_folders=bin_folders,
                         output_file=os.path.join(vm_home_dir,
                                                  prefix + TestResultConfig.FILE_DEFAULT),
                         platform=plf)

    def get_run_test_cmd_by_batch_script(self):
        return "./{0}".format(UsedScript.RUN_TEST_BAT)

    @staticmethod
    def get_test_cases(query_str):
        return "{0} {1} {2}".format(LinuxCmd.PYTHON,
                                    ScriptPath.GET_TEST_CASES,
                                    query_str)

    def compare_two_file(self, src_file, dest_file):
        return "diff '{0}' '{1}' > abcd-gh07-d203abc3a4be_diff.log".format(src_file, dest_file)


CommandConfig = CommandConfigClass()