# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Le Duc Nam
# Email:            nam.leduc@toshiba-tsdv.com
# Date create:      10/10/2017
# Last update:      18/07/2018
# Editor:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Description:      This script used to generate xml junit file from test result and compare
# result file in json format
import argparse
import sys_path
sys_path.insert_sys_path()
from report.lib_summary_report.junit_xml_reporter import JunitXmlReporter


# Parsing arguments
def parse_argument():
    parser = argparse.ArgumentParser(description='Export junit xml format from test and compare result file')
    parser.add_argument('-r', '--test-file', required = True,
                        help='Test result file which is generated from run_all.py')
    parser.add_argument('-c', '--compare-file', required = True,
                        help='Compare result file which is generated from compare.py')
    parser.add_argument('-o', '--output',
                        help='Output junit xml file')

    return parser.parse_args()


def main():
    args = parse_argument()

    # Create handlers for test and compare result
    exporter = JunitXmlReporter(test_file=args.test_file, compare_file=args.compare_file,
                                output_file=args.output)
    # Write file
    exporter.do_work()

if __name__ == "__main__":
    main()
