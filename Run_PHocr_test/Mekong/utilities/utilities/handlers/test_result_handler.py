# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created:     12/01/2017
# Last updated:     29/06/2017
# Update by:        Phung Dinh Tai
# Description:      This script define a class for handling json test result
import os
import fnmatch
from abc import ABCMeta
from configs.common import file_extension
from configs.database import TestcaseConfig
from configs.test_result import TestResultJsonKeys, TestResultConfig
from handlers.test_spec_handler import TestSpecHandler
from handlers.lib_base.json_handler import JsonHandler
from report.lib_summary_report.defines import ErrorFlags
from database.lib_base.test_case_manager import TestCaseManager
from configs.database import SpecKeys
from configs.projects.phocr import PhocrProject


class TestResultHandler(JsonHandler):

    __metaclass__ = ABCMeta

    def __init__(self, test_folder=None, **kwargs):
        super(TestResultHandler, self).__init__(**kwargs)
        self.test_folder = test_folder
        self.test_cases_manager = TestCaseManager()

    # Get run test time of a test case
    def get_time(self, test_name):
        if TestResultJsonKeys.TIME in self.data[test_name]:
            return self.data[test_name][TestResultJsonKeys.TIME]
        return None

    # Get list name of all test case
    def get_list_tests(self):
        return sorted(self.data.keys())

    # Check if test case is error or not
    def is_error(self, test_name):
        if (not self.data[test_name]) or (self.data[test_name][TestResultJsonKeys.CODE] != 0):
            return True
        else:
            return False

    # Get information
    # Get std output
    def get_std_out(self, test_name):
        if self.data[test_name] and TestResultJsonKeys.STDOUT in self.data[test_name]:
            return self.data[test_name][TestResultJsonKeys.STDOUT]

    # Get std error
    def get_std_err(self, test_name):
        if self.data[test_name]:
            if TestResultJsonKeys.STDERR in self.data[test_name]:
                return self.data[test_name][TestResultJsonKeys.STDERR]
            elif TestResultJsonKeys.SYSTEM_ERROR in self.data[test_name]:
                return self.data[test_name][TestResultJsonKeys.SYSTEM_ERROR]

    # Get list of error tests
    def get_list_error_tests(self):
        result = []
        for test_name in self.data.keys():
            if self.is_error(test_name):
                result.append(test_name)
        return result

    def is_output_0B(self, platform, test_name, output_folder, spec_folder=None):
        if test_name in self.get_list_error_tests():
            return False
        if not spec_folder:
            spec_file = os.path.join(output_folder, test_name, TestcaseConfig.SPEC_FILE)
        else:
            spec_file = os.path.join(spec_folder, test_name, TestcaseConfig.SPEC_FILE)
        spec_handler = TestSpecHandler(input_file=spec_file)
        output_folder = os.path.join(output_folder, test_name, TestcaseConfig.OUTPUT_FOLDER)
        platform_output_folder = os.path.join(output_folder, platform)
        if not os.path.isdir(platform_output_folder):
            return False

        if os.listdir(platform_output_folder):
            if spec_handler.is_output_formatting():
                for root, dirs, files in os.walk(platform_output_folder):
                    for f in files:
                        if self.is_office_output(f):
                            full_path = os.path.join(root, f)
                            file_size = os.path.getsize(full_path)
                            if file_size == 0:
                                return True

    # Check file is office output
    def is_office_output(self, file_name):
        if file_name.endswith(file_extension.DOCX) \
                or file_name.endswith(file_extension.EXCEL) \
                or file_name.endswith(file_extension.PPTX):
            return True

    def get_list_output_0B(self, error_folder, platform, spec_folder=None):
        results = []
        if error_folder:
            output_folder = error_folder
            list_test_name = os.listdir(output_folder)
        else:
            output_folder = self.test_folder
            list_test_name = self.data.keys()
        for test_name in list_test_name:
            if self.is_output_0B(platform=platform, test_name=test_name,
                                 output_folder=output_folder, spec_folder=spec_folder):
                results.append(test_name)
        return results

    # Get list of not error test cases. List contains changed and not changed tests
    def get_list_not_error_tests(self):
        result = []
        for test_name in self.data:
            if not self.is_error(test_name):
                result.append(test_name)
        return result

    # Get total test time of all test cases
    def get_test_time(self):
        total = 0
        for test_name in self.data:
            total += self.data[test_name][TestResultJsonKeys.TIME]
        return total

    def get_mem_peak_info(self, test_name):
        """
        Get memory peak information

        Parameters
        ----------
        test_name: str
             test case name

        Returns
        -------
        int : memory peak of test case

        """
        if not self.data[test_name]:
            return -1
        if TestResultJsonKeys.MEMORY not in self.data[test_name]:
            return -1
        memory_info = self.data[test_name][TestResultJsonKeys.MEMORY]
        if not memory_info:
            return -1
        else:
            return memory_info[0][TestResultJsonKeys.MemoryItem.MEMORY_PEAK]

    def get_mem_peak_command(self, test_name):
        """
        Get command which run to check memory peak of test case.

        Parameters
        ----------
        test_name: str
             test case name

        Returns
        -------
        str : Command which run to check memory peak of test case.

        """
        if not self.data[test_name]:
            return ""
        if TestResultJsonKeys.MEMORY not in self.data[test_name]:
            return ""
        memory_info = self.data[test_name][TestResultJsonKeys.MEMORY]
        if not memory_info:
            return ""
        else:
            return u'{command}'.format(command=memory_info[0][
                TestResultJsonKeys.MemoryItem.COMMAND])

    # Get exit/return code of a test case
    def get_exit_code(self, test_name):
        if not self.data[test_name]:
            return None
        return self.data[test_name][TestResultJsonKeys.CODE]

    # Get information of barcode functionality testing
    # Get list of barcode functionality accuracy tests
    def get_list_barcode_acc_tests(self, test_folder):
        result = list()
        for test_name in self.data:
            spec_file = os.path.join(test_folder, test_name, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            if ((spec_handler.get_component() == PhocrProject.components.BARCODE) and
                    (spec_handler.get_product() == PhocrProject.PRODUCT)):
                result.append(test_name)
        return result

    def is_output_not_exist(self, test_file, platform_output_folder):
        list_file_output = []
        for root, dirs, files in os.walk(platform_output_folder):
            for file_output in files:
                if fnmatch.fnmatch(file_output, test_file):
                    list_file_output.append(file_output)
        if list_file_output:
            return False
        else:
            return True

    # Check test case is missing output or not
    def is_output_missing(self, platform, test_name, test_folder, spec_folder=None):
        list_condition_check = [[PhocrProject.functionalities.EXPORT_DOCX,
                                 file_extension.DOCX],
                                [PhocrProject.functionalities.EXPORT_EXCEL,
                                 file_extension.EXCEL],
                                [PhocrProject.functionalities.EXPORT_PPTX,
                                 file_extension.PPTX],
                                [PhocrProject.functionalities.EXPORT_PDF,
                                 file_extension.PDF],
                                [PhocrProject.functionalities.EXPORT_PDFA,
                                 file_extension.PDFA],
                                [PhocrProject.functionalities.EXPORT_PDFA_BIN,
                                 file_extension.PDFA],
                                [PhocrProject.functionalities.EXPORT_PDFA_HALFTONE,
                                 file_extension.PDFA],
                                [PhocrProject.functionalities.EXPORT_PDFA_PHOTO_HALFTONE,
                                 file_extension.PDFA],
                                [PhocrProject.functionalities.NO_OCR_PDF,
                                 file_extension.PDF],
                                [PhocrProject.functionalities.OCR,
                                 file_extension.TXT],
                                [PhocrProject.functionalities.EXPORT_TXT,
                                 file_extension.TXT],
                                [PhocrProject.functionalities.TEXT_LAYOUT,
                                 file_extension.TEXT_LAYOUT],
                                [PhocrProject.functionalities.GET_TEXT_PAGE,
                                 file_extension.GET_TEXT_PAGE],
                                [PhocrProject.functionalities.GET_TEXT_DOCUMENT,
                                 file_extension.GET_TEXT_DOCUMENT]
                                ]
        if not spec_folder:
            des_spec_folder = test_folder
        else:
            des_spec_folder = spec_folder
        spec_file = os.path.join(des_spec_folder, test_name, TestcaseConfig.SPEC_FILE)
        spec_handler = TestSpecHandler(input_file=spec_file)
        output_folder = os.path.join(test_folder, test_name, TestcaseConfig.OUTPUT_FOLDER)
        platform_output_folder = os.path.join(output_folder, platform)
        if not os.path.isdir(platform_output_folder):
            return True

        # Get test case's component
        component = spec_handler.get_component()
        if component == PhocrProject.components.DEFAULT:
            if spec_handler.get_tag(SpecKeys.Tags.IS_MEMCHECK):
                if not os.path.exists(os.path.join(platform_output_folder,
                                                   TestResultConfig.MEM_CHECK_LOG)):
                    return True
            if spec_handler.get_tag(SpecKeys.Tags.IS_MEMCHECK_PEAK):
                list_result = list()
                for _file in os.listdir(platform_output_folder):
                    import re
                    flags = re.M
                    re_compile = re.compile("massif", flags)
                    search_result = re_compile.search(_file)
                    if search_result:
                        list_result.append(_file)
                if len(list_result) == 0:
                    return True
            test_data_folder = os.path.join(test_folder, test_name, TestcaseConfig.TEST_DATA_DIR)
            if os.path.isdir(test_data_folder):
                if len(os.listdir(test_data_folder)) != 0:
                    list_test_file_name = os.listdir(test_data_folder)
                else:
                    return False
            else:
                list_test_file_name = \
                    self.test_cases_manager.get_list_test_data_name(test_name)
            first_test_file_name = str(list_test_file_name[0])
            # Check is missing output or not with PHOcr's test case
            list_functions = spec_handler.get_functions()
            for func in list_functions:
                for condition in list_condition_check:
                    if func == condition[0]:
                        if func == PhocrProject.functionalities.GET_TEXT_PAGE or \
                            func == PhocrProject.functionalities.GET_TEXT_DOCUMENT:
                            test_file = condition[1]
                        else:
                            test_file = first_test_file_name + condition[1]
                        is_miss_func_output = self.is_output_not_exist(test_file,
                                                                       platform_output_folder)
                        if is_miss_func_output:
                            return True
            return False

    def get_list_test_cases_missing_output(self, error_folder, platform, spec_folder=None):
        results = []
        if error_folder:
            test_folder = error_folder
            list_test_name = os.listdir(test_folder)
        else:
            test_folder = self.test_folder
            list_test_name = self.data.keys()
        for test_name in list_test_name:
            if self.is_output_missing(platform=platform, test_name=test_name,
                                      test_folder=test_folder, spec_folder=spec_folder):
                results.append(test_name)
        return results

    # Get list errors of barcode accuracy tests
    def get_list_barcode_acc_error_tests(self, test_folder):
        result = list()
        if not test_folder:
            test_folder = self.test_folder
        barcode_acc_list = self.get_list_barcode_acc_tests(test_folder)
        for test_name in barcode_acc_list:
            if self.is_error(test_name):
                result.append(test_name)
        return result

    def get_test_flag(self, test_name):
        exit_code = self.get_exit_code(test_name=test_name)
        if exit_code > 0:
            return ErrorFlags.F_GENERAL
        elif exit_code == 0:
            return None
        elif exit_code < 0:
            return ErrorFlags.F_CRASH
        else:
            return ErrorFlags.F_SYSTEM