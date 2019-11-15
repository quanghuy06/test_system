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
from report.lib_summary_report.local_test_reporter import LocalTestReporter
from handlers.compare_handlers.compare_bb_result_handler import CompareBbResultHandler

BB_ACCURACY_REPORT_DEFAULT_NAME = "BoundingBoxAccuracyReport{suffix}.xlsx"


class BbAccuracyReporter(LocalTestReporter):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(BbAccuracyReporter, self).__init__(**kwargs)
        if not self.output_file_set:
            suffix = ""
            if self.change_number:
                suffix = "_C{change}_D{delta}".format(change=self.change_number, delta=self.delta)
            self.output_file = BB_ACCURACY_REPORT_DEFAULT_NAME.format(suffix=suffix)

    def set_compare_handler(self):
        self.compare_result_handler = CompareBbResultHandler(input_file=self.compare_file,
                                                             test_folder=self.test_folder)

    def get_list_tests(self):
        for test_name in self.test_result_handler.get_list_tests():
            spec_file = os.path.join(self.test_folder, test_name, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            is_text_accuracy_test = PhocrProject.functionalities.TEXT_LAYOUT in \
                spec_handler.get_functions() and spec_handler.get_tag(tag=SpecKeys.Tags.ACCURACY)
            is_check_memory_leak = spec_handler.get_tag(tag=SpecKeys.Tags.IS_MEMCHECK)
            if is_text_accuracy_test and (not is_check_memory_leak):
                self.list_tests.append(test_name)
