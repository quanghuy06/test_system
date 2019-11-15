# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           TaiPD
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      13/07/2018
# Description:
import os
from abc import ABCMeta

from configs.database import TestcaseConfig, SpecKeys
from configs.projects.phocr import PhocrProject
from handlers.compare_handlers.lib_base.compare_accuracy_handler import \
    CompareAccuracyResultHandlerClass
from handlers.test_spec_handler import TestSpecHandler


# Title
COMPARE_TEXT_TITLE = "Compare text file"


class CompareTextResultHandler(CompareAccuracyResultHandlerClass):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(CompareTextResultHandler, self).__init__(**kwargs)

    def set_title(self):
        self.title = COMPARE_TEXT_TITLE

    def get_list_tests(self):
        list_tests = list()
        for test_name in self.data.keys():
            spec_file = os.path.join(self.test_folder, test_name, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            is_text_accuracy_test = PhocrProject.functionalities.EXPORT_TXT in \
                spec_handler.get_functions() and spec_handler.get_tag(tag=SpecKeys.Tags.ACCURACY)
            # Only report text accuracy for test case which don't check for
            # memory leak or memory peak
            is_check_memory = self.is_memory_checking(spec_handler)
            if is_text_accuracy_test and (not is_check_memory):
                list_tests.append(test_name)
        return list_tests
