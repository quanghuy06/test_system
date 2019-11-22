# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      06/09/2019
# Description:      This script use for report memory peak of all test case
import argparse
import sys_path
sys_path.insert_sys_path()
from report.lib_memory_report.mem_peak_tsv_reporter import MemPeakTsvReporter


def parse_arguments():
    # Parsing arguments
    parser = argparse.ArgumentParser(description="Report memory peak of test "
                                                 "case")
    parser.add_argument("-t", "--test-folder", required=True,
                        help="Folder of OCR result generated from using "
                             "run_all.py script")
    parser.add_argument("-r", "--test-file", required=True,
                        help="Json file that is generated from executing "
                             "run_all.py script")
    parser.add_argument('-o', '--output-file',
                        help='Name of report and should be tsv format')
    return parser


def main():
    # Parse arguments
    parser = parse_arguments()
    args = parser.parse_args()

    # Initial reporter
    reporter = MemPeakTsvReporter(test_file=args.test_file,
                                  test_folder=args.test_folder)
    # Make report
    reporter.do_work()


if __name__ == "__main__":
    main()