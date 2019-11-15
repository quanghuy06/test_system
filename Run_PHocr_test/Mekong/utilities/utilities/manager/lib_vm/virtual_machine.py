# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      25/06/2018
# Description:      This script define base class for a virtual machine.
import pexpect
import re
import os
from abc import ABCMeta, abstractmethod
from manager.lib_manager.worker import Worker
from configs.timeout import TimeOut
from manager.lib_vm.defines import VBShareFolder
from configs.svn_resource import DataPathSVN
from configs.virtual_manager import VirtualManagerConf


class VirtualMachine(Worker):
    __metaclass__ = ABCMeta

    def __init__(self, working_state, **kwargs):
        self.working_state = working_state
        super(VirtualMachine, self).__init__(**kwargs)
        self.shared_on_host = os.path.join(os.getcwd(), VBShareFolder.NAME, self.name)
        self.phocr_lib_svn = os.path.join(self.svn_dir,
                                          DataPathSVN.PHOCR_LIB)
        self.python_3rd_repo_path = os.path.join(self.svn_dir,
                                                 DataPathSVN.THIRD_PARTY_PYTHON)

    @abstractmethod
    def prepare_work(self):
        pass

    @abstractmethod
    def do_work(self):
        pass

    @abstractmethod
    def post_process(self):
        pass

    def start(self):
        # Force to turn off virtual machine if it's running
        if self.is_running():
            self.stop()
        # Restore to working state
        self.restore_working_state()
        # Run command to start virtual machine
        child = pexpect.spawn(VirtualManagerConf.CMD_START_VM.format(self.name),
                              timeout=TimeOut.VirtualMachine.START)
        child.expect(pexpect.EOF)
        self.logger.add_line(child.before)
        if VirtualManagerConf.EXPECT_START not in child.before:
            raise Exception("Failed to start {vm}".format(vm=self.name))

    def restore_working_state(self):
        # Check if virtual machine is running -> power off
        if self.is_running():
            self.stop()
        # Run command
        restore_cmd = VirtualManagerConf.CMD_RESTORE_SNAPSHOT.format(self.name,
                                                                     self.working_state)
        child = pexpect.spawn(command=restore_cmd, timeout=TimeOut.VirtualMachine.RESTORE)
        child.expect(pexpect.EOF)
        self.logger.add_line(child.before)
        if VirtualManagerConf.EXPECT_RESTORE not in child.before:
            raise Exception("Failed to restore {vm} to {state}"
                            "".format(vm=self.name, state=self.working_state))

    def stop(self):
        if self.is_running():
            stop_cmd = VirtualManagerConf.CMD_STOP_VM.format(self.name)
            child = pexpect.spawn(stop_cmd, timeout=TimeOut.VirtualMachine.STOP)
            child.expect(pexpect.EOF)
            self.logger.add_line(child.before)
            if VirtualManagerConf.EXPECT_STOP not in child.before:
                raise Exception("Failed to stop {vm}".format(vm=self.name))

    def is_running(self):
        child = pexpect.spawn(command=VirtualManagerConf.CMD_LIST_RUNNING_VMS,
                              timeout=TimeOut.VirtualMachine.CHECK_RUNNING)
        child.expect(pexpect.EOF)
        lines = child.before.split("\n")
        for line in lines:
            search_result = re.search('".+"', line)
            if not search_result:
                continue
            current_vm = search_result.group(0)
            current_vm = current_vm.replace('"', '')
            if self.name == current_vm:
                return True
        return False

    def add_shared_folder_to_vm(self):
        self.logger.start_step("Add shared folder for virtual machine")
        host_path = os.path.join(os.getcwd(), VBShareFolder.NAME)
        if not os.path.isdir(host_path):
            error_msg = "Shared folder {0} does not exist, please create them first" \
                        "".format(host_path)
            raise Exception(error_msg)

        cmd = VirtualManagerConf.CMD_ADD_SHARE_FOLDER_VM.format(self.name, VBShareFolder.NAME,
                                                                host_path)
        self.logger.log_and_print(cmd)
        child = pexpect.spawn(cmd, timeout=TimeOut.VirtualMachine.ADD_SHARED_FOLDER)
        child.expect(pexpect.EOF)
        self.logger.end_step(child.before)

        if child.exitstatus:
            error_msg = "Failure to add shared folder to vm {0}".format(self.name)
            raise Exception(error_msg)

    def is_snapshot_exist(self, snapshot_name):
        """
        Check if current virtual machine has a snapshot.

        Parameters
        ----------
        snapshot_name str

        Returns
        -------
        bool
            True if virtual machine has the snapshot. Otherwise, return False.

        """
        cmd = VirtualManagerConf.CMD_SNAPSHOT_LIST.format(vm=self.name)
        child = pexpect.spawn(cmd, timeout=TimeOut.VirtualMachine.DEFAULT)
        child.expect(pexpect.EOF)
        lines = child.before.split("\n")
        for line in lines:
            start_index = line.find("Name: ") + len("Name: ")
            end_index = line.find(" (UUID")
            current_vm = line[start_index:end_index]
            if snapshot_name == current_vm:
                return True
        return False

    def rename_snapshot(self, old_name, new_name):
        """
        Rename for a snapshot of current virtual machine. If snapshot does not exist then nothing
        to do.

        Parameters
        ----------
        old_name str
        new_name str

        Returns
        -------
        None

        """
        if not self.is_snapshot_exist(snapshot_name=old_name):
            return

        # Rename
        cmd = VirtualManagerConf.CMD_SNAPSHOT_RENAME.format(vm=self.name, old_name=old_name,
                                                            new_name=new_name)
        child = pexpect.spawn(cmd, timeout=TimeOut.VirtualMachine.DEFAULT)
        child.expect(pexpect.EOF)

    def delete_snapshot(self, snapshot_name):
        """
        Delete a snapshot of current virtual machine. If snapshot does not exist then nothing to do.

        Parameters
        ----------
        snapshot_name str

        Returns
        -------
        None

        """
        if not self.is_snapshot_exist(snapshot_name=snapshot_name):
            return

        # Delete
        cmd = VirtualManagerConf.CMD_SNAPSHOT_DELETE.format(vm=self.name, snapshot=snapshot_name)
        child = pexpect.spawn(cmd, timeout=TimeOut.VirtualMachine.SNAPSHOT_DELETE)
        child.expect(pexpect.EOF)

    def take_snapshot(self, snapshot_name):
        """
        Take a snapshot of current running state of virtual machine. This will create new snapshot
        for virtual machine after static data is updated. If current virtual machine is not
        running then nothing to do.

        Parameters
        ----------
        snapshot_name str

        Returns
        -------
        None

        """
        if not self.is_running():
            return

        # Take snapshot
        cmd = VirtualManagerConf.CMD_SNAPSHOT_TAKE.format(vm=self.name, snapshot=snapshot_name)
        child = pexpect.spawn(cmd, timeout=TimeOut.VirtualMachine.SNAPSHOT_TAKE)
        child.expect(pexpect.EOF)
