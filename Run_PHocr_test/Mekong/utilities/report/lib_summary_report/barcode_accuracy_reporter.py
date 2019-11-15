# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      18/07/2018
# Updated by:       Phung Dinh Tai
# Description:
import os
from abc import ABCMeta
from report.lib_base.xlsx_reporter import XlsxReporter
from handlers.test_result_handler import TestResultHandler
from handlers.compare_handlers.compare_barcode_result_handler import CompareBarcodeHandler
from report.lib_base.cell_format import Align, Color
from report.lib_summary_report.defines import ErrorFlags


class BCARConfiguration(object):
    FILE_NAME_DEFAULT = "BarcodeAccuracyReport{suffix}.xlsx"
    TEST_NAME = "Test name"
    IMAGE = "Test image file"
    DIFF = "Compare with reference"
    CHANGE = "Compare with ground truth"
    ORIGINAL = "Reference vs ground truth"
    VARIANCE = "Variance of number error barcodes"
    TYPE = "Type of comparison"

    # Headers of raw data sheet
    NUM_CORRECT = "Number correct barcodes"
    NUM_ERROR = "Number error barcodes"
    TOTAL_BARS = "Total barcodes in ground truth"

    # Compare status
    S_FAIL = "Fail"
    S_PASS = "Pass"
    S_CHANGE = "Changed"
    S_NOT_CHANGE = "Not changed"

    # Error flag
    H_TYPE = "Error Type"
    F_CRASH = "CRASH"
    F_GENERAL = "GENERAL"

    # Heading by test status
    H_ERROR = "TEST CASES ERROR"
    H_CHANGE = "TEST CASES CHANGED"
    H_NOT_CHANGED = "TEST CASES NOT CHANGED"

    # Sheet name
    SHEET_SUMMARY = "Summary"
    SHEET_RAW = "Raw Data"


