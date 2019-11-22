# TOSHIBA - TSDV
# Team:             PHOcr
# Author:
# Email:
# Date create:
# Last update by:      Phung Dinh Tai
# Date:             02/10/2019
# Description:      This script is used to submit delta accuracy report to SVN in Post
#                   Integration when a change is merged into base line of project
import argparse
import sys
import time

import sys_path
sys_path.insert_sys_path()
from configs.common import SupportedPlatform, Platform
from svn_manager.defines import SVN
from svn_manager.lib_base.add_accuracy_to_svn_base import AddAccuracyToSVN
from report.lib_base.defines import ReportNames
from configs.jenkins import JenkinsHelper
from jenkins.lib_parsers.delta_version_projects_parser import DeltaVersionProjectsParser


MANUAL = """
This script should be called after delta accuracy report is generated in Post Integration where
delta accuracy report is placed in working directory. It will submit accuracy report to SVN for
the project.
"""


def parse_argument():
    """
    Parse arguments from command line

    Returns
    -------
    ArgumentParser
        Object allows us access arguments of the command line

    """
    parser = argparse.ArgumentParser(MANUAL)
    parser.add_argument('-p', '--project',
                        required=True,
                        help='Name of the project for reporting')
    return parser


def main():
    # Parser argument
    parser = parse_argument()
    args = parser.parse_args()

    print("<SM> Submit delta accuracy report to SVN")

    # Calculate time for processes
    start_time = time.time()

    # Create data parser for delta version of projects json file to extract current delta version
    # of project
    version_data_parser = \
        DeltaVersionProjectsParser(
            mapping_file=JenkinsHelper.get_path_delta_version_projects_file())

    # Get current delta version of the project
    current_delta_version = version_data_parser.get_delta_version(project=args.project)

    # Create object which help us submit data to SVN
    svn_accuracy_uploader = AddAccuracyToSVN()

    # Check status of submission
    submit_good = True

    # Return code when something wrong happens
    exit_code = 0

    for platform in SupportedPlatform:
        print("\n+ Submission on {platform}".format(platform=platform))

        # Get full name of report by suffix with delta version and platform of it
        delta_acc_report_file_name = \
            ReportNames.DELTA_ACCURACY.format(current_delta_version, platform)

        print("Report: {report}".format(report=delta_acc_report_file_name))

        if platform == Platform.LINUX:
            svn_accuracy_url = SVN.path.accuracy_linux_url
        else:
            svn_accuracy_url = SVN.path.accuracy_windows_url

        print("Target SVN url: {svn_url}".format(svn_url=svn_accuracy_url))

        submit_good = svn_accuracy_uploader.add_accuracy_report_to_svn(
            delta_acc_report_file_name, svn_accuracy_url
        )

        # Check status of submission
        if not submit_good:
            print("Status: FAIL")
            submit_good = False
        else:
            print("Status: OK")

    if not submit_good:
        print("WARN: Something wrong in submission delta accuracy to SVN")

    print("\n<EM> Finish in: {execution_time}s".format(execution_time=time.time() - start_time))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
