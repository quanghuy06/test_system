# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Le Duc Nam
# Email:            nam.leduc@toshiba-tsdv.com
# Date create:      20/11/2017
# Last update:      29/06/2107
# Editor:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Description:      Adhoc testing. Run test.

import sys_path
sys_path.insert_sys_path()

import sys
import os
from optparse import OptionParser
import traceback
import configs.common
from configs.test_result import TestResultConfig
from baseapi.file_access import write_json

###############################################################################
# Parsing arguments
def parse_argument():
    parser = OptionParser()
    parser.add_option('-b', '--bin-folder', dest="bin_folder",
                        help='Folder contain executable')
    parser.add_option('-t', '--test-folder', dest="test_folder",
                        help='Folder contain test set')
    parser.add_option('-o', '--output-file', dest="output_file",
                        default=TestResultConfig.FILE_DEFAULT,
                        help='Test output file to export in json format')
    parser.add_option('-p', '--platform', dest='platform',
                      help="Platform execute test")
    return parser.parse_args()

###############################################################################
# Get test set
def get_test_set(test_folder):
    test_set = []
    for x in os.listdir(test_folder):
        test_set.append(x)
    return test_set


###############################################################################
# Main function
def main():
    (args, options) = parse_argument()

    bin_folders = args.bin_folder.split(",")
    abs_bin_folders = []
    for f in bin_folders:
        if os.path.isdir(f):
            abs_bin_folders.append(os.path.abspath(f))
        else:
            print("Folder {0} does not exist!".format(f))
            sys.exit(1)

    if not args.platform:
        print ("Platform to test is not defined!")
        sys.exit(1)

    if args.platform.lower() not in configs.common.SupportedPlatform:
        print ("Platform {0} is not valid!".format(args.platform))
        sys.exit(1)

    test_set = sorted(get_test_set(args.test_folder))

    from lib_runner.test_runner import TestRunner
    runner = TestRunner()

    results = {}
    index = 1
    for test_id in test_set:
        print('[' + str(index) + '/' + str(len(test_set)) +
              '] Run with testcase "' + str(test_id) + '"')
        index += 1
        try:
            run_infor = runner.run(test_folder=args.test_folder,
                                   abs_bin_folders=abs_bin_folders,
                                   test_id=test_id, plf=args.platform.lower())
            results[test_id] = run_infor
        except Exception as e:
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
            sys.exit(1)

        output_file = test_id + "_result.json"
        write_json(results, output_file)
        del results

    # Write test result to json file
    # write_json(results, args.output_file)

###############################################################################
# Check name of module
if __name__ == "__main__":
    main()
