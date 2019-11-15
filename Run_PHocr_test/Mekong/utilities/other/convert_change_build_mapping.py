# This script is used temporarily to convert old change-build mapping to new style of
# change-build mapping
# 01/10/2019

import argparse
import sys_path
sys_path.insert_sys_path()

from baseapi.file_access import read_json
from jenkins.lib_parsers.change_build_mapping_parser import ChangeBuildMappingParser


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--change-mapping-file',
                        required=True,
                        help='Path to change build mapping file')
    parser.add_argument('-o', '--output-file',
                        required=True,
                        help='Path to output new change build mapping json file')
    return parser.parse_args()


def main():

    args = parse_argument()

    mapping_data = read_json(args.change_mapping_file)

    data_parser = ChangeBuildMappingParser(mapping_file=args.output_file)

    for change_number in mapping_data:
        build_list = mapping_data[change_number]
        for build_number in build_list:
            data_parser.update(change_number=change_number, patch_set=1,
                               build_number=build_number,
                               status=ChangeBuildMappingParser.STATUS_SUCCESS)


if __name__ == "__main__":
    main()