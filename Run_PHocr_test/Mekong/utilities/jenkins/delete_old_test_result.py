# TOSHIBA - TSDV
# Team:             PHOcr
# Author:
# Email:
# Date create:
# Last update by:      Phung Dinh Tai
# Date:             01/10/2019
# Description:      This script is used to delete all build and test results from both of
#                   Engineering Test and Integration Test and only keep results of latest build
#                   on Integration Test when a change was merged into base line of project. This
#                   script should be run on master of jenkins where we store all results for jobs.
import os
import sys
import time
import argparse
import sys_path
sys_path.insert_sys_path()
from configs.jenkins import JenkinsHelper
from configs.json_key import JobName
from baseapi.file_access import remove_paths
from jenkins.lib_parsers.change_build_mapping_parser import ChangeBuildMappingParser


MANUAL = """
This script is used to delete all build and test results from both of Engineering Test and
Integration Test when a change was merged into base line of project. We only keep the latest
success build as reference. Note that there are some specific configuration for jenkins archive
directory, then this script should only be run on master node of jenkins in Post Integration.
"""


def parse_argument():
    parser = argparse.ArgumentParser(MANUAL)
    parser.add_argument('-g', '--gerrit-number',
                        required=True,
                        help='Change number to be removed data')
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_argument()

    # Calculate time for processes
    start_time = time.time()

    # Prepare configuration for deleting. Currently, we will remove all results from Engineering
    # Test and Integration Test of a change when it is merged to base line of project.
    list_job_name = [JobName.ET, JobName.IT]
    change_number = args.gerrit_number

    print("<SM> Deleting old results for jobs: {jobs_list}"
          "".format(jobs_list=", ".join(list_job_name)))

    # Return code when finish
    exit_code = 0

    for job_name in list_job_name:
        print("\n+ {job}".format(job=job_name))
        print("  Look into: {archive_dir}"
              "".format(archive_dir=os.path.join(JenkinsHelper.ARTIFACT_DIR, job_name)))
        # Get mapping file
        change_build_mapping_file = \
            JenkinsHelper.get_file_mapping(job_name=job_name,
                                           file_name=JenkinsHelper.CHANGE_BUILD_MAPPING_FILE)

        # Create data parser for change build mapping information
        data_parser = ChangeBuildMappingParser(mapping_file=change_build_mapping_file)

        # Get all build number correspond with change number
        list_build_number = list(data_parser.get_list_build(change_number=change_number))

        # For Integration Test, we need to keep the latest build/test result for reference later.
        if job_name == JobName.IT:
            latest_build = data_parser.get_latest_success_build(change_number=change_number)
            list_build_number.remove(latest_build)
            print("\tKeeping {build} in {job}".format(build=latest_build, job=job_name))

        if not list_build_number:
            print("\tWARN: There is no build for {job}!".format(job=job_name))
            exit_code = 1
            continue
        else:
            print("\tList build of {job} will be deleted: {build_list}"
                  "".format(job=job_name, build_list=", ".join(list_build_number)))

        # Go through all build in the list and do removal
        for build_number in list_build_number:
            # Get path to archive folder for build of the job
            archive_folder = os.path.join(JenkinsHelper.ARTIFACT_DIR, job_name, build_number)
            # Remove data of old build
            if os.path.exists(archive_folder):
                print("Removing {archive_folder}".format(archive_folder=archive_folder))
                remove_paths(archive_folder)
            else:
                # Notice use that result folder for build number does not exist or accidentally
                # removed
                print("\tWARN: Archive folder for build {build} of {job} does not exist or "
                      "accidentally removed by someone!".format(build=build_number, job=job_name))
                exit_code = 2

    # Calculate execution time
    print("\n<EM> Finished in: {execution_time}s".format(execution_time=time.time()-start_time))
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
