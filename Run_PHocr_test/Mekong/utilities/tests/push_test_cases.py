# Toshiba - TSDV
# Team:         PHOcr
# Author:       Luong Van Huan
# Email:        huan.luongvan@toshiba-tsdv.com
# Date created: 27/08/2016
# Last update:  18/07/2017
# Updated by:   Phung Dinh Tai
# Description:  This script allow user to push test case to database

import sys_path
sys_path.insert_sys_path()

import os
import argparse

from database.lib_base.test_case_manager import TestCaseManager
from configs.database import TestcaseConfig
from manager.lib_post_it.jenkins_post_it_updater import JenkinsPostItUpdater


def parse_argument():
    parser = argparse.ArgumentParser(description='Push test cases from/to database')
    parser.add_argument('-u', '--user', required=True,
                        help='Username to access Mekong database')
    parser.add_argument('-p', '--password', required=True,
                        help='Password to access Mekong database')
    parser.add_argument('-f', '--test-folder', default=TestcaseConfig.FOLDER_DEFAULT,
                        help='Folder contains test cases')
    parser.add_argument('--force', default=False, action='store_true',
                        help="Force to push test cases if they already existed on"
                             " Mekong database")

    parser.add_argument('-i', "--test-id",
                        help="Test case ID of test case should be push or update."
                             " If test id is not defined, "
                             "action will be apply for all test case in test folder."
                             " Please use comma to seperate test id.")
    parser.add_argument('-cl', "--changed_log", required=True,
                        help="Why you need to push new test cases on DB")
    parser.add_argument("--update-reference", default=False, action='store_true',
                        help="Update reference data.")
    parser.add_argument("--update-test-data", default=False, action='store_true',
                        help="Update test data.")
    parser.add_argument("--update-ground", default=False, action='store_true',
                        help="Update ground truth data.")
    parser.add_argument("--update-scripts", default=False, action='store_true',
                        help="Update scripts. Should pass through scripts folder")
    parser.add_argument("--update-spec", default=False, action='store_true',
                        help="Update specification of test case.")
    return parser


def main() :

    parser = parse_argument()
    args = parser.parse_args()
    test_case_manager = TestCaseManager(args.user, args.password)
    test_folder = args.test_folder
    update_on = args.update_reference\
                or args.update_test_data\
                or args.update_scripts\
                or args.update_spec\
                or args.update_ground
    changed_log=args.changed_log

    # Get list of test case directory
    test_path_list = []
    if args.test_id:
        from configs.common import Delimiter
        test_id_list = args.test_id.split(Delimiter.LIST)
        test_path_list = []
        for test_id in test_id_list:
            test_path = os.path.join(test_folder, test_id)
            if os.path.isdir(test_path):
                test_path_list.append(test_path)
            else:
                print "ERROR: No such file or directory {0}".format(test_path)
    else:
        for fname in sorted(os.listdir(test_folder)):
            test_path = os.path.join(test_folder, fname)
            if os.path.isdir(test_path):
                test_path_list.append(test_path)

    if update_on:
        # Update test cases
        total = len(test_path_list)
        count = 1
        updated_parts = []
        for test_path in test_path_list:
            test_id = os.path.basename(test_path)
            print "[{0}/{1}] Update test case {2}".format(count, total, test_id)
            # Update reference data
            if args.update_reference:
                ref_data_dir = os.path.join(test_path, TestcaseConfig.REF_DATA_DIR)
                test_case_manager.update_reference_data(ref_data_dir, test_id)
                updated_parts.append(TestcaseConfig.REF_DATA_DIR)

            # Update test data
            if args.update_test_data:
                test_data_dir = os.path.join(test_path, TestcaseConfig.TEST_DATA_DIR)
                test_case_manager.update_test_data(test_data_dir, test_id)
                updated_parts.append(TestcaseConfig.TEST_DATA_DIR)

            # Update ground truth data
            if args.update_ground:
                ground_truth_dir = os.path.join(test_path, TestcaseConfig.GROUND_TRUTH_DATA_DIR)
                test_case_manager.update_ground_truth_data(ground_truth_dir, test_id)
                updated_parts.append(TestcaseConfig.GROUND_TRUTH_DATA_DIR)

            # Update scripts
            if args.update_scripts:
                scripts_dir = os.path.join(test_path, TestcaseConfig.SCRIPT_DIR)
                test_case_manager.update_scripts(scripts_dir, test_id)
                updated_parts.append(TestcaseConfig.SCRIPT_DIR)

            # Update spec
            if args.update_spec:
                spec_file = os.path.join(test_path, TestcaseConfig.SPEC_FILE)
                test_case_manager.update_spec(test_id, spec_file)
                updated_parts.append(TestcaseConfig.SPEC_FILE)
            count += 1
            if updated_parts:
                changed_log += "." + JenkinsPostItUpdater.KEY_UPDATED + ", ".join(updated_parts)
                test_case_manager.add_new_changed_log(test_id, changed_log)
            del updated_parts[:]
            changed_log = args.changed_log
    else:
        # Push test  cases
        added_test_cases = test_case_manager.push_test_cases(test_path_list, args.force)
        for testcase in added_test_cases:
            test_case_manager.add_new_changed_log(testcase, changed_log)


if __name__ == "__main__" :
    main()
