# Toshiba - TSDV
# Team:         PHOcr
# Author:       Le Duc Nam
# Email:        nam.leduc@toshiba-tsdv.com
# Date create:  20/08/2016
# Last update:  19/07/2017
# Updated by:   Phung Dinh Tai
# Description:  This script define runner class for comparison
import imp
import os
import traceback
import sys_path
sys_path.insert_sys_path()
from configs.database import TestcaseConfig
from baseapi.file_access import remove_paths
from tests.lib_comparison.auto_executor import AutoComparisonExecutor
from baseapi.file_access import move_globs
from configs.compare_result import CompareResultConfig


class CompareRunner(object):
    @staticmethod
    def change_working_dir(working_dir):
        # Change current directory before run real test
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
        os.chdir(working_dir)

    # Run comparison for one test case
    def run(self, test_folder, test_id, platform,
            compare_folder=CompareResultConfig.FOLDER_DEFAULT):
        abs_test_folder = os.path.abspath(test_folder)
        compare_folder = os.path.abspath(compare_folder)
        curr_dir = os.getcwd()  # Directory run this scripts
        tmp_folder = 'e7968b1d-19c6-43e4-bc07-d203abc3a4be_cmp_runner_{0}_{1}'
        tmp_folder = tmp_folder.format(test_id, platform)
        tmp_folder_path = os.path.join(curr_dir, tmp_folder)
        try:

            # Change to temporary working directory
            self.change_working_dir(tmp_folder_path)

            script_runner_path = os.path.join(abs_test_folder, test_id,
                                              TestcaseConfig.SCRIPT_DIR,
                                              TestcaseConfig.Scripts.COMPARE)
            if os.path.isfile(script_runner_path):
                # Load runner of test cases
                mod_name, file_ext = os.path.splitext(TestcaseConfig.Scripts.COMPARE)
                # Load user defined script
                source = imp.load_source(mod_name, script_runner_path)
                executor = source.Compare()
                # Run test
                compare_result = executor.run()

            else:
                # If can not excute custom compare script, use auto-gen compare flow instead
                executor = AutoComparisonExecutor(abs_test_folder, test_id, platform)
                compare_result = executor.run()
            # Move compare output to test folder
            result_tmp_dir = os.path.join(tmp_folder_path,
                                          CompareResultConfig.FOLDER_DEFAULT,
                                          test_id)
            glob_name = os.path.join(result_tmp_dir, "*")
            target_folder = os.path.join(os.path.dirname(abs_test_folder),
                                         compare_folder, test_id)
            if not os.path.isdir(target_folder):
                os.makedirs(target_folder)

            # For case, test case has test result, move it to target folder
            # And if it does not have, just ignore and continue compare other
            # test case.
            if os.path.isdir(result_tmp_dir):
                move_globs(glob_name, target_folder)
            return compare_result
        except:
            traceback.print_exc()
        finally:

            # Always come back to current working directory and remove temporary working directory
            self.change_working_dir(curr_dir)
            remove_paths(tmp_folder_path)
