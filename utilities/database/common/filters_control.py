# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Description:
import sys
from configs.database import SpecKeys, SpecHelper


def add_args_parser(parser):
    parser.add_argument('-id', '--test-case-id',
                        help='Query by test case id, support multiple test cases')
    parser.add_argument('-q', '--query',
                        help='Query test cases by query json in file')
    parser.add_argument('-pro', '--product',
                        help='Query by product')
    parser.add_argument('-c', '--component',
                        help='Query by component')
    parser.add_argument('-f', '--functions',
                        help='Query by function')
    parser.add_argument('-t', '--tags',
                        help='Query by tags')
    parser.add_argument('--list-products', default=False, action='store_true',
                        help="List all of available products")
    parser.add_argument('--list-components', default=False, action='store_true',
                        help="List all of available components")
    parser.add_argument('--list-functions', default=False, action='store_true',
                        help="List all of available functions")
    parser.add_argument('--list-tags', default=False, action='store_true',
                        help="List all of available tags")


def get_filters(parser):
    args = parser.parse_args()
    # create filters from user input
    filters = {}

    if args.test_case_id:
        filters[SpecKeys.ID] = args.test_case_id

    if args.product:
        filters[SpecKeys.PRODUCT] = args.product

    if args.component:
        filters[SpecKeys.COMPONENT] = args.component

    if args.functions:
        filters[SpecKeys.FUNCTIONALITIES] = args.functions

    if args.tags:
        filters[SpecKeys.TAGS] = args.tags

    return filters


def show_info(parser):
    args = parser.parse_args()
    # Helper
    db_helper = SpecHelper()
    if args.list_products:
        db_helper.list_product()
        sys.exit(0)

    if args.list_components:
        db_helper.list_component()
        sys.exit(0)

    if args.list_functions:
        db_helper.list_functionality()
        sys.exit(0)

    if args.list_tags:
        db_helper.list_tags()
        sys.exit(0)
