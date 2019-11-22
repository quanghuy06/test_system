# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/04/2017
# Last update:      12/09/2019
# Description:      Class for overall information testing report
import os
from abc import ABCMeta

from baseapi.common import get_accuracy_value, get_unique_list, convert_from_kb_to_mb, takeThird
from baseapi.file_access import write_line, remove_paths
from configs.database import TestcaseConfig, SpecKeys
from configs.projects.phocr import PhocrProject
from handlers.compare_handlers.compare_result_handler import CompareResultHandler
from handlers.compare_handlers.compare_bb_result_handler import CompareBbResultHandler
from handlers.compare_handlers.compare_text_result_handler import CompareTextResultHandler
from handlers.test_result_handler import TestResultHandler
from handlers.test_spec_handler import TestSpecHandler
from report.lib_base.reporter import Reporter
from report.lib_summary_report.defines import ErrorFlags
from database.lib_base.test_case_manager import TestCaseManager
from report.lib_summary_report.defines import Threshold
from configs.compare_result import CompareJsonKeys


class OIRConfiguration(object):
    # File name
    FILE_NAME_DEFAULT = "OverallInformation{suffix}.txt"

    # Summary bounding box accuracy information
    BB_ACC_TITLE = "**** Overall information of Bounding Box Accuracy ****"
    CHANGE_ERRORS_DEFAULT = "Your change"
    CHANGE_ACC_DEFAULT = "Your Accuracy"
    REFERENCE_ERRORS_DEFAULT = "Reference"
    REFERENCE_ACC_DEFAULT = "Reference Accuracy"
    TOTAL_CHARACTERS = "Total characters"
    TOTAL_ERRORS = "Total errors"
    TOTAL_REF_ERRORS = "Total errors of reference"
    VARIANCE = "Variance"
    LANGUAGE = "Language"

    # Summary text accuracy information
    TEXT_ACC_TITLE = "**** Overall information of Text Accuracy ****"

    # Summary information of testing
    TESTING_INFORMATION_TITLE = "**** Overall information of Testing ****"
    NUM_COMPLETED = "Number of completed tests"
    NUM_ERROR = "Number of error tests"
    NUM_CHANGED = "Number of changed tests"
    NUM_NOT_CHANGED = "Number of not changed tests"
    NUM_CHANGED_MEM_PEAK = "Number of changed memory peak tests"

    # Headers of more detail information
    LIST_ERROR = "****  LIST OF ERROR TESTS  ****"
    LIST_DOWN_PERFORMANCE = "****  LIST OF DOWN PERFORMANCE TESTS  ****"
    LIST_CHANGE = "****  LIST OF CHANGED TESTS  ****"
    LIST_NOT_CHANGE = "****  LIST OF NOT CHANGED TESTS  ****"
    LIST_CHANGE_MEMORY_PEAK = "**** LIST OF CHANGED MEMORY PEAK TESTS *****"

    # Changed type flag
    CHANGE_TYPE_FROM_ERR = "< NO MORE ERROR >"
    CHANGE_TYPE_NORMAL = "< CONTENT CHANGE >"
    CHANGE_STDOUT = "< STDOUT CHANGED >"
    CHANGE_STDERR = "< STDERR CHANGED >"
    BUG_NUMBER = "< BUG NUMBER: {bug_number} >"


