# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/01/2019
# Description:      Run script to validate a test case folder
import sys
import os
from argparse import ArgumentParser

import sys_path
sys_path.insert_sys_path()
from database.lib_test_case.mekong_test_case import MekongTestCase


def parse_arguments():
    """
    Handle arguments passed to run script

    Returns
    -------
    ArgumentParser

    """
    parser = ArgumentParser(
        description='Validate a test case folder'
    )
    parser.add_argument('-f', '--test-case-folder',
                        help='Optional: Path to folder of test case')
    return parser


def main():
    """
    Main

    """
    # Get parser argument object
    parser = parse_arguments()
    # Parse arguments
    args = parser.parse_args()

    test_case_dir = args.test_case_folder

    if test_case_dir is None:
        parser.print_help()
        sys.exit(1)

    # Initial validator
    validator = MekongTestCase(args.test_case_folder)
    # Set value for validation
    validator.validate()

    test_case_name = os.path.basename(test_case_dir)
    validator.add_meta_field_to_error(test_case_name)
    # Show the status of validation
    validator.print_errors()


if __name__ == "__main__":
    main()
