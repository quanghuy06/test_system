# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      18/04/2017
# Last update:      18/04/2107
# Description:      Script for overall information testing report
import argparse
import sys_path
sys_path.insert_sys_path()
from report.lib_summary_report.overall_information_reporter import OverallInformationReporter


def parse_arguments():
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test-folder', required=True,
                        help="Folder contains test cases")
    parser.add_argument('-r', '--test-file', required=True,
                        help="Test result file which is generated from run_all.py")
    parser.add_argument('-c', '--compare-file', required=True,
                        help="Compare result file which is generated from compare_all.py")
    parser.add_argument('-p', '--platform', required=True,
                        help='Platform to report')
    return parser


def main():
    parser = parse_arguments()
    args = parser.parse_args()

    # Initial reporter
    reporter = OverallInformationReporter(test_file=args.test_file, test_folder=args.test_folder,
                                          error_folder=None, compare_file=args.compare_file,
                                          platform=args.platform)

    # Do report
    reporter.do_work()


if __name__ == "__main__":
    main()