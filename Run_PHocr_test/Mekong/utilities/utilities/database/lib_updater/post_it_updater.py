# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      11/07/2018
# Description:
from database.lib_updater.weight_updater import WeightUpdater
from database.lib_updater.error_flag_updater import ErrorFlagUpdater
from database.lib_updater.history_data_updater import HistoryDataUpdater


# TODO(HuanLV) Remove this unused class
class PostItUpdater:

    def __init__(self, username, password, platform, test_result_file=None, compare_file=None,
                 history_data_file=None, history_product=None, history_version=None):
        self.username = username
        self.password = password
        self.platform = platform
        self.test_file = test_result_file
        self.compare_file = compare_file
        self.history_data_file = history_data_file
        self.history_product = history_product
        self.history_version = history_version

    def run_update(self):
        # Initial list of updaters
        list_updaters = []

        if self.test_file:
            # Update weight
            list_updaters.append(WeightUpdater(username=self.username, password=self.password,
                                               input_file=self.test_file, platform=self.platform))

            # Update error flag
            list_updaters.append(ErrorFlagUpdater(username=self.username, password=self.password,
                                                  input_file=self.test_file,
                                                  platform=self.platform,
                                                  compare_file=self.compare_file))

        if self.history_data_file:
            # Update history data
            list_updaters.append(HistoryDataUpdater(username=self.username,
                                                    password=self.password,
                                                    input_file=self.history_data_file,
                                                    product=self.history_product,
                                                    platform=self.platform,
                                                    version=self.history_version))

        # Run progress
        for updater in list_updaters:
            updater.do_work()
