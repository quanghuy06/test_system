# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Description:
import argparse
import sys_path
sys_path.insert_sys_path()
from database.lib_updater.history_data_updater import HistoryDataUpdater


def parse_arguments():
    # Parsing arguments
    parser = argparse.ArgumentParser(description="Update spec info by tsv file input")
    parser.add_argument('-u', '--username', required=True,
                        help='Req: Username to access Mongo DB')
    parser.add_argument('-p', '--password', required=True,
                        help='Req: Password to access Mongo DB')
    parser.add_argument('-i', '--input-file',
                        help='Name of input file, should be in tsv format')
    parser.add_argument('-t', '--product',
                        help='Req: Product to update data')
    parser.add_argument('-v', '--version',
                        help='Req: Delta version of product will be updated')
    parser.add_argument('-e', '--platform',
                        help='Req: Platform to upate information')
    parser.add_argument('-cl', "--changed_log", required=True,
                        help="Why you need to push new test cases on DB")
    return parser


def main():
    # Parse arguments
    parser = parse_arguments()
    # Get arguments
    args = parser.parse_args()
    # Initial reporter
    updater = HistoryDataUpdater(username=args.username, password=args.password,
                                 input_file=args.input_file, product=args.product,
                                 version=args.version, platform=args.platform)
    # Make report
    updater.do_work()
    changed_log = args.changed_log
    updater.add_changed_log_for_updated_test_cases(changed_log)


if __name__ == "__main__":
    main()