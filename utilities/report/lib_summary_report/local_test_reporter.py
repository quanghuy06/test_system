# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/07/2018
# Updated by:       Phung Dinh Tai
# Description:
import os
from abc import ABCMeta, abstractmethod

from baseapi.common import format_string
from configs.database import TestcaseConfig, SpecKeys
from configs.projects.phocr import PhocrProject
from handlers.test_result_handler import TestResultHandler
from handlers.test_spec_handler import TestSpecHandler
from report.lib_base.cell_format import Color, Align
from report.lib_base.tags_informer import TagsInformer
from report.lib_base.xlsx_reporter import XlsxReporter


class LTARConfiguration(object):

    FILE_NAME_DEFAULT = "AccuracyReport{suffix}.xlsx"

    # Sheet names
    SHEET_SUMMARY = "Summary accuracy"
    SHEET_BY_DOCUMENTS = "Accuracy by document types"
    SHEET_BY_LANGUAGES = "Accuracy by languages"
    SHEET_BY_TEST_CASE = "Accuracy by test cases"
    SHEET_RAW = "Raw data"

    # Headers of raw data
    TEST_NAME = "Test case"
    CHANGE = "C{change_number}"
    CHANGE_DEFAULT = "Your change"
    REFERENCE = "D{delta}"
    REFERENCE_DEFAULT = "Reference"
    VARIANCE = "Variance"
    TOTAL_CHARACTERS = "Total characters"

    # Headers of summary sheet
    PRODUCT = "Testing product"
    OVERALL_INFO = "Overall information"
    NUM_COMPLETED = "Number of completed tests"
    NUM_ERROR = "Number of error test cases"
    NUM_CHANGED = "Number of changed test cases"
    NUM_NOT_CHANGED = "Number of not changed test cases"
    OVERALL_ACC = "Overall accuracy"
    CHAR_ACC = "Character accuracy"
    DETAIL = "Detail number of errors"
    TOTAL_ERROR = "Total errors"
    TOTAL_TIME = "Total time"

    # By test cases headers
    ERROR = "TEST CASES ERROR"
    CHANGED = "TEST CASES CHANGED"
    NOT_CHANGED = "TEST CASES NOT CHANGED"
    ERROR_TYPE = "Type of error"
    CURRENT_ACCURACY = "Current accuracy"


