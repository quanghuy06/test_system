# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      09/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from abc import ABCMeta, abstractmethod
from handlers.test_result_handler import TestResultHandler
from report.lib_base.tsv_reporter import TsvReporter
from handlers.compare_handlers.compare_result_handler import CompareResultHandler


class ETRConfiguration(object):
    TEST_NAME = "Test case"
    TOTAL_ERRORS = "Total errors"
    TOTAL_CHARACTERS = "Total characters"
    INSERT_ERRORS = "Insert errors"
    REPLACE_ERRORS = "Replace errors"
    DELETE_ERRORS = "Delete errors"


class ErrorsReporter(TsvReporter):

    __metaclass__ = ABCMeta

    def __init__(self, test_file, compare_file, test_folder, change_number=None,
                 delta_version=None, **kwargs):
        self.change_number = change_number
        self.delta_version = delta_version
        self.test_folder = test_folder
        self.test_file = test_file
        self.compare_file = compare_file
        super(ErrorsReporter, self).__init__(**kwargs)
        self.test_result_handler = TestResultHandler(input_file=self.test_file,
                                                     test_folder=self.test_folder)
        self.compare_result_handler = CompareResultHandler(input_file=self.compare_file)
        self.list_test_names = list()
        self.headers = list()

    def collect_data(self):
        # Get headers
        self.get_headers()

        # Get list of test names
        self.get_list_test_names()

    @abstractmethod
    def get_list_test_names(self):
        pass

    @abstractmethod
    def get_headers(self):
        pass

    @abstractmethod
    def get_line_data(self, test_name):
        pass
