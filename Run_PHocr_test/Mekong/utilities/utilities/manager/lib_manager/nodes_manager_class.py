# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      26/06/2018
# Description:      This script define class for manage nodes to execute build
import os
import traceback
import sys
import time
from abc import ABCMeta, abstractmethod
from threading import Timer
import configs.run_counter
from baseapi.file_access import copy_paths, move_paths, remove_paths, read_json, write_json
from baseapi.common import get_time_str
from configs.common import Platform
from configs.test_result import FinalTestResult
from handlers.parameters_handler import ParameterHandler, ParametersJson
from handlers.profile_handler import ProfileHandler
from manager.lib_manager.worker import Worker
from configs.projects.mekong import SystemInfo


class NodeNotDoneException(Exception):
    pass


class NodesManager(Worker):
    __metaclass__ = ABCMeta

    # Default name for execution data of processes on automation test system
    EXECUTION_TIME_DATA_FILE = "performance_data_system.json"
    # Key for execution time of management processes on master
    EXECUTION_TIME_MANAGEMENT_KEY = "__execution_time_management__"
    # Key for execution time of processes on node thread
    EXECUTION_TIME_NODE_THREADS_KEY = "__execution_time_node_threads__"
    # Key for execution time detail of workers management on node
    EXECUTION_TIME_WORKERS_MANAGEMENT_KEY = "__execution_time_workers_management__"
    # Key for total execution time on master
    EXECUTION_TIME_TOTAL = "Total time"

    def __init__(self, profile_path, parameters_file=None, **kwargs):
        parameters_handler = None
        if parameters_file:
            parameters_handler = ParameterHandler(input_file=parameters_file)
        self.profile_handler = ProfileHandler(input_file=profile_path,
                                              parameters_handler=parameters_handler)
        super(NodesManager, self).__init__(info_handler=parameters_handler,
                                           platform=Platform.LINUX,
                                           log_level=2, **kwargs)
        self.work_nodes = []
        self.log_folder = None
        # Time execution of processes on node threads collections
        self.node_threads_execution_data = dict()
        # Time execution data of whole system
        self.performance_data = dict()

    @abstractmethod
    def pre_process(self):
        pass

    # Prepare for work by cleaning workspace
    @abstractmethod
    def prepare_work(self):
        pass

    # Run build on workers
    def do_work(self):
        try:
            # Do some pre-process before we can get work nodes.
            # Such as executing distribution before execute testing
            self.pre_process()

            # Initial all workers. This list maybe pre-initialed
            self.work_nodes = self.get_work_nodes()

            # Prepare for work
            self.prepare_work()

            # Run workers
            self.run_workers()

            # Post build to arrange build results
            self.post_process()

            # All good, we can stop run
            configs.run_counter.RUN_STOPPED = True

        except NodeNotDoneException:
            self.combine_result_when_node_not_done_exception()
            # When a node fail to work, consider to try again on others
            if configs.run_counter.RUN_COUNT + 1 > configs.run_counter.MAX_RUN_TIMES:
                # Try enough, stop run
                configs.run_counter.RUN_STOPPED = True
                var = traceback.format_exc()
                if self.log_level >= 0:
                    self.logger.log_and_print(var)
                else:
                    print(var)
                sys.exit(1)
            else:
                # Try again
                pass
        except:
            # Other exceptions is system error on master, so we need to stop run
            # immediately
            configs.run_counter.RUN_STOPPED = True
            var = traceback.format_exc()
            if self.log_level >= 0:
                self.logger.log_and_print(var)
            else:
                print(var)
            sys.exit(1)
        finally:
            # Get log for this run
            if self.log_folder:
                self.get_log()
            # Turn to next run if possible
            configs.run_counter.RUN_COUNT += 1

    def run_workers(self):
        # Initial thread for workers control
        self.logger.start_step("Working on remote nodes by running workers manager script")
        if not self.work_nodes:
            self.logger.end_step(is_success=False)
            sys.exit(2)
        threads = []
        for node in self.work_nodes:
            threads.append(Timer(1, node.do_work, []))
        # Ask worker to work
        for x in threads:
            x.start()
        # Wait for all work done
        for x in threads:
            x.join()
        self.logger.end_step(True)

        # Check if any worker has not done the work
        self.logger.start_step("Collect work status of nodes")
        nodes_not_done = []
        for node in self.work_nodes:
            if not node.work_done:
                nodes_not_done.append(node.name)

        # Collect execution profiling data of node threads
        for node in self.work_nodes:
            self.node_threads_execution_data[node.name] = node.logger.performance_data

        if nodes_not_done:
            self.logger.end_step(False)
            raise NodeNotDoneException("Fail to do work on workers: {0}"
                                       "".format(",".join(nodes_not_done)))
        else:
            self.logger.end_step(True)

    # Get log and arrange final results folder
    @abstractmethod
    def post_process(self):
        pass

    @abstractmethod
    def get_work_nodes(self):
        pass

    def get_log(self):
        self.logger.start_step("Get information of test system")
        final_info_folder = FinalTestResult.INFO
        if not os.path.isdir(final_info_folder):
            os.makedirs(final_info_folder)
        # Arrange parameters json file
        copy_paths(ParametersJson.DEFAULT_NAME, final_info_folder)
        # Arrange log
        log_folder_by_latest_run = \
            configs.run_counter.RUN_FOLDER_TEMPLATE.format(count=configs.run_counter.RUN_COUNT)
        log_folder_by_run_time = os.path.join(self.log_folder, log_folder_by_latest_run)
        log_master_folder = os.path.join(log_folder_by_run_time,
                                         self.logger.OBJECT_LOG_FOLDER.format(self.name))
        if not os.path.isdir(log_folder_by_run_time):
            os.makedirs(log_folder_by_run_time)
        if not os.path.isdir(log_master_folder):
            os.makedirs(log_master_folder)
        system_info = {}
        for node in self.work_nodes:
            move_paths(node.logger.output_file, log_master_folder)
            if os.path.isdir(node.result_folder):
                src_node_log_folder = os.path.join(node.result_folder, FinalTestResult.LOG)
                final_node_log_folder = \
                    os.path.join(log_folder_by_run_time,
                                 node.logger.OBJECT_LOG_FOLDER.format(node.name))
                if os.path.isdir(final_node_log_folder):
                    remove_paths(final_node_log_folder)
                move_paths(src_node_log_folder, final_node_log_folder)
                remove_paths(node.result_folder)
                # Combine system information for all node
                node_info_file = os.path.join(final_node_log_folder, SystemInfo.SYSTEM_INFO_FILE)
                if os.path.isfile(node_info_file):
                    system_info[node.name] = read_json(path=node_info_file)
                else:
                    system_info[node.name] = {}

        # Write system information to log folder
        final_system_info_file = os.path.join(log_folder_by_run_time, SystemInfo.SYSTEM_INFO_FILE)
        write_json(obj=system_info, file_name=final_system_info_file)

        # Get profile system of this run
        copy_paths(self.profile_handler.input_file, log_folder_by_run_time)

        # Get some more log
        try:
            self.get_more_log()
        except:
            traceback.print_exc()
            print("Can not get more log for processes!")

        self.logger.end_step(True)
        move_paths(self.logger.output_file, log_master_folder)

    @abstractmethod
    def get_more_log(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    # This need to be done when NodeNotDoneException is raised
    @abstractmethod
    def combine_result_when_node_not_done_exception(self):
        pass

    def generate_execution_time_data(self):
        """
        This action will be done when job done on master. We collect execution data from all
        elements of automation test system and combine them into only 1 data json file.
        - Execution time of management processes on master
        - Execution time of processes on node thread
        - Execution time which is receive from remote node when execute workers_manage.py

        Returns
        -------
        None

        """
        # End the logger
        self.logger.end(write_to_file=False)
        # Collect all performance data from nodes
        self.performance_data = dict()
        # Add execution time data for node management on master
        self.performance_data[self.EXECUTION_TIME_MANAGEMENT_KEY] = self.logger.performance_data
        # Add detail execution time data on node threads
        self.performance_data[self.EXECUTION_TIME_NODE_THREADS_KEY] = \
            self.node_threads_execution_data
        # Total time of processing on master
        total_time = get_time_str(time.time() - self.logger.start_time)
        self.performance_data[self.EXECUTION_TIME_TOTAL] = total_time
        # Write execution information to log folder
        # Name of the logging folder for current run time
        log_folder_by_latest_run = \
            configs.run_counter.RUN_FOLDER_TEMPLATE.format(count=configs.run_counter.RUN_COUNT)
        # Full path on master to logging folder for current run time
        log_folder_by_run_time = os.path.join(self.log_folder, log_folder_by_latest_run)
        # Logging folder for a run time includes log from master and also log from nodes. So we
        # need to define a folder to store logging data which is generated on master.
        log_master_folder = os.path.join(log_folder_by_run_time,
                                         self.logger.OBJECT_LOG_FOLDER.format(self.name))
        # Make sure all directory exists before interaction
        if not os.path.isdir(log_folder_by_run_time):
            os.makedirs(log_folder_by_run_time)
        if not os.path.isdir(log_master_folder):
            os.makedirs(log_master_folder)
        # Get path for final output data file
        execution_time_data_file_master = \
            os.path.join(log_master_folder,
                         self.logger.DEFAULT_PERFORMANCE_DATA_JSON_FILE.format(self.logger.name))
        # Write execution data to json file. This json file could be used to generate an excel
        # report later.
        write_json(obj=self.performance_data, file_name=execution_time_data_file_master)
