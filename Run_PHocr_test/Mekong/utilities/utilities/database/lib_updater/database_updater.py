# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from abc import ABCMeta, abstractmethod

from baseapi.log_manager import Logger
from database.lib_base.test_case_manager import TestCaseManager


class DatabaseUpdater(object):

    __metaclass__ = ABCMeta

    def __init__(self, username, password, input_file=None, log_enable=False):
        self.username = username
        self.password = password
        self.input_file = input_file
        self.work_good = True
        self.data = None
        self.logger = Logger(log_disable=(not log_enable))
        self.test_case_manager = TestCaseManager(user=username, password=password)
        self.updated_test_cases = []

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def update_data(self):
        pass

    def get_updated_test_cases(self):
        return self.updated_test_cases

    def do_work(self):
        # Collect data
        self.get_data()

        # Update data to database
        self.update_data()

    def add_changed_log_for_updated_test_cases(self, changed_log):
        """
        Add changed log for updated test cases

        Parameters
        ----------
        changed_log: str
            Log need to add to test case's revision history

        Returns
        -------
        None
            None if successfully,
            raise Exception if failure

        """
        for test_case in self.updated_test_cases:
            self.test_case_manager.add_new_changed_log(test_case, changed_log)
