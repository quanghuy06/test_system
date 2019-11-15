# Toshiba - TSDV
# Team:         PHOcr
# Author:       Luong Van Huan
# Email:        huan.luongvan@toshiba-tsdv.com
# Date created: 27/08/2016
# Last update:  04/07/2017
# Updated by:   Phung Dinh Tai
# Description:  This script is used to delete test case by id

import sys_path
sys_path.insert_sys_path()

import argparse

from database.lib_base.test_case_manager import TestCaseManager


def main():
    parser = argparse.ArgumentParser(description='Get test spec, test data,'
                                                 ' reference data from data base')
    parser.add_argument('-u', '--user', required=True,
                        help='User name')
    parser.add_argument('-p', '--password', required=True,
                        help='Password')
    parser.add_argument('-id', '--test-cases-id',
                        help='Delete by test case id. List should seperate by ","')
    args = parser.parse_args()
    test_case_manager = TestCaseManager(args.user, args.password)
    if args.test_cases_id :
        from configs.common import Delimiter
        test_list = args.test_cases_id.split(Delimiter.LIST)
        test_case_manager.delete_test_cases(test_list)
    else :
        print "You need pass list of test cases name"
        parser.print_help()


if __name__ == "__main__":
    main()