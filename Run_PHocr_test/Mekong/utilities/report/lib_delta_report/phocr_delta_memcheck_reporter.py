import os
from abc import ABCMeta
from report.lib_base.xlsx_reporter import XlsxReporter
from report.lib_base.cell_format import Color, Align
from configs.test_result import TestResultJsonKeys, MemCheckInfo
from configs.compare_result import CompareJsonKeys
from baseapi.file_access import read_json
from handlers.test_result_handler import TestResultHandler
from configs.database import TestcaseConfig, SpecKeys
from handlers.test_spec_handler import TestSpecHandler
from configs.common import Platform


class DATConfiguration:
    # File output name
    FILE_NAME = "Memcheck_info{suffix}.xlsx"
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
    OTHER_ERROR_TEST_CASE = "OTHER ERROR TEST CASES"

    # Header of details sheet
    TEST_CASE_NAME = "Test case"
    LEAK_SUMMARY = "LEAK SUMMARY"
    ERROR_SUMMARY = "ERROR SUMMARY"
    COL_DEFINITELY_LOST = "Definitely lost"
    COL_INDIRECTLY_LOST = "Indirectly lost"
    COL_POSSIBLY_LOST = "Possibly lost"


class PHOcrDeltaMemoryLeakReporter(XlsxReporter):

    __metaclass__ = ABCMeta

    def __init__(self, test_folder, test_file, compare_file, error_folder=None, change_number=None,
                 delta_version=None, **kwargs):
        super(PHOcrDeltaMemoryLeakReporter, self).__init__(**kwargs)
        self.test_folder = test_folder
        self.test_file = test_file
        self.compare_file = compare_file
        self.error_folder = error_folder
        self.list_test = list()
        self.list_not_error_tests = list()
        self.list_error_tests = list()
        self.list_exit_code_not_equal_0 = list()
        self.list_not_output = list()
        self.change_number = change_number
        self.delta_version = delta_version
        self.test_results = read_json(self.test_file)
        self.compare_results = read_json(self.compare_file)
        self.test_result_handler = TestResultHandler(input_file=self.test_file,
                                                     test_folder=self.test_folder)

    def get_memory_info(self, test_id):
        if not CompareJsonKeys.INFO in self.compare_results[test_id]:
            return []
        detail_info = self.compare_results[test_id][CompareJsonKeys.INFO]
        output_info = {}
        for info in detail_info:
            if info[CompareJsonKeys.TITLE] == CompareJsonKeys.INFO_OUTPUT:
                output_info = info
        if not output_info:
            return []
        definitely_lost = output_info[MemCheckInfo.TAG_DEFINITELY]
        definitely_lost_bytes = definitely_lost[MemCheckInfo.LEAK_BYTE]
        definitely_lost_blocks = definitely_lost[MemCheckInfo.LEAK_BLOCK]

        indirectly_lost = output_info[MemCheckInfo.TAG_INDERECTLY]
        indirectly_lost_bytes = indirectly_lost[MemCheckInfo.LEAK_BYTE]
        indirectly_lost_blocks = indirectly_lost[MemCheckInfo.LEAK_BLOCK]

        possibly_lost = output_info[MemCheckInfo.TAG_POSSIBLY]
        possibly_lost_bytes = possibly_lost[MemCheckInfo.LEAK_BYTE]
        possibly_lost_blocks = possibly_lost[MemCheckInfo.LEAK_BLOCK]

        error_info = output_info[MemCheckInfo.ERROR_SUMMARY]
        error_contexts = error_info[MemCheckInfo.ERROR_CONTEXT]
        errors = error_info[MemCheckInfo.ERROR]

        return [definitely_lost_blocks, definitely_lost_bytes,
                indirectly_lost_blocks, indirectly_lost_bytes,
                possibly_lost_blocks, possibly_lost_bytes,
                error_contexts, errors]

    # Setup name of output file, headers base on change number and delta version
    def setup_names(self):
        # Set up name of output file in case it's name is not defined
        if not self.output_file_set:
            if self.change_number is None:
                file_suffix = ""
            else:
                file_suffix = "_C{change_number}_D{delta}".format(
                    change_number=self.change_number, delta=self.delta_version)
            self.output_file = DATConfiguration.FILE_NAME.format(suffix=file_suffix)

    def get_list_tests(self):
        for test_name in self.test_result_handler.get_list_tests():
            spec_file = os.path.join(self.test_folder, test_name, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            is_memcheck_test = spec_handler.get_tag(tag=SpecKeys.Tags.IS_MEMCHECK)
            if is_memcheck_test:
                self.list_test.append(test_name)

    def collect_data(self):
        self.setup_names()
        self.get_list_tests()
        # Get data for summary sheet
        for test_case in self.list_test:
            test_case_info = self.test_results[test_case]
            if test_case_info[TestResultJsonKeys.CODE] == 0:
                # Check if test result of test case return code is 0 but it doesn't have output file
                is_missing_output = False
                if self.error_folder:
                    if os.path.isdir(os.path.join(self.error_folder, test_case)):
                        is_missing_output = \
                            self.test_result_handler.is_output_missing(Platform.LINUX,
                                                                       test_case,
                                                                       self.error_folder,
                                                                       spec_folder=self.test_folder)
                else:
                    is_missing_output = \
                        self.test_result_handler.is_output_missing(Platform.LINUX,
                                                                   test_case,
                                                                   self.test_folder,
                                                                   spec_folder=self.test_folder)
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
        # Add summary sheet
        self.add_summary_sheet()

        # Add Detail sheet
        self.add_detail_sheet()

    def add_summary_sheet(self):
        self.logger.start_step("Make sheet : {0}".format(DATConfiguration.SHEET_SUMMARY))
        sheet = self.book.add_worksheet(name=DATConfiguration.SHEET_SUMMARY)

        # Cell format used
        header_format = self.get_cell_format(set_border=True, set_bold=True, align=Align.CENTER,
                                             bg_color=Color.LIGHT_GREEN)
        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True, align=Align.RIGHT, num_format='#,##0')

        start_column = 0
        # Product information
        line = 1
        line_data = [DATConfiguration.PRODUCT_TITLE, DATConfiguration.PRODUCT]
        line_formats = [header_format, text_format]
        self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                     formats=line_formats, start_position=start_column)

        # Overall information
        line += 2
        line_data = [DATConfiguration.OVERALL_INFO]
        self.write_line(sheet=sheet, line=line, value_array=line_data, cell_format=header_format,
                        start_position=start_column)
        line_formats = [text_format, number_format]
        line_data_list = list()
        # Number of complete tests
        line_data_list.append([DATConfiguration.NUM_COMPLETED, len(self.list_test)])
        # Number of error tests
        line_data_list.append([DATConfiguration.NUM_ERROR, len(self.list_error_tests)])
        # Number of changed tests
        line_data_list.append([DATConfiguration.NUM_NOT_ERROR, len(self.list_not_error_tests)])
        # Write overall information data
        for line_data in line_data_list:
            line += 1
            self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                         formats=line_formats, start_position=start_column)

        # Column width
        col = 0
        sheet.set_column(col, col, 25)
        col += 1
        sheet.set_column(col, col, 10)

        # Write error test case if have
        if self.list_exit_code_not_equal_0:
            line_start = 0
            self.write_error_test_case(self.list_exit_code_not_equal_0,
                                       [DATConfiguration.TEST_CASE_EXIT_CODE_NOT_EQUAL_0],
                                       sheet, header_format, text_format, line_start)
        if self.list_not_output:
            line_start = 2 + len(self.list_exit_code_not_equal_0)
            self.write_error_test_case(self.list_not_output,
                                       [DATConfiguration.TEST_CASE_NOT_OUTPUT],
                                       sheet, header_format, text_format, line_start)

        self.logger.end_step(True)

    def add_detail_sheet(self):
        self.logger.start_step("Make sheet : {0}".format(DATConfiguration.SHEET_DETAIL))
        sheet = self.book.add_worksheet(name=DATConfiguration.SHEET_DETAIL)

        # Cell format template
        header_format = self.get_cell_format(set_border=True, set_bold=True, align=Align.CENTER,
                                             bg_color=Color.LIGHT_GREEN)
        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True, align=Align.RIGHT, num_format='#,##0')

        sheet.merge_range('A1:A3', data=DATConfiguration.TEST_CASE_NAME,
                          cell_format=header_format)
        sheet.merge_range('B1:G1', data=DATConfiguration.LEAK_SUMMARY, cell_format=header_format)
        sheet.merge_range('H1:I2', data=DATConfiguration.ERROR_SUMMARY, cell_format=header_format)
        sheet.merge_range('B2:C2', data=DATConfiguration.COL_DEFINITELY_LOST,
                          cell_format=header_format)
        sheet.merge_range('D2:E2', data=DATConfiguration.COL_INDIRECTLY_LOST,
                          cell_format=header_format)
        sheet.merge_range('F2:G2', data=DATConfiguration.COL_POSSIBLY_LOST,
                          cell_format=header_format)

        # Write type on header
        line = 2
        start_column = 1
        line_data = [MemCheckInfo.LEAK_BLOCK, MemCheckInfo.LEAK_BYTE,
                     MemCheckInfo.LEAK_BLOCK, MemCheckInfo.LEAK_BYTE,
                     MemCheckInfo.LEAK_BLOCK, MemCheckInfo.LEAK_BYTE,
                     MemCheckInfo.ERROR_CONTEXT, MemCheckInfo.ERROR]
        line_formats = []
        for i in range(0, len(line_data)):
            line_formats.append(header_format)
        self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                     formats=line_formats, start_position=start_column)
        # Write each test case's data to file
        for test_name in self.list_not_error_tests:
            start_column = 0
            line += 1
            line_data = list()
            line_data.append(test_name)
            line_data += self.get_memory_info(test_name)
            if len(line_data)>1:
                line_formats = [text_format]
                for i in range(0, len(self.get_memory_info(test_name))):
                    line_formats.append(number_format)
                self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                             formats=line_formats, start_position=start_column)
        sheet.set_column(0, 0, 35)
        sheet.set_column(1, 8, 10)

        self.logger.end_step(True)

    def write_error_test_case(self, list_error, title, sheet, header_format, text_format, line_start):
        line_data = title
        start_column = 5
        self.write_line(sheet=sheet, line=line_start, value_array=line_data,
                        cell_format=header_format, start_position=start_column)

        for test_name in list_error:
            line_start += 1
            line_data = [test_name]
            self.write_line(sheet=sheet, line=line_start, value_array=line_data,
                            cell_format=text_format, start_position=start_column)

        sheet.set_column(start_column, start_column, 50)
