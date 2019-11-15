# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Description:
import argparse
import sys_path
sys_path.insert_sys_path()
from database.lib_updater.error_flag_updater import ErrorFlagUpdater


def parse_arguments():
    # Parsing arguments
    parser = argparse.ArgumentParser(description="Update spec info by tsv file input")
    parser.add_argument('-u', '--username', required=True,
                        help='Username to access Mongo DB')
    parser.add_argument('-p', '--password', required=True,
                        help='Password to access Mongo DB')
    parser.add_argument('-t', '--test-file', required=True,
                        help='Test result json file')
    parser.add_argument('-c', '--compare_file', default=None,
                        help='Compare result file in json format')
    parser.add_argument('-e', '--platform', required=True,
                        help='Platform to update')
    parser.add_argument('-cl', "--changed_log", required=True,
                        help="Why you need to push new test cases on DB")
    return parser


def main():
    # Parse arguments
    parser = parse_arguments()
    # Get arguments
    args = parser.parse_args()
    # Initial reporter
    updater = ErrorFlagUpdater(username=args.username, password=args.password,
                               input_file=args.test_file, platform=args.platform,
                               compare_file=args.compare_file)
    # Make report
    updater.do_work()
    changed_log = args.changed_log
    updater.add_changed_log_for_updated_test_cases(changed_log)


if __name__ == "__main__":
    main()