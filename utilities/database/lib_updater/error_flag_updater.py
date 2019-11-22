# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from database.sys_path import insert_sys_path
insert_sys_path()
from abc import ABCMeta

from database.lib_updater.database_updater import DatabaseUpdater
from handlers.compare_handlers.compare_result_handler import CompareResultHandler
from handlers.test_result_handler import TestResultHandler
from baseapi.file_access import read_json
from configs.common import Machines, Platform
from configs.database import TestcaseConfig, SpecKeys
import os


class ErrorFlagUpdater(DatabaseUpdater):
    __metaclass__ = ABCMeta

    def __init__(self, platform, compare_file, **kwargs):
        self.platform = platform
        self.compare_file = compare_file
        super(ErrorFlagUpdater, self).__init__(**kwargs)

    def get_data(self):
        self.logger.start_step("get_data for ErrorFlagUpdater for {0}".format(self.platform))
        self.data = {}
        test_result_handler = TestResultHandler(input_file=self.input_file)
        compare_result_handler = CompareResultHandler(input_file=self.compare_file)
        for test_name in test_result_handler.get_list_tests():
            is_error = test_result_handler.is_error(test_name=test_name)
            if self.compare_file:
                is_error = is_error or test_name in compare_result_handler.get_list_failed_tests()
            self.data[test_name] = is_error
        self.logger.end_step(True)

    def update_data(self):
        self.logger.start_step("update error flag for {0}".format(self.platform))
        tc_folder_path = Machines.MASTER_MACHINE[Machines.TC_FOLDER]
        for test_name in self.data:
            test_spec_file = os.path.join(tc_folder_path, test_name, TestcaseConfig.SPEC_FILE)
            data = read_json(test_spec_file)
            if data[SpecKeys.ERROR_FLAGS][Platform.LINUX] != self.data[test_name]:
                self.test_case_manager.update_error_flag_platform(
                        test_id=test_name,
                        new_value=self.data[test_name],
                        platform=self.platform)
                self.updated_test_cases.append(test_name)
        self.logger.end_step(True)
