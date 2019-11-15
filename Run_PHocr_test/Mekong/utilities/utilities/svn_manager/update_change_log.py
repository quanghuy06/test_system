import argparse
import os
import sys_path
sys_path.insert_sys_path()

from datetime import date
from handlers.parameters_handler import ParameterHandler
from manager.lib_distribution.filter_parser import *
from configs.database import FilterInterfaceConfig
from configs.commit_message import CommitMessage
from configs.svn_resource import SVNResource, DataPathSVN
from utils.svn_helper import SVNHelper

FILE_NAME_DEFAULT = "ChangeLog"


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--parameters', default="parameters.json",
                        required=True,
                        help="All parameter needed for master to"
                             " manage test nodes")
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
    parameter_handler = ParameterHandler(input_file=args.parameters)

    # Get delta version
    version = parameter_handler.get_delta_version()

    svn_resource = SVNResource()
    change_log_url = svn_resource.get_url(DataPathSVN.CHANGE_LOG)
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
    content = f.readlines()
    # Here, we prepend the string we want to on first line
    content.insert(0, all_contents)
    f.close()

    # We again open the file in WRITE mode
    f = open(change_log_file_path, "w")
    f.writelines(content)
    f.close()

    # Commit change log file to SVN
    cm_update_change_log = "Update change log. Add log of D{0}!".format(version)
    svn_helper.commit(cm_update_change_log, [change_log_file_path])


if __name__ == '__main__':
    main()



