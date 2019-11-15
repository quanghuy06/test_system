# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      16/09/2019
# Description:      This script implement a class which help parsing execution time data
#                   profiling from automation test system
from baseapi.file_access import read_json
from baseapi.log_manager import Logger
from manager.lib_manager.nodes_manager_updater import NodesManagerUpdater
from manager.lib_manager.workers_manager_updater import WorkersManagerUpdater


class ExecutionTimeDataParser(object):

    # Key to extract total time of all processes
    TOTAL_TIME_KEY = "Total time"

    # Key to extract time of processes on main thread
    MAIN_PROCESSES_TIME_KEY = [
        NodesManagerUpdater.EXECUTION_TIME_MANAGEMENT_KEY,
        WorkersManagerUpdater.EXECUTION_TIME_MANAGEMENT_KEY
    ]

    # Key to extract execution time of processes on threads which execute ssh connection to
    # remote workers
    PROCESSES_ON_THREAD_TIME_KEY = [
        NodesManagerUpdater.EXECUTION_TIME_NODE_THREADS_KEY,
        WorkersManagerUpdater.EXECUTION_TIME_WORKERS_KEY
    ]

    # Key to extract execution time of build stage will include this sub-string
    BUILD_STAGE_KEY_INCLUDE = "BUILD "

    # Key to extract execution time of test stage will include this sub-string
    TEST_STAGE_KEY_INCLUDE = "TEST "

    def __init__(self, input_file=None, name=None):
        """
        Constructor for the class.

        Parameters
        ----------
        input_file: str
            Path to json data file which need to parse.

        """
        # Some data objects which are useful to be used
        self._data = None
        self._main_processes_time_data = None
        self._processes_on_threads_data = None
        # Set the name to identify a parser in a list
        self.name = name
        # Set up path to input json file and extract data objects
        self.input_file = input_file

    @property
    def name(self):
        """
        Get name of the data parser object

        Returns
        -------
        str
            Name of the parser

        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Set a name for the parser for identification

        Parameters
        ----------
        name: str
            Name of the data parser

        Returns
        -------
        None

        """
        self._name = name

    @property
    def input_file(self):
        """
        Getter for path to json data file

        Returns
        -------
        str
            Path to json data file

        """
        return self._input_file

    @input_file.setter
    def input_file(self, input_file):
        """
        Setter for path to json data file

        Parameters
        ----------
        input_file: str
            Path to json data file

        Returns
        -------
        None

        """
        self._input_file = input_file
        # Try to extract data from json data file into data object
        if self._input_file:
            # Read data into json object
            self.data = read_json(self._input_file)

    @property
    def data(self):
        """
        Getter for json data object

        Returns
        -------
        dict/list
            Json data object

        """
        return self._data

    @data.setter
    def data(self, json_object):
        """
        Setter for json object file. In this setter, we also extract some data object which will
        be used later.

        Parameters
        ----------
        json_object: dict/list
            Data object which need to be processed

        Returns
        -------
        None

        """
        self._data = json_object
        # Extract execution time data for processes on the main thread
        main_processes_time_key = list(key for key in self.MAIN_PROCESSES_TIME_KEY if key in
                                       self._data)[0]
        self.main_processes_time_data = self._data[main_processes_time_key]
        # Extract execution time data for processes on a thread
        processes_on_thread_key = list(key for key in self.PROCESSES_ON_THREAD_TIME_KEY if key in
                                       self._data)[0]
        self.processes_on_thread_time_data = self._data[processes_on_thread_key]

    def total_time(self):
        """
        Get execution time of total process

        Returns
        -------
        float
            Total time of all processes

        """
        return self.data[self.TOTAL_TIME_KEY]

    @property
    def main_processes_time_data(self):
        """
        Getter for execution time data of processes on the main thread

        Returns
        -------
        list
            List of data object. Currently, one dictionary for execution time data for processes
            and one for total time of processes.

        """
        return self._main_processes_time_data

    @main_processes_time_data.setter
    def main_processes_time_data(self, execution_time_data):
        """
        Setter for execution time data of processes on the main thread.

        Parameters
        ----------
        execution_time_data: list
            Execution time data of processes on the main thread. This should include two objects,
            one for execution time data of processes and one for total time of all processes.

        Returns
        -------
        None

        """
        self._main_processes_time_data = execution_time_data

    @property
    def processes_on_thread_time_data(self):
        """
        Getter for execution time data of processes which are executed on threads.

        Returns
        -------
        dict
            Key in this case is name of the worker and value is detail execution on thread which
            control worker over ssh connection.

        """
        return self._processes_on_threads_data

    @processes_on_thread_time_data.setter
    def processes_on_thread_time_data(self, execution_time_data):
        """
        Setter for execution time data on the threads which control workers over ssh connection

        Parameters
        ----------
        execution_time_data: dict
            Key is the name of worker. Value is a data object includes execution time of
            processes on the thread.

        Returns
        -------
        None

        """
        self._processes_on_threads_data = execution_time_data

    def get_stages_list(self):
        """
        Get list name of stages on the main thread. Currently, execution time data for the main
        processes is constructed like this:
        [
            {
                "stage_name": {
                    "Steps": [
                        {
                            "step_name_1": <float value>
                        },
                        {
                            "step_name_2": <float value>
                        }
                    ],
                    "Total time": <float value>
                },
                "stage_name_2": {...},
                "step_name": <float value>,
                ...
            },
            {
                "Total time": <float value>
            }
        ]
        Then a stage block data has value type is a dictionary. For this case, list of stages
        should be ["stage_name", "stage_name_2"]

        Returns
        -------
        list
            List name of stages on the main thread

        """
        stages = list()
        for obj in self._main_processes_time_data:
            for key in obj:
                if type(obj[key]) is dict:
                    # Execution data for a stage is a dictionary, not just a value
                    stages.append(key)
        return stages

    def get_stage_time_data(self, stage_name):
        """
        Get data object of execution time of a processes on a stage

        Parameters
        ----------
        stage_name: str
            Name of stage to extract data

        Returns
        -------
        dict
            Data object of execution time of processes on a stage. None is return if stage can
            not be found.

        """
        for obj in self._main_processes_time_data:
            if stage_name in obj:
                return obj[stage_name]

    def get_stage_total_time(self, stage_name):
        """
        Get total execution time on a stage

        Parameters
        ----------
        stage_name: str
            Name of stage to extract data

        Returns
        -------
        float
            Total execution time of stage

        """
        return self.get_stage_time_data(stage_name)[self.TOTAL_TIME_KEY]

    def get_steps_list(self):
        """
        Get list name of steps on the main thread. Currently, on the main thread, maybe there are
        some steps which has the same level with stages such like this:
        [
            {
                "stage_name": {
                    <data object>
                }
            },
            {
                "step_name_1": <float value>
            },
            {
                "step_name_2": <float value>
            },
            {
                "Total time": <float value>
            }
        ]
        Then a step data example has key different from "Total time" and has type float to
        distinguish with stage data. For the example, list name of steps should be [
        "step_name_1", "step_name_2"]

        Returns
        -------
        list
            List name of steps on the main thread

        """
        main_steps = list()
        for obj in self._main_processes_time_data:
            for key in obj:
                if key != self.TOTAL_TIME_KEY and self.is_number(obj[key]):
                    # A step execution data has key not total time and has type float, not object
                    main_steps.append(key)
        return main_steps

    def get_step_execution_time(self, step_name):
        """
        Get execution time of a step on the main thread

        Parameters
        ----------
        step_name: str
            Name of step to extract execution time data

        Returns
        -------
        float
            Execution time of a step on the main thread. Return 0 if step not found.

        """
        for obj in self._main_processes_time_data:
            if step_name in obj:
                return obj[step_name]
        # Return 0 if step doesn't exist on the main thread data
        return 0

    def get_steps_list_on_stage(self, stage_name):
        """
        Get list name of steps on a stage on main thread. Currently, the following is structure
        of data for a stage:
        {
            "Steps": [
                {
                    "step_name_1": <float value>
                },
                {
                    "step_name_2": <float value>
                },
                ...
            ],
            "Total time": <float value>
        }
        Then for the above structure, list name of steps on the stage is ["step_name_1",
        "step_name_2"]

        Parameters
        ----------
        stage_name: str
            Name of stage to extract data

        Returns
        -------
        list
            List name of steps on stage processes on main thread

        """
        # Get execution time data for steps of the stage
        steps_on_stage_time_data = self.get_stage_time_data(stage_name)[Logger.STEP_DATA_KEY]
        # Collect name of steps on the stage
        steps = list()
        for obj in steps_on_stage_time_data:
            for key in obj:
                if key != self.TOTAL_TIME_KEY and self.is_number(obj[key]):
                    # Data value of a step should be float type
                    steps.append(key)
        return steps

    def get_step_execution_time_on_stage(self, stage_name, step_name):
        """
        Get execution time of a step on a stage on the main thread

        Parameters
        ----------
        stage_name: str
            Name of stage to extract data
        step_name: str
            Name of step to extract data

        Returns
        -------
        float
            Execution time of step on the stage. Return 0 if step can be found.

        """
        # Get execution time data for steps on the stage
        steps_on_stage_time_data = self.get_stage_time_data(stage_name)[Logger.STEP_DATA_KEY]
        for obj in steps_on_stage_time_data:
            if step_name in obj:
                # Step found
                return obj[step_name]
        # Return 0 if step can not be found
        return 0

    def get_threads_list(self):
        """
        Get list name of threads/workers. Currently, structure of execution time data for threads
        look like this:
        {
            "thread_1": {...},
            "thread_2": {...},
            ...
        }
        For this example, list name of threads is ["thread_1", "thread_2"]

        Returns
        -------
        list
            List name threads/workers

        """
        return sorted(self.processes_on_thread_time_data.keys())

    def get_total_execution_time_on_thread(self, thread_name):
        """
        Get total execution time on a thread

        Parameters
        ----------
        thread_name: str
            Name of thread to extract data

        Returns
        -------
        float
            Total execution time on a thread. If total time key can not be found, then return 0

        """
        for obj in self._processes_on_threads_data[thread_name]:
            for key in obj:
                if key == self.TOTAL_TIME_KEY:
                    return obj[key]
        return 0

    def get_thread_execution_time_data(self, thread_name):
        """
        Get execution time data on a thread control. Thread is using to control a worker over ssh
        connection. Currently, processes on a thread are separated into steps only. There is no
        stage to be presented.

        Parameters
        ----------
        thread_name: str
            Name of thread/worker

        Returns
        -------
        list
            List of execution time of steps on the thread

        """
        return self._processes_on_threads_data[thread_name]

    def get_steps_list_on_thread(self, thread_name):
        """
        Get list name of steps of processes on a thread. Currently, this is the structure of data
        for threads:
        {
            "thread_name_1": [
                {
                    "step_name_1": <float value>
                },
                {
                    "step_name_2": <float value>
                },
                ...
            ],
            ...
        }
        So, for this case, list name of steps of thread_name_1 is ["step_name_1", "step_name_2"]

        Parameters
        ----------
        thread_name: str
            Name of the thread/worker to extract data

        Returns
        -------
        list
            List name of steps on the thread

        """
        # Execution time data of processes on thread which control worker over ssh connection
        execution_time_data_on_thread = self._processes_on_threads_data[thread_name]
        # Collect list name of steps
        steps = list()
        for obj in execution_time_data_on_thread:
            for key in obj:
                if key != self.TOTAL_TIME_KEY and self.is_number(obj[key]):
                    # Step data value should be a float value
                    steps.append(key)
        return steps

    def get_step_execution_time_on_thread(self, thread_name, step_name):
        """
        Get execution time of a step on a thread.

        Parameters
        ----------
        thread_name: str
            Name of the thread/worker which need to be extracted data
        step_name: str
            Name of step to extract data

        Returns
        -------
        float
            Execution data of the step on thread

        """
        # Get execution time of processes on the thread
        execution_time_data_on_thread = self._processes_on_threads_data[thread_name]
        # Extract execution time data of the step
        for obj in execution_time_data_on_thread:
            if step_name in obj:
                return obj[step_name]
        # Return 0 if step can not be found
        return 0

    @staticmethod
    def is_number(input_value):
        """
        Check if an input value is number or not. A number should has type int or float

        Parameters
        ----------
        input_value: int/float
            Value need to be checked

        Returns
        -------
        bool
            True if input value is number which has type int or float. Otherwise, return False.

        """
        if isinstance(input_value, int) or isinstance(input_value, float):
            return True
        return False