# Note that you should always set up test result handler before setting up
# compare result handler
class OverallInformationReporter(Reporter):

    __metaclass__ = ABCMeta

    MIN_DOWN_PERFORMANCE_TIMES = 3

    # Initial
    def __init__(self, test_file, compare_file, test_folder, error_folder,
                 platform, change_number=None, delta_version=None, **kwargs):
        super(OverallInformationReporter, self).__init__(**kwargs)
        self.test_folder = test_folder
        self.error_folder = error_folder
        self.test_file = test_file
        self.compare_file = compare_file
        self.change_number = change_number
        self.delta_version = delta_version
        self.platform = platform
        self.test_result_handler = \
            TestResultHandler(input_file=self.test_file,
                              test_folder=self.test_folder)
        self.compare_result_handler = \
            CompareResultHandler(input_file=self.compare_file)
        self.compare_bb_result_handler = \
            CompareBbResultHandler(input_file=self.compare_file,
                                   test_folder=self.test_folder)
        self.compare_text_result_handler = \
            CompareTextResultHandler(input_file=self.compare_file,
                                     test_folder=self.test_folder)
        # Initial test case manage object to query database
        self.test_case_manager = TestCaseManager()

        # Information
        self.list_bb_acc_tests = list()
        self.list_bb_acc_languages = list()
        self.list_text_acc_tests = list()
        self.list_text_acc_languages = list()
        self.list_tests = list()
        self.list_error_tests = list()
        self.list_error_output = list()
        self.list_miss_output = list()
        self.list_changed_tests = list()
        self.list_not_changed_tests = list()
        self.list_changed_no_more_error = list()
        self.down_performance_tests = list()
        self.list_changed_mem_peak = list()

    # Setup name of output file, headers base on change number and delta version
    def setup_names(self):
        # Set up name of output file in case it's name is not defined
        if not self.output_file_set:
            if self.change_number is None:
                file_suffix = ""
            else:
                file_suffix = "_C{change_number}_D{delta}".format(
                    change_number=self.change_number, delta=self.delta_version)
            self.output_file = OIRConfiguration.FILE_NAME_DEFAULT.format(
                suffix=file_suffix)

    def do_work(self):
        # Collect data
        self.collect_data()

        # Check and remove old file
        if os.path.isfile(self.output_file):
            remove_paths(self.output_file)

        # Write data
        self.write_data()

    def collect_data(self):
        # Setup name of output file
        self.setup_names()

        # Get list tests
        self.list_tests = self.test_result_handler.get_list_tests()

        # Get list of error tests
        self.collect_testing_information()

    def collect_accuracy_data(self, function_name):
        if function_name == PhocrProject.functionalities.TEXT_LAYOUT:
            compare_handler = self.compare_bb_result_handler
        elif function_name == PhocrProject.functionalities.EXPORT_TXT:
            compare_handler = self.compare_text_result_handler
        else:
            return
        data = {}
        for test_name in compare_handler.get_list_tests():
            spec_file = os.path.join(self.test_folder,
                                     test_name,
                                     TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            if function_name in spec_handler.get_functions():
                languages = spec_handler.get_tag(tag=SpecKeys.Tags.LANGS)
                for language in languages:
                    if language not in data:
                        data[language] = {
                            OIRConfiguration.TOTAL_ERRORS: 0,
                            OIRConfiguration.TOTAL_REF_ERRORS: 0,
                            OIRConfiguration.TOTAL_CHARACTERS: 0
                        }
                    total_errors = compare_handler.get_total_errors(
                        test_name=test_name)
                    data[language][OIRConfiguration.TOTAL_ERRORS] += total_errors
                    total_ref_errors = compare_handler.get_total_ref_errors(
                        test_name=test_name)
                    data[language][OIRConfiguration.TOTAL_REF_ERRORS] += total_ref_errors
                    total_characters = compare_handler.get_total_characters(
                        test_name=test_name)
                    data[language][OIRConfiguration.TOTAL_CHARACTERS] += total_characters
        return data

    def collect_testing_information(self):
        data = dict()
        # Number of completed tests
        data[OIRConfiguration.NUM_COMPLETED] = len(self.test_result_handler.get_list_tests())

        # Number of errors test case (which exit code not equal 0)
        self.list_error_tests = self.test_result_handler.get_list_error_tests()
        # Number of failed test case (use for memcheck test case : exit code is 0 but number of
        # context is greater than 0)
        for test_name in self.compare_result_handler.get_list_failed_tests():
            if test_name not in self.list_error_tests:
                self.list_error_tests.append(test_name)

        # Get list extra error test case ex: error output (output's size is 0B), missing output
        if self.error_folder:
            self.list_error_output = \
                self.test_result_handler.get_list_output_0B(self.error_folder,
                                                            platform=self.platform,
                                                            spec_folder=self.test_folder)
            self.list_miss_output = \
                self.test_result_handler.get_list_test_cases_missing_output(
                    self.error_folder, platform=self.platform, spec_folder=self.test_folder)
        else:
            self.list_error_output = \
                self.test_result_handler.get_list_output_0B(None, self.platform)
            self.list_miss_output = \
                self.test_result_handler.get_list_test_cases_missing_output(None, self.platform)
        if self.list_error_output:
            self.list_error_tests += self.list_error_output
        if self.list_miss_output:
            self.list_error_tests += self.list_miss_output
        self.list_error_tests = sorted(get_unique_list(self.list_error_tests))

        # Get change extra list: Which change from error to not error
        for test_name in self.list_tests:
            if test_name not in self.list_error_tests:
                spec_file = os.path.join(self.test_folder,
                                         test_name,
                                         TestcaseConfig.SPEC_FILE)
                spec_handler = TestSpecHandler(input_file=spec_file)
                reference_is_error = \
                    spec_handler.get_error_flag(platform=self.platform)
                if reference_is_error:
                    self.list_changed_no_more_error.append(test_name)

        # Number of changed tests (ignore test case change to error and it's stdout is changed ):
        #   Get list test case which are changed by compare test result
        #   Test case is changed and have test result (in test_result.json) but output is missing
        #   or 0B, moved to list error test case and remove from list change test case.
        for test_name in self.compare_result_handler.get_list_changed_tests():
            if test_name not in self.list_error_tests:
                self.list_changed_tests.append(test_name)
        for test_name in self.list_changed_no_more_error:
            if test_name not in self.list_changed_tests:
                self.list_changed_tests.append(test_name)
        self.list_changed_tests = sorted(get_unique_list(self.list_changed_tests))

        # Number of not changed tests
        for test_name in self.compare_result_handler.get_list_not_changed_tests():
            if test_name not in self.list_changed_no_more_error \
                    and test_name not in self.list_error_tests:
                self.list_not_changed_tests.append(test_name)
        self.list_not_changed_tests = sorted(self.list_not_changed_tests)

        self.list_test_cases_really_down_performance()
        self.get_list_change_mem_peak()

    def list_test_cases_really_down_performance(self):
        for test_name in self.list_tests:
            current_time = self.test_result_handler.get_time(test_name)
            spec_file = os.path.join(self.test_folder, test_name, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            previous_time = spec_handler.get_weight(platform=self.platform)
            if OverallInformationReporter.MIN_DOWN_PERFORMANCE_TIMES * previous_time < current_time:
                self.down_performance_tests.append([test_name, str(previous_time), str(current_time)])

    def get_list_change_mem_peak(self):
        """
        Get list test cases that change memory peak more than specific threshold

        Returns
        -------

        """
        for test_name in self.list_tests:
            mem_peak_info = self.test_result_handler.get_mem_peak_info(test_name)
            mem_peak_convert_to_mb = convert_from_kb_to_mb(int(mem_peak_info))
            spec_file = os.path.join(self.test_folder, test_name,
                                     TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            if self.delta_version:
                previous_mem_peak = spec_handler.get_mem_peak_info(
                    platform=self.platform,
                    delta=self.delta_version,
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
            memory_peak_change = mem_peak_convert_to_mb - previous_mem_peak_convert_to_mb
            if abs(memory_peak_change) > Threshold.CHANGE_MEMORY_PEAK_MB:
                memory_peak_unicode = u"{0}MB".format(mem_peak_convert_to_mb)
                self.list_changed_mem_peak.append(
                    [test_name, memory_peak_unicode, memory_peak_change])

    def write_data(self):
        # Write summary bounding box accuracy block
        self.write_accuracy_block(functional=PhocrProject.functionalities.TEXT_LAYOUT,
                                  title=OIRConfiguration.BB_ACC_TITLE)

        # Add space lines
        self.write_space_line(num_lines=2)

        # Write summary text accuracy block
        self.write_accuracy_block(functional=PhocrProject.functionalities.EXPORT_TXT,
                                  title=OIRConfiguration.TEXT_ACC_TITLE)

        # Add space lines
        self.write_space_line(num_lines=2)

        # Write information of testing
        self.write_testing_information()

        # Add space lines
        self.write_space_line(num_lines=2)

        # Write list of error test cases
        self.write_error_list()

        # Add space lines
        self.write_space_line(num_lines=2)

        # Write list test case that worse performance
        self.write_worse_performance_list()
        # Add space lines
        self.write_space_line(num_lines=2)

        # Write list of changed test cases
        self.write_changed_list()
        # Add space lines
        self.write_space_line(num_lines=2)

        # Write list high memory peak.
        self.write_changed_memory_peak_list()
        # Add space lines
        self.write_space_line(num_lines=2)

        # Write list of not changed test cases
        self.write_not_changed_list()

    def write_accuracy_block(self, functional, title):
        # Write inform
        self.write_line(title)
        # Write header line
        header1 = [OIRConfiguration.LANGUAGE,
                   OIRConfiguration.CHANGE_ERRORS_DEFAULT,
                   OIRConfiguration.REFERENCE_ERRORS_DEFAULT,
                   OIRConfiguration.VARIANCE,
                   OIRConfiguration.CHANGE_ACC_DEFAULT,
                   OIRConfiguration.REFERENCE_ACC_DEFAULT,
                   OIRConfiguration.TOTAL_CHARACTERS]
        self.write_line(self.get_accuracy_line_string(header1))
        header2 = ["", "", "", "", "    %", "    %", ""]
        self.write_line(self.get_accuracy_line_string(header2))
        self.write_line("-"*20*len(header1))
        # Get data
        data = self.collect_accuracy_data(function_name=functional)
        # Write data
        for language in sorted(data.keys()):
            line_data = list()
            line_data.append(language)
            change_error = data[language][OIRConfiguration.TOTAL_ERRORS]
            ref_error = data[language][OIRConfiguration.TOTAL_REF_ERRORS]
            total_characters = data[language][OIRConfiguration.TOTAL_CHARACTERS]
            line_data.append(str(change_error))
            line_data.append(str(ref_error))
            line_data.append(str(change_error - ref_error))
            change_acc = get_accuracy_value(errors=change_error,
                                            total_characters=total_characters)
            line_data.append(self.get_accuracy_string(change_acc))
            ref_acc = get_accuracy_value(errors=ref_error,
                                         total_characters=total_characters)
            line_data.append(self.get_accuracy_string(ref_acc))
            line_data.append(str(total_characters))
            self.write_line(self.get_accuracy_line_string(line_data=line_data))

    def write_testing_information(self):
        # Write inform line
        self.write_line(OIRConfiguration.TESTING_INFORMATION_TITLE)
        # Add space line
        self.write_line("-"*len(OIRConfiguration.TESTING_INFORMATION_TITLE))
        # Number of completed tests
        line_data = [OIRConfiguration.NUM_COMPLETED,
                     str(len(self.list_tests))]
        self.write_line(self.get_info_line_string(line_data=line_data))
        # Number of error tests
        line_data = [OIRConfiguration.NUM_ERROR,
                     str(len(self.list_error_tests))]
        self.write_line(self.get_info_line_string(line_data=line_data))
        # Number of changed tests
        line_data = [OIRConfiguration.NUM_CHANGED,
                     str(len(self.list_changed_tests))]
        self.write_line(self.get_info_line_string(line_data=line_data))
        # Number of not changed tests
        line_data = [OIRConfiguration.NUM_NOT_CHANGED,
                     str(len(self.list_not_changed_tests))]
        self.write_line(self.get_info_line_string(line_data=line_data))
        # Number of test cases that change memory peak more than 10MB.
        line_data = [OIRConfiguration.NUM_CHANGED_MEM_PEAK,
                     str(len(self.list_changed_mem_peak))]
        self.write_line(self.get_info_line_string(line_data=line_data))

    def write_error_list(self):
        # Write header line
        self.write_line(OIRConfiguration.LIST_ERROR)
        self.write_line("-"*len(OIRConfiguration.LIST_ERROR))
        # Write data list
        for test_name in self.list_error_tests:
            line_data = [test_name, self.get_error_flag(test_name=test_name)]
            flag_bug_number = self.get_bug_number_flag(test_name)
            if flag_bug_number is not None:
                line_data.append(flag_bug_number)
            self.write_line(self.get_detail_line_string(line_data=line_data))

    def write_changed_memory_peak_list(self):
        """
        Write list test case that change memory peak more than threshold

        Returns
        -------

        """
        # Write header
        self.write_line(OIRConfiguration.LIST_CHANGE_MEMORY_PEAK)
        self.write_line("-" * len(OIRConfiguration.LIST_CHANGE_MEMORY_PEAK))

        self.list_changed_mem_peak.sort(key=takeThird, reverse=True)

        # Write data list
        for test_case in self.list_changed_mem_peak:
            mem_peak_change = takeThird(test_case)
            if mem_peak_change >= 0:
                memory_peak_change_unicode = u"+{0}MB".format(mem_peak_change)
            else:
                memory_peak_change_unicode = u"{0}MB".format(mem_peak_change)
            test_case[2] = memory_peak_change_unicode

            self.write_line(self.get_detail_line_string(test_case))

    def write_worse_performance_list(self):
        # Write header line
        self.write_line(OIRConfiguration.LIST_DOWN_PERFORMANCE)
        self.write_line("-" * len(OIRConfiguration.LIST_DOWN_PERFORMANCE))
        # Write data list
        for test_case in self.down_performance_tests:
            flag_bug_number = self.get_bug_number_flag(test_case[0])
            if flag_bug_number is not None:
                test_case.append(flag_bug_number)
            self.write_line(self.get_detail_line_string(line_data=test_case))

    def write_changed_list(self):
        # Write header line
        self.write_line(OIRConfiguration.LIST_CHANGE)
        self.write_line("-" * len(OIRConfiguration.LIST_CHANGE))
        # Write data list
        for test_name in self.list_changed_tests:
            line_data = [test_name]
            for item in self.get_changed_flag(test_name=test_name):
                line_data.append(item)
            self.write_line(self.get_detail_line_string(line_data=line_data))

    def write_not_changed_list(self):
        # Write header line
        self.write_line(OIRConfiguration.LIST_NOT_CHANGE)
        self.write_line("-" * len(OIRConfiguration.LIST_NOT_CHANGE))
        # Write data list
        for test_name in self.list_not_changed_tests:
            line_data = [test_name]
            flag_bug_number = self.get_bug_number_flag(test_name)
            if flag_bug_number is not None:
                line_data.append(flag_bug_number)
            self.write_line(self.get_detail_line_string(line_data=line_data))

    @staticmethod
    def get_accuracy_line_string(line_data):
        return ("%-20s" * len(line_data)) % tuple(line_data)

    @staticmethod
    def get_info_line_string(line_data):
        return ": ".join(line_data)

    @staticmethod
    def get_detail_line_string(line_data):
        return "\t".join(line_data)

    @staticmethod
    def get_accuracy_string(acc_value):
        acc_value = acc_value * 100
        return "%.3f" % acc_value

    def write_space_line(self, num_lines=1):
        for i in range(0, num_lines):
            write_line(message="", file_path=self.output_file)

    def write_line(self, line_string):
        write_line(message=line_string, file_path=self.output_file)

    def get_error_flag(self, test_name):
        if test_name in self.compare_result_handler.get_list_failed_tests():
            return ErrorFlags.F_EXTRA
        else:
            exit_code = self.test_result_handler.get_exit_code(test_name=test_name)
            if exit_code < 0:
                return ErrorFlags.F_CRASH
            elif exit_code > 0:
                return ErrorFlags.F_GENERAL
            else:
                if test_name in self.list_error_output:
                    return ErrorFlags.F_OUTPUT_OFFICE_0B
                elif test_name in self.list_miss_output:
                    return ErrorFlags.F_MISSING_OUTPUT
                else:
                    return ErrorFlags.F_GENERAL

    def get_bug_number_flag(self, test_name):
        spec_file = os.path.join(self.test_folder, test_name, TestcaseConfig.SPEC_FILE)
        spec_handler = TestSpecHandler(input_file=spec_file)
        list_bug_number = spec_handler.get_tag(SpecKeys.Tags.BUG_LIST)
        str_bug_number = ",".join(list_bug_number).strip()
        flag_bug_number = None
        if len(str_bug_number) > 0:
            flag_bug_number = OIRConfiguration.BUG_NUMBER.format(bug_number=str_bug_number)
        return flag_bug_number

    def get_changed_flag(self, test_name):
        list_flag = []
        list_stdout_changed = \
            self.compare_result_handler.get_list_std_changed_test(CompareJsonKeys.IS_STDOUT_CHANGED)
        list_stderr_changed = \
            self.compare_result_handler.get_list_std_changed_test(CompareJsonKeys.IS_STDERR_CHANGED)
        if test_name in list_stdout_changed:
            list_flag.append(OIRConfiguration.CHANGE_STDOUT)
        if test_name in list_stderr_changed:
            list_flag.append(OIRConfiguration.CHANGE_STDERR)
        if test_name not in self.list_changed_no_more_error \
                and test_name not in list_stdout_changed \
                and test_name not in list_stderr_changed:
            list_flag.append(OIRConfiguration.CHANGE_TYPE_NORMAL)
        if test_name in self.list_changed_no_more_error:
            list_flag.append(OIRConfiguration.CHANGE_TYPE_FROM_ERR)

        flag_bug_number = self.get_bug_number_flag(test_name)
        if flag_bug_number is not None:
            list_flag.append(flag_bug_number)
        return list_flag
