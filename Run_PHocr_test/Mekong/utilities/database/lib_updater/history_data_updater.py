# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from abc import ABCMeta
from database.lib_parser.history_data_parser import HistoryDataParser
from database.lib_updater.database_updater import DatabaseUpdater


class HistoryDataUpdater(DatabaseUpdater):

    __metaclass__ = ABCMeta

    def __init__(self, product, platform, version, **kwargs):
        self.product = product
        self.platform = platform
        self.version = version
        super(HistoryDataUpdater, self).__init__(**kwargs)
        self.data_parser = None

    def get_data(self):
        self.logger.start_step("get_data for HistoryDataUpdater for {0}".format(self.platform))
        self.data_parser = HistoryDataParser(input_file=self.input_file)
        self.data_parser.do_work()
        self.logger.end_step(True)

    def update_data(self):
        self.logger.start_step("update history_data for {0}".format(self.platform))
        for header in self.data_parser.headers:
            data = self.data_parser.data[header]
            for test_name in data:
                new_value = data[test_name]
                if new_value is None:
                    continue
                self.test_case_manager.update_history_data_by_value(test_id=test_name,
                                                                    product=self.product,
                                                                    platform=self.platform,
                                                                    version=self.version,
                                                                    label=header,
                                                                    new_value=new_value)
                if test_name not in self.updated_test_cases:
                    self.updated_test_cases.append(test_name)

        self.logger.end_step(True)
