# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from abc import ABCMeta

from database.lib_updater.database_updater import DatabaseUpdater
from handlers.test_result_handler import TestResultHandler


class WeightUpdater(DatabaseUpdater):

    __metaclass__ = ABCMeta

    def __init__(self, platform, **kwargs):
        self.platform = platform
        super(WeightUpdater, self).__init__(**kwargs)

    def get_data(self):
        self.logger.start_step("get_data for weight updater")
        self.data = {}
        test_result_handler = TestResultHandler(input_file=self.input_file)
        for test_name in test_result_handler.get_list_not_error_tests():
            self.data[test_name] = test_result_handler.get_time(test_name=test_name)

        self.logger.end_step(True)

    def update_data(self):
        self.logger.start_step("update weight for {0}".format(self.platform))
        for test_name in self.data:
            self.test_case_manager.update_weight_platform(test_id=test_name,
                                                          platform=self.platform,
                                                          new_value=self.data[test_name])
            if test_name not in self.updated_test_cases:
                self.updated_test_cases.append(test_name)
        self.logger.end_step(True)
