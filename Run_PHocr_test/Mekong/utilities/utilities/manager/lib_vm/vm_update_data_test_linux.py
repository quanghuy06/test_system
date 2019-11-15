# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/09/2019
# Description:      This script define class for updating static data on a test virtual machine on
#                   Node
import os
import time
from manager.lib_vm.test_on_linux import TestOnLinux
from manager.lib_vm.defines import VBShareFolder
from configs.system_data_updater import DataUpdatesAvailable
from configs.git_resource import GITResource
from configs.svn_resource import DataPathSVN
from configs.projects.mekong import ValGrind


class VmUpdateDataTestLinux(TestOnLinux):

    def __init__(self, update_list=None, reset_backup=False, **kwargs):
        """
        Constructor for class which help to update static data for testing on virtual machine.

        Parameters
        ----------
        update_list : list
             List of data need to be updated. Valid values is defined in enum class
             DataUpdatesAvailable
        """
        super(VmUpdateDataTestLinux, self).__init__(**kwargs)
        self.home_folder = os.path.join("/home", self.username)
        self.shared_folder = os.path.join(self.home_folder,
                                          VBShareFolder.NAME,
                                          self.name)
        self.phocr_data_dir = os.path.join(self.home_folder, self.PHOCR_DATA_DIR)
        self.mekong_data_dir = os.path.join(self.home_folder, self.MEKONG_DATA_DIR)

        if update_list is not None:
            self.update_list = update_list
        else:
            self.update_list = list()

        # Flag to reset all virtual machines to backup snapshot
        self.reset_backup = reset_backup

    def prepare_work(self):
        """
        Prepare for work

        Returns
        -------
        None

        """
        pass

    def run_test(self):
        """
        Actual run updating data and create new snapshot for virtual machine.

        Returns
        -------
        None

        """
        # In case a request to reset virtual machine to backup snapshot, then nothing to do.
        if self.reset_backup:
            return

        # Create phocr data on test virtual machine
        if not self.is_exist(self.phocr_data_dir):
            self.make_directory(self.phocr_data_dir)

        # Create mekong data on test virtual machine
        if not self.is_exist(self.mekong_data_dir):
            self.make_directory(self.mekong_data_dir)

        # Check to update trained data for virtual machine
        if DataUpdatesAvailable.PHOCR_TRAINED_DATA in self.update_list:
            self.update_phocr_trained_data()

        # Check to update python portable package for virtual machine
        if DataUpdatesAvailable.PYTHON_PORTABLE in self.update_list:
            self.update_python_portable()

        # Check to update valgrind utility for memory checking on virtual machine
        if DataUpdatesAvailable.VALGRIND_MEKONG in self.update_list:
            self.update_valgrind_mekong()

    def post_process(self):
        """
        Some work after updating data. Remove snapshot backup if it exists then move current clean
        state to backup state. Create new clean state where static data is already update.

        Returns
        -------
        None

        """
        # Reset virtual machine to backup snapshot
        if self.reset_backup and self.is_snapshot_exist(snapshot_name=self.SNAPSHOT_BACKUP):
            # Check to remove current snapshot which is used for testing
            if self.is_snapshot_exist(snapshot_name=self.SNAPSHOT_TEST):
                self.delete_snapshot(snapshot_name=self.SNAPSHOT_TEST)
            # Rename backup snapshot as the nam of snapshot which is used for testing
            self.rename_snapshot(old_name=self.SNAPSHOT_BACKUP, new_name=self.SNAPSHOT_TEST)
        else:
            # For the first time, where current Clean-State snapshot is really clean then we should
            # make a snapshot backup for really state and we can reset to this state later if
            # required. To know this situation, we can check if back up snapshot exists or not.
            # Move current clean state snapshot to a backup snapshot.
            if not self.is_snapshot_exist(snapshot_name=self.SNAPSHOT_BACKUP):
                self.rename_snapshot(old_name=self.SNAPSHOT_TEST, new_name=self.SNAPSHOT_BACKUP)
            # Remove current snapshot which is used for testing
            self.delete_snapshot(self.SNAPSHOT_TEST)
            # Create new snapshot for testing where data is updated
            self.take_snapshot(snapshot_name=self.SNAPSHOT_TEST)

        # Processes done, then log execution time of system to json file
        self.logger.end()

    def prepare_shared_folder(self):
        """
        Do not use shared folder for transferring data between node and virtual machine. We only
        need to use ssh copy for stable.

        Returns
        -------
        None

        """
        pass

    def clean_test_machine(self):
        """
        Clean test machine before testing.
        This function use for testing on board.
        So we won't do nothing here

        """
        pass

    def prepare_build_packages(self):
        """
        Because we only update static data on test virtual machine, so we don't need prepare build
        packages for testing.

        Returns
        -------
        None

        """
        pass

    def copy_hanoi_package_to_pho_build(self):
        """
        We don't need to build, then no need to prepare build packages

        Returns
        -------
        None

        """
        pass

    def update_phocr_trained_data(self):
        """
        Update new trained data for PHOcr on test virtual machine. Remove old data then copy new
        data from git folder on Node to location on VM. This trained data is updated from git.

        Returns
        -------
        None

        """
        phocr_data_dir_on_node = os.path.join(self.git_dir, GITResource.PHOcr.PHOCR_FOLDER,
                                              GITResource.PHOcr.PHOCR_DATA_DIR)
        phocr_trained_data_dir_on_node = \
            os.path.join(phocr_data_dir_on_node, GITResource.PHOcr.TRAINED_DATA_FOLDER)
        ambitrains_data_dir_on_node = \
            os.path.join(phocr_data_dir_on_node, GITResource.PHOcr.AMBITRAINS_DATA_FOLDER)
        font_data_dir_on_node = \
            os.path.join(phocr_data_dir_on_node, GITResource.PHOcr.FONT_DATA_FOLDER)
        dest_dir_on_vm = os.path.join(self.home_folder, self.PHOCR_DATA_DIR,
                                      self.PHOCR_TRAINED_DATA_DIR)
        # Remove old trained data
        self.remove_directory(dest_dir_on_vm)
        # Copy new trained data to virtual machine
        self.make_directory(dest_dir_on_vm)
        # Copy phocr trained data to virtual machine
        self.get(local_path=phocr_trained_data_dir_on_node, client_path=dest_dir_on_vm)
        # Copy ambitrains data to virtual machine
        self.get(local_path=ambitrains_data_dir_on_node, client_path=dest_dir_on_vm)
        # Copy font data to virtual machine
        self.get(local_path=font_data_dir_on_node, client_path=dest_dir_on_vm)

    def update_python_portable(self):
        """
        Update python portable package which is used for PHOcr office testing on test virtual
        machine. This python package will be updated from SVN.

        Returns
        -------
        None

        """
        src_dir_on_node = os.path.join(self.svn_dir, DataPathSVN.PYTHON_PORTABLE, self.platform,
                                       DataPathSVN.PYTHON_FOLDER)
        dest_dir_on_vm = os.path.join(self.home_folder, self.PHOCR_DATA_DIR,
                                      self.PYTHON_PORTABLE_DIR)
        # Remove old data
        self.remove_directory(dest_dir_on_vm)
        # Make sure destination directory exists for copying
        self.make_directory(dest_dir_on_vm)
        # Copy new python package to virtual machine
        self.get(local_path=src_dir_on_node, client_path=dest_dir_on_vm)

    def update_valgrind_mekong(self):
        """
        Update valgrind utility which is used for Mekong to check memory leak on test virtual
        machine. This package is updated from SVN.

        Returns
        -------
        None

        """
        src_path_on_node = os.path.join(self.svn_dir, DataPathSVN.MEKONG_3RD_PARTY_DIR,
                                        ValGrind.VALGRIND_PACKAGE)
        mekong_data_dir_on_vm = os.path.join(self.home_folder, self.MEKONG_DATA_DIR)
        valgrind_folder_on_vm = os.path.join(mekong_data_dir_on_vm, ValGrind.VALGRIND_FOLDER)
        # Remove old data
        self.remove_directory(valgrind_folder_on_vm)
        # Make sure mekong data directory exists on virtual machine for copying
        self.make_directory(mekong_data_dir_on_vm)
        # Copy new valgrind package to virtual machine
        self.get(local_path=src_path_on_node, client_path=mekong_data_dir_on_vm)
        # Extract compressed valgrind package
        cmd = "cd {0} && tar xzf {1}".format(mekong_data_dir_on_vm, ValGrind.VALGRIND_PACKAGE)
        self.exec_command(cmd=cmd)
        # Remove valgind package on virtual machine
        valgrind_package_path_on_vm = os.path.join(mekong_data_dir_on_vm, ValGrind.VALGRIND_PACKAGE)
        self.remove_file(valgrind_package_path_on_vm)

    def get_run_test_command(self):
        """
        No need to run test.

        Returns
        -------
        None

        """
        pass

    def put_test_output(self):
        """
        No test run then no output.

        Returns
        -------
        None

        """
        pass
