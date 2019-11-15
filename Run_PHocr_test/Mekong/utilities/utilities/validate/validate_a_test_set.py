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
import json

def parse_arguments():
    """
    Handle arguments passed to run script

    Returns
    -------
    ArgumentParser

    """
    parser = ArgumentParser(
        description='Validate a test set folder which contains multiple of '
                    'test case folders'
    )
    parser.add_argument('-f', '--test-set-folder',
                        help='Optional: Path to folder of test set')
    return parser


def main():
    """
    Main

    """
    # Get parser argument object
    parser = parse_arguments()
    # Parse arguments
    args = parser.parse_args()

    if args.test_set_folder is None:
        parser.print_help()
        sys.exit(1)

    # Check if exist folder
    if not os.path.isdir(args.test_set_folder):
        print(
            'No such directory "{directory}"'
            ''.format(directory=args.test_set_folder)
        )
        sys.exit(1)

    # Get list of test folders which need to be validated
    list_validation = list()
    for name in os.listdir(args.test_set_folder):
        data_path = \
            os.path.join(
                args.test_set_folder,
                name
            )
        list_validation.append(os.path.abspath(data_path))

    results = dict()
    for test_case_dir in list_validation:
        validator = MekongTestCase(test_case_dir)
        validator.validate()
        test_case_name = os.path.basename(test_case_dir)
        validator.add_meta_field_to_error(test_case_name)
        results[test_case_name] = validator.get_errors_in_dict()

    print(json.dumps(results, indent=4))


if __name__ == "__main__":
    main()
