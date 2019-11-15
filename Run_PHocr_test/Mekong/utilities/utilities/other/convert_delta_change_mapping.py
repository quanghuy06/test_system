# This script is used temporarily to convert old delta-change mapping to new style of
# delta-change mapping
# 02/10/2019

import argparse
import sys_path
sys_path.insert_sys_path()

from baseapi.file_access import read_json
from jenkins.lib_parsers.delta_change_mapping_parser import DeltaChangeMappingParser


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--delta-change-file',
                        required=True,
                        help='Path to delta change mapping file')
    parser.add_argument('-o', '--output-file',
                        required=True,
                        help='Path to output new delta-change mapping json file')
    return parser.parse_args()


def main():

    args = parse_argument()

    mapping_data = read_json(args.delta_change_file)

    data_parser = DeltaChangeMappingParser(mapping_file=args.output_file)

    for change_number in mapping_data:
        data_parser.update(delta_version=mapping_data[change_number], change_number=change_number)


if __name__ == "__main__":
    main()