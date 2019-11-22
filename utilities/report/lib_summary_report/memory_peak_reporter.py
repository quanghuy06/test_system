# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      10/09/2019
import os

from abc import ABCMeta
from configs.database import TestcaseConfig, SpecKeys
from handlers.test_spec_handler import TestSpecHandler
from report.lib_base.xlsx_reporter import XlsxReporter
from handlers.test_result_handler import TestResultHandler
from report.lib_base.cell_format import Color, Align
from report.lib_summary_report.defines import Threshold
from baseapi.common import convert_from_kb_to_mb, takeThird

MEM_PEAK_REPORT_DEFAULT_NAME = "MemoryPeakReport{suffix}.xlsx"


class MemPeakConfig(object):
    # Sheet name:
    SHEET_SUMMARY = "Summary"
    SHEET_RAW_DATA = "Raw data"

    # Header of raw data
    TEST_NAME = "Test case"
    CHANGE = "C{change_number}"
    CHANGE_DEFAULT = "Your change"
    REFERENCE = "D{delta}"
    REFERENCE_DEFAULT = "Reference"
    VARIANCE = "Variance"

    # Header of sheet summary
    OVERALL_INFO = "Overall information"
    NUM_COMPLETE = "Number of complete test case"
    NUM_HIGH_MEMORY_PEAK_TEST_CASE = "Number of test cases have memory peak " \
                                     "> {0}M ".format(Threshold.MEMORY_PEAK_MB)
    NUM_CHANGE_MEMORY_PEAK = "Number of test case change > {0}MB".format(
                              Threshold.CHANGE_MEMORY_PEAK_MB)
    TEST_CASE_HIGH_MEMORY_PEAK = "TEST CASES HIGH MEMORY PEAK"
    TEST_CASE_CHANGE_MEMORY_PEAK = "TEST CASES CHANGED MEMORY PEAK"
    MEMORY_PEAK_CHANGED = "MEMORY PEAK CHANGED"
    MEMORY_PEAK = "MEMORY PEAK"


