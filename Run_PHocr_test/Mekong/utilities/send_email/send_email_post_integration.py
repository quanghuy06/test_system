# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      27/09/2019
# Description:      This python script is used to update information in delta version of projects
#                   file. This information is useful for us to get current delta version of base
#                   line of project to specify base line version for build/test results.
import argparse
import os
import sys
import time
import fnmatch
import sys_path
sys_path.insert_sys_path()
from send_email.SMTPEmail import EmailSender
from configs.projects.mekong import TestSystem
from configs.test_result import FinalTestResult
from configs.json_key import ParametersJson
from handlers.parameters_handler import ParameterHandler
from manager.lib_distribution.filter_parser import *
from configs.common import Platform
from configs.commit_message import CommitMessage
from baseapi.file_access import suffix_file
from baseapi.file_access import read_json, copy_paths
from configs.jenkins import JenkinsHelper
from jenkins.lib_parsers.delta_version_projects_parser import DeltaVersionProjectsParser
from jenkins.lib_parsers.delta_change_mapping_parser import DeltaChangeMappingParser
from jenkins.lib_parsers.change_build_mapping_parser import ChangeBuildMappingParser

MANUAL = """
This script help us send email with accuracy and performance reports attached in Post Integration
"""


def parse_argument():
    """
    Parse arguments list from executing script

    Returns
    -------
    ArgumentParser
        Object which allow us access to arguments of running script

    """
    parser = argparse.ArgumentParser(MANUAL)
    parser.add_argument('-p', '--project',
                        required=True,
                        help='Name of project to report')
    parser.add_argument('-j', '--job-name',
                        required=True,
                        help='Name of jenkins job for Integration Test of the project')
    return parser


def main():
    # Parse arguments from command line
    parser = parse_argument()
    args = parser.parse_args()

    print("<SM> Send email for reporting in Post Integration Test")

    # Calculate execution time of the processes
    start_time = time.time()

    # Create data parser to extract information from delta version file of projects to get
    # current delta version for requested project.
    version_data_parser = \
        DeltaVersionProjectsParser(
            mapping_file=JenkinsHelper.get_path_delta_version_projects_file())

    # Get latest build number for integration test of the change to get accuracy report
    current_delta_version = version_data_parser.get_delta_version(project=args.project)
    # Check if has no information about current delta version then warning and return
    if current_delta_version == "0":
        print("WARN: There is no information for current delta version of the project on Jenkins!")
        print("\n<EM> Finish in: {execution_time}s".format(execution_time=time.time() - start_time))
        sys.exit(1)
    # Log information of project
    print("\n+ Project:       {project}".format(project=args.project))
    print("+ Delta version: {version}".format(version=current_delta_version))

    # Create data parser to extract information from delta-change mapping file to get change
    # number which relates to current delta version of the project
    delta_change_mapping_parser = DeltaChangeMappingParser(
        mapping_file=JenkinsHelper.get_path_delta_change_mapping_file(project=args.project))

    # Get change number which relates to current delta version of project
    change_number = \
        delta_change_mapping_parser.get_change_number(delta_version=current_delta_version)

    # Create data parser to extract information from change-build mapping file of job to get
    # latest success build number of the change then get accuracy report for attachment
    change_build_mapping_parser = \
        ChangeBuildMappingParser(
            mapping_file=JenkinsHelper.get_path_change_build_mapping_file(job_name=args.job_name))

    # Get latest success build the change of current delta version
    latest_success_build_number = \
        change_build_mapping_parser.get_latest_success_build(change_number=change_number)

    # Get path to reports in archives folder of Jenkins
    archive_folder = JenkinsHelper.get_archive_path(job_name=args.job_name,
                                                    build_number=latest_success_build_number)

    # Check if there is no archive folder for latest success build then results is already be
    # removed by accidents then warning and return
    if not os.path.exists(archive_folder):
        print("WARN: Archive results folder was accidentally removed by someone!")
        print("\n<EM> Finish in: {execution_time}s".format(execution_time=time.time() - start_time))
        sys.exit(2)

    # Path to folder includes report of the latest success build of the change
    report_folder = os.path.join(archive_folder, Platform.LINUX, FinalTestResult.REPORT)

    # Notice that for the latest build of the change, the change was not merged into base line of
    # project then it based on previous delta version and all report at that time has suffix
    # <change number>_<previous delta version>
    suffix = "C{change}_D{delta}".format(change=change_number, delta=int(current_delta_version)-1)

    # Name of memory peak report at that time
    memory_peak_report_name = suffix_file(file_name=FinalTestResult.FILE_REPORT_MEMORY_PEAK,
                                          suffix=suffix)

    # Full path to memory peak report of the latest success build
    memory_peak_report_path = os.path.join(report_folder, memory_peak_report_name)

    # Copy memory peak report to current working directory to prepare attachment
    copy_paths(memory_peak_report_path, os.getcwd())

    # Path to parameters file
    parameters_file = os.path.join(archive_folder, FinalTestResult.INFO,
                                   ParametersJson.DEFAULT_NAME)

    # Load configuration of sending email in Post Integration
    configuration = read_json(TestSystem.Paths.SEND_EMAIL_CONFIGURE)
    list_to_address = configuration["to_address"]
    list_cc_address = configuration["cc_address"]
    list_file_send = configuration["list_file_send"]
    subject = configuration["subject"]
    message = configuration["message"]

    # Prepare attachments
    attachments = list()
    for f_name in os.listdir(os.getcwd()):
        f_name = convert_to_unicode(f_name)
        for item in list_file_send:
            if fnmatch.fnmatch(f_name, item):
                attachments.append(f_name.encode('utf-8'))

    # Create data parser for parameters file to extract commit message for description of problem
    parameters_handler = ParameterHandler(input_file=parameters_file)

    # Extract commit message to prepare content of email
    commit_message = parameters_handler.get_commit()

    # Get title of the change
    summary = parse_commit_message_contents_by_topic(
        CommitMessage.SUMMARY,
        commit_message
    )
    if summary:
        message += u"\n\n" \
                   + unicode(CommitMessage.SUMMARY) \
                   + u"\n" \
                   + summary

    # Extract detail description of commit message
    description = parse_commit_message_contents_by_topic(
        CommitMessage.DESCRIPTION,
        commit_message)
    if description:
        message += unicode(CommitMessage.DESCRIPTION) \
                   + u"\n"\
                   + description

    # Make sure message in Unicode to present all characters correctly
    message = convert_to_unicode(message)

    # Prepare subject of the email
    subject = subject + current_delta_version
    subject = convert_to_unicode(subject)

    # Sent to addresses
    to_addresses = ",".join(list_to_address)
    to_addresses = convert_to_unicode(to_addresses)

    # CC addresses
    cc_addresses = ",".join(list_cc_address)
    cc_addresses = convert_to_unicode(cc_addresses)

    # Ready to send
    print("Sending email ...")
    EmailSender.send(to_addresses, cc_addresses, subject, message, attachments)

    # Finish
    print("\n<EM> Finish in: {execution_time}s".format(execution_time=time.time()-start_time))
    sys.exit(0)


if __name__ == "__main__":
    main()
