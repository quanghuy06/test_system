# Toshiba - TSDV
# Team:         PHOcr
# Author:       Hoang Minh Phuc
# Email:        phuc.hoangminh@toshiba-tsdv.com
# Date created:     29/01/2017
# Last update:      29/06/2017
# Updated by:       Phung Dinh Tai
# Description:      This script define class for compare folder contains bounding box layout
#                   file comparison
import os
import argparse
import filecmp
import subprocess
import sys
import traceback
import platform
from os import path
from configs.compare_result import CompareJsonKeys, CompareResultConfig
from configs.projects.mekong import MekongProject
from configs.common import Platform
from baseapi.file_access import write_json


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


class CompareFolderIncludingBoundingBox:

    def __init__(self):
        self.title = CompareResultConfig.TTILE_CMP_FOLDER_BB

    def compare(self, dir1, dir2, result_folder, postfix=""):
        # Check input
        if not os.path.exists(dir1):
            raise Exception("Path \"" + dir1 + "\" is not exist")
        if not os.path.exists(dir2):
            raise Exception("Path \"" + dir2 + "\" is not exist")
        if not os.path.exists(result_folder):
            os.makedirs(result_folder)

        """
        Compare two directory trees content.
        Return False if they differ, True is they are the same.
        Additional, if having .txt files, using difftool (SaigonDiff) to compare bounding box
        """
        # Compare structure
        compare_result = {
            CompareJsonKeys.TITLE: 'Compare folder including bounding box',
            CompareJsonKeys.SRC: str(dir1),
            CompareJsonKeys.TARGET: str(dir2),
            CompareJsonKeys.IS_CHANGE: False,
            CompareJsonKeys.INFO: [],
            CompareJsonKeys.TOTAL_ERROR: 0
        }
        total_errors = 0

        # Using method of Python to compare two folders
        compared = DirCmp(dir1, dir2)

        # If changed, compare bounding box
        is_changed = compared.left_only or compared.right_only or compared.diff_files or \
            compared.funny_files
        if is_changed:
            compare_result[CompareJsonKeys.IS_CHANGE] = True
            info = []

            # Path to tools (Cross platform)
            sys_str = platform.system()
            if sys_str.lower() == Platform.LINUX:  # If platform is Linux
                diff_tool = MekongProject.EXEC_SAIGON_LINUX_ABS
            elif sys_str.lower() == Platform.WINDOWS:  # If platform is Windows
                diff_tool = MekongProject.EXEC_SAIGON_WINDOWS_ABS
            else:  # If other platforms
                err_msg = "Platform {0} is not supported!".format(sys_str)
                raise Exception(err_msg)

            for common_file in compared.common_files:
                filename, file_extension = os.path.splitext(common_file)
                output_file = os.path.join(dir1, common_file)
                ref_file = os.path.join(dir2, common_file)
                if file_extension == CompareResultConfig.TXT_SUFFIX:
                    result_file = filename + "_" + postfix + CompareResultConfig.HTML_SUFFIX
                    option = os.path.join(result_folder, result_file)
                    compare_bb = {
                        CompareJsonKeys.TITLE: 'Compare bounding box',
                        CompareJsonKeys.SRC: str(output_file),
                        CompareJsonKeys.TARGET: str(ref_file),
                        CompareJsonKeys.IS_CHANGE: False,
                        CompareJsonKeys.TOTAL_ERROR: 0,
                        CompareJsonKeys.TOTAL_CHARACTER: 0,
                        CompareJsonKeys.HTML_PATH: ""
                    }
                    cmds = [diff_tool]
                    cmds += ['-bbcompare']
                    cmds += [output_file]
                    cmds += [ref_file]
                    cmds += ['-o']
                    cmds += [option]
                    diff_process = subprocess.Popen(cmds, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE, shell=False)
                    diff_stdout, diff_stderr = diff_process.communicate()
                    rc = diff_process.returncode
                    if rc != 0:
                        continue
                    if len(diff_stdout) > 0:
                        compare_bb[CompareJsonKeys.TOTAL_ERROR] = int(diff_stdout)
                        total_errors += int(diff_stdout)
                    cmds += ['-tc']
                    diff_process = subprocess.Popen(cmds, stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE, shell=False)
                    diff_stdout, diff_stderr = diff_process.communicate()
                    if len(diff_stdout) > 0:
                        compare_bb[CompareJsonKeys.TOTAL_CHARACTER] = int(diff_stdout)
                    compare_bb[CompareJsonKeys.HTML_PATH] = option
                    if not filecmp.cmp(output_file, ref_file):
                        compare_bb[CompareJsonKeys.IS_CHANGE] = True
                    info.append(compare_bb)

            for subdir in compared.common_dirs:
                compare_info = self.compare(os.path.join(dir1, subdir),
                                            os.path.join(dir2, subdir),
                                            result_folder,
                                            postfix)
                info.append(compare_info)
                total_errors += compare_info[CompareJsonKeys.TOTAL_ERROR]
            compare_result[CompareJsonKeys.INFO] = info
            compare_result[CompareJsonKeys.TOTAL_ERROR] = total_errors
        return compare_result


def parse_argument():
    parser = argparse.ArgumentParser(description='Compare folder including bounding box')
    parser.add_argument('-s', '--source',
                        help='Path to source folder',
                        required=True)
    parser.add_argument('-d', '--target',
                        help='Path to reference folder',
                        required=True)
    parser.add_argument('-o', '--output-folder',
                        help='Folder output that contains compare result',
                        required=True)
    return parser.parse_args()


def main():
    args = parse_argument()
    try:
        if not os.path.isdir(args.output_folder):
            os.makedirs(args.output_folder)

        # Initial compare runner and execute comparison
        runner = CompareFolderIncludingBoundingBox()
        compare_result = runner.compare(args.source, args.target, args.output_folder)
        print('Comparing result: ' + str(compare_result))

        # Export compare result to json file
        target_file = path.join(args.output_folder, CompareResultConfig.FILE_DEFAULT)
        write_json(compare_result, target_file)

    except:
        traceback.print_exc(file=sys.stdout)

###############################################################################
# Check name of module
if __name__ == "__main__":
    main()

# How to run:
# For ex: python Mekong/utilities/tests/lib_runner/compare_folder_including_bb.py
    #  -s ~/Desktop/test_set_Ubuntu10.04-32bit-1/0033_bmp_folder/output/linux/
    #  -d ~/Desktop/test_set_Ubuntu10.04-32bit-1/0033_bmp_folder/ref_data/linux/
    #  -o ~/Desktop/result
