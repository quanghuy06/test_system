import os
from abc import ABCMeta
from report.lib_base.xlsx_reporter import XlsxReporter
from configs.test_result import TestResultJsonKeys
from baseapi.file_access import read_json
from handlers.test_result_handler import TestResultHandler
from report.lib_base.cell_format import Color, Align
from configs.test_result import MemPeakInfo
from configs.common import Platform


class MemPeakReportConfiguration:
    """
    Configuration for PHOcr Memory peak report.
    """
    FILE_NAME = "MemPeak_info{suffix}.xlsx"

    # Sheet name
    SHEET_SUMMARY = "Summary"
    SHEET_DETAIL = "Detail"

    # Header of summary sheet
    PRODUCT_TITLE = "Product"
    PRODUCT = "PHOcr"
    OVERALL_INFO = "Overall information"
    NUM_COMPLETED = "Number of completed tests"
    NUM_ERROR = "Number of error test cases"
    NUM_NOT_ERROR = "Number of not error test cases"
    TEST_CASE_EXIT_CODE_NOT_EQUAL_0 = "TEST CASES HAS EXIT CODE NOT EQUAL 0"
    TEST_CASE_NOT_OUTPUT = "TEST CASE DOESN'T HAVE OUTPUT"

    TEST_CASE_NAME = "Test case"