class MemPeakReporter(XlsxReporter):

    __metaclass__ = ABCMeta

    def __init__(self, test_file, test_folder, platform, change_number=None,
                 delta=None, **kwargs):
        super(MemPeakReporter, self).__init__(**kwargs)
        self.test_file = test_file
        self.test_folder = test_folder
        self.change_number = change_number
        self.platform = platform
        if self.change_number:
            MemPeakConfig.CHANGE = MemPeakConfig.CHANGE.format(
                change_number=self.change_number)
        else:
            MemPeakConfig.CHANGE = MemPeakConfig.CHANGE_DEFAULT

        self.delta = delta
        if self.delta:
            MemPeakConfig.REFERENCE = MemPeakConfig.REFERENCE.format(
                delta=self.delta)
        else:
            MemPeakConfig.REFERENCE = MemPeakConfig.REFERENCE_DEFAULT

        self.test_result_handler = TestResultHandler(
            input_file=self.test_file, test_folder=self.test_folder)
        self.compare_result_handler = None

        if not self.output_file_set:
            suffix = ""
            if self.change_number and self.delta:
                suffix = "_C{change}_D{delta}".format(change=self.change_number,
                                                      delta=self.delta)
            self.output_file = MEM_PEAK_REPORT_DEFAULT_NAME.format(
                suffix=suffix)

        self.headers = list()
        self.list_tests = list()
        self.list_raw_tests = list()
        self.line_start_data = 0
        self.line_end_data = 0
        self.list_change_mem_peak = list()
        self.list_high_mem_peak = list()

    def get_list_tests(self):
        """
        Get list successful test case.

        Returns
        -------

        """
        self.list_tests = sorted(self.test_result_handler.get_list_tests())

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

    def get_list_change_mem_peak(self):
        """
        Get list test case which change memory peak more than specific threshold

        Returns
        -------

        """
        for test_name in self.list_tests:
            mem_peak_info = self.test_result_handler.get_mem_peak_info(test_name)
            mem_peak_convert_to_mb = convert_from_kb_to_mb(int(mem_peak_info))
            if mem_peak_convert_to_mb > Threshold.MEMORY_PEAK_MB:
                self.list_high_mem_peak.append([test_name,
                                               mem_peak_convert_to_mb])
            spec_file = os.path.join(self.test_folder, test_name,
                                     TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            if self.delta:
                previous_mem_peak = spec_handler.get_mem_peak_info(
                    platform=self.platform,
                    delta=self.delta,
                    product=SpecKeys.History_data.PHOCR_TEST_MACHINE)
            else:
                delta = spec_handler.get_max_delta(platform=self.platform,
                                                   product=SpecKeys.History_data.PHOCR_TEST_MACHINE)
                if not delta:
                    previous_mem_peak = 0
                else:
                    previous_mem_peak = spec_handler.get_mem_peak_info(
                        platform=self.platform,
                        delta=delta,
                        product=SpecKeys.History_data.PHOCR_TEST_MACHINE)
            previous_mem_peak_convert_to_mb = convert_from_kb_to_mb(
                previous_mem_peak)
            memory_peak_changed = mem_peak_convert_to_mb - previous_mem_peak_convert_to_mb
            if abs(memory_peak_changed) > Threshold.CHANGE_MEMORY_PEAK_MB:
                self.list_change_mem_peak.append(
                    [test_name, mem_peak_convert_to_mb, memory_peak_changed])

    def collect_data(self):
        self.headers = [MemPeakConfig.TEST_NAME,
                        MemPeakConfig.CHANGE,
                        MemPeakConfig.REFERENCE,
                        MemPeakConfig.VARIANCE]
        self.get_list_tests()
        self.create_mappings()
        self.get_list_change_mem_peak()

    def add_sheets(self):
        # Summary information
        self.add_summary_sheet()
        # Raw data sheet
        self.add_raw_data_sheet()

    def add_summary_sheet(self):
        """
        Summary information.

        Returns
        -------

        """
        header_format = self.get_cell_format(set_border=True,
                                             set_bold=True,
                                             align=Align.CENTER,
                                             bg_color=Color.CUSTOM_GREEN)
        text_format = self.get_cell_format(set_border=True,
                                           align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True,
                                             align=Align.RIGHT,
                                             num_format='#,##0')
        sheet = self.book.add_worksheet(name=MemPeakConfig.SHEET_SUMMARY)
        start_column = 0
        line = 0
        line_data = [MemPeakConfig.OVERALL_INFO]
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=line_data,
                        cell_format=header_format,
                        start_position=start_column)
        line_data_list = list()
        line_formats = [text_format, number_format]
        # Number of complete test case.
        line_data_list.append([MemPeakConfig.NUM_COMPLETE, len(self.list_tests)])
        line_data_list.append([MemPeakConfig.NUM_HIGH_MEMORY_PEAK_TEST_CASE,
                               len(self.list_high_mem_peak)])
        line_data_list.append([MemPeakConfig.NUM_CHANGE_MEMORY_PEAK,
                               len(self.list_change_mem_peak)])
        for line_data in line_data_list:
            line += 1
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_formats,
                                         start_position=start_column)

        # Write list test case that have memory peak greater than 250M
        line = 0
        start_column = 3
        line_data = [MemPeakConfig.TEST_CASE_HIGH_MEMORY_PEAK,
                     MemPeakConfig.MEMORY_PEAK]
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=line_data,
                        cell_format=header_format,
                        start_position=start_column)
        for test_name in self.list_high_mem_peak:
            line_data = list()
            line += 1
            for info in test_name:
                line_data.append(info)
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_formats,
                                         start_position=start_column)

        # Write list test cases that increase memory peak 10MB with reference
        line = 0
        start_column = 6
        line_formats = [text_format, number_format, number_format]
        line_data = [MemPeakConfig.TEST_CASE_CHANGE_MEMORY_PEAK,
                     MemPeakConfig.MEMORY_PEAK,
                     MemPeakConfig.MEMORY_PEAK_CHANGED]
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=line_data,
                        cell_format=header_format,
                        start_position=start_column)
        self.list_change_mem_peak.sort(key=takeThird, reverse=True)
        variant_cells = list()
        for test_name in self.list_change_mem_peak:
            line_data = list()
            line += 1
            for info in test_name:
                line_data.append(info)
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_formats,
                                         start_position=start_column)
            variant_cells.append(self.get_cell_str(line, 8))
        for cell in variant_cells:
            self.add_format_for_variant_cell(worksheet=sheet,
                                             cell=cell,
                                             is_increase_is_positive=False,
                                             in_percent=False)

        # Set column width
        sheet.set_column(0, 0, 42)
        sheet.set_column(1, 1, 5)
        sheet.set_column(3, 3, 35)
        sheet.set_column(4, 4, 15)
        sheet.set_column(6, 6, 40)
        sheet.set_column(7, 7, 15)
        sheet.set_column(8, 8, 25)

    def add_raw_data_sheet(self):
        """
        Add raw data (memory peak information)

        Returns
        -------

        """
        header_format = self.get_cell_format(set_border=True,
                                             set_bold=True,
                                             align=Align.CENTER,
                                             bg_color=Color.CUSTOM_GREEN)
        text_format = self.get_cell_format(set_border=True,
                                           align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True,
                                             align=Align.RIGHT,
                                             num_format='#,##0')
        sheet = self.book.add_worksheet(name=MemPeakConfig.SHEET_RAW_DATA)
        line = 0
        # Write header
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=self.headers,
                        cell_format=header_format)
        # Write data
        line_format = [text_format]
        for i in range(0, 3):
            line_format.append(number_format)

        variant_cells = list()
        for test_name in self.list_tests:
            line_data = list()
            line += 1
            line_data.append(test_name)
            # Memory peak information of change.
            mem_peak_info = convert_from_kb_to_mb(int(
                self.test_result_handler.get_mem_peak_info(test_name=test_name)))
            line_data.append(mem_peak_info)
            change_mem_peak_cell = self.get_cell_str(line_idx=line,
                                                     col_idx=len(line_data)-1)
            self.add_format_for_negative_cell_by_value(worksheet=sheet,
                                                       cell=change_mem_peak_cell,
                                                       value=Threshold.MEMORY_PEAK_MB,
                                                       is_increase_is_negative=True,
                                                       in_percent=False)

            # Memory peak information of reference
            ref_mem_peak_cell = self.get_cell_str(line_idx=line,
                                                  col_idx=len(line_data))
            self.add_format_for_negative_cell_by_value(worksheet=sheet,
                                                       cell=ref_mem_peak_cell,
                                                       value=Threshold.MEMORY_PEAK_MB,
                                                       is_increase_is_negative=True,
                                                       in_percent=False)
            spec_file = os.path.join(self.test_folder, test_name,
                                     TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            ref_peak_info = convert_from_kb_to_mb(spec_handler.get_mem_peak_info(
                platform="linux",
                delta=self.delta,
                product=SpecKeys.History_data.PHOCR_TEST_MACHINE))
            line_data.append(ref_peak_info)

            # Variance
            variant_formula = self.get_variance_formula(
                first_cell=change_mem_peak_cell, second_cell=ref_mem_peak_cell)
            line_data.append(variant_formula)
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_format)
            variant_cells.append(self.get_cell_str(line, 3))
        for cell in variant_cells:
            self.add_format_for_variant_cell(worksheet=sheet,
                                             cell=cell,
                                             is_increase_is_positive=False,
                                             in_percent=False)

        # Set column width
        sheet.set_column(0, 0, 50)
        sheet.set_column(1, 6, 15)
