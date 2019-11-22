# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      26/06/2018
# Description:      This script define class for a virtual machine that build PHOcr on linux
#                   platform.
import os
import sys
import traceback
import time
from abc import ABCMeta, abstractmethod
from threading import Timer
from baseapi.file_access import move_paths, remove_paths, write_json
from configs.common import Platform
from configs.json_key import ProfileJson
from handlers.parameters_handler import ParameterHandler
from handlers.profile_handler import ProfileHandler
from manager.lib_manager.worker import Worker
from configs.projects.mekong import SystemInfo
from manager.lib_vm.defines import VBLogFile


class WorkerNotDoneException(Exception):
    pass


class WorkersManager(Worker):
    __metaclass__ = ABCMeta

    # Error code for missing parameters information for testing
    ERR_NO_MISSING_PARAMETERS = 1

    # Execution time of management processes on node
    EXECUTION_TIME_MANAGEMENT_KEY = "__execution_time_management__"
    # Execution time logging data from workers key
    EXECUTION_TIME_WORKERS_KEY = "__execution_time_on_workers__"
    # Total execution time on node for job
    EXECUTION_TIME_TOTAL_KEY = "Total time"

    def __init__(self, parameters_file=None, profile_path=None, **kwargs):
        """
        Constructor for a abstract workers manager. This help manage virtual machines on a node
        to execute a task. For specific purpose, there will be a derived class from this one to
        execute the work.

        Parameters
        ----------
        parameters_file : str
            Path to parameters json file. This file includes information which is necessary for
            build/test. No require in case update data job.
        profile_path : str
            Path to system profile configuration file. This is required for all jobs
        """
        parameters_handler = None
        if parameters_file:
            parameters_handler = ParameterHandler(input_file=parameters_file)
        self.profile_handler = ProfileHandler(input_file=profile_path,
                                              parameters_handler=parameters_handler)
        super(WorkersManager, self).__init__(info_handler=parameters_handler,
                                             platform=Platform.LINUX, **kwargs)
        self.update_profile()
        self.workers = list()
        self.result_node_folder = None
        # List of failed workers
        self.workers_not_done = list()

        # Detail execution time logging from workers
        self.workers_time_execution_data = dict()
        self.performance_data = dict()

    def update_profile(self):
        node_info = self.profile_handler.get_node_info(self.name)
        if node_info:
            self.ip = node_info[ProfileJson.info.IP]
            self.username = node_info[ProfileJson.info.USER]

    # Prepare for work by cleaning workspace
    @abstractmethod
    def prepare_work(self):
        pass

    # Run build on workers
    def do_work(self):
        try:
            # Initial all workers
            self.workers = self.get_workers()
            if self.workers:
                # Prepare for work
                self.prepare_work()

                # Run workers
                self.run_workers()

                # Post build to arrange build results
                self.post_process()
            else:
                self.logger.log_and_print("No workers to be run!")
        except WorkerNotDoneException:
            var = traceback.format_exc()
            print(var)
            if self.log_level >= 0:
                self.logger.log_and_print(var)
            else:
                print(var)
            self.combine_results_when_worker_not_done_exception()
            sys.exit(1)
        except:
            var = traceback.format_exc()
            print(var)
            if self.log_level >= 0:
                self.logger.log_and_print(var)
            else:
                print(var)
            sys.exit(1)
        finally:
            self.get_log()

    def run_workers(self):
        # Initial all worker
        self.logger.start_step("Initial workers")
        self.logger.log_and_print("Workers:")
        for worker in self.workers:
            self.logger.log_and_print("{0}: Working on {1}".format(worker.name,
                                                                   worker.platform))
        self.logger.end_step(True)

        # Wake all workers up
        self.logger.start_step("Wake up all workers")
        for worker in self.workers:
            try:
                worker.start()
            except:
                worker.work_done = False
                self.workers_not_done.append(worker.name)
        self.logger.end_step(True)

        # Reset time clock of logger of workers to really start working. Also, currently we need
        # to wait for some seconds to let virtual machines start and initial their network
        time_wait_workers_wake_up = 25
        for worker in self.workers:
            worker.logger.reset_time_clock()
            worker.logger.performance_data.append(
                {
                    "Wait for virtual machine get up": time_wait_workers_wake_up
                }
            )

        # Initial thread for workers control
        self.logger.start_step("Working on virtual machines")
        threads = []
        for worker in self.workers:
            if worker.name not in self.workers_not_done:
                threads.append(Timer(time_wait_workers_wake_up, worker.do_work, []))
        # Ask worker to work
        for x in threads:
            x.start()
        # Wait for all work done
        for x in threads:
            x.join()
        self.logger.end_step(True)

        self.logger.start_step("Get status of system")
        # Get full list of worker not done work
        for worker in self.workers:
            if (not worker.work_done) and worker.name not in self.workers_not_done:
                self.workers_not_done.append(worker.name)

        # Check if any worker has not done the work
        system_info = {}
        for worker in self.workers:
            if not worker.work_done:
                system_info[worker.name] = SystemInfo.F_FAILED
            else:
                system_info[worker.name] = SystemInfo.F_SUCCESS
        # Write system information
        write_json(obj=system_info, file_name=SystemInfo.SYSTEM_INFO_FILE)

        # Collect detail execution data on workers
        for worker in self.workers:
            self.workers_time_execution_data[worker.name] = worker.logger.performance_data

        if self.workers_not_done:
            raise WorkerNotDoneException("Fail to do work on workers: {0}"
                                         "".format(",".join(self.workers_not_done)))
        self.logger.end_step(True)

    @abstractmethod
    def post_process(self):
        """
        This is abstract method and need to be implemented on derive class. For different job,
        we have different action to combine results and finish the job when receive raw results
        from virtual machines

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def get_workers(self):
        """
        This is abstract method and need to be implemented on derive class. Base on BUILD or TEST
        job and system configuration then we have different workers to initial.

        Returns
        -------
        None

        """
        pass

    def get_log(self):
        """
        Arrange log folder on node

        Returns
        -------
        None

        """
        # Create final test result folder
        if not os.path.isdir(self.result_node_folder):
            os.makedirs(self.result_node_folder)
        # Arrange log
        log_folder = os.path.join(self.result_node_folder, "log")
        if os.path.isdir(log_folder):
            remove_paths(log_folder)
        os.makedirs(log_folder)
        for worker in self.workers:
            move_paths(worker.logger.output_file, log_folder)
        move_paths(self.logger.output_file, log_folder)

        # Get build log on windows
        if os.path.isfile(VBLogFile.LOG_BUILD_DEBUG):
            move_paths(VBLogFile.LOG_BUILD_DEBUG, log_folder)
        if os.path.isfile(VBLogFile.LOG_BUILD_RELEASE):
            move_paths(VBLogFile.LOG_BUILD_RELEASE, log_folder)

        # System information
        if os.path.isfile(SystemInfo.SYSTEM_INFO_FILE):
            move_paths(SystemInfo.SYSTEM_INFO_FILE, log_folder)

        # Execution time data of test system
        execution_time_data_file = self.logger.DEFAULT_PERFORMANCE_DATA_JSON_FILE.format(self.name)
        if os.path.isfile(execution_time_data_file):
            move_paths(execution_time_data_file, log_folder)

    def start(self):
        """
        This class same as a node, then a node always online and no need a start method to control.

        Returns
        -------
        None

        """
        pass

    def stop(self):
        """
        This class same as a node, then a node always online and no need a stop method.

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def combine_results_when_worker_not_done_exception(self):
        """
        Abstract method need to be implemented on derive classes. Currently, there are some work
        need to be done when run fail on any virtual machine.

        Returns
        -------
        None

        """
        pass

    def generate_execution_time_data(self):
        """
        Collect execution time of management processes and detail execution time on each worker
        thread and write to json file.

        Returns
        -------
        None

        """
        self.logger.end(write_to_file=False)
        self.performance_data = dict()
        # Execution time of management processes on node
        self.performance_data[self.EXECUTION_TIME_MANAGEMENT_KEY] = self.logger.performance_data
        # Detail execution time on worker threads
        self.performance_data[self.EXECUTION_TIME_WORKERS_KEY] = self.workers_time_execution_data
        # Total time on node
        total_time = time.time() - self.logger.start_time
        self.performance_data[self.EXECUTION_TIME_TOTAL_KEY] = total_time
        # Write collected data to json file
        write_json(self.performance_data, self.logger.DEFAULT_PERFORMANCE_DATA_JSON_FILE.format(
            self.name))
