# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      02/08/2017
# Last update:      02/08/2107
# Editor:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Description:      Update ground truth name after change of Mitchell on output file name of text
#                   and bounding box
import sys_path
sys_path.insert_sys_path()

import argparse
import os
from baseapi.file_access import copy_paths, remove_paths, move_paths
from configs.database import TestcaseConfig
from configs.common import Platform


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--test-folder", required=True,
                        help="Folder contains test cases")
    parser.add_argument('-o', '--output-folder', default="GRUPDATED",
                        help="Output folder")
    return parser

ext_list = []
for i in range(0, 10):
    ext_list.append("_{0}.txt".format(i))

def main():
    parser = parse_argument()
    args = parser.parse_args()
    if os.path.exists(args.output_folder):
        remove_paths(args.output_folder)
    os.makedirs(args.output_folder)

    print "Copy test case"
    test_list = os.listdir(args.test_folder)
    total = len(test_list)
    count = 1
    for name in test_list:
        print "[{0}/{1}] {2}".format(count, total, name)
        test_path = os.path.join(args.test_folder, name)
        copy_paths(test_path, args.output_folder)
        count += 1

    # Rename ground truth name
    print "Rename ground truth name for text file and bounding box file"
    test_list = os.listdir(args.output_folder)
    total = len(test_list)
    count = 1
    for test_name in test_list:
        print "[{0}/{1}] {2}".format(count, total, test_name)
        gr_dir = os.path.join(args.output_folder, test_name, TestcaseConfig.GROUND_TRUTH_DATA_DIR, Platform.LINUX)
        test_data_dir = os.path.join(args.output_folder, test_name, TestcaseConfig.TEST_DATA_DIR)
        image_name = os.listdir(test_data_dir)[0]
        for fname in os.listdir(gr_dir):
            fpath = os.path.join(gr_dir, fname)
            for ext_str in ext_list:
                if fname.endswith(ext_str):
                    dname = "{0}{1}".format(image_name, ext_str)
                    dpath = os.path.join(gr_dir, dname)
                    move_paths(fpath, dpath)
            if fname == "{0}.txt".format(test_name):
                dname = "{0}.txt".format(image_name)
                dpath = os.path.join(gr_dir, dname)
                move_paths(fpath, dpath)
        count += 1

if __name__ == "__main__":
    main()
