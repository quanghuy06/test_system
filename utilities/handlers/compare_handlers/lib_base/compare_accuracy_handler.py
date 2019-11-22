# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           TaiPD
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      13/07/2018
# Description:
from abc import ABCMeta
from handlers.compare_handlers.lib_base.compare_result_handler_class import \
    CompareResultHandlerClass, CRHDLConfiguration
from configs.projects.phocr import PhocrProject


class CAHDLConfiguration(object):
    # Information keys
    TOTAL_ERROR = "total_errors"
    TOTAL_CHARACTER = "total_characters"
    INSERT_ERR = "insert_errors"
    REPLACE_ERR = "replace_errors"
    DELETE_ERR = "delete_errors"
    SRC = "source"
    TARGET = "target"
    HTML_PATH = "html_path"


class CompareAccuracyResultHandlerClass(CompareResultHandlerClass):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(CompareAccuracyResultHandlerClass, self).__init__(**kwargs)

    def get_total_characters(self, test_name):
        if PhocrProject.components.BINARY_TEST in self.data[test_name]:
            return 0
        data = self.data[test_name][CRHDLConfiguration.ORIGIN][CRHDLConfiguration.DETAIL_INFO]
        return self.get_sum(data=data, info_key=CAHDLConfiguration.TOTAL_CHARACTER)

    def get_total_errors(self, test_name):
        # Ignore binary_test test cases
        if PhocrProject.components.BINARY_TEST in self.data[test_name]:
            return 0

        if self.is_changed(test_name=test_name):
            # Because test case is reported change when bounding box is changed or office output is
            # changed. If only office output change, compare_result.json will not report compare
            # result between change and reference or change with ground truth.
            if CRHDLConfiguration.CHANGE in self.data[test_name]:
                data = self.data[test_name][CRHDLConfiguration.CHANGE][CRHDLConfiguration.DETAIL_INFO]
            else:
                data = self.data[test_name][CRHDLConfiguration.ORIGIN][CRHDLConfiguration.DETAIL_INFO]
        else:
            data = self.data[test_name][CRHDLConfiguration.ORIGIN][CRHDLConfiguration.DETAIL_INFO]
        return self.get_sum(data=data, info_key=CAHDLConfiguration.TOTAL_ERROR)

    def get_total_ref_errors(self, test_name):
        # Ignore binary_test test cases
        if PhocrProject.components.BINARY_TEST in self.data[test_name]:
            return 0

        data = self.data[test_name][CRHDLConfiguration.ORIGIN][CRHDLConfiguration.DETAIL_INFO]
        return self.get_sum(data=data, info_key=CAHDLConfiguration.TOTAL_ERROR)

    def get_sum(self, data, info_key):
        total = 0
        for result in data:
            if result[CRHDLConfiguration.TITLE] == self.title:
                total += result[info_key]
        return total
