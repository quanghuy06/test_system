# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      05/09/2018
# Description:      This script used for create base for report memory

from abc import ABCMeta, abstractmethod
from report.lib_base.tsv_reporter import TsvReporter
from handlers.test_result_handler import TestResultHandler


class MERConfiguration(object):
    # Header
    TEST_NAME = "Test case"
    PEAK_INFO = "Memory peak"
    PEAK_COMMAND = "Run command"


class MemoryReporter(TsvReporter):

    __metaclass__ = ABCMeta

    def __init__(self, test_file, test_folder, change_number=None,
                 delta_version=None, **kwargs):
        super(MemoryReporter, self).__init__(**kwargs)
        self.change_number = change_number
        self.delta_version = delta_version
        self.test_file = test_file
        self.test_folder = test_folder
        self.test_result_handler = TestResultHandler(
            input_file=self.test_file, test_folder=self.test_folder)
        self.list_test_name = list()
        self.header = list()

    def collect_data(self):
        """
        Collect data to report
        -------

        """

        # Get header of sheet
        self.get_header()

        # Get list of test name
        self.get_list_test_names()

    @abstractmethod
    def get_header(self):
        pass

    @abstractmethod
    def get_list_test_names(self):
        pass

    @abstractmethod
    def get_line_data(self, test_name):
        pass