class BarcodeAccuracyReporter(XlsxReporter):

    __metaclass__ = ABCMeta

    def __init__(self, test_file, compare_file, test_folder, change_number=None,
                 delta_version=None, **kwargs):
        self.test_file = test_file
        self.compare_file = compare_file
        self.test_folder = test_folder
        self.change_number = change_number
        self.delta_version = delta_version
        super(BarcodeAccuracyReporter, self).__init__(**kwargs)
        self.test_result_handler = TestResultHandler(input_file=self.test_file,
                                                     test_folder=self.test_folder)
        self.compare_result_handler = CompareBarcodeHandler(input_file=self.compare_file,
                                                            test_folder=self.test_folder)

        # Set output file name
        if not self.output_file_set:
            suffix = ""
            if self.change_number:
                suffix = "_C{change}_D{delta}".format(change=self.change_number,
                                                      delta=self.delta_version)
            self.output_file = BCARConfiguration.FILE_NAME_DEFAULT.format(suffix=suffix)

        self.changed_list = []
        self.not_changed_list = []
        self.error_list = []
        self.not_error_list = []

    def collect_data(self):

        # Get error list
        self.error_list = self.compare_result_handler.get_list_error_compare()

        # Get changed list
        self.changed_list = self.compare_result_handler.get_list_changed_tests()

        # Get not changed list
        self.not_changed_list = self.compare_result_handler.get_list_not_changed_tests()

        # Get list of not error list
        self.not_error_list = self.test_result_handler.get_list_not_error_tests()

    def add_sheets(self):
        # Add summary sheet
        self.add_summary_sheet()

        # Add raw data sheet
        self.add_raw_data_sheet()

    def add_summary_sheet(self):
        sheet = self.book.add_worksheet(name=BCARConfiguration.SHEET_SUMMARY)
        # Get used cell format
        header_format = self.get_cell_format(align=Align.CENTER, set_border=True, set_bold=True,
                                             bg_color=Color.GREY)

        # Write header line
        headers = [BCARConfiguration.TEST_NAME, BCARConfiguration.IMAGE, BCARConfiguration.DIFF,
                   BCARConfiguration.ORIGINAL, BCARConfiguration.CHANGE,
                   BCARConfiguration.VARIANCE, BCARConfiguration.H_TYPE]
        line = 0
        self.write_line(sheet=sheet, value_array=headers, cell_format=header_format, line=line)

        # Write error tests
        line += 1
        line = self.write_error_tests_block(sheet=sheet, start_line=line)

        # Write changed tests
        line += 2
        line = self.write_accuracy_summary_block(sheet=sheet, label=BCARConfiguration.H_CHANGE,
                                                 tests_list=self.changed_list, start_line=line)
        # Write not changed tests
        line += 2
        self.write_accuracy_summary_block(sheet=sheet, label=BCARConfiguration.H_NOT_CHANGED,
                                          tests_list=self.not_changed_list, start_line=line)
        sheet.set_column(0, 6, 25)

    def add_raw_data_sheet(self):
        sheet = self.book.add_worksheet(name=BCARConfiguration.SHEET_RAW)
        # Get used cell format
        header_format = self.get_cell_format(align=Align.CENTER, set_border=True, set_bold=True,
                                             bg_color=Color.GREY)
        headers = [BCARConfiguration.TEST_NAME,
                   BCARConfiguration.IMAGE,
                   BCARConfiguration.NUM_CORRECT,
                   BCARConfiguration.NUM_ERROR,
                   BCARConfiguration.TOTAL_BARS]
        line = 0
        self.write_line(sheet=sheet, value_array=headers, cell_format=header_format, line=line)

        # Write error list
        line += 1
        line = self.write_error_tests_block(sheet=sheet, start_line=line)
        # Write changed list
        line += 2
        line = self.write_raw_info_block(sheet=sheet, tests_list=self.changed_list,
                                         label=BCARConfiguration.H_CHANGE, start_line=line)
        # Write not changed list
        line += 2
        self.write_raw_info_block(sheet=sheet, tests_list=self.not_changed_list,
                                  label=BCARConfiguration.H_NOT_CHANGED, start_line=line)
        sheet.set_column(0, 4, 25)

    def write_error_tests_block(self, sheet, start_line):
        line = start_line
        # Get cell formats
        header_format = self.get_cell_format(align=Align.CENTER, set_bold=True,
                                             set_border=True, bg_color=Color.BLUE)
        text_format = self.get_cell_format(align=Align.LEFT, set_border=True)
        # Header
        headers = [BCARConfiguration.H_ERROR, ""]
        self.write_line(line=line, sheet=sheet, value_array=headers, cell_format=header_format)
        for test_name in self.error_list:
            line += 1
            # Get line data
            line_data = list()
            # Test name
            line_data.append(test_name)
            # Error flag
            line_data.append(self.get_error_flag(test_name=test_name))
            # Write data
            self.write_line(sheet=sheet, line=line, value_array=line_data, cell_format=text_format)

        return line

    def get_error_flag(self, test_name):
        exit_code = self.test_result_handler.get_exit_code(test_name=test_name)
        if exit_code < 0:
            return ErrorFlags.F_CRASH
        elif exit_code == 0:
            return ErrorFlags.F_GOOD
        elif exit_code > 0:
            return ErrorFlags.F_GENERAL
        else:
            return ErrorFlags.F_SYSTEM

    def write_accuracy_summary_block(self, sheet, label, tests_list, start_line):
        # Get used cell formats
        text_format = self.get_cell_format(align=Align.LEFT, set_border=True)
        label_format = self.get_cell_format(align=Align.CENTER, set_border=True, set_bold=True,
                                            bg_color=Color.BLUE)
        text_center_format = self.get_cell_format(align=Align.CENTER, set_border=True)
        test_name_format = self.get_cell_format(align=Align.LEFT, set_border=True, set_bold=True,
                                                bg_color=Color.YELLOW, font_color=Color.RED)
        line = start_line
        # Write label
        line_data = [label]
        num_column = 7
        for i in range(0, num_column - len(line_data)):
            line_data.append("")
        self.write_line(sheet=sheet, line=line, value_array=line_data, cell_format=label_format)
        # Add data
        for test_name in tests_list:
            # Line test name
            line += 1
            line_data = [test_name]
            for i in range(0, num_column - len(line_data)):
                line_data.append("")
            self.write_line(sheet=sheet, line=line, value_array=line_data,
                            cell_format=test_name_format)
            # Detail information of images
            for image in self.compare_result_handler.get_list_images(test_name=test_name):
                line += 1
                line_data = list()
                line_format = list()
                # Image name
                line_data.append(image)
                line_format.append(text_format)
                # Compare change with reference status
                changed_status = self.get_changed_status(test_name=test_name, image=image)
                is_good = self.is_good_status(status=changed_status)
                line_data.append(changed_status)
                line_format.append(self.get_cell_status_format(is_good=is_good))
                # Compare reference with ground truth status
                ref_pass_status = self.get_ref_pass_status(test_name=test_name, image=image)
                is_good = self.is_good_status(status=ref_pass_status)
                line_data.append(ref_pass_status)
                line_format.append(self.get_cell_status_format(is_good=is_good))
                # Compare change with ground truth status
                pass_status = self.get_pass_status(test_name=test_name, image=image)
                is_good = self.is_good_status(status=pass_status)
                line_data.append(pass_status)
                line_format.append(self.get_cell_status_format(is_good=is_good))
                # Variance of error barcode
                variance = self.compare_result_handler.variance_change_vs_ref_bars(
                    test_name=test_name, image=image)
                line_data.append(variance)
                line_format.append(self.get_cell_variance_format(variance=variance))
                # Comparison type
                line_data.append(self.compare_result_handler.comparison_type(test_name=test_name))
                line_format.append(text_center_format)

                # Write data
                self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                             formats=line_format, start_position=1)

        return line

    def get_changed_status(self, test_name, image):
        if self.compare_result_handler.is_barcode_changed(test_name=test_name, image=image):
            return BCARConfiguration.S_CHANGE
        else:
            return BCARConfiguration.S_NOT_CHANGE

    def get_pass_status(self, test_name, image):
        if self.compare_result_handler.is_barcode_pass(test_name=test_name, image=image):
            return BCARConfiguration.S_PASS
        else:
            return BCARConfiguration.S_FAIL

    def get_ref_pass_status(self, test_name, image):
        if self.compare_result_handler.is_ref_barcode_pass(test_name=test_name, image=image):
            return BCARConfiguration.S_PASS
        else:
            return BCARConfiguration.S_FAIL

    def get_cell_status_format(self, is_good):
        if is_good:
            return self.get_cell_format(align=Align.CENTER, set_border=True, font_color=Color.GREEN,
                                        bg_color=Color.LIGHT_GREEN)
        else:
            return self.get_cell_format(align=Align.CENTER, set_border=True, set_bold=True,
                                        font_color=Color.RED, bg_color=Color.LIGHT_ORANGE)

    def get_cell_variance_format(self, variance):
        if variance < 0:
            return self.get_cell_format(align=Align.CENTER, set_border=True, set_bold=True,
                                        font_color=Color.RED, bg_color=Color.LIGHT_ORANGE,
                                        num_format='#,##0')
        elif variance > 0:
            return self.get_cell_format(align=Align.CENTER, set_border=True, font_color=Color.GREEN,
                                        bg_color=Color.LIGHT_GREEN,
                                        num_format='#,##0')
        else:
            return self.get_cell_format(align=Align.CENTER, set_border=True, num_format='#,##0')

    @staticmethod
    def is_good_status(status):
        if status == BCARConfiguration.S_PASS or status == BCARConfiguration.S_NOT_CHANGE:
            return True
        else:
            return False

    def write_raw_info_block(self, sheet, start_line, tests_list, label):
        # Get used cell formats
        text_format = self.get_cell_format(align=Align.LEFT, set_border=True)
        label_format = self.get_cell_format(align=Align.CENTER, set_border=True, set_bold=True,
                                            bg_color=Color.BLUE)
        number_format = self.get_cell_format(align=Align.CENTER, set_border=True,
                                             num_format='#,##0')
        test_name_format = self.get_cell_format(align=Align.LEFT, set_bold=True, set_border=True,
                                                bg_color=Color.YELLOW, font_color=Color.RED)
        line = start_line
        num_column = 5
        # Write label
        line_data = [label]
        for i in range(0, num_column - len(line_data)):
            line_data.append("")
        self.write_line(sheet=sheet, line=line, value_array=line_data, cell_format=label_format)
        # Add data
        line_format = [text_format, number_format, number_format, number_format]
        for test_name in tests_list:
            # Line test name
            line += 1
            line_data = [test_name]
            for i in range(0, num_column - len(line_data)):
                line_data.append("")
            self.write_line(sheet=sheet, line=line, value_array=line_data,
                            cell_format=test_name_format)
            # Detail information of images
            for image in self.compare_result_handler.get_list_images(test_name=test_name):
                line += 1
                line_data = list()
                # Image name
                line_data.append(image)
                # Number of correct barcode
                line_data.append(self.compare_result_handler.num_correct_bars(test_name=test_name,
                                                                              image=image))
                # Number of error barcode
                line_data.append(self.compare_result_handler.num_error_bars(test_name=test_name,
                                                                            image=image))
                # Total barcode
                line_data.append(self.compare_result_handler.total_bars(test_name=test_name,
                                                                        image=image))
                # Write data
                self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                                 formats=line_format, start_position=1)
        return line
