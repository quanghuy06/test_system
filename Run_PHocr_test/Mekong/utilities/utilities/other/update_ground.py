# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      05/09/2017
# Last update:      05/09/2017
# Description:      Script can be use to update ground truth data from a folder/file
#                   that contains ground truth data

import sys_path
sys_path.insert_sys_path()

import os
import sys
import argparse
from database.lib_base.test_case_manager import TestCaseManager

def parse_test_name_from_ground_file(gname):
    split_gname = gname.split("_")
    split_iname = split_gname[0:-1]
    iname = "_".join(split_iname)
    split_iname = iname.split(".")
    split_testname = split_iname[0:-1]
    test_name = ".".join(split_testname)
    return test_name


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--mekong-user', required=True)
    parser.add_argument('-p', '--password', required=True)
    parser.add_argument('-g', '--ground-data', required=True)
    parser.add_argument('-cl', "--changed_log", required=True,
                        help="Why you need to push new test cases on DB")
    parser.add_argument('--force', default=False, action="store_true")
    args = parser.parse_args()

    # Get file list
    file_list = []
    if os.path.isdir(args.ground_data):
        file_list = os.listdir(args.ground_data)
    if os.path.isfile(args.ground_data):
        file_list.append(args.ground_data)
    if not file_list:
        print "Path {0} does not exist!".format(args.ground_data)
        sys.exit(1)

    # Initial a test case manager
    tc_manager = TestCaseManager(user=args.mekong_user, password=args.password)

    # Update ground truth
    total = len(file_list)
    count = 1
    for fname in file_list:
        print "[{0}/{1}] {2}".format(count, total, fname)
        if os.path.isfile(fname):
            fpath = fname
        else:
            fpath = os.path.join(args.ground_data, fname)
        test_name = parse_test_name_from_ground_file(fname)
        if not tc_manager.is_test_case_on_db(test_name):
            print "File {0} does not match any test case on database!".format(fname)
        else:
            # Update ground truth file
            if args.force:
                tc_manager.delete_ground_truth_data(test_name)
            changed_log = args.changed_log
            tc_manager.push_ground_truth_file(fpath, test_name, changed_log)
        count += 1


if __name__ == "__main__":
    main()