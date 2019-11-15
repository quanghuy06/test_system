# Toshiba - TSDV
# Team:         PHOcr
# Author:       Hoang Minh Phuc
# Email:        phuc.hoangminh@toshiba-tsdv.com
# Date created:     29/01/2017
# Last update:      29/06/2017
# Updated by:       Phung Dinh Tai
# Description:      This script define class for text comparison
import os
import argparse
import filecmp
import json
import subprocess
import sys
import traceback
import platform
from os import path
from configs.compare_result import CompareJsonKeys, CompareResultConfig
from configs.common import Platform
from configs.projects.mekong import MekongProject


class CompareTextFile:

    def __init__(self, is_arabic=False):
        self.title = CompareResultConfig.TITLE_CMP_TEXT
        self.is_arabic = is_arabic

    def compare(self, src_file, des_file, result_folder):
        # Check input
        if not os.path.exists(src_file):
            raise Exception("Path \"" + src_file + "\" is not exist")
        if not os.path.exists(des_file):
            raise Exception("Path \"" + des_file + "\" is not exist")
        if not os.path.exists(result_folder):
            raise Exception("Path \"" + result_folder + "\" is not exist")

        """
        Compare text file using diff tool
        """
        # Compare structure
        compare_result = {
            CompareJsonKeys.TITLE: 'Compare text file',
            CompareJsonKeys.IS_CHANGE: False,
            CompareJsonKeys.HTML_PATH: ""
        }

        # Separate path to file into path and base name
        src_file_path, src_base_name = os.path.split(src_file)
        des_file_path, des_base_name = os.path.split(des_file)

        # Get file name and file extension of base name
        src_file_name, src_file_extension = os.path.splitext(src_base_name)
        des_file_name, dest_file_extension = os.path.splitext(des_base_name)

        if (src_file_extension != CompareResultConfig.TXT_SUFFIX) or \
                (dest_file_extension != CompareResultConfig.TXT_SUFFIX):
            raise ValueError("Source file or dest file is not .txt format!")

        # Path to tools (Cross platform)
        sys_str = platform.system()
        if sys_str.lower() == Platform.LINUX:  # If platform is Linux
            diff_tool = MekongProject.EXEC_SAIGON_LINUX_ABS
        elif sys_str == Platform.WINDOWS:  # If platform is Windows
            diff_tool = MekongProject.EXEC_SAIGON_WINDOWS_ABS
        else:  # If other platforms
            raise Exception("Platform {0} is not supported!".format(sys_str))

        # Execute
        try:
            result_file = des_file_name + CompareResultConfig.HTML_SUFFIX
            output_file = str(src_file)
            ref_file = str(des_file)
            if not os.path.exists(result_folder):
                os.makedirs(result_folder)
            option = os.path.join(result_folder, result_file)
            cmd = [diff_tool]
            cmd += [output_file]
            cmd += [ref_file]
            if self.is_arabic:
                cmd += ['--arabic']
            cmd += ['-o']
            cmd += [option]
            diff_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                            shell=False)
            diff_stdout, diff_stderr = diff_process.communicate()
            if len(diff_stdout) > 0:
                details = diff_stdout.split(",")
                compare_result[CompareJsonKeys.TOTAL_ERROR] = int(details[0])
                compare_result[CompareJsonKeys.TOTAL_CHARACTER] = int(details[1])
            rc = diff_process.returncode
            if rc != 0:
                raise Exception("Can not compare text file")
            if not filecmp.cmp(src_file, des_file):
                compare_result[CompareJsonKeys.IS_CHANGE] = True
            compare_result[CompareJsonKeys.HTML_PATH] = option
        except Exception as e:
            raise e
        return compare_result


###############################################################################
# Parsing arguments
def parse_argument():
    parser = argparse.ArgumentParser(description='Compare text file')
    parser.add_argument('-s', '--source',
                        help='Path to source file',
                        required=True)
    parser.add_argument('-d', '--target',
                        help='Path to reference file',
                        required=True)
    parser.add_argument('-o', '--output-folder',
                        help='Folder output that contains compare result',
                        required=True)
    return parser.parse_args()


###############################################################################
# Main function
def main():
    args = parse_argument()
    try:
        run = CompareTextFile()
        if not os.path.exists(args.result_folder):
            os.makedirs(args.result_folder)
        compare_result = run.compare(args.src, args.dest, args.result_folder)
        print('Comparing result: ' + str(compare_result))
        result_file = path.join(args.result_folder, CompareResultConfig.FILE_DEFAULT)
        if os.path.exists(result_file):
            os.remove(result_file)
        with open(result_file, 'w+') as f:
            f.write(json.dumps(compare_result, indent=4, sort_keys=True))
    except:
        traceback.print_exc(file=sys.stdout)

###############################################################################
# Check name of module
if __name__ == "__main__":
    main()

# How to run:
# For ex: python Mekong/utilities/tests/lib_runner/compare_text_file.py -s
    # ~/Desktop/test_set_Ubuntu10.04-32bit-1/0033_bmp_folder/output/linux/0033.txt -d
    # ~/Desktop/test_set_Ubuntu10.04-32bit-1/0033_bmp_folder/ref_data/linux/0033.txt -o
    # ~/Desktop/result
