# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/04/2017
# Last update:      18/04/2107
# Description:      Script for barcode functionality testing report
import argparse
import sys_path
sys_path.insert_sys_path()
from report.lib_summary_report.barcode_accuracy_reporter import BarcodeAccuracyReporter


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--test-file', required=True,
                        help="Test result file which is generated from run_all.py")
    parser.add_argument('-c', '--compare-file', required=True,
                        help="Compare result file which is generated from compare_all.py")
    parser.add_argument('-t', '--test-folder', required=True,
                        help="Test folder which is required to read specification of test cases")
    parser.add_argument('-o', '--output',
                        help='Output file name')
    args = parser.parse_args()

    # Initial reporter
    barcode_reporter = BarcodeAccuracyReporter(test_file=args.test_file,
                                               compare_file=args.compare_file,
                                               test_folder=args.test_folder,
                                               output_file=args.output)

    # Do report
    barcode_reporter.do_work()

if __name__ == "__main__":
    main()
