# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Description:
import argparse
import sys
import sys_path
sys_path.insert_sys_path()
from database.lib_exporter.history_data_exporter import HistoryDataExporter
from database.common.filters_control import add_args_parser, show_info, get_filters
from report.lib_base.history_data_informer import HistoryDataConfiguration
from baseapi.common import get_list_defined_string


def parse_arguments():
    # Parsing arguments
    parser = argparse.ArgumentParser(description="Export specification of test cases")
    parser.add_argument('-d', '--product-report',
                        help='Req: Product to report data')
    parser.add_argument('-v', '--version',
                        help='Req: Delta version to report data')
    parser.add_argument('-e', '--platform',
                        help='Req: Platform to report data')
    add_args_parser(parser=parser)
    parser.add_argument('-o', '--output-file',
                        help='Name of report and should be tsv format')
    parser.add_argument('--list-product-data', default=False, action='store_true',
                        help='List all products in history data')
    return parser


def main():
    # Parse arguments
    parser = parse_arguments()
    args = parser.parse_args()
    # Check if show information is ON
    show_info(parser)
    # List product data
    if args.list_product_data:
        for product in get_list_defined_string(HistoryDataConfiguration.Product):
                print product
        sys.exit(0)
    # Get arguments
    args = parser.parse_args()
    # Get filters
    filters = get_filters(parser)
    # Initial reporter
    exporter = HistoryDataExporter(filters=filters,
                                   output_file=args.output_file, product=args.product_report,
                                   version=args.version, platform=args.platform)
    # Make report
    exporter.do_work()


if __name__ == "__main__":
    main()