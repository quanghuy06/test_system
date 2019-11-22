# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/07/2018
# Description:      This script is used on node master jenkins in automation test system to
#                   update reference data to MongoDB when gerrit trigger a changed merged event.
import os
import sys
import time
import argparse
import traceback
import sys_path
sys_path.insert_sys_path()
from configs.database import DbConfig
from manager.lib_post_it.jenkins_post_it_updater import JenkinsPostItUpdater
from configs.messages import TestSystemMessage
from jenkins.lib_parsers.delta_version_projects_parser import DeltaVersionProjectsParser
from jenkins.lib_parsers.delta_change_mapping_parser import DeltaChangeMappingParser
from jenkins.lib_parsers.change_build_mapping_parser import ChangeBuildMappingParser
from configs.jenkins import JenkinsHelper


MANUAL = """
This script is used to update test result of latest success build on Integration Test as new
reference data to Mekong database when a change was merged into base line. This script should be
executed after delta version of projects file was updated.
"""


def parse_arguments():
    """
    Parse arguments from command line

    Returns
    -------
    ArgumentParser
        Object allows us access to arguments input from command line

    """
    parser = argparse.ArgumentParser(description='Update data when a change is merged. This '
                                                 'script should be run on Jenkins master')
    parser.add_argument('-p', '--project',
                        required=True,
                        help='Name of project to get test results for reference')
    parser.add_argument('-j', "--job-name",
                        required=True,
                        help="Name of Integration Test of project")
    return parser


def main():
    # Parse arguments
    parser = parse_arguments()
    args = parser.parse_args()

    print("<SM> Update reference data to database when change merged in Post Integration")

    # Calculate execution time of processes
    start_time = time.time()

    exit_code = 0

    # Load configuration to get account to access Mekong database
    user, password = DbConfig.get_account_base_on_permission(is_readwrite=True)

    # Create data parser for delta version file of projects to get current delta version of the
    # requested project
    version_data_parser = \
        DeltaVersionProjectsParser(
            mapping_file=JenkinsHelper.get_path_delta_version_projects_file())

    # Get current delta version of requested project
    current_delta_version = version_data_parser.get_delta_version(project=args.project)

    # Create data parser for delta-change mapping of requested project
    delta_change_mapping_parser = \
        DeltaChangeMappingParser(
            mapping_file=JenkinsHelper.get_path_delta_change_mapping_file(project=args.project))

    # Get change number relates to current delta version of the project
    change_number = \
        delta_change_mapping_parser.get_change_number(
            delta_version=current_delta_version)

    # Path to change-build mapping file of Integration Test of the project
    change_build_mapping_file = JenkinsHelper.get_path_change_build_mapping_file(
        job_name=args.job_name)

    # Create data parser for change-build mapping file to get latest success build of project in
    # Integration Test
    change_build_mapping_parser = ChangeBuildMappingParser(mapping_file=change_build_mapping_file)

    # Get build number of latest success build on Integration Test of the project
    latest_success_build = \
        change_build_mapping_parser.get_latest_success_build(
            change_number=change_number)

    # Path to archive folder on Jenkins server
    archive_folder = JenkinsHelper.get_archive_path(job_name=args.job_name,
                                                    build_number=latest_success_build)

    # Check if archive folder does not exist then it can be accidentally removed by someone
    if not os.path.exists(archive_folder):
        print("WARN: No such directory {archive_folder}! It can be accidentally removed by "
              "someone!".format(archive_folder=archive_folder))
        print("\n<EM> Finish in: {execution_time}".format(execution_time=time.time()-start_time))
        sys.exit(1)

    # Create object to help update
    updater = JenkinsPostItUpdater(username=user,
                                   password=password,
                                   job_name=args.job_name,
                                   build_number=latest_success_build,
                                   delta_version=current_delta_version,
                                   change_number=change_number,
                                   archive_folder=archive_folder,
                                   log_enable=True)

    try:
        # Run update
        print("\n+ Update reference data and specification of test cases")
        updater.do_work()
        print("SUCCESSFULLY")

        # Add changed log for changed test cases.
        print("\n+ Update change log of test cases")
        changed_log_template = TestSystemMessage.TestCase.UPDATE
        changed_log = changed_log_template.format(current_delta_version)
        updater.add_changed_log_for_updated_test_cases(changed_log)
    except:
        exit_code = 2
        traceback.print_exc()
        print("WARN: Update FAILED")

    # Update data on SVN
    # NamLD:
    # Because only Hanoi here, therefore, disable for now
    # svn_updater = SVNPostItUpdater(args.job_name, args.build_number)
    # svn_updater.update()

    print("\n<EM> Finish in: {execution_time}s".format(execution_time=time.time()-start_time))
    sys.exit(exit_code)


if __name__ == "__main__" :
    main()
