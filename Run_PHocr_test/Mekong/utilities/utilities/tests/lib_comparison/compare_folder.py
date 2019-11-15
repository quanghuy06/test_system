# Toshiba - TSDV
# Team:         PHOcr
# Author:       Hoang Minh Phuc
# Email:        phuc.hoangminh@toshiba-tsdv.com
# Date created:     29/01/2017
# Last update:      29/06/2017
# Updated by:       Phung Dinh Tai
# Description:      This script define class for comparison of 2 folders
import os
import argparse
import filecmp
import sys
import traceback
import sys_path
sys_path.insert_sys_path()
from configs.compare_result import CompareJsonKeys, CompareResultConfig
from baseapi.file_access import write_json, remove_paths, copy_paths, move_paths


class DirCmp(filecmp.dircmp):
    """
    Compare the content of dir1 and dir2. In contrast with filecmp.dircmp, this
    subclass compares the content of files with the same path.
    """
    def phase3(self):
        """
        Find out differences between common files.
        Ensure we are using content comparison with shallow=False.
        """
        f_comp = filecmp.cmpfiles(self.left, self.right, self.common_files,
                                  shallow=False)
        self.same_files, self.diff_files, self.funny_files = f_comp


class CompareFolder:

    def __init__(self):
        self.title = CompareResultConfig.TITLE_CMP_FOLDER

    def compare(self, src, des):
        # Check input
        compare_result = {
            CompareJsonKeys.TITLE: 'Compare folder',
            CompareJsonKeys.IS_CHANGE: False,
            CompareJsonKeys.INFO: {
                "left_only": [],
                "right_only": [],
                "diff_files": [],
                "funny_files": []
            }
        }

        self.compare_(src, des, compare_result)
        return compare_result

    def compare_(self, src, des, compare_result):
        try:
            # Using method of Python to compare two folders
            compared = DirCmp(src, des)
            # If changed
            is_changed = compared.left_only or compared.right_only or compared.diff_files or \
                compared.funny_files
            if is_changed:
                compare_result[CompareJsonKeys.IS_CHANGE] = True
                compare_result[CompareJsonKeys.INFO]["left_only"] += compared.left_only
                compare_result[CompareJsonKeys.INFO]["right_only"] += compared.right_only
                compare_result[CompareJsonKeys.INFO]["diff_files"] += compared.diff_files
                compare_result[CompareJsonKeys.INFO]["funny_files"] += compared.funny_files

            for subdir in compared.common_dirs:
                des_subdir = os.path.join(des, subdir)
                src_subdir = os.path.join(src, subdir)
                self.compare_(src_subdir, des_subdir, compare_result)
        except:
            traceback.print_exc()

        return compare_result


def parse_argument():
    parser = argparse.ArgumentParser(description='Compare folder (support for excluding files)')
    parser.add_argument('-s', '--source',
                        help='Path to output folder',
                        required=True)
    parser.add_argument('-d', '--target',
                        help='Path to reference folder',
                        required=True)
    parser.add_argument('-o', '--outfile',
                        help='Output file in json format')
    return parser.parse_args()


def main():
    args = parse_argument()
    try:

        # Create compare runner and execute comparison
        runner = CompareFolder()
        compare_result = runner.compare(args.source, args.target)
        print compare_result

        # Write compare result to json file
        if not args.outfile:
            args.outfile = "compare_result.json"
        write_json(compare_result, args.outfile)

    except:
        traceback.print_exc(file=sys.stdout)


if __name__ == "__main__":
    main()

# How to run:
# For ex: python Mekong/utilities/tests/lib_runner/compare_folder.py
    #  -s ~/Desktop/test_set_Ubuntu10.04-32bit-1/0033_bmp_folder/output/linux/
    #  -d ~/Desktop/test_set_Ubuntu10.04-32bit-1/0033_bmp_folder/ref_data/linux/
    #  -o ~/Desktop/result
