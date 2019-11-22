# TOSHIBA - TSDV
# Team:             PHOcr
# Author:
# Email:
# Date create:
# Last update by:      Phung Dinh Tai
# Date:             03/10/2019
# Description:      This script defines class which help synchronizing data on nodes in test system
#                   from node master
import time
import subprocess
import threading
import sys_path
sys_path.insert_sys_path()
from configs.common import Machines
from configs.linux import LinuxCmd
from baseapi.log_manager import Logger
from baseapi.common import get_time_str


class NodesSynchronizer(object):
    def __init__(self, log_sync_file="NodesSynchronization"):
        """
        Constructor for class which help synchronizing data for nodes from master

        Parameters
        ----------
        log_sync_file: str
            Path to logging file for processes
        """
        self.logger = Logger(name=log_sync_file)

    def synchronize_test_cases(self):
        """
        API to run synchronization for test cases folder on nodes

        Returns
        -------
        None

        """
        self._sync_test_cases_all_nodes()

    def _sync_test_cases_node(self, machine, lock):
        """
        Run synchronization for a node from master. This is private use only.

        Sync TESTS folder on ocr3 machine to each test machine.
        Some options of rsync.
        -a: archive mode
        -v: increase verbosity
        -z: compress data before transfer. (Transfer will be fast.
            But, maybe harm disk if data is big)
        --delete: Normally, if you delete some file in source folder and run
        rsync without --delete option. These file won't be deleted
        in destination folder. So if you want to sync deleted file, the --delete option
        should be added.

        Parameters
        ----------
        machine: dict
            Information of node to be synchronized.
        lock: Lock
            Threading lock for writing logging data

        Returns
        -------
        None

        """
        # Options to run command synchronization on Linux
        option_sync = "-av --delete"

        # Calculate time for processing
        start_time = time.time()

        log_message = ">>> Sync test case for machine: {0} .....\n".format(machine[0])

        # Destination path of synchronization on remote node
        remote_path = \
            "{name}@{ip}:{tc_folder}".format(name=machine[0],
                                             ip=machine[1][Machines.IP],
                                             tc_folder=machine[1][Machines.TC_FOLDER])

        cmd_sync_data = "{rsync} {master_path} {remote_path}".format(
            rsync=LinuxCmd.RSYNC.format(option=option_sync),
            master_path=Machines.MASTER_MACHINE[Machines.TC_FOLDER],
            remote_path=remote_path
        )

        log_message += subprocess.check_output(cmd_sync_data, shell=True)

        # Use threading lock to avoid conflict when logging between threads
        lock.acquire()
        self.logger.add_line(log_message)
        self.logger.log_and_print("\nFinish in: {execution_time}".format(
            execution_time=get_time_str(time.time()-start_time)))
        lock.release()

    def _sync_test_cases_all_nodes(self):
        """
        Sync all tc in /media/ocr3/data/MekongTC/ to every nodes using multiple threads

        Returns
        -------
        None

        """
        self.logger.log_and_print(">> Synchronize test cases for all nodes on system")

        # Calculate execution time for processing
        start_time = time.time()
        # Use threading lock to avoid conflict when write to log file
        lock = threading.Lock()
        # Create list of working threads
        list_threads = list()
        for machine_node in Machines.NODE_MACHINES.items():
            thread = threading.Thread(target=self._sync_test_cases_node,
                                      args=(machine_node, lock, ))
            list_threads.append(thread)

        # Run synchronization on threads
        for thread in list_threads:
            thread.start()

        # Wait for all jobs finish
        for thread in list_threads:
            thread.join()

        self.logger.log_and_print("\n>> Total time of synchronization: {execution_time}".format(
            execution_time=get_time_str(time.time()-start_time)))
