# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      27/09/2019
# Description:      This python script is used to update information in delta version of projects
#                   file. This information is useful for us to get current delta version of base
#                   line of project to specify base line version for build/test results.
import sys
import time
import argparse
import traceback
import sys_path
sys_path.insert_sys_path()
from jenkins.lib_parsers.delta_version_projects_parser import DeltaVersionProjectsParser


MANUAL = """
This script update information of current delta version of projects. This information let us know
current base line of each project quickly to specify base line for build/test results. These
information should be updated when a change is integrated into base line of project or when data
information is out-date.
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
    parser.add_argument('-f', '--file',
                        required=True,
                        help='Path to json data file')
    parser.add_argument('-p', '--project',
                        required=True,
                        help='Name of project to update current delta version in '
                             'delta version of projects file.')
    parser.add_argument('-c', '--change-number',
                        help='Update delta version file when a change was merged. Check if the '
                             'change existing in delta-change mapping file first, only update '
                             'delta version file if change number was not in delta-change mapping')
    parser.add_argument('-d', '--delta-version',
                        help='OPTIONAL: Current delta version on base line of the project. This '
                             'is an optional, by default delta version of project is updated by'
                             'increasing current delta version by 1. This option useful to update'
                             'delta version of project when it out-date.')
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

    print("<SM> Update delta version projects file")

    # Calculate execution time for processing
    start_time = time.time()

    # Return code when finish
    exit_code = 0

    try:
        # Create object to help update mapping file
        data_updater = DeltaVersionProjectsParser(mapping_file=args.file)

        # Get current delta version of project
        current_delta_version = data_updater.get_delta_version(project=args.project)

        # Update information
        if args.delta_version:
            # Update specific version of the project
            data_updater.update(project=args.project, version=args.delta_version)
        else:
            # Check if the change existing in delta-change mapping of project first before
            # increasing current version of project by 1
            data_updater.change_merge(project=args.project, change_number=args.change_number)

        # Delta version of project after update
        updated_delta_version = data_updater.get_delta_version(project=args.project)

        print("Old delta version:     {old_version}".format(old_version=current_delta_version))
        print("Updated delta version: {new_version}".format(new_version=updated_delta_version))

    except:
        traceback.print_exc()
        print("WARN: Failed to update delta version of projects file!")
        exit_code = 1

    print("<EM> Finish in: {execution_time}s".format(execution_time=time.time()-start_time))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
