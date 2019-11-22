# Toshiba - TSDV
# Team:         PHOcr
# Author:       Hoang Minh Phuc
# Email:        phuc.hoangminh@toshiba-tsdv.com
# Date created:     29/01/2017
# Last update:      06/07/2017
# Updated by:       Phung Dinh Tai
# Description:      This script define class for comparison of 2 bounding box layout files
import os
import argparse
import filecmp
import subprocess
import sys
import traceback
import platform
from configs.compare_result import CompareResultConfig, CompareJsonKeys
from configs.projects.mekong import MekongProject
from configs.common import Platform
from baseapi.file_access import write_json
from baseapi.common import specify_file_name


class CompareBoundingBox:

    def __init__(self, html_suffix=None, is_arabic=False):
        self.html_suffix = html_suffix
        self.is_arabic = is_arabic
        self.title = CompareResultConfig.TITLE_CMP_BB

    def compare(self, src_file, des_file, result_folder):
        # Check input
        if not os.path.exists(src_file):
            raise Exception("Path \"" + src_file + "\" is not exist")
        if not os.path.exists(des_file):
            raise Exception("Path \"" + des_file + "\" is not exist")

        """
        Compare bounding box using difftool
        """
        # Compare structure
        compare_result = {
            CompareJsonKeys.TITLE: 'Compare bounding box',
            CompareJsonKeys.IS_CHANGE: False,
            CompareJsonKeys.TOTAL_ERROR: 0,
            CompareJsonKeys.TOTAL_CHARACTER: 0,
            CompareJsonKeys.HTML_PATH: ""
        }
        # Separate path to file into path and base name
        src_file_path, src_base_name = os.path.split(src_file)
        des_file_path, des_base_name = os.path.split(des_file)

        # Get file name and file extension of base name
        src_file_name, src_file_extension = os.path.splitext(src_base_name)
        des_file_name, des_file_extension = os.path.splitext(des_base_name)

        if (src_file_extension != CompareResultConfig.TXT_SUFFIX) or \
                (des_file_extension != CompareResultConfig.TXT_SUFFIX):
            raise ValueError("Source file or dest file is not .txt format!")

        # Path to tools (Cross platform)
        sys_str = platform.system()
        if sys_str.lower() == Platform.LINUX:  # If platform is Linux
            diff_tool = MekongProject.EXEC_SAIGON_LINUX_ABS
        elif sys_str.lower() == Platform.WINDOWS:  # If platform is Windows
            diff_tool = MekongProject.EXEC_SAIGON_WINDOWS_ABS
        else:  # If other platforms
            raise Exception("Platform {0} is not supported!".format(sys_str))

        # Execute comparison
        try:
            result_file = des_file_name + CompareResultConfig.HTML_SUFFIX
            if self.html_suffix:
                result_file = specify_file_name(result_file, self.html_suffix)
            output_file = str(src_file)
            ref_file = str(des_file)
            if not os.path.exists(result_folder):
                os.makedirs(result_folder)
            option = os.path.join(result_folder, result_file)
            cmd = [diff_tool]
            cmd += ['-bbcompare']
            cmd += [output_file]
            cmd += [ref_file]
            if self.is_arabic:
                cmd += ['--arabic']
            cmd += ['-o']
            cmd += [option]
            diff_process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, shell=False)
            diff_stdout, diff_stderr = diff_process.communicate()
            rc = diff_process.returncode
            if rc != 0:
                print diff_stderr
                raise Exception("Can not compare bounding box")
            if len(diff_stdout) > 0:
                compare_result[CompareJsonKeys.TOTAL_ERROR] = int(diff_stdout)

            # Get detail errors and total characters
            cmd += ['-v']
            diff_process = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE, shell=False)
            diff_stdout, diff_stderr = diff_process.communicate()
            if len(diff_stdout) > 0:
                details = diff_stdout.split(",")
                compare_result[CompareJsonKeys.INSERT_ERR] = int(details[0])
                compare_result[CompareJsonKeys.DELETE_ERR] = int(details[1])
                compare_result[CompareJsonKeys.REPLACE_ERR] = int(details[2])
                compare_result[CompareJsonKeys.TOTAL_CHARACTER] = int(details[3])
            compare_result[CompareJsonKeys.HTML_PATH] = option
            if int(compare_result[CompareJsonKeys.TOTAL_ERROR]) > 0:
                compare_result[CompareJsonKeys.IS_CHANGE] = True
        except:
            traceback.print_exc()

        return compare_result


def parse_argument():
    parser = argparse.ArgumentParser(description='Compare bounding box')
    parser.add_argument('-s', '--source-file',
                        help='Path to source file',
                        required=True)
    parser.add_argument('-d', '--target-file',
                        help='Path to target file',
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

        # Init compare runner and execute comparison
        runner = CompareBoundingBox()
        compare_result = runner.compare(args.source_file, args.target_file,
                                        args.output_folder)
        print('Comparing result: ' + str(compare_result))

        # Export compare result to json file
        target_file = os.path.join(args.output_folder,
                                   CompareResultConfig.FILE_DEFAULT)
        write_json(compare_result, target_file)

    except:
        traceback.print_exc(file=sys.stdout)

if __name__ == "__main__":
    main()

# How to run:
# For ex: python Mekong/utilities/tests/lib_runner/compare_bounding_box.py
    #  -s ~/Desktop/test_set_Ubuntu10.04-32bit-1/0033_bmp_folder/output/linux/0033.txt
    #  -d ~/Desktop/test_set_Ubuntu10.04-32bit-1/0033_bmp_folder/ref_data/linux/0033.txt
    #  -o ~/Desktop/result
