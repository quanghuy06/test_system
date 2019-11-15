# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      27/09/2019
# Description:      This python script is used update mapping file between delta version with
#                   change number of gerrit when a change is integrated into project line.
import sys
import time
import argparse
import traceback
import sys_path
sys_path.insert_sys_path()
from jenkins.lib_parsers.delta_change_mapping_parser import DeltaChangeMappingParser
from jenkins.lib_parsers.delta_version_projects_parser import DeltaVersionProjectsParser


MANUAL = """
This script update mapping between gerrit delta version with change number relates to it. If the
request change is already existing in mapping data, then it's a Post Integration re-triggered and
nothing need to be updated. If the request change does not exist then increase latest delta
version in mapping data by 1 and add the request change to mapping file.
This is also possible to update json file which presents current delta version of projects on
gerrit when you pass path to delta version file.
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
                        help="Change number on Gerrit which is integrated into project "
                             "base line")
    parser.add_argument('-f', '--file',
                        required=True,
                        help='Path to mapping json file for gerrit delta version and '
                             'gerrit change number relates to it')
    parser.add_argument('-d', '--delta-version',
                        help='OPTIONAL: Delta version corresponding to the change. This is useful'
                             'in case information in mapping file is out-date.')
    parser.add_argument('-v', '--versions-file',
                        help='OPTIONAL: Path to delta versions file which presents current delta '
                             'version of projects on gerrit')
    parser.add_argument('-p', '--project',
                        help='OPTIONAL: Name of project to update current delta version in '
                             'versions file.')
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

    print("<SM> Update delta-change mapping file")

    # Calculate execution time for processing
    start_time = time.time()

    # Return code when finish
    exit_code = 0

    try:
        # Create object to help update mapping file
        data_updater = DeltaChangeMappingParser(mapping_file=args.file)

        # Update information
        if args.delta_version:
            # Update when information is out-date. In this case delta version of projects file will
            # not be updated anyway.
            delta_version, change_number = data_updater.update(delta_version=args.delta_version,
                                                               change_number=args.change_number)
        else:
            # Update when a change is integrated into project base line
            delta_version, change_number = data_updater.change_merge(
                change_number=args.change_number)

            # Update delta version of projects file if required
            if args.versions_file and args.project:
                DeltaVersionProjectsParser.change_merge(project=args.project)
        # Log out update values
        print("+ Value updated:")
        print("Delta version: {version}".format(version=delta_version))
        print("Change number: {change}".format(change=change_number))
    except:
        traceback.print_exc()
        print("WARN: Failed to update delta change mapping file for the project!")
        exit_code = 1

    print("<EM> Finish in: {execution_time}s".format(execution_time=time.time()-start_time))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
