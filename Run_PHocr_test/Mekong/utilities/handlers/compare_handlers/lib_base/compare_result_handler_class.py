# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           TaiPD
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      13/07/2018
# Description:      This python script define a base class for json handlers
from abc import ABCMeta, abstractmethod
from handlers.lib_base.json_handler import JsonHandler
from configs.compare_result import CompareJsonKeys, CompareResultConfig
from configs.database import SpecKeys


class CRHDLConfiguration(object):
    # Conclusions
    IS_CHANGED = "is_changed"
    IS_FAILED = "is_failed"

    # Compare what
    CHANGE = "compare_change_vs_ground_truth"
    DIFF = "compare_change_vs_reference"
    ORIGIN = "compare_reference_vs_ground_truth"

    # Detail information
    DETAIL_INFO = "detail_information"

    # Title key
    TITLE = "title"


class CompareResultHandlerClass(JsonHandler):

    __metaclass__ = ABCMeta

    def __init__(self, test_folder=None, **kwargs):
        self.test_folder = test_folder
        self.title = None
        super(CompareResultHandlerClass, self).__init__(**kwargs)
        self.list_test_names = self.get_list_tests()
        self.set_title()
        self.list_error_compare = list()
        self.get_list_error_compare()

    @abstractmethod
    def set_title(self):
        pass

    @abstractmethod
    def get_list_tests(self):
        pass

    @staticmethod
    def is_memory_checking(spec_handler):
        if spec_handler.get_tag(tag=SpecKeys.Tags.IS_MEMCHECK) \
                or spec_handler.get_tag(tag=SpecKeys.Tags.IS_MEMCHECK_PEAK):
            return True
        else:
            return False

    def get_list_error_compare(self):
        for test_name in self.list_test_names:
            if not self.data[test_name]:
                self.list_error_compare.append(test_name)
        return self.list_error_compare

    def get_list_changed_tests(self):
        list_changed = list()
        for test_name in self.list_test_names:
            if self.data[test_name][CRHDLConfiguration.IS_CHANGED]:
                list_changed.append(test_name)
        return list_changed

    def get_list_not_changed_tests(self):
        list_not_changed = list()
        for test_name in self.list_test_names:
            if not self.data[test_name][CRHDLConfiguration.IS_CHANGED]:
                list_not_changed.append(test_name)
        return list_not_changed

    def get_list_failed_tests(self):
        list_failed = list()
        for test_name in self.list_test_names:
            is_failed = (not self.data[test_name]) or \
                        (CRHDLConfiguration.IS_FAILED in self.data[test_name].keys() and
                         self.data[test_name][CRHDLConfiguration.IS_FAILED])
            if is_failed:
                list_failed.append(test_name)
        return list_failed

    def get_list_std_changed_test(self, is_std_change):
        list_std_changed = list()
        for test_name in self.list_test_names:
            if CompareJsonKeys.DIFF in self.data[test_name]:
                diff_info = self.data[test_name][CompareJsonKeys.DIFF]
                if is_std_change in diff_info and \
                        diff_info[is_std_change]:
                            list_std_changed.append(test_name)
        return list_std_changed

    def is_changed(self, test_name):
        if test_name not in self.list_error_compare:
            return self.data[test_name][CRHDLConfiguration.IS_CHANGED]

    def is_bb_changed(self, test_name):
        if test_name not in self.list_error_compare:
            if CRHDLConfiguration.CHANGE in self.data[test_name]:
                detail_info = self.data[test_name][CRHDLConfiguration.CHANGE][CRHDLConfiguration.DETAIL_INFO]
                for info in detail_info:
                    if info[CompareJsonKeys.TITLE] == CompareResultConfig.TITLE_CMP_BB:
                        return info[CompareJsonKeys.IS_CHANGE]
