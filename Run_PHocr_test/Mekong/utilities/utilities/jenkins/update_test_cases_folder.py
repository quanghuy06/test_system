# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Tran Quang Huy
# Email:            huy.tranquang@toshiba-tsdv.com
# Date create:      4/11/2019
# Last update by:
# Date:
# Description:      This script is used to update test cases folder on local machine from database.
#                   It will download all the test cases from database to a target folder or check
#                   latest change log of test case to decide which parts will be updated.
import os
import sys
import time
import argparse
import traceback
import sys_path
sys_path.insert_sys_path()
from jenkins.lib_synchronization.test_cases_updater import TestCasesUpdater
from configs.database import DbConfig
from baseapi.file_access import make_dir


MANUAL = """
"""


def parse_argument():
    """
    Parse argument for run script.

    Returns
    -------
    ArgumentParser
        Arguments parser object

    """
    parser = argparse.ArgumentParser(MANUAL)
    parser.add_argument('-f', '--test-folder',
                        required=True,
                        help="Path to test cases folder to update")
    return parser


def main():

    # Parse arguments
    parser = parse_argument()
    args = parser.parse_args()

    print("<SM> Update test cases folder from Mekong database on {server}".format(
        server=DbConfig.HOST))

    # Calculate execution time for processing
    start_time = time.time()

    # Update test cases folder on master machine includes getting new test cases and updating for
    # changed test cases
    try:
        # Safe guard
        test_folder = args.test_folder
        if not test_folder:
            print ("ERROR: Please define test folder, it can not be empty!")
            sys.exit(1)
        elif not os.path.isdir(test_folder):
            make_dir(test_folder)

        test_cases_updater = TestCasesUpdater(test_folder=test_folder)
        test_cases_updater.do_works()
    except:
        traceback.print_exc()
        print("WARN: Failed to update test cases folder on master machine!")
        print("<EM> Finish in: {execution_time}s".format(execution_time=time.time() - start_time))
        sys.exit(1)

    print("<EM> Finish in: {execution_time}s".format(execution_time=time.time()-start_time))
    sys.exit(0)


if __name__ == "__main__":
    main()
