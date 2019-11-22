import argparse
import os
import time
import sys_path
sys_path.insert_sys_path()

from datetime import date
from handlers.parameters_handler import ParameterHandler
from manager.lib_distribution.filter_parser import *
from configs.database import FilterInterfaceConfig
from configs.commit_message import CommitMessage
from configs.svn_resource import SVNResource, DataPathSVN
from utils.svn_helper import SVNHelper
from configs.jenkins import JenkinsHelper
from configs.json_key import JobName
from jenkins.lib_parsers.change_build_mapping_parser import ChangeBuildMappingParser
from configs.test_result import FinalTestResult

FILE_NAME_DEFAULT = "ChangeLog"


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--parameters', default="parameters.json",
                        required=True,
                        help="All parameter needed for master to"
                             " manage test nodes")
    parser.add_argument('-g', '--gerrit-number',
                        required=True,
                        help='Change number to get parameter file')
    return parser


def replace_content(content, version):
    label = "[D" + str(version) + "]"
    import re
    pattern = "\n\n.*\[D"
    paragraph = re.split(pattern, content)
    for num, para in enumerate(paragraph, 1):
        lines = re.split("\n", para)
        for line in lines:
            filter_value = line.find(label)
            if filter_value == 0:
                content = content.replace(para + "\n\n", "")
                return 0, content
    return 1, content


def main():

    # Parse argument
    parse = parse_argument()
    args = parse.parse_args()
    start_time = time.time()
    change_number = args.gerrit_number

    print("<SM> Start update change log")
    # Get mapping file
    change_build_mapping_file = \
        JenkinsHelper.get_file_mapping(job_name=JobName.IT,
                                       file_name=JenkinsHelper.CHANGE_BUILD_MAPPING_FILE)

    # Create data parser for change build mapping information
    data_parser = ChangeBuildMappingParser(mapping_file=change_build_mapping_file)
    latest_build = data_parser.get_latest_success_build(change_number=change_number)

    # Path to archive folder on Jenkins server
    archive_folder = JenkinsHelper.get_archive_path(job_name=JobName.IT,
                                                    build_number=latest_build)
    parameter_file = os.path.join(archive_folder, FinalTestResult.INFO, args.parameters)

    parameter_handler = ParameterHandler(input_file=parameter_file)

    # Get delta version
    version = int(parameter_handler.get_delta_version()) + 1

    svn_resource = SVNResource()
    change_log_url = svn_resource.get_url(DataPathSVN.CHANGE_LOG)
    print("\n+ Change log url: {0}".format(change_log_url))
    change_log_local_path = os.path.join(os.getcwd(), DataPathSVN.CHANGE_LOG)
    svn_helper = SVNHelper(change_log_url, change_log_local_path)
    if not svn_helper.is_checkouted():
        svn_helper.checkout()
    svn_helper.update()

    # Parse commit message
    commit_message = parameter_handler.get_commit()
    filter_commit = parse_heading_message(commit_message)

    # Get main content of change log
    delta_summary = u" *{0}:".format(CommitMessage.SUMMARY) \
                    + unicode(filter_commit.encode('utf-8').strip(FilterInterfaceConfig.PHOCR_HEADER)) \
                    + u"\n"

    # Get commit date
    commit_date = date.today()
    delta_and_date = u"[D" + unicode(version) + u"]" + u" - " + unicode(commit_date) + "\n"
    delta_description = u" *{0}: \n".format(CommitMessage.DESCRIPTION) \
                        + parse_commit_message_contents_by_topic(CommitMessage.DESCRIPTION,
                                                                 commit_message)

    # Write content to change log file
    change_log_file_path = os.path.join(os.path.abspath(change_log_local_path),
                                        FILE_NAME_DEFAULT)
    all_contents = unicode(delta_and_date) \
                   + unicode(delta_summary) \
                   + unicode(delta_description)

    # Check if delta log is writen, delete old log
    f = open(change_log_file_path, "r+")
    content = f.read()
    num, content = replace_content(content, version)
    if num == 0:
        # Delete file content if it has current delta log
        f.truncate(0)
        f.close()
        # Write file content after delete current delta log
        f = open(change_log_file_path, "r+")
        f.write(content)
        f.close()
    else:
        f.close()

    f = open(change_log_file_path, "r")
    contents = list()
    for line in f.readlines():
        contents.append(unicode(line.decode('utf-8')))
    # Here, we prepend the string we want to on first line
    contents.insert(0, all_contents)
    f.close()

    # We again open the file in WRITE mode
    f = open(change_log_file_path, "wb")
    f.writelines([unicode(line).encode('utf-8') for line in contents])
    f.close()

    # Commit change log file to SVN
    cm_update_change_log = "Update change log. Add log of D{0}!".format(version)
    svn_helper.commit(cm_update_change_log, [change_log_file_path])

    # Calculate execution time
    print("\n<EM> Finished in: {execution_time}s".format(execution_time=time.time() - start_time))


if __name__ == '__main__':
    main()



