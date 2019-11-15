# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      25/06/2018
# Description:      This python script is used update mapping a version of source code change
#                   with jenkins build which test for it.
import sys
import time
import argparse
import traceback
import sys_path
sys_path.insert_sys_path()
from jenkins.lib_parsers.change_build_mapping_parser import ChangeBuildMappingParser


MANUAL = """
This script update mapping between jenkins build jobs with change of gerrit. For a gerrit change,
developer can have multiple patch sets and a patch set can be tested by a jenkins build.
Currently, this information will be helpful in case if a change is merged then we need to know
location which stores data of latest success Integration Build to execute Post Integration test
to update data to database.
"""


def parse_argument():
    """
    Parse argument for run script.

    Returns
    -------
    ArgumentParser
        Arguments parser object

    """
    parser = argparse.ArgumentParser(MANUAL)
    parser.add_argument('-c', '--change-number',
                        required=True,
                        help="Change number on Gerrit to be updated data")
    parser.add_argument('-p', '--patch-set',
                        required=True,
                        help='Patch set version of the change to be updated data')
    parser.add_argument('-b', '--build-number',
                        required=True,
                        help='Build number of jenkins relate to change')
    parser.add_argument('-s', '--status',
                        required=True,
                        help='Status of jenkins build')
    parser.add_argument('-f', '--file',
                        required=True,
                        help='Path to mapping json file for gerrit changes and jenkins '
                             'build')
    return parser


def main():
    """
    Execute update information to mapping file or create new file if necessary

    Returns
    -------
    None

    """
    # Parse arguments
    parser = parse_argument()
    args = parser.parse_args()

    print("<SM> Update change-build mapping file")

    # Calculate execution time for processing
    start_time = time.time()

    # Return code when finish
    exit_code = 0

    try:
        # Create object to help update mapping file
        data_updater = ChangeBuildMappingParser(mapping_file=args.file)

        # Update information
        data_updater.update(change_number=args.change_number,
                            patch_set=args.patch_set,
                            build_number=args.build_number,
                            status=args.status)
    except:
        traceback.print_exc()
        print("WARN: Failed to update change build mapping file for the job!")
        exit_code = 1

    print("<EM> Finish in: {execution_time}s".format(execution_time=time.time()-start_time))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
