# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date create:  30/06/2017
# Last update:  28/08/2018
# Updated by:   Le Thi Thanh
# Description:  This script define executer for HanoiWorkflow result comparison

import os
import sys_path
sys_path.insert_sys_path()

from configs.compare_result import CompareJsonKeys
from configs.database import TestcaseConfig
from configs.compare_result import CompareResultConfig
from configs.test_result import FinalTestResult
from baseapi.common import add_empty_file_2_dir
from tests.lib_comparison.compare_folder_test_result import CompareFolderTestResult


class HanoiCompareExecutor:

    def __init__(self, test_folder, test_id, platform,
                 result_folder=CompareResultConfig.FOLDER_DEFAULT):
        self.test_folder = test_folder
        self.test_id = test_id
        self.test_path = os.path.join(test_folder, test_id)
        self.result_folder = os.path.join(result_folder, test_id)
        self.platform = platform

    def execute(self):
        all_result = {}
        all_result[CompareJsonKeys.DIFF] = {}
        diff_info = {
            CompareJsonKeys.IS_CHANGE: False,
            CompareJsonKeys.INFO: {
                CompareResultConfig.NOT_IN_REFERENCE: [],
                CompareResultConfig.NOT_IN_OUTPUT: [],
                CompareResultConfig.DIFF_FILE: []
            }
        }
        compare_test_result = CompareFolderTestResult(self.test_folder, self.test_id)
        o_folder = os.path.join(self.test_path, TestcaseConfig.OUTPUT_FOLDER, self.platform)
        if not os.path.isdir(o_folder):
            os.makedirs(o_folder)
        add_empty_file_2_dir(o_folder)
        r_folder = os.path.join(self.test_path, TestcaseConfig.REF_DATA_DIR, self.platform)
        if not os.path.isdir(r_folder):
            os.makedirs(r_folder)
        not_in_r, not_in_o, detail_infos = compare_test_result.compare_two_folder(r_folder,
                                                                   o_folder)

        is_change = False
        if not_in_r or not_in_o:
            is_change = True
        for info in detail_infos:
            if info[CompareJsonKeys.IS_CHANGE] == True:
                is_change = True
        if not_in_r:
            diff_info[CompareJsonKeys.INFO][CompareResultConfig.NOT_IN_REFERENCE] = not_in_r
            diff_info[CompareJsonKeys.IS_CHANGE] = True
        if not_in_o:
            diff_info[CompareJsonKeys.INFO][CompareResultConfig.NOT_IN_OUTPUT] = not_in_o
            diff_info[CompareJsonKeys.IS_CHANGE] = True
        if detail_infos:
            diff_info[CompareJsonKeys.INFO][CompareResultConfig.DIFF_FILE] = detail_infos
            for info in detail_infos:
                if info[CompareJsonKeys.IS_CHANGE]:
                    diff_info[CompareJsonKeys.IS_CHANGE] = True
        is_stdout_changed = compare_test_result.is_file_changed(r_folder, o_folder,
                                                             FinalTestResult.Test.STDOUT_FILE_NAME)
        is_stderr_changed = compare_test_result.is_file_changed(r_folder, o_folder,
                                                             FinalTestResult.Test.STDERR_FILE_NAME)
        diff_info[CompareJsonKeys.IS_STDOUT_CHANGED] = is_stdout_changed
        diff_info[CompareJsonKeys.IS_STDERR_CHANGED] = is_stderr_changed
        if is_stderr_changed or is_stdout_changed:
            is_change = True
        all_result[CompareJsonKeys.DIFF] = diff_info
        all_result[CompareJsonKeys.IS_CHANGE] = is_change
        return all_result
