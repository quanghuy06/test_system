# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      09/07/2018
# Updated by:       Phung Dinh Tai
# Description:
import os
from abc import ABCMeta

from configs.database import TestcaseConfig, SpecKeys
from configs.projects.phocr import PhocrProject
from handlers.test_spec_handler import TestSpecHandler
from report.lib_errors_report.errors_reporter import ErrorsReporter, ETRConfiguration
from handlers.compare_handlers.compare_bb_result_handler import CompareBbResultHandler
from report.lib_base.history_data_informer import HistoryDataConfiguration

BB_ERROR_TYPES_REPORT_NAME_DEFAULT = "BoundingBoxErrorTypes{suffix}.tsv"


class BbErrorTypesReporter(ErrorsReporter):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(BbErrorTypesReporter, self).__init__(**kwargs)
        self.compare_result_handler = CompareBbResultHandler(input_file=self.compare_file,
                                                             test_folder=self.test_folder)
        if not self.output_file_set:
            suffix = ""
            if self.change_number:
                suffix = "_C{change}_D{delta}".format(change=self.change_number,
                                                      delta=self.delta_version)
            self.output_file = BB_ERROR_TYPES_REPORT_NAME_DEFAULT.format(suffix=suffix)

    def get_list_test_names(self):
        # Get list of test cases
        for test_name in self.test_result_handler.get_list_not_error_tests():
            spec_file = os.path.join(self.test_folder, test_name, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            is_bb_accuracy_test = PhocrProject.functionalities.TEXT_LAYOUT in \
                spec_handler.get_functions() and spec_handler.get_tag(tag=SpecKeys.Tags.ACCURACY)
            is_check_memory_leak = spec_handler.get_tag(SpecKeys.Tags.IS_MEMCHECK)
            if is_bb_accuracy_test and not is_check_memory_leak:
                self.list_test_names.append(test_name)
        self.list_test_names = sorted(self.list_test_names)

    def get_headers(self):
        self.headers = [ETRConfiguration.TEST_NAME,
                        HistoryDataConfiguration.BbAccuracy.INSERT_ERRORS,
                        HistoryDataConfiguration.BbAccuracy.REPLACE_ERRORS,
                        HistoryDataConfiguration.BbAccuracy.DELETE_ERRORS,
                        HistoryDataConfiguration.BbAccuracy.TOTAL_ERRORS,
                        HistoryDataConfiguration.BbAccuracy.TOTAL_CHARACTERS]

    def get_line_data(self, test_name):
        line_data = list()
        # Test name
        line_data.append(test_name)
        # Number of insert errors
        line_data.append(self.compare_result_handler.get_insert_errors(test_name=test_name))
        # Number of replace errors
        line_data.append(self.compare_result_handler.get_replace_errors(test_name=test_name))
        # Number of delete errors
        line_data.append(self.compare_result_handler.get_delete_errors(test_name=test_name))
        # Number of total errors
        line_data.append(self.compare_result_handler.get_total_errors(test_name=test_name))
        # Number of total characters
        line_data.append(self.compare_result_handler.get_total_characters(test_name=test_name))
        return line_data
