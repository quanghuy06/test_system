# Editor:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Description:      Checking data of test cases
import sys_path
sys_path.insert_sys_path()
import argparse
import os
import sys
from configs.database import TestcaseConfig

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--test-folder',
                        help="Folder contains test cases")
    parser.add_argument('--check-bb-ground', default=False, action='store_true',
                        help="Check if any test case missing bounding box ground truth")
    parser.add_argument('--check-text-ground', default=False, action='store_true',
                        help="Check if any test case missing text ground truth")
    return parser

def main():
    parser = parse_argument()
    args = parser.parse_args()
    if not os.path.isdir(args.test_folder):
        print "Test folder {0} does not exist!"
        sys.exit(1)

    # Checking bounding box ground truth
    if args.check_bb_ground:
        print ">>> CHECKING BOUNDING BOX GROUND TRUTH"
        print "Please wait..."
        count = 0
        for test_name in sorted(os.listdir(args.test_folder)):
            test_data = os.path.join(args.test_folder, test_name, TestcaseConfig.TEST_DATA_DIR)
            ground_data = os.path.join(args.test_folder, test_name, TestcaseConfig.GROUND_TRUTH_DATA_DIR, "linux")
            for iname in sorted(os.listdir(test_data)):
                gname = iname + "_0.txt"
                gfile = os.path.join(ground_data, gname)
                if not os.path.isfile(gfile):
                    print "{0}- {1} : Missing {2}".format(count, test_name, gname)
                    count += 1
        if count == 0:
            print "Everything OK!"

    # Checking text ground truth
    if args.check_text_ground:
        print ">>> CHECKING GROUND TRUTH TEXT"
        print "Please wait..."
        count = 0
        for test_name in sorted(os.listdir(args.test_folder)):
            test_data = os.path.join(args.test_folder, test_name, TestcaseConfig.TEST_DATA_DIR)
            ground_data = os.path.join(args.test_folder, test_name, TestcaseConfig.GROUND_TRUTH_DATA_DIR, "linux")
            for iname in sorted(os.listdir(test_data)):
                gname = iname + ".txt"
                gfile = os.path.join(ground_data, gname)
                if not os.path.isfile(gfile):
                    print "{0}- {1} : Missing {2}".format(count, test_name, gname)
                    count += 1
        if count == 0:
            print "Everything OK!"

if __name__ == "__main__":
    main()