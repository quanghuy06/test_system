# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Le Duc Nam
# Email:            nam.leduc@toshiba-tsdv.com
# Date create:      20/11/2017
# Last update:      29/06/2107
# Editor:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Description:      Adhoc testing. Run test for only one test case in test folder.

import sys_path
sys_path.insert_sys_path()
import os
import sys
import argparse
import traceback
import configs.common
from configs.test_result import TestResultConfig
from baseapi.file_access import write_json

###############################################################################
# Parsing arguments
def parse_argument():
    parser = argparse.ArgumentParser(description='Run one test case')
    parser.add_argument('-b', '--bin-folder', required=True,
                        help='Folder contain executable')
    parser.add_argument('-t', '--test-folder',
                        help='Folder contain test set',
                        required = True)
    parser.add_argument('-id', '--test-id', required=True,
                        help='Test case id')
    parser.add_argument('-o', '--output-file', default=TestResultConfig.FILE_DEFAULT,
                        help='Test output file to export in json format')
    parser.add_argument('-p', '--platform', required=True,
                      help="Platform execute test")
    return parser.parse_args()

###############################################################################
# Main function
def main():
    args = parse_argument()

    bin_folders = args.bin_folder.split(",")
    abs_bin_folders = []
    for f in bin_folders:
        if os.path.isdir(f):
            abs_bin_folders.append(os.path.abspath(f))
        else:
            print("Folder {0} does not exist!".format(f))
            sys.exit(1)

    if args.platform.lower() not in configs.common.SupportedPlatform:
        print ("Platform {0} is not valid!".format(args.platform))
        sys.exit(1)

    from lib_runner.test_runner import TestRunner
    runner = TestRunner()

    results = {}
    try:
        run_infor = runner.run(test_folder=args.test_folder, abs_bin_folders=abs_bin_folders,
                               test_id=args.test_id, plf=args.platform)
        results[args.test_id] = run_infor
    except Exception as e:
        print('-'*60)
        traceback.print_exc(file=sys.stdout)
        print('-'*60)

    # Write test result to json file
    write_json(results, args.output_file)

###############################################################################
# Check name of module
if __name__ == "__main__":
    main()