class LocalTestReporter(XlsxReporter):

    __metaclass__ = ABCMeta

    def __init__(self, test_file, compare_file, test_folder, change_number=None, delta=None,
                 **kwargs):
        self.change_number = change_number
        if self.change_number:
            LTARConfiguration.CHANGE = LTARConfiguration.CHANGE.format(
                change_number=self.change_number)
        else:
            LTARConfiguration.CHANGE = LTARConfiguration.CHANGE_DEFAULT
        self.delta = delta
        if self.delta:
            LTARConfiguration.REFERENCE = LTARConfiguration.REFERENCE.format(delta=self.delta)
        else:
            LTARConfiguration.REFERENCE = LTARConfiguration.REFERENCE_DEFAULT
        self.test_folder = test_folder
        self.test_file = test_file
        self.compare_file = compare_file
        self.test_result_handler = TestResultHandler(input_file=self.test_file,
                                                     test_folder=self.test_folder)
        self.compare_result_handler = None
        self.set_compare_handler()
        super(LocalTestReporter, self).__init__(**kwargs)
        if not self.output_file_set:
            suffix = ""
            if self.change_number:
                suffix = "_C{change}_D{delta}".format(change=self.change_number, delta=self.delta)
            self.output_file = LTARConfiguration.FILE_NAME_DEFAULT.format(suffix=suffix)
        self.tag_headers = []
        self.ignore_tags = [SpecKeys.Tags.BUG_LIST,
                            SpecKeys.Tags.CMD_OPTION,
                            SpecKeys.Tags.DOC_NAME,
                            SpecKeys.Tags.DOC_PAGE,
                            SpecKeys.Tags.ACCURACY,
                            SpecKeys.Tags.IS_NON_INTEGRATION,
                            SpecKeys.Tags.IS_MEMCHECK_PEAK,
                            SpecKeys.Tags.IS_EXTREME_TEST]
        self.headers = []
        self.list_tests = []
        self.list_error_tests = []
        self.list_changed_tests = []
        self.list_not_changed_tests = []
        self.list_raw_tests = []  # List test names in raw data sheet:
        # contains changed and not changed test -> No error tests
        self.line_start_data = 0
        self.line_end_data = 0
        self.primary_conditions_string = ""
        # Get some range string for formula calculation
        self.change_errors_range = ""
        self.ref_errors_range = ""
        self.total_chars_range = ""
        # Total test time
        self.total_test_time = 0

    @abstractmethod
    def set_compare_handler(self):
        pass

    def collect_data(self):
        # Get raw headers
        list_tag = TagsInformer.get_tags_header()
        # Ignore unnecessary tag
        self.tag_headers = [item for item in list_tag if item not in self.ignore_tags]
        self.headers = [LTARConfiguration.TEST_NAME, LTARConfiguration.CHANGE,
                        LTARConfiguration.REFERENCE, LTARConfiguration.VARIANCE,
                        LTARConfiguration.TOTAL_CHARACTERS]
        self.headers += self.tag_headers

        # Get list test names
        self.get_list_tests()

        # Separate list tests to types of results
        self.separate_list_tests()

        # Create line and column mappings
        self.create_mappings()

        # Get some range strings
        self.change_errors_range = self.get_range_string(header=LTARConfiguration.CHANGE)
        self.ref_errors_range = self.get_range_string(header=LTARConfiguration.REFERENCE)
        self.total_chars_range = self.get_range_string(header=LTARConfiguration.TOTAL_CHARACTERS)

        # Get primary conditions for data collection
        self.get_primary_conditions_string()

    def add_sheets(self):
        # Summary information
        self.add_summary_sheet()

        # Accuracy by document types
        self.add_by_document_types_sheet()

        # Accuracy by languages
        self.add_by_languages_sheet()

        # Report error test cases
        self.add_by_test_cases_sheet()

        # Raw data sheet
        self.add_raw_data_sheet()

    def add_summary_sheet(self):
        sheet = self.book.add_worksheet(name=LTARConfiguration.SHEET_SUMMARY)
        # Cell format used
        header_format = self.get_cell_format(set_border=True, set_bold=True, align=Align.CENTER,
                                             bg_color=Color.CUSTOM_GREY)
        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True, align=Align.RIGHT, num_format='#,##0')
        accuracy_format = self.get_cell_format(set_border=True, align=Align.RIGHT,
                                               num_format='0.00%')


        # Write data line by line
        start_column = 0
        # Product information
        line = 1
        line_data = [LTARConfiguration.PRODUCT, PhocrProject.PRODUCT]
        line_formats = [header_format, text_format]
        self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                     formats=line_formats, start_position=start_column)
        # Overall information
        line += 2
        line_data = [LTARConfiguration.OVERALL_INFO]
        self.write_line(sheet=sheet, line=line, value_array=line_data, cell_format=header_format,
                        start_position=start_column)
        line_formats = [text_format, number_format]
        line_data_list = list()
        # Number of complete tests
        line_data_list.append([LTARConfiguration.NUM_COMPLETED, len(self.list_tests)])
        # Number of error tests
        line_data_list.append([LTARConfiguration.NUM_ERROR, len(self.list_error_tests)])
        # Number of changed tests
        line_data_list.append([LTARConfiguration.NUM_CHANGED, len(self.list_changed_tests)])
        # Number of not changed tests
        line_data_list.append([LTARConfiguration.NUM_NOT_CHANGED, len(self.list_not_changed_tests)])
        # Write overall information data
        for line_data in line_data_list:
            line += 1
            self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                         formats=line_formats, start_position=start_column)

        # Detail number of errors
        line += 2
        # Headers
        line_data = [LTARConfiguration.DETAIL, LTARConfiguration.CHANGE,
                     LTARConfiguration.REFERENCE, LTARConfiguration.TOTAL_CHARACTERS]
        self.write_line(sheet=sheet, line=line, value_array=line_data, cell_format=header_format,
                        start_position=start_column)
        # Data with formulas
        line += 1
        line_data = [""]
        change_errors_formula = self.get_sum_formula(
            range_string=self.change_errors_range, conditions_string=self.primary_conditions_string)
        change_errors_cell = self.get_cell_str(line_idx=line, col_idx=start_column + len(line_data))
        line_data.append(change_errors_formula)
        ref_errors_formula = self.get_sum_formula(range_string=self.ref_errors_range,
                                                  conditions_string=self.primary_conditions_string)
        ref_errors_cell = self.get_cell_str(line_idx=line, col_idx=start_column + len(line_data))
        line_data.append(ref_errors_formula)
        total_chars_formula = self.get_sum_formula(range_string=self.total_chars_range,
                                                   conditions_string=self.primary_conditions_string)
        total_chars_cell = self.get_cell_str(line_idx=line, col_idx=start_column + len(line_data))
        line_data.append(total_chars_formula)
        line_formats = [text_format, number_format, number_format, number_format]
        self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                     formats=line_formats, start_position=start_column)

        # Overall accuracy
        line += 2
        line_data = [LTARConfiguration.OVERALL_ACC, LTARConfiguration.CHANGE,
                     LTARConfiguration.REFERENCE, LTARConfiguration.VARIANCE]
        self.write_line(sheet=sheet, line=line, value_array=line_data, cell_format=header_format,
                        start_position=start_column)
        # Character accuracy
        line += 1
        # Label
        line_data = list()
        line_data.append(LTARConfiguration.CHAR_ACC)
        # Change accuracy
        line_data.append(self.get_accuracy_formula(errors_cell=change_errors_cell,
                                                   total_cell=total_chars_cell))
        change_acc_cell = self.get_cell_str(line_idx=line, col_idx=start_column+len(line_data)-1)
        # Reference accuracy
        line_data.append(self.get_accuracy_formula(errors_cell=ref_errors_cell,
                                                   total_cell=total_chars_cell))
        ref_acc_cell = self.get_cell_str(line_idx=line, col_idx=start_column+len(line_data)-1)
        # Variance
        line_data.append(self.get_variance_formula(first_cell=change_acc_cell,
                                                   second_cell=ref_acc_cell))
        line_formats = [text_format,
                        accuracy_format,
                        accuracy_format,
                        accuracy_format]
        self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                     formats=line_formats, start_position=start_column)

        # Set condition format for varient cell
        varient_cell_address = self.get_cell_str(line, 3)
        self.add_format_for_variant_cell(sheet,
                                         varient_cell_address,
                                         is_increase_is_positive=True,
                                         in_percent=True)

        # Total test time
        line += 2
        line_data = [LTARConfiguration.TOTAL_TIME, self.total_test_time]
        line_formats = [header_format, number_format]
        self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                     formats=line_formats, start_position=start_column)
        # Set columns width
        sheet.set_column(0, 0, 28)
        sheet.set_column(1, 3, 15)

    def add_by_document_types_sheet(self):
        sheet = self.book.add_worksheet(name=LTARConfiguration.SHEET_BY_DOCUMENTS)
        # Get list of document types
        doc_type_list = list()
        for test_name in self.list_raw_tests:
            spec_file = os.path.join(self.test_folder, test_name, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            doc_type = spec_handler.get_tag(tag=SpecKeys.Tags.DOC_TYPE)
            if doc_type and (doc_type not in doc_type_list):
                doc_type_list.append(doc_type)
        doc_type_list = sorted(doc_type_list)
        self.write_block_accuracy(sheet=sheet, header=SpecKeys.Tags.DOC_TYPE,
                                  list_values=doc_type_list)
        # Set columns width
        sheet.set_column(0, 0, 35)
        sheet.set_column(1, 4, 20)

    def add_by_languages_sheet(self):
        sheet = self.book.add_worksheet(name=LTARConfiguration.SHEET_BY_LANGUAGES)
        # Get list of languages
        languages = list()
        for test_name in self.list_raw_tests:
            spec_file = os.path.join(self.test_folder, test_name, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            languages_of_test = spec_handler.get_tag(tag=SpecKeys.Tags.LANGS)
            for language in languages_of_test:
                if language not in languages:
                    languages.append(language)
        languages = sorted(languages)
        self.write_block_accuracy(sheet=sheet, header=SpecKeys.Tags.LANGS, list_values=languages)
        # Set columns width
        sheet.set_column(0, 0, 35)
        sheet.set_column(1, 4, 20)

    def add_by_test_cases_sheet(self):
        sheet = self.book.add_worksheet(name=LTARConfiguration.SHEET_BY_TEST_CASE)
        # Cell formats used
        header_format = self.get_cell_format(set_border=True, set_bold=True, align=Align.CENTER,
                                             bg_color=Color.CUSTOM_GREY)
        text_format = self.get_cell_format(set_border=True, set_bold=True, align=Align.LEFT)
        text_center_format = self.get_cell_format(set_border=True, align=Align.CENTER)
        accuracy_format = self.get_cell_format(set_border=True, align=Align.RIGHT,
                                               num_format='0.00%')
        # Write list of error test cases
        line = 0
        start_column = 0
        line_data = [LTARConfiguration.ERROR, LTARConfiguration.ERROR_TYPE]
        self.write_line(sheet=sheet, line=line, value_array=line_data, cell_format=header_format,
                        start_position=start_column)
        line_format = [text_format, text_center_format]
        for test_name in self.list_error_tests:
            line += 1
            line_data = [test_name, self.test_result_handler.get_test_flag(test_name=test_name)]
            self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                         formats=line_format, start_position=start_column)

        sheet.set_column(0, 0, 35)
        sheet.set_column(1, 1, 15)

        # Write list of changed test cases and it's accuracy
        line = 0
        start_column += 3
        varient_cells = []
        line_data = [LTARConfiguration.CHANGED, LTARConfiguration.CHANGE,
                     LTARConfiguration.REFERENCE, LTARConfiguration.VARIANCE]
        self.write_line(sheet=sheet, line=line, value_array=line_data, cell_format=header_format,
                        start_position=start_column)
        line_format = [text_format, accuracy_format, accuracy_format, accuracy_format]
        for test_name in self.list_changed_tests:
            line += 1
            line_data = [test_name]
            change_errors_cell = self.get_cell_external(sheet_name=LTARConfiguration.SHEET_RAW,
                                                        test_name=test_name,
                                                        header=LTARConfiguration.CHANGE)
            ref_errors_cell = self.get_cell_external(sheet_name=LTARConfiguration.SHEET_RAW,
                                                     test_name=test_name,
                                                     header=LTARConfiguration.REFERENCE)
            total_chars_cell = self.get_cell_external(sheet_name=LTARConfiguration.SHEET_RAW,
                                                      test_name=test_name,
                                                      header=LTARConfiguration.TOTAL_CHARACTERS)
            change_acc_formula = self.get_accuracy_formula(errors_cell=change_errors_cell,
                                                           total_cell=total_chars_cell)
            change_acc_cell = self.get_cell_str(line_idx=line, col_idx=start_column+len(line_data))
            line_data.append(change_acc_formula)
            ref_acc_formula = self.get_accuracy_formula(errors_cell=ref_errors_cell,
                                                        total_cell=total_chars_cell)
            ref_acc_cell = self.get_cell_str(line_idx=line, col_idx=start_column+len(line_data))
            line_data.append(ref_acc_formula)
            variance_formula = self.get_variance_formula(first_cell=change_acc_cell,
                                                         second_cell=ref_acc_cell)
            line_data.append(variance_formula)
            self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                         formats=line_format, start_position=start_column)
            varient_cells.append(self.get_cell_str(line, start_column + 3))

        for cell in varient_cells:
            self.add_format_for_variant_cell(sheet, cell, True, True)

        sheet.set_column(start_column, start_column, 35)
        sheet.set_column(start_column + 1, start_column + 3, 15)

        # Write list of not changed test cases and it's accuracy
        line = 0
        start_column += 5
        line_data = [LTARConfiguration.NOT_CHANGED, LTARConfiguration.CURRENT_ACCURACY]
        self.write_line(sheet=sheet, line=line, value_array=line_data, cell_format=header_format,
                        start_position=start_column)
        line_format = [text_format, accuracy_format]
        for test_name in self.list_not_changed_tests:
            line += 1
            line_data = [test_name]
            change_errors_cell = self.get_cell_external(sheet_name=LTARConfiguration.SHEET_RAW,
                                                        test_name=test_name,
                                                        header=LTARConfiguration.CHANGE)
            total_chars_cell = self.get_cell_external(sheet_name=LTARConfiguration.SHEET_RAW,
                                                      test_name=test_name,
                                                      header=LTARConfiguration.TOTAL_CHARACTERS)
            current_acc_formula = self.get_accuracy_formula(errors_cell=change_errors_cell,
                                                            total_cell=total_chars_cell)
            line_data.append(current_acc_formula)
            self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                         formats=line_format, start_position=start_column)
        sheet.set_column(start_column, start_column, 35)
        sheet.set_column(start_column + 1, start_column + 3, 15)

    def add_raw_data_sheet(self):
        # Get cell formats
        header_format = self.get_cell_format(set_border=True, align=Align.CENTER, set_bold=True,
                                             bg_color=Color.CUSTOM_GREY)
        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True, align=Align.RIGHT, num_format='#,##0')
        tag_value_format = self.get_cell_format(set_border=True, align=Align.CENTER, wrap_text=True)
        sheet = self.book.add_worksheet(name=LTARConfiguration.SHEET_RAW)
        # Write header
        line = 0
        self.write_line(sheet=sheet, line=line, value_array=self.headers, cell_format=header_format)
        # Write data
        line_format = [text_format]
        for i in range(0, 3):
            line_format.append(number_format)
        line_format.append(number_format)
        for i in range(0, len(self.tag_headers)):
            line_format.append(tag_value_format)

        varient_cells = []
        for test_name in self.list_raw_tests:
            line += 1
            line_data = list()
            line_data.append(test_name)
            # Total errors of change
            line_data.append(self.compare_result_handler.get_total_errors(test_name=test_name))
            change_errors_cell = self.get_cell_str(line_idx=line, col_idx=len(line_data)-1)
            # Total errors of reference
            line_data.append(self.compare_result_handler.get_total_ref_errors(test_name=test_name))
            ref_errors_cell = self.get_cell_str(line_idx=line, col_idx=len(line_data)-1)
            # Variance
            variance_formula = self.get_variance_formula(first_cell=change_errors_cell,
                                                         second_cell=ref_errors_cell)
            line_data.append(variance_formula)
            # Total characters
            line_data.append(self.compare_result_handler.get_total_characters(test_name=test_name))
            # Tags value
            line_data += self.get_tags_value(test_name=test_name)
            # Write line data
            self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                         formats=line_format)
            varient_cells.append(self.get_cell_str(line, 3))

        for cell in varient_cells:
            self.add_format_for_variant_cell(sheet, cell, False, False)

        # Set columns width
        sheet.set_column(0, 0, 50)
        sheet.set_column(1, 6, 15)
        sheet.set_column(7, len(self.tag_headers), 20)

    def write_block_accuracy(self, sheet, header, list_values):
        # Cell formats used
        header_format = self.get_cell_format(set_border=True, set_bold=True, align=Align.CENTER,
                                             bg_color=Color.CUSTOM_GREY)
        text_format = self.get_cell_format(set_border=True, align=Align.CENTER)
        number_format = self.get_cell_format(set_border=True, align=Align.RIGHT, num_format='#,##0')
        accuracy_format = self.get_cell_format(set_border=True, align=Align.RIGHT,
                                               num_format='0.00%')
        # Detail errors block
        line = 0
        start_column = 0
        self.write_cell(sheet=sheet, line=line, column=start_column, cell_format=header_format,
                        value=LTARConfiguration.TOTAL_CHARACTERS)
        # Line headers
        line += 1
        line_data_headers = [header, LTARConfiguration.CHANGE, LTARConfiguration.REFERENCE,
                             LTARConfiguration.VARIANCE, LTARConfiguration.TOTAL_CHARACTERS]
        self.write_line(sheet=sheet, line=line, value_array=line_data_headers,
                        start_position=start_column, cell_format=header_format)
        # Write data
        line_format = [text_format, number_format, number_format, number_format, number_format]
        value_mapping = {}
        varient_cells = []
        for value in list_values:
            line += 1
            line_data = list()
            line_data.append(value)
            value_str = "\"{0}\"".format(value)
            conditions_string = self.get_condition_string(header=header, value=value_str)
            if self.primary_conditions_string:
                conditions_string += "," + self.primary_conditions_string
            # Change errors
            change_errors_formula = self.get_sum_formula(range_string=self.change_errors_range,
                                                         conditions_string=conditions_string)
            change_errors_cell = self.get_cell_str(line_idx=line, col_idx=start_column+len(
                line_data))
            line_data.append(change_errors_formula)
            # Reference errors
            ref_errors_formula = self.get_sum_formula(range_string=self.ref_errors_range,
                                                      conditions_string=conditions_string)
            ref_errors_cell = self.get_cell_str(line_idx=line, col_idx=start_column+len(line_data))
            line_data.append(ref_errors_formula)
            # Variance
            variance_formula = self.get_variance_formula(first_cell=change_errors_cell,
                                                         second_cell=ref_errors_cell)
            line_data.append(variance_formula)
            # Total characters
            total_chars_formula = self.get_sum_formula(range_string=self.total_chars_range,
                                                       conditions_string=conditions_string)
            total_chars_cell = self.get_cell_str(line_idx=line, col_idx=start_column+len(line_data))
            line_data.append(total_chars_formula)
            self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                         formats=line_format, start_position=start_column)
            value_mapping[value] = [change_errors_cell, ref_errors_cell, total_chars_cell]

            varient_cells.append(self.get_cell_str(line, 3))

        # Add conditional format for varient cells
        for cell in varient_cells:
            self.add_format_for_variant_cell(sheet,
                                             cell,
                                             is_increase_is_positive=False,
                                             in_percent=False)

        # Accuracy block
        varient_cells = []
        line += 2
        self.write_cell(sheet=sheet, line=line, column=start_column,
                        value=LTARConfiguration.CHAR_ACC, cell_format=header_format)
        # Header line
        line += 1
        line_data_headers = [header, LTARConfiguration.CHANGE, LTARConfiguration.REFERENCE,
                             LTARConfiguration.VARIANCE]
        self.write_line(sheet=sheet, line=line, value_array=line_data_headers,
                        cell_format=header_format, start_position=start_column)
        # Write accuracy data
        line_format = [text_format, accuracy_format, accuracy_format, accuracy_format]
        for value in list_values:
            line += 1
            line_data = list()
            line_data.append(value)
            change_acc_formula = self.get_accuracy_formula(errors_cell=value_mapping[value][0],
                                                           total_cell=value_mapping[value][2])
            change_acc_cell = self.get_cell_str(line_idx=line, col_idx=len(line_data))
            line_data.append(change_acc_formula)
            ref_acc_formula = self.get_accuracy_formula(errors_cell=value_mapping[value][1],
                                                        total_cell=value_mapping[value][2])
            ref_acc_cell = self.get_cell_str(line_idx=line, col_idx=len(line_data))
            line_data.append(ref_acc_formula)
            variance_acc_formula = self.get_variance_formula(first_cell=change_acc_cell,
                                                             second_cell=ref_acc_cell)
            line_data.append(variance_acc_formula)
            self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                         formats=line_format, start_position=start_column)
            varient_cells.append(self.get_cell_str(line, 3))

        # Add conditional format for varient cells
        for cell in varient_cells:
            self.add_format_for_variant_cell(sheet,
                                             cell,
                                             is_increase_is_positive=True,
                                             in_percent=True)

    def create_mappings(self):
        # Column mappings
        for i in range(0, len(self.headers)):
            self.column_mapping[self.headers[i]] = i
        # Line mappings
        self.line_start_data = 1
        line = 1
        for test_name in self.list_raw_tests:
            self.line_mapping[test_name] = line
            line += 1
        self.line_end_data = line

    @abstractmethod
    def get_list_tests(self):
        pass

    def separate_list_tests(self):
        for test_name in self.list_tests:
            if self.test_result_handler.is_error(test_name=test_name):
                self.list_error_tests.append(test_name)
            elif self.compare_result_handler.is_changed(test_name=test_name):
                self.list_changed_tests.append(test_name)
            else:
                self.list_not_changed_tests.append(test_name)

        self.list_raw_tests = self.list_changed_tests + self.list_not_changed_tests
        self.list_raw_tests = sorted(self.list_raw_tests)

    def get_primary_conditions_string(self):
        # Need to have phocr errors, esdk errors and total characters
        conditions = list()
        conditions.append(
            self.get_condition_string(header=LTARConfiguration.CHANGE, value="\"<>\""))
        conditions.append(
            self.get_condition_string(header=LTARConfiguration.REFERENCE, value="\"<>\""))
        self.primary_conditions_string = ",".join(conditions)

    def get_condition_string(self, header, value):
        column = self.column_mapping[header]
        return self.get_condition_formula(sheet=LTARConfiguration.SHEET_RAW, column=column,
                                          line_start=self.line_start_data,
                                          line_end=self.line_end_data, value=value)

    def get_range_string(self, header):
        column = self.column_mapping[header]
        return self.get_range_formula(sheet=LTARConfiguration.SHEET_RAW, column=column,
                                      line_start=self.line_start_data, line_end=self.line_end_data)

    def get_tags_value(self, test_name):
        tags_value = list()
        spec_file = os.path.join(self.test_folder, test_name, TestcaseConfig.SPEC_FILE)
        spec_handler = TestSpecHandler(input_file=spec_file)
        for tag_name in self.tag_headers:
            tag_value = spec_handler.get_tag(tag=tag_name)
            tags_value.append(format_string(value=tag_value))
        return tags_value

    # Get cell reference
    def get_cell_reference(self, sheet_name, test_name, header):
        line = self.line_mapping[test_name]
        column = self.column_mapping[header]
        cell_str = self.get_cell_str(line_idx=line, col_idx=column)
        return "=\'{sheet_name}\'!{cell_str}".format(sheet_name=sheet_name, cell_str=cell_str)

    def get_cell_external(self, sheet_name, test_name, header):
        return self.get_cell_reference(sheet_name=sheet_name, test_name=test_name,
                                       header=header).replace("=", "")
