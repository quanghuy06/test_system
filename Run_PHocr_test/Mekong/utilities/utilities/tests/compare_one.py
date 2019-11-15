# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Le Duc Nam
# Email:            nam.leduc@toshiba-tsdv.com
# Date create:      20/11/2017
# Last update:      02/07/2107
# Editor:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Description:      Adhoc testing. Run compare test result for only one test case in a test folder


import sys_path
sys_path.insert_sys_path()

import sys
import os
import argparse
import traceback

from configs.compare_result import CompareResultConfig
from baseapi.file_access import write_json
from tests.lib_comparison.compare_runner import CompareRunner

###############################################################################
# Parsing arguments
def parse_argument():
    parser = argparse.ArgumentParser(
                description='Compare output and reference of one test case')
    parser.add_argument('-t', '--test-folder', required = True,
                        help='Folder contain test set')
    parser.add_argument('-id', '--test_id', required = True,
                        help='Test case id')
    parser.add_argument('-o', '--output-file', default=CompareResultConfig.FILE_DEFAULT,
                        help='Compare output file to export in json format')
    parser.add_argument('-p', '--platform',
                        help='Platform want to compare')
    parser.add_argument('-f', '--output-folder', default=CompareResultConfig.FOLDER_DEFAULT,
                        help='Result folder to export')
    parser.add_argument('-e', '--error-json', default=CompareResultConfig.FILE_ERROR_DEFAULT,
                        help='Summary of errors file to export in json format')
    return parser.parse_args()

###############################################################################
# Main function
def main():
    # Parse arguments
    args = parse_argument()

    runner = CompareRunner()

    results = {}
    try:
        run_infor = runner.run(args.test_folder, args.test_id, args.platform, args.output_folder)
        results[args.test_id] = run_infor
    except Exception as e:
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)

    # Write test result to json file
    write_json(results, args.output_file)

###############################################################################
# Check name of module
if __name__ == "__main__":
    main()
