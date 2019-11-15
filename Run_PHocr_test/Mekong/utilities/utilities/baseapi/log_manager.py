# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      07/10/2016
# Description:      This script define class to manage log writer of
#                   test system
# Change log:
#       2018-04-21: Refactor a common Logger class for all objects use
import time
from abc import ABCMeta
from baseapi.file_access import write_line, write_text, write_json
from baseapi.common import get_time_str
from datetime import datetime


class Logger(object):
    __metaclass__ = ABCMeta

    # Default name of performance data json file
    DEFAULT_PERFORMANCE_DATA_JSON_FILE = "performance_data_{0}.json"

    # Key for performance data of stages
    STAGE_DATA_KEY = "Stages"

    # Prefix for stage logging
    STEP_LOGGING_PREFIX = ">>>"

    # Key for performance data of steps
    STEP_DATA_KEY = "Steps"

    # Key for total time of process
    TOTAL_TIME_KEY = "Total time"

    # Default text log file
    TEXT_LOG_OUTPUT_DEFAULT = "log.txt"

    # Default log file for a specific object
    OBJECT_LOG_OUTPUT = "{0}.log"

    # Default log folder
    OBJECT_LOG_FOLDER = "log_{0}"

    # Time stamp format
    TIME_STAMP_FORMAT = "[%m/%d/%Y %H:%M:%S]"

    def __init__(self, name=None, output_file=None, log_disable=False):
        """
        Constructor for logger object.

        Parameters
        ----------
        name : str
            Name of object which logger works for
        output_file : str
            Path to text output file for logging information
        log_disable : str
            Flag to request disable logging
        """
        self.disable = log_disable
        self.name = name
        # Set up target output text log file
        if output_file:
            self.output_file = output_file
        elif self.name:
            self.output_file = self.OBJECT_LOG_OUTPUT.format(self.name)
        else:
            self.output_file = self.TEXT_LOG_OUTPUT_DEFAULT
        # Time logging
        # Start for logger object
        self.start_time = time.time()
        # Start time for current stage. Logging information could includes some stage. Then a
        # stage could includes some small steps.
        self.stage_start_time = 0
        self.current_stage = ""
        # Start time for current step. A step is a child task in a stage
        self.step_start_time = 0
        self.current_step = ""
        # Data logging for system performance
        self.performance_data = list()
        self.performance_stage_data = dict()

    def init_performance_stage_data(self):
        """
        Initial/Reset execution data for a stage when initial object or end of stage

        Returns
        -------

        """
        self.performance_stage_data = dict()
        self.performance_stage_data[self.STEP_DATA_KEY] = list()

    def time_stamp_now(self):
        """
        Get current time stamp in right format for text logging

        Returns
        -------
        str
            Time stamp for now in string format

        """
        return datetime.now().strftime(self.TIME_STAMP_FORMAT)

    def end(self, execution_log_output=None, write_to_file=True):
        """
        End of logging. Collect data and generate logging files.

        Returns
        -------
        None

        """
        # Log total execution time of whole process on object
        self.performance_data.append(
            {
                self.TOTAL_TIME_KEY: time.time() - self.start_time
            }
        )
        # Write execution time logging to json file
        if execution_log_output:
            execution_output_file = execution_log_output
        else:
            execution_output_file = self.DEFAULT_PERFORMANCE_DATA_JSON_FILE.format(self.name)

        # Write logging information to file
        if write_to_file:
            write_json(self.performance_data, execution_output_file)

    def start_stage(self, stage_name, width=80):
        """
        Prepare for stage starting such as save start time of the

        Parameters
        ----------
        stage_name : str
            Name of stage
        width : int
            Width for stage header logging

        Returns
        -------
        None

        """
        if not self.disable:
            self.current_stage = stage_name
            # Only accept even number
            if width % 2 == 1:
                width -= 1
            # Minimum of width
            if width < (10 + len(stage_name)):
                width = 10 + len(stage_name)
            self.log_and_print("-"*width)
            num_space = int((width - 1 - len(stage_name)) / 2)
            self.log_and_print("|" + " " * num_space + stage_name + " " * num_space + "|")
            self.log_and_print("-"*width)
            self.log_and_print("")
            self.stage_start_time = time.time()
            # Prepare dictionary to store execution time of steps
            self.init_performance_stage_data()

    def end_stage(self, is_success, width=80):
        """
        Post process at ending of a stage:
        - Add text logging to output file
        - Add total time to execution time data of stage
        - Append stage performance data to performance data of object
        - Reset stage performance data for the next stage

        Parameters
        ----------
        is_success : bool
            Status of job. True if job finishes successfully and False if it fail.
        width : int
            Length of start stage header string in log output file.

        Returns
        -------
        None

        """
        if not self.disable:
            status = "SUCCESSFULLY"
            if not is_success:
                status = "FAILED"
            self.log_and_print("End of stage {status}!".format(status=status))
            total_time = time.time() - self.stage_start_time
            # Add time execute value for stage
            self.performance_stage_data[self.TOTAL_TIME_KEY] = total_time
            # Append execute time data of stage to execute time of object
            self.performance_data.append(
                {
                    self.current_stage: self.performance_stage_data
                }
            )
            # Print time execute to text log output
            self.log_and_print("Total time stage: {0}".format(get_time_str(total_time)))
            self.log_and_print("-"*width)
            self.log_and_print("")
            # Reset performance stage data for the next one
            self.init_performance_stage_data()

    def start_step(self, step_name):
        """
        Adding log to notice a step started.

        Parameters
        ----------
        step_name

        Returns
        -------

        """
        if not self.disable:
            self.current_step = step_name
            self.log_and_print("{prefix} {step_name}".format(prefix=self.STEP_LOGGING_PREFIX,
                                                             step_name=step_name))
            self.step_start_time = time.time()

    def end_step(self, is_success):
        """
        Post process when a step end:
        - Add text logging to output file
        - Add total time to execution time data of step
        - Append step performance data to performance data of current stage

        Parameters
        ----------
        is_success : Status of executing the step. True if step finishes successfully and False
        if execution of step fails.

        Returns
        -------
        None

        """
        if not self.disable:
            status = "successfully"
            if not is_success:
                status = "failed"
            total_time = time.time() - self.step_start_time
            # Add time execution for step
            if self.performance_stage_data:
                # Add execution time for step to current stage which it belongs to
                self.performance_stage_data[self.STEP_DATA_KEY].append(
                    {
                        self.current_step: total_time
                    }
                )
            else:
                # Step is on main thread, same level as a stage
                self.performance_data.append(
                    {
                        self.current_step: total_time
                    }
                )
            # Write execution time for log file and standard output
            self.log_and_print("End of step {0} {1}: {2}"
                               "".format(self.current_step, status, get_time_str(total_time)))

    def add_line(self, message):
        """
        Write message to log file and add a new line after the message

        Parameters
        ----------
        message : str
            Message to write to log file

        Returns
        -------
        None

        """
        if not self.disable:
            write_line(message, self.output_file)

    def add_end_line(self, num=1):
        """
        Write a new line to log file

        Parameters
        ----------
        num : Number of new line to write

        Returns
        -------

        """
        if not self.disable:
            for i in range(0, num):
                write_line("", self.output_file)

    def reset(self):
        """
        Empty log file

        Returns
        -------
        None

        """
        if not self.disable:
            write_text("", self.output_file)

    def reset_time_clock(self):
        """
        Reset start time to current time

        Returns
        -------
        None

        """
        self.start_time = time.time()

    def log_and_print(self, message):
        """
        Write logging message to both of log file and standard output such as monitor.

        Parameters
        ----------
        message : Message to log

        Returns
        -------
        None

        """
        if not self.disable:
            full_message = ""
            # Name of object logging
            if self.name:
                full_message += "[{object_name}]".format(object_name=self.name)
            # Add time stamp for logging
            full_message += self.time_stamp_now()
            full_message += " {message}".format(message=message)
            # Write log message to file
            write_line(full_message, self.output_file)
            # Write log message to standard output (monitor)
            print(full_message)
