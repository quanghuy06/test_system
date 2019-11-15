# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      17/09/2019
# Description:      This script implement a class which help generating report for performance of
#                   automation test system from collected data in json files.
from abc import ABCMeta
from report.lib_base.xlsx_reporter import XlsxReporter
from report.lib_base.cell_format import Color, Align
from report.lib_system_performance.execution_time_data_parser import ExecutionTimeDataParser


class SystemPerformanceReporter(XlsxReporter):
    __metaclass__ = ABCMeta

    # Default for output excel report
    TEMPLATE_NAME_OUTPUT_FILE = "system_performance{suffix}.xlsx"

    # Name of sheet which includes execution time for build job
    SHEET_NAME_BUILD_MASTER = "Build processes"

    # Name of sheet which includes execution time for build processes on nodes threads
    SHEET_NAME_BUILD_NODES = "Build processes on Nodes"

    # Name of sheet which includes execution time for test processes on master
    SHEET_NAME_TEST_MASTER = "Test processes on Master"

    # Name of sheet which includes execution time of test processes on node threads
    SHEET_NAME_TEST_NODES = "Test processes on Nodes"

    # Header for processes
    HEADER_PROCESSES = "Processes"

    # Header for build memory
    HEADER_BUILD_MEMORY = "Build Memory"

    # Header for build release
    HEADER_BUILD_RELEASE = "Build Release"

    # Header for execution time
    HEADER_EXECUTION_TIME = "Execution time (s)"

    # Header for actual total time
    HEADER_ACTUAL_TOTAL_TIME = "Actual total time"

    # Header for average value
    HEADER_MEAN = "Mean"

    # Header for percentage of execution time of process on total execution time
    HEADER_PERCENTAGE = "Percentage"

    # Header for balancing between max value with mean value
    HEAD_MAX_BY_MEAN = "Max - Mean"

    # Prefix for processes on master
    PREFIX_MASTER = "(Master)"

    # Prefix for processes on nodes
    PREFIX_NODE = "(Node)"

    # Prefix for processes on virtual machine threads
    PREFIX_VM = "(VM)"

    # Format for float number
    FORMAT_FLOAT_NUMBER = '#,##0.00'

    # Format for int number
    FORMAT_INT_NUMBER = '#,##0'

    def __init__(self, master_build_data_parser=None, node_build_data_parsers=None,
                 master_test_data_parser=None, node_test_data_parsers=None, **kwargs):
        """
        Constructor of reporter class for performance of automation test system

        Parameters
        ----------
        master_data_parser: ExecutionTimeDataParser
            Data parser for execution time data collection on master
        node_data_parsers: list
            List of ExecutionTimeDataParser for execution data which is received from nodes
        """
        super(SystemPerformanceReporter, self).__init__(**kwargs)
        # Execution time data for build job
        self.master_build_data_parser = master_build_data_parser
        self.node_build_data_parsers = node_build_data_parsers
        # Execution time data for test job
        self.master_test_data_parser = master_test_data_parser
        self.node_test_data_parsers = node_test_data_parsers
        # Current sheet, line, column for writing data
        self._current_sheet = None
        self._current_line = None
        self._start_column = None
        # This store max width of each column in the sheet to set width of columns
        self._max_widths = list()

    @property
    def master_build_data_parser(self):
        """
        Getter for execution data parser for execution profiling data on master

        Returns
        -------
        ExecutionTimeDataParser
            Data parser object to help parsing execution data on master

        """
        return self._master_build_data_parser

    @master_build_data_parser.setter
    def master_build_data_parser(self, data_parser):
        """
        Set up data parser object of execution time on master for build job

        Parameters
        ----------
        data_parser: ExecutionTimeDataParser
            Data parser object of execution time data on master

        Returns
        -------
        None

        """
        self._master_build_data_parser = data_parser

    @property
    def node_build_data_parsers(self):
        """
        Getter for list of data parser objects for execution data which are received from nodes
        for build job

        Returns
        -------
        list
            List of data parser objects to help parse execution data from nodes

        """
        return self._node_build_data_parsers

    @node_build_data_parsers.setter
    def node_build_data_parsers(self, data_parsers):
        """
        Setter for list data parser objects for execution data from nodes for build job

        Parameters
        ----------
        data_parsers: list
            List of data parser objects which help parsing execution data from nodes

        Returns
        -------
        None

        """
        self._node_build_data_parsers = data_parsers

    def get_node_build_data_parsers(self, node_name):
        """
        Get data parser object to help parsing data receive from a node

        Parameters
        ----------
        node_name: str
            Name of the node which need to extract data

        Returns
        -------
        ExecutionTimeDataParser
            Data parser object which parse data receive from a node

        """
        for parser in self._node_build_data_parsers:
            if parser.name == node_name:
                return parser

    @property
    def master_test_data_parser(self):
        """
        Getter for data parser object to help parsing execution data on master

        Returns
        -------
        ExecutionTimeDataParser

        """
        return self._master_test_data_parser

    @master_test_data_parser.setter
    def master_test_data_parser(self, data_parser):
        """
        Setter for data parser object to parse execution time data on master

        Parameters
        ----------
        data_parser: ExecutionTimeDataParser
            Data parser object to parse execution time data on master

        Returns
        -------
        None

        """
        self._master_test_data_parser = data_parser

    @property
    def node_test_data_parsers(self):
        """
        Getter for list of data parser object to help parsing execution data from a node which
        call to worker_manager.py

        Returns
        -------
        list
            List of data parser object to parse execution time data from node which call to
            worker_manager.py

        """
        return self._node_test_data_parsers

    @node_test_data_parsers.setter
    def node_test_data_parsers(self, data_parsers):
        """
        Setter for list of data parser object to parse execution time data from node which call to
        worker_manager.py

        Parameters
        ----------
        data_parsers: list
            List of data parser object for execution time data from nodes

        Returns
        -------

        """
        self._node_test_data_parsers = data_parsers

    def get_node_test_data_parser(self, node_name):
        """
        Get data parser for execution time for a node which call to workers_manager.py

        Parameters
        ----------
        node_name: str
            Name of the node which need to be extracted data

        Returns
        -------
        ExecutionTimeDataParser
            Data parser object for execution time data for data collected from a node

        """
        for parser in self._node_test_data_parsers:
            if parser.name == node_name:
                return parser

    def collect_data(self):
        """
        Collect data for exporting report. Currently, we have execution time data parsers are
        being set up from outside, then nothing need to do here.

        Returns
        -------
        None

        """
        pass

    def add_sheets(self):
        """
        Add work sheets to report

        Returns
        -------
        None

        """
        # Add sheet for execution time of build processes
        self.add_build_execution_time_master_sheet()

        # Add sheet for execution time of build processes on node (where worker_manager.py is
        # called)
        self.add_build_execution_time_nodes_sheet()

        # Add sheet for execution time on master of test processes
        self.add_test_execution_time_master_sheet()

        # Add sheet for detail execution time of processes on node (where worker_manager.py is
        # called)
        self.add_test_execution_time_nodes_sheet()

    def add_build_execution_time_master_sheet(self):
        """
        Add sheet for build processes execution time on master (where nodes_manager.py is called)

        Returns
        -------
        None

        """
        # If there is no execution data for build processes then nothing to report
        if not self.master_build_data_parser:
            return
        # Width of columns
        self._max_widths = list()
        # Create sheet for start writing data
        self._current_sheet = self.book.add_worksheet(name=self.SHEET_NAME_BUILD_MASTER)
        # Initial line and column for writing data. Start to write data at top left cell of the
        # sheet
        self._current_line = 0
        self._start_column = 0
        # Reset column width
        self._max_widths = list()
        # Write execution data of stages on master data
        self._add_data_block_stage_on_master(master_data_parser=self._master_build_data_parser)

        # Write execution data of processes on node thread which manage ssh connection with
        # remote node from master on build
        self._next_line(step=2)
        self._add_data_block_node_threads_on_master(
            master_data_parser=self._master_build_data_parser)
        # Set columns width to present contents clearly
        self._setup_column_width()

    def add_build_execution_time_nodes_sheet(self):
        """
        Add sheets for detail execution time of build processes on node (where workers_manager.py is
        called)

        Returns
        -------
        None

        """
        # If has no data parser objects for execution time, then nothing to report
        if not self._node_build_data_parsers:
            return

        # Execution time data which is received from a remote node will be places in a work sheet
        # of the report separately
        for node_data_parser in self._node_build_data_parsers:
            # Add new sheet for processes on a node
            self._current_sheet = self.book.add_worksheet(name=node_data_parser.name)
            # Reset start line and start column
            self._current_line = 0
            self._start_column = 0
            # Reset column width
            self._max_widths = list()
            # Write execution time data for virtual machines management on the main thread of
            # worker_manager.py
            self._add_data_block_main_processes_on_node(node_data_parser=node_data_parser)
            # Write execution time data block for processes on virtual machine threads
            self._next_line()
            self._add_data_block_processes_on_virtual_machine_threads(
                node_data_parser=node_data_parser)
            # Set columns width to present contents clearly
            self._setup_column_width()

    def add_test_execution_time_master_sheet(self):
        """
        Add sheet for test time of processes on master

        Returns
        -------
        None

        """
        # If there is no execution data for test processes then nothing to report
        if not self.master_test_data_parser:
            return

        # Create sheet for start writing data
        self._current_sheet = self.book.add_worksheet(name=self.SHEET_NAME_TEST_MASTER)
        # Initial line and column for writing data. Start to write data at top left cell of the
        # sheet
        self._current_line = 0
        self._start_column = 0
        # Reset column width
        self._max_widths = list()

        # Write execution data of stages on master data
        self._add_data_block_stage_on_master(master_data_parser=self._master_test_data_parser)

        # Write execution data of processes on node thread which manage ssh connection with
        # remote node from master on test processes
        self._next_line(step=2)
        self._add_data_block_node_threads_on_master(
            master_data_parser=self._master_test_data_parser)
        # Set columns width to present contents clearly
        self._setup_column_width()

    def add_test_execution_time_nodes_sheet(self):
        """
        Add sheets for detail execution time of process on node (where worker_manager.py is called)

        Returns
        -------
        None

        """
        # If there is no execution data for test processes then nothing to report
        if not self.master_test_data_parser:
            return

        # Execution time data which is received from a remote node will be places in a work sheet
        # of the report separately
        for node_data_parser in self._node_test_data_parsers:
            # Add new sheet for processes on a node
            self._current_sheet = self.book.add_worksheet(name=node_data_parser.name)
            # Reset start line and start column
            self._current_line = 0
            self._start_column = 0
            # Reset column width
            self._max_widths = list()
            # Write execution time data for virtual machines management on the main thread of
            # worker_manager.py
            self._add_data_block_main_processes_on_node(node_data_parser=node_data_parser)
            # Write execution time data block for processes on virtual machine threads
            self._next_line()
            self._add_data_block_processes_on_virtual_machine_threads(
                node_data_parser=node_data_parser)
            # Set columns width to present contents clearly
            self._setup_column_width()

    def _next_line(self, step=1):
        """
        Go to the next line to write data by increasing current line index by a number of steps

        Parameters
        ----------
        step: int
            Number of lines to jump. Default is go to the next line.

        Returns
        -------
        None

        """
        self._current_line += step

    def next_column(self, step=1):
        """
        Go to the next column to write data by increasing current column index by a number of steps

        Parameters
        ----------
        step: int
            Number of columns to jump. Default is go the next column

        Returns
        -------

        """
        self._start_column += step

    def _add_data_block_stage_on_master(self, master_data_parser):
        """
        Write a block of data for execution time of processes on master

        Parameters
        ----------
        master_data_parser: ExecutionTimeDataParser
            Data parser object to extract execution time information to make report. This is
            parser for processes on master for jobs (BUILD/TEST)

        Returns
        -------
        None

        """
        # Write data line by line from current line and current column
        # Write header line
        header_format = self.get_cell_format(set_border=True, set_bold=True, align=Align.CENTER,
                                             bg_color=Color.CUSTOM_GREY)
        line_data = [self.HEADER_PROCESSES, self.HEADER_EXECUTION_TIME]
        self.write_line(sheet=self._current_sheet, line=self._current_line,
                        cell_format=header_format, value_array=line_data,
                        start_position=self._start_column)
        # Update information for columns width
        self._update_columns_width(line_data=line_data)
        # Write execution time data
        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True, align=Align.RIGHT,
                                             num_format=self.FORMAT_FLOAT_NUMBER)
        stage_format = self.get_cell_format(set_border=True, set_bold=True)
        header_total_time_format = \
            self.get_cell_format(set_border=True, set_bold=True, align=Align.RIGHT,
                                 num_format=self.FORMAT_FLOAT_NUMBER)
        stages_list = master_data_parser.get_stages_list()
        for stage in stages_list:
            # Write stage name to the first line
            self._next_line()
            line_data = [stage, ""]
            self.write_line(sheet=self._current_sheet, line=self._current_line,
                            value_array=line_data, cell_format=stage_format,
                            start_position=self._start_column)
            # Update information for columns width
            self._update_columns_width(line_data=line_data)
            self._next_line()
            for step in master_data_parser.get_steps_list_on_stage(stage_name=stage):
                # Write actual execution time of steps
                # Prepare data and suitable cell format to write data
                line_data = list()
                cells_format = list()
                # Step name
                step_label = self.PREFIX_MASTER + " " + step
                line_data.append(step_label)
                cells_format.append(text_format)
                # Execution time
                line_data.append(master_data_parser.get_step_execution_time_on_stage(
                    stage_name=stage, step_name=step))
                cells_format.append(number_format)
                # Write data for a step
                self.write_line_multi_format(sheet=self._current_sheet, line=self._current_line,
                                             values=line_data, formats=cells_format)
                # Update information for columns width
                self._update_columns_width(line_data=line_data)
                self._next_line()

            # Add actual total time data to the end of stage processes
            line_data = [self.HEADER_ACTUAL_TOTAL_TIME, master_data_parser.get_stage_total_time(
                stage_name=stage)]
            self.write_line(sheet=self._current_sheet, line=self._current_line,
                            value_array=line_data, cell_format=header_total_time_format,
                            start_position=self._start_column)
            # Update information for columns width
            self._update_columns_width(line_data=line_data)
            self._next_line()

    def _add_data_block_node_threads_on_master(self, master_data_parser):
        """
        This is block data will be placed into work sheet of execution time on master below data
        block of main stages/steps of the main thread. By this data block we can see different
        execution times on different nodes for each processes.

        Parameters
        ----------
        master_data_parser: ExecutionTimeDataParser
            Data parser for execution time data of processes on master (where nodes_manager.py is
            called)

        Returns
        -------
        None

        """
        # Write data line by line from current line and current column
        nodes_list = master_data_parser.get_threads_list()
        # Write header line
        header_format = self.get_cell_format(set_border=True, set_bold=True, align=Align.CENTER,
                                             bg_color=Color.CUSTOM_GREY)
        line_data = list()
        line_data.append(self.HEADER_PROCESSES)
        line_data += nodes_list
        self.write_line(sheet=self._current_sheet, line=self._current_line,
                        cell_format=header_format, value_array=line_data,
                        start_position=self._start_column)
        # Update information for columns width
        self._update_columns_width(line_data=line_data)
        self._next_line()

        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        execution_time_format = self.get_cell_format(set_border=True, align=Align.RIGHT,
                                                     num_format=self.FORMAT_FLOAT_NUMBER)

        # Add safeguard if nodes list is empty
        if not nodes_list:
            return

        # Collect list name of processes on node thread
        steps_list = master_data_parser.get_steps_list_on_thread(thread_name=nodes_list[0])
        for step in steps_list:
            # Prepare data to write to line
            line_data = list()
            line_formats = list()
            # Name of step with prefix
            step_label = self.PREFIX_NODE + " " + step
            line_data.append(step_label)
            line_formats.append(text_format)
            # Collect execution data of step on node threads
            for node_name in nodes_list:
                line_data.append(master_data_parser.get_step_execution_time_on_thread(
                    thread_name=node_name, step_name=step))
                line_formats.append(execution_time_format)
            # Write line data to the work sheet
            self.write_line_multi_format(sheet=self._current_sheet, line=self._current_line,
                                         values=line_data, formats=line_formats,
                                         start_position=self._start_column)
            # Update information for columns width
            self._update_columns_width(line_data=line_data)
            self._next_line()

        # Total time of processes on virtual machine thread
        total_execution_time_format = self.get_cell_format(set_border=True, set_bold=True,
                                                           num_format=self.FORMAT_FLOAT_NUMBER,
                                                           align=Align.RIGHT)
        line_data = list()
        line_data.append(self.HEADER_ACTUAL_TOTAL_TIME)
        for node_name in nodes_list:
            line_data.append(master_data_parser.get_total_execution_time_on_thread(
                thread_name=node_name))
        self.write_line(sheet=self._current_sheet, line=self._current_line,
                        value_array=line_data, cell_format=total_execution_time_format,
                        start_position=self._start_column)
        # Update information for columns width
        self._update_columns_width(line_data=line_data)
        self._next_line()

    def _add_data_block_main_processes_on_node(self, node_data_parser):
        """
        Add block data for management processes on the main thread of workers_manager.py which is
        called on remote node to control virtual machines to run BUILD/TEST.

        Parameters
        ----------
        node_data_parser: ExecutionTimeDataParser
            Data parser object for execution time which is generated by workers_manager.py on
            node. The json execution time data file is sent to the master in log folder of node
            results.

        Returns
        -------
        None

        """
        # Write data line by line from current line and current column
        # Write header line
        header_format = self.get_cell_format(set_border=True, set_bold=True, align=Align.CENTER,
                                             bg_color=Color.CUSTOM_GREY)
        line_data = [self.HEADER_PROCESSES, self.HEADER_EXECUTION_TIME]
        self.write_line(sheet=self._current_sheet, line=self._current_line,
                        cell_format=header_format, value_array=line_data,
                        start_position=self._start_column)
        # Update information for columns width
        self._update_columns_width(line_data=line_data)
        self._next_line()

        # Write execution time data
        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        execution_time_format = self.get_cell_format(set_border=True, align=Align.RIGHT,
                                                     num_format=self.FORMAT_FLOAT_NUMBER)
        header_total_time_format = \
            self.get_cell_format(set_border=True, set_bold=True, align=Align.RIGHT,
                                 num_format=self.FORMAT_FLOAT_NUMBER)
        steps_list = node_data_parser.get_steps_list()
        for step in steps_list:
            # Write actual execution time of steps
            # Prepare data and suitable cell format to write data
            line_data = list()
            cells_format = list()
            # Step name
            step_label = self.PREFIX_NODE + " " + step
            line_data.append(step_label)
            cells_format.append(text_format)
            # Execution time
            line_data.append(node_data_parser.get_step_execution_time(step_name=step))
            cells_format.append(execution_time_format)
            # Write data for a step
            self.write_line_multi_format(sheet=self._current_sheet, line=self._current_line,
                                         values=line_data, formats=cells_format)
            # Update information for columns width
            self._update_columns_width(line_data=line_data)
            self._next_line()

        # Add actual total time data to the end of stage processes
        line_data = [self.HEADER_ACTUAL_TOTAL_TIME, node_data_parser.total_time()]
        self.write_line(sheet=self._current_sheet, line=self._current_line,
                        value_array=line_data, cell_format=header_total_time_format,
                        start_position=self._start_column)
        # Update information for columns width
        self._update_columns_width(line_data=line_data)
        self._next_line()

    def _add_data_block_processes_on_virtual_machine_threads(self, node_data_parser):
        """
        Write execution time block for management processes on the main thread of
        workers_manager.py when it's called on remote node.

        Parameters
        ----------
        node_data_parser: ExecutionTimeDataParser
            Data parser object for execution time of management processes on main thread of
            workers_manager.py from remote node.

        Returns
        -------
        None

        """
        # Write data line by line from current line and current column
        vms_list = node_data_parser.get_threads_list()
        # Write header line
        header_format = self.get_cell_format(set_border=True, set_bold=True, align=Align.CENTER,
                                             bg_color=Color.CUSTOM_GREY)
        line_data = list()
        line_data.append(self.HEADER_PROCESSES)
        line_data += vms_list
        self.write_line(sheet=self._current_sheet, line=self._current_line,
                        cell_format=header_format, value_array=line_data,
                        start_position=self._start_column)
        # Update information for columns width
        self._update_columns_width(line_data=line_data)
        self._next_line()

        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        execution_time_format = self.get_cell_format(set_border=True, align=Align.RIGHT,
                                                     num_format=self.FORMAT_FLOAT_NUMBER)

        # Collect list name of processes on node thread
        steps_list = node_data_parser.get_steps_list_on_thread(thread_name=vms_list[0])
        for step in steps_list:
            # Prepare data to write to line
            line_data = list()
            line_formats = list()
            # Name of step with prefix
            step_label = self.PREFIX_VM + " " + step
            line_data.append(step_label)
            line_formats.append(text_format)
            # Collect execution data of step on node threads
            for vm_name in vms_list:
                line_data.append(node_data_parser.get_step_execution_time_on_thread(
                    thread_name=vm_name, step_name=step))
                line_formats.append(execution_time_format)
            # Write line data to the work sheet
            self.write_line_multi_format(sheet=self._current_sheet, line=self._current_line,
                                         values=line_data, formats=line_formats,
                                         start_position=self._start_column)
            # Update information for columns width
            self._update_columns_width(line_data=line_data)
            self._next_line()

        # Total time of processes on virtual machine thread
        total_execution_time_format = self.get_cell_format(set_border=True, set_bold=True,
                                                           num_format=self.FORMAT_FLOAT_NUMBER,
                                                           align=Align.RIGHT)
        line_data = list()
        line_data.append(self.HEADER_ACTUAL_TOTAL_TIME)
        for vm_name in vms_list:
            line_data.append(node_data_parser.get_total_execution_time_on_thread(
                thread_name=vm_name))
        self.write_line(sheet=self._current_sheet, line=self._current_line,
                        value_array=line_data, cell_format=total_execution_time_format,
                        start_position=self._start_column)
        # Update information for columns width
        self._update_columns_width(line_data=line_data)
        self._next_line()

    def _update_columns_width(self, line_data):
        """
        Whenever a line is added to the current sheet, max width of value in columns will be
        updated. This information will be used to update column width of the sheet.

        Parameters
        ----------
        line_data: list
            Data to write to a line of the work sheet

        Returns
        -------
        None

        """
        column_index = self._start_column
        for cell_data in line_data:
            if column_index < len(self._max_widths):
                if self.is_string(cell_data) and len(cell_data) > self._max_widths[column_index]:
                    # Update new width which is larger
                    self._max_widths[column_index] = len(cell_data)
            else:
                # Column is expand, then add this new to the setup
                self._max_widths.append(len(cell_data))
            column_index += 1

    def _setup_column_width(self):
        """
        Base on max width of columns information, we setup width of column in the current sheet
        for a better view of the sheet. Data will be presented clearly without hiding content.

        Returns
        -------
        None

        """
        counter = 0
        for width in self._max_widths:
            # Set width for the column
            self._current_sheet.set_column(counter, counter, width)
            counter += 1

    @staticmethod
    def is_string(input_str):
        """
        Check if input data is string/unicode or not

        Parameters
        ----------
        input_str: str/unicode/bytes

        Returns
        -------
        bool
            True if input is a string. Otherwise, return False.

        """
        if isinstance(input_str, str) or isinstance(input_str, unicode):
            return True
        return False
