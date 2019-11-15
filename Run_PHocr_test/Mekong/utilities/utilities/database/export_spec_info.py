# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Description:
import argparse
import sys_path
sys_path.insert_sys_path()
from database.lib_exporter.spec_info_exporter import SpecInfoExporter
from database.common.filters_control import add_args_parser, show_info, get_filters


def parse_arguments():
    # Parsing arguments
    parser = argparse.ArgumentParser(description="Export specification of test cases")
    add_args_parser(parser=parser)
    parser.add_argument('-o', '--output-file',
                        help='Name of report and should be tsv format')
    return parser


def main():
    # Parse arguments
    parser = parse_arguments()
    # Check if show information is ON
    show_info(parser)
    # Get arguments
    args = parser.parse_args()
    # Get filters
    filters = get_filters(parser)
    # Initial reporter
    exporter = SpecInfoExporter(filters=filters,
                                output_file=args.output_file)
    # Make report
    exporter.do_work()


if __name__ == "__main__":
    main()