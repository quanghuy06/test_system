# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      10/09/2019
# Description:      This script used for report memory peak.
import argparse
import sys_path
sys_path.insert_sys_path()
from report.lib_summary_report.memory_peak_reporter import MemPeakReporter


def parse_arguments():
    # Parsing arguments
    parser = argparse.ArgumentParser(
        description="Export accuracy report of PHOcr product.")
    parser.add_argument("-t", "--test-folder", required=True,
                        help="folder of OCR result generated from using "
                             "run_all.py script")
    parser.add_argument("-r", "--test-file", required=True,
                        help="Json file that is generated from executing "
                             "run_all.py script")
    parser.add_argument('-n', "--change-number",
                        help="Change number, should prefix such as C<number>")
    parser.add_argument('-d', "--delta-version",
                        help="Delta version of base line, should prefix such "
                             "as D<number>")
    parser.add_argument('-p', "--platform",
                        help="Platform of testing")
    parser.add_argument('-o', '--output-file',
                        help='Name of report and should be xlsx format')
    return parser


def main():
    # Parse arguments
    parser = parse_arguments()
    args = parser.parse_args()

    if args.change_number:
        change_number = int(args.change_number)
    else:
        change_number = None

    if args.delta_version:
        delta = int(args.delta_version)
    else:
        delta = None

    # Initial reporter
    reporter = MemPeakReporter(test_file=args.test_file,
                               test_folder=args.test_folder,
                               change_number=change_number,
                               delta=delta,
                               platform=args.platform)
    # Make report
    reporter.do_work()


if __name__ == "__main__":
    main()