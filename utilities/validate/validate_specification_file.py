# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      09/01/2019
# Description:      Run script to validate a specification json file
import json
import sys
from argparse import ArgumentParser

import sys_path
from configs.database import TestcaseConfig

sys_path.insert_sys_path()
from database.lib_test_case.specification import Specification


def parse_arguments():
    """
    Handle arguments passed to run script

    Returns
    -------
    ArgumentParser

    """
    parser = ArgumentParser(
        description='Validate a specification file of a test case'
    )
    parser.add_argument('-f', '--file-path',
                        required=True,
                        help='Optional: Path to specification file of test '
                             'case which is in json format')
    return parser


def main():
    """
    Main

    """
    # Get parser argument object
    parser = parse_arguments()
    # Parse arguments
    args = parser.parse_args()

    # Print help
    if args.file_path is None:
        parser.print_help()
        sys.exit(1)
    with open(args.file_path) as f:
        spec_json = json.loads(f.read())

    spec = Specification(json_data=spec_json, required=True)
    spec.validate()
    spec.add_meta_field_to_error(
        TestcaseConfig.SPEC_FILE
    )
    spec.print_errors()


if __name__ == "__main__":
    main()