class PHOcrMemoryPeakReporter(XlsxReporter):
    """
    This class define all attributes and functions used for report memory peak
    information
    """

    __metaclass__ = ABCMeta

    def __init__(self,
                 test_folder,
                 test_file,
                 combine_file,
                 error_folder=None,
                 change_number=None,
                 delta_version=None,
                 **kwargs):
        super(PHOcrMemoryPeakReporter, self).__init__(**kwargs)
        self.test_folder = test_folder
        self.test_file = test_file
        self.combine_file = combine_file
        self.error_folder = error_folder
        self.change_number = change_number
        self.delta_version = delta_version
        self.list_not_output = list()
        self.list_error_tests = list()
        self.list_not_error_tests = list()
        self.list_exit_code_not_equal_0 = list()
        self.test_results = read_json(self.test_file)
        self.combine_result = read_json(self.combine_file)
        self.test_result_handler = \
            TestResultHandler(input_file=self.test_file,
                              test_folder=self.test_folder)
        self.list_test = self.test_result_handler.get_list_tests()

    def setup_names(self):
        """
        # Set up name of output file in case it's name is not defined

        """
        if not self.output_file_set:
            if self.change_number is None:
                file_suffix = ""
            else:
                file_suffix = "_C{change_number}_D{delta}".format(
                    change_number=self.change_number, delta=self.delta_version)
            self.output_file = MemPeakReportConfiguration.FILE_NAME.format(
                suffix=file_suffix)

    def get_mem_peak_info(self, test_name):
        """
        Get memory peak information of test case.

        Parameters
        ----------
        test_name: str
            Test case name

        Returns
        -------
        list
            Memory peak information.

        """
        test_id_info = self.combine_result[test_name]
        mem_heap_B = test_id_info[MemPeakInfo.MEM_HEAP_B]
        mem_heap_extra_B = test_id_info[MemPeakInfo.MEM_HEAP_EXTRA_B]
        return [mem_heap_B, mem_heap_extra_B]

    def collect_data(self):
        """
        Collect data for reporting.

        """
        self.setup_names()
        for test_case in self.list_test:
            test_case_info = self.test_results[test_case]
            if test_case_info[TestResultJsonKeys.CODE] == 0:
                # Check if test result of test case return code is 0 but it
                # doesn't have output file
                is_missing_output = False
                if self.error_folder:
                    if os.path.isdir(os.path.join(self.error_folder, test_case)):
                        is_missing_output = \
                            self.test_result_handler.is_output_missing(Platform.LINUX,
                                                                       test_case,
                                                                       self.error_folder,
                                                                       spec_folder=self.test_folder
                                                                       )
                else:
                    is_missing_output = \
                        self.test_result_handler.is_output_missing(Platform.LINUX,
                                                                   test_case,
                                                                   self.test_folder)
                if is_missing_output:
                    self.list_not_output.append(test_case)
                else:
                    self.list_not_error_tests.append(test_case)
            else:
                self.list_exit_code_not_equal_0.append(test_case)

        if self.list_not_output:
            self.list_error_tests += self.list_not_output
        if self.list_exit_code_not_equal_0:
            self.list_error_tests += self.list_exit_code_not_equal_0

    def add_sheets(self):
        """
        Add sheet to report file.

        """
        # Add summary sheet
        self.add_summary_sheet()

        # Add Detail sheet
        self.add_detail_sheet()

    def add_summary_sheet(self):
        """
        Add summary sheet.

        """
        self.logger.start_step(
            "Make sheet : {0}".format(MemPeakReportConfiguration.SHEET_SUMMARY))
        sheet = self.book.add_worksheet(
            name=MemPeakReportConfiguration.SHEET_SUMMARY)

        # Cell format used
        header_format = self.get_cell_format(set_border=True,
                                             set_bold=True,
                                             align=Align.CENTER,
                                             bg_color=Color.LIGHT_GREEN)
        text_format = self.get_cell_format(set_border=True,
                                           align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True,
                                             align=Align.RIGHT,
                                             num_format='#,##0')

        start_column = 0
        # Product information
        line = 1
        line_data = [MemPeakReportConfiguration.PRODUCT_TITLE,
                     MemPeakReportConfiguration.PRODUCT]
        line_formats = [header_format, text_format]
        self.write_line_multi_format(sheet=sheet,
                                     line=line,
                                     values=line_data,
                                     formats=line_formats,
                                     start_position=start_column)

        # Overall information
        line += 2
        line_data = [MemPeakReportConfiguration.OVERALL_INFO]
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=line_data,
                        cell_format=header_format,
                        start_position=start_column)
        line_formats = [text_format, number_format]
        line_data_list = list()
        # Number of complete tests
        line_data_list.append(
            [MemPeakReportConfiguration.NUM_COMPLETED, len(self.list_test)])
        # Number of error tests
        line_data_list.append(
            [MemPeakReportConfiguration.NUM_ERROR, len(self.list_error_tests)])
        # Number of changed tests
        line_data_list.append([MemPeakReportConfiguration.NUM_NOT_ERROR,
                               len(self.list_not_error_tests)])
        # Write overall information data
        for line_data in line_data_list:
            line += 1
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_formats,
                                         start_position=start_column)

        # Column width
        col = 0
        sheet.set_column(col, col, 25)
        col += 1
        sheet.set_column(col, col, 10)

        # Write error test case if have
        if self.list_exit_code_not_equal_0:
            line_start = 0
            self.write_error_test_case(self.list_exit_code_not_equal_0,
                                       [MemPeakReportConfiguration.TEST_CASE_EXIT_CODE_NOT_EQUAL_0],
                                       sheet, header_format,
                                       text_format,
                                       line_start)
        if self.list_not_output:
            line_start = 2 + len(self.list_exit_code_not_equal_0)
            self.write_error_test_case(self.list_not_output,
                                       [MemPeakReportConfiguration.TEST_CASE_NOT_OUTPUT],
                                       sheet,
                                       header_format,
                                       text_format,
                                       line_start)

        self.logger.end_step(True)

    def add_detail_sheet(self):
        """
        Add detail sheet.

        """
        self.logger.start_step(
            "Make sheet : {0}".format(MemPeakReportConfiguration.SHEET_DETAIL))
        sheet = self.book.add_worksheet(
            name=MemPeakReportConfiguration.SHEET_DETAIL)

        # Cell format template
        header_format = self.get_cell_format(set_border=True,
                                             set_bold=True,
                                             align=Align.CENTER,
                                             bg_color=Color.LIGHT_GREEN)
        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True,
                                             align=Align.RIGHT,
                                             num_format='#,##0')
        start_column = 0
        line = 0
        line_data = [MemPeakReportConfiguration.TEST_CASE_NAME,
                     MemPeakInfo.MEM_HEAP_B,
                     MemPeakInfo.MEM_HEAP_EXTRA_B]
        line_formats = [header_format,
                        header_format,
                        header_format]
        self.write_line_multi_format(sheet=sheet,
                                     line=line,
                                     values=line_data,
                                     formats=line_formats,
                                     start_position=start_column)
        # Write each test case's data to file
        for test_name in self.list_not_error_tests:
            start_column = 0
            line += 1
            line_data = list()
            line_data.append(test_name)
            line_data += self.get_mem_peak_info(test_name)
            if len(line_data) > 1:
                line_formats = [text_format]
                for i in range(0, len(self.get_mem_peak_info(test_name))):
                    line_formats.append(number_format)
                self.write_line_multi_format(sheet=sheet, line=line,
                                             values=line_data,
                                             formats=line_formats,
                                             start_position=start_column)
        sheet.set_column(0, 0, 35)
        sheet.set_column(1, 8, 15)

        self.logger.end_step(True)

    def write_error_test_case(self, list_error, title, sheet, header_format,
                              text_format, line_start):
        line_data = title
        start_column = 5
        self.write_line(sheet=sheet,
                        line=line_start,
                        value_array=line_data,
                        cell_format=header_format,
                        start_position=start_column)

        for test_name in list_error:
            line_start += 1
            line_data = [test_name]
            self.write_line(sheet=sheet,
                            line=line_start,
                            value_array=line_data,
                            cell_format=text_format,
                            start_position=start_column)

        sheet.set_column(start_column, start_column, 50)

