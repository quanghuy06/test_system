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
    CompareAccuracyResultHandlerClass, CAHDLConfiguration
from handlers.compare_handlers.lib_base.compare_result_handler_class import CRHDLConfiguration
from handlers.test_spec_handler import TestSpecHandler


# Title
COMPARE_BB_TITLE = "Compare bounding box"


class CompareBbResultHandler(CompareAccuracyResultHandlerClass):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(CompareBbResultHandler, self).__init__(**kwargs)

    def set_title(self):
        self.title = COMPARE_BB_TITLE

    def get_list_tests(self):
        list_tests = list()
        for test_name in self.data.keys():
            spec_file = os.path.join(self.test_folder, test_name, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            is_bb_accuracy_test = PhocrProject.functionalities.TEXT_LAYOUT in \
                spec_handler.get_functions() and spec_handler.get_tag(tag=SpecKeys.Tags.ACCURACY)
            is_check_memory = self.is_memory_checking(spec_handler)
            if is_bb_accuracy_test and (not is_check_memory):
                list_tests.append(test_name)
        return list_tests

    def get_delete_errors(self, test_name):
        if self.is_bb_changed(test_name=test_name):
            data = self.data[test_name][CRHDLConfiguration.CHANGE][CRHDLConfiguration.DETAIL_INFO]
        else:
            data = self.data[test_name][CRHDLConfiguration.ORIGIN][CRHDLConfiguration.DETAIL_INFO]
        return self.get_sum(data=data, info_key=CAHDLConfiguration.DELETE_ERR)

    def get_insert_errors(self, test_name):
        if self.is_bb_changed(test_name=test_name):
            data = self.data[test_name][CRHDLConfiguration.CHANGE][CRHDLConfiguration.DETAIL_INFO]
        else:
            data = self.data[test_name][CRHDLConfiguration.ORIGIN][CRHDLConfiguration.DETAIL_INFO]
        return self.get_sum(data=data, info_key=CAHDLConfiguration.INSERT_ERR)

    def get_replace_errors(self, test_name):
        if self.is_bb_changed(test_name=test_name):
            data = self.data[test_name][CRHDLConfiguration.CHANGE][CRHDLConfiguration.DETAIL_INFO]
        else:
            data = self.data[test_name][CRHDLConfiguration.ORIGIN][CRHDLConfiguration.DETAIL_INFO]
        return self.get_sum(data=data, info_key=CAHDLConfiguration.REPLACE_ERR)
