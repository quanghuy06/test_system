# TOSHIBA - TSDV
# Team:             PHOcr
# Author:
# Email:
# Date create:
# Last update by:      Phung Dinh Tai
# Date:             01/10/2019
# Description:      This script is used to prepare a build package for release in Post Integration
#                   Currently, we only need go to archive folder of latest success build of
#                   Integration Test to get build package and rename it suitable then copy
#                   package to archive folder of Post Integration build.
import os
import sys
import time
import pexpect
import argparse
import sys_path
sys_path.insert_sys_path()
from configs.jenkins import JenkinsHelper
from configs.common import SupportedPlatform
from configs.test_result import FinalTestResult, FinalResultsHelper
from baseapi.file_access import make_dir, copy_paths, move_paths
from configs.linux import GetLinuxCmd
from jenkins.lib_parsers.delta_version_projects_parser import DeltaVersionProjectsParser
from jenkins.lib_parsers.delta_change_mapping_parser import DeltaChangeMappingParser
from jenkins.lib_parsers.change_build_mapping_parser import ChangeBuildMappingParser


MANUAL = """
This script is used to prepare a build package for release in Post Integration. Currently,
we only need go to archive folder of latest success build of Integration Test to get build
package and rename it suitable then copy package to archive folder of Post Integration build.
This script need to be called after delta version of projects file was updated.
"""


def parse_argument():
    """
    Parse arguments from command line

    Returns
    -------
    ArgumentParser
        Object allows us to access arguments from command line

    """
    parser = argparse.ArgumentParser(MANUAL)
    parser.add_argument('-p', '--project',
                        required=True,
                        help='Name of project to be prepared release build package')
    parser.add_argument('-i', '--it-job-name',
                        required=True,
                        help='Name of Integration Test job for the project to get build package '
                             'of latest success build')
    parser.add_argument('-d', '--destination',
                        required=True,
                        help='Path to archive folder of current build of Post Integration to '
                             'store release build package')
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_argument()

    # Calculate time for processes
    start_time = time.time()

    # Return code when finish
    exit_code = 0

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
        job_name=args.it_job_name)

    # Create data parser for change-build mapping file to get latest success build of project in
    # Integration Test
    change_build_mapping_parser = ChangeBuildMappingParser(mapping_file=change_build_mapping_file)

    # Get build number of latest success build on Integration Test of the project
    latest_success_build = \
        change_build_mapping_parser.get_latest_success_build(
            change_number=change_number)

    print("<SM> Prepare build package for release")

    # Get path to archive folder of the latest build of Integration Test where store build
    # packages which suffix by change number and old base line
    latest_success_archive_folder = \
        JenkinsHelper.get_archive_path(job_name=args.it_job_name, build_number=latest_success_build)

    # Create if necessary archive folder of Post Integration to archive release build package of
    # new delta version of the project
    if not os.path.exists(args.destination):
        make_dir(args.destination)

    # Currently, for each test we have 2 build packages, one for normal testing which is built
    # with ICC, one for memory checking which is built with GCC. Both of these need to be
    # archived in Post Integration
    build_modes = [FinalResultsHelper.RELEASE_BUILD,
                   FinalResultsHelper.MEMORY_BUILD]

    for platform in SupportedPlatform:
        print("\n- Prepare build packages for platform {platform}".format(platform=platform))
        # Direct path to build archive folder - include build packages
        archive_latest_build_dir = \
            os.path.join(latest_success_archive_folder, platform, FinalTestResult.BUILD)

        # Check if archive folder of latest success build exists or not
        if not os.path.exists(archive_latest_build_dir):
            print("WARN: No such directory {archive_folder}".format(
                archive_folder=archive_latest_build_dir))
            exit_code = 1
            continue

        package_helper = FinalResultsHelper(project=args.project,
                                            baseline_version=int(current_delta_version)-1,
                                            change_number=change_number,
                                            patch_set=None,
                                            platform=platform)

        for build_mode in build_modes:
            # Prepare release build which built with ICC
            package_helper.build_mode = build_mode

            # Name of target build package for current delta version
            target_package_name = \
                package_helper.get_name_build_package_delta(delta_version=current_delta_version)

            print("\nArchive: {package}".format(package=target_package_name))

            # Name of old build package of latest success build
            old_release_build_package_path = os.path.join(
                archive_latest_build_dir, package_helper.get_name_build_package_change())

            if not os.path.exists(old_release_build_package_path):
                print("WARN: No such file {archive_package}".format(
                    archive_package=old_release_build_package_path))
                exit_code = 3
                continue

            # Copy release build package from archive folder of latest success build to current
            # working directory
            copy_paths(old_release_build_package_path, os.getcwd())

            # Extract build package
            pexpect.run(
                command=GetLinuxCmd.tar_extract(
                    package=package_helper.get_name_build_package_change()),
                timeout=300
            )

            # Name of build folder for the change after extracted
            build_folder_change = package_helper.get_name_build_folder_change()

            # Target name for release build folder of delta version
            build_folder_delta = \
                package_helper.get_name_build_folder_delta(delta_version=current_delta_version)

            # Change name of build folder for the change to target name for current delta version
            pexpect.run(
                command=GetLinuxCmd.rename(old_name=build_folder_change,
                                           new_name=build_folder_delta)
            )

            # Compress build folder for current delta version (after name changed)
            pexpect.run(
                command=GetLinuxCmd.tar_compress(package=target_package_name,
                                                 folder=build_folder_delta),
                timeout=300
            )

            # Move changed name build package for current delta version to destination archive
            # folder
            if not (os.path.abspath(args.destination) == os.getcwd()):
                move_paths(paths=target_package_name, des=args.destination)

            # Check if everything good
            target_build_package = os.path.join(args.destination, target_package_name)
            if not os.path.exists(target_build_package):
                print("WARN: Failed to get {target_package}".format(
                    target_package=target_package_name))
                exit_code = 2
            else:
                print("Successfully!")

    # Calculate execution time
    print("\n<EM> Finished in: {execution_time}s".format(execution_time=time.time()-start_time))
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
