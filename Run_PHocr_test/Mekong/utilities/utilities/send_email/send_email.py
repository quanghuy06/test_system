#!/usr/bin/env python
import sys_path
sys_path.insert_sys_path()
import argparse
import os
import sys
import json
import shutil
import fnmatch
from SMTPEmail import EmailSender
from configs.projects.mekong import TestSystem
from configs.jenkins import JenkinsHelper
from configs.test_result import FinalTestResult
from configs.json_key import ParametersJson
from handlers.parameters_handler import ParameterHandler
from manager.lib_distribution.filter_parser import *
from configs.common import Platform, SupportedPlatform
from configs.commit_message import CommitMessage
from report.lib_delta_report.phocr_delta_performance_reporter import PHOcrDeltaPerformanceReporter
from report.lib_delta_report.phocr_delta_accuracy_reporter import PHOcrDeltaAccuracyReporter
from baseapi.file_access import suffix_file


def parse_argument():
    parser = argparse.ArgumentParser(
        description='Auto send report through email.'
                    'Please edit configure in the same path with script'
                    'and send_report_config.json on config/default/ before run the script')
    parser.add_argument('-a', '--to_address',
                        help='Receiver email address ')
    parser.add_argument('-c', '--cc-address',
                        help='Cc email address ')
    parser.add_argument('-s', '--subject',
                        help='Email subject')
    parser.add_argument('-m', '--message',
                        help='Email content : message')
    parser.add_argument('-at', '--attachment-file',
                        help='List of attachment file')
    parser.add_argument("--post-jenkins", default=False, action="store_true",
                        help='Send email with default information')
    parser.add_argument("--report", default=False, action="store_true",
                        help="Run report scripts and send reports")
    parser.add_argument('-j', "--job-name",
                        help="Jenkins job name")
    parser.add_argument('-b', "--build-number",
                        help="Jenkins build number will contain reference data")
    parser.add_argument('-p', '--parameters', default="parameters.json",
                        help="All parameter needed for master to"
                             " manage test nodes")
    return parser.parse_args()


def run_report():
    # Report time performance and accuracy
    print "Reporting time performance and accuracy ..."
    for platform in SupportedPlatform:
        # Report time performance
        per_reporter = PHOcrDeltaPerformanceReporter(platform=platform)
        per_reporter.do_work()
        # Report accuracy
        acc_reporter = PHOcrDeltaAccuracyReporter(platform=platform)
        acc_reporter.do_work()


def send_email_extra(list_to_address, list_cc_address, subject, message, list_file_send, work_dir):
    # Get list attachment
    list_attachment = []
    for fname in os.listdir(work_dir):
        fname = convert_to_unicode(fname)
        for item in list_file_send:
            if fnmatch.fnmatch(fname, item):
                list_attachment.append(fname.encode('utf-8'))

    # Get list receiver address  and Cc address
    to_add = ""
    cc_add = ""
    to_address = ""
    cc_address = ""
    for item in list_to_address:
        to_add = to_add + item + ","
        to_address = to_add[:-1]
    for cc in list_cc_address:
        cc_add = cc_add + cc + ","
        cc_address = cc_add[:-1]
    to_address = convert_to_unicode(to_address)
    cc_address = convert_to_unicode(cc_address)
    subject = convert_to_unicode(subject)
    message = convert_to_unicode(message)
    # Send email
    print "Sending email ..."
    EmailSender.send(to_address, cc_address, subject, message, list_attachment)


def main():
    args = parse_argument()
    build_number = args.build_number
    job_name = args.job_name
    current_dir = os.getcwd()
    data = json.load(open(TestSystem.Paths.SEND_EMAIL_CONFIGURE))
    list_to_address = data["to_address"]
    list_cc_address = data["cc_address"]
    list_file_send = data["list_file_send"]
    subject = data["subject"]
    message = data["message"]
    # UC1: Send reports on Jenkins post integration
    if args.post_jenkins:
        if build_number and job_name:
            archive_folder = JenkinsHelper.get_archive_path(job_name, build_number)
            linux_folder = os.path.join(archive_folder, Platform.LINUX)
            report_folder = os.path.join(linux_folder, FinalTestResult.REPORT)
            info_folder = os.path.join(archive_folder, FinalTestResult.INFO)
            parameter_file = os.path.join(info_folder, ParametersJson.DEFAULT_NAME)
            # Get change number and current delta
            parameter_handler = ParameterHandler(input_file=parameter_file)
            change_number = str(parameter_handler.get_change_number())
            current_delta = int(parameter_handler.get_delta_version())
            suffix = "C{0}_D{1}".format(change_number, str(current_delta))
            mem_peak_report_file = suffix_file(
                FinalTestResult.FILE_REPORT_MEMORY_PEAK, suffix)
            memory_peak_report_path = os.path.join(report_folder,
                                                mem_peak_report_file)

            # Copy text accuracy file to current folder
            shutil.copyfile(memory_peak_report_path,
                            os.path.join(current_dir, mem_peak_report_file))
            # Get description of change from commit message
            commit_message = parameter_handler.get_commit()
            summary = parse_commit_message_contents_by_topic(
                CommitMessage.SUMMARY,
                commit_message
            )
            if summary:
                message += u"\n\n" \
                           + unicode(CommitMessage.SUMMARY) \
                           + u"\n" \
                           + summary
            description = parse_commit_message_contents_by_topic(
                CommitMessage.DESCRIPTION,
                commit_message)
            if description:
                message += unicode(CommitMessage.DESCRIPTION) \
                           + u"\n"\
                           + description
            subject = subject + str(current_delta + 1)
        send_email_extra(list_to_address,
                         list_cc_address,
                         subject, message,
                         list_file_send,
                         current_dir)

    # UC2: Run report scripts and send reports manually
    elif args.report:
        if os.path.isfile(args.parameters):
            tmp = os.path.join(current_dir, "tmp")
            if not os.path.exists(tmp):
                os.makedirs(tmp)
            else:
                shutil.rmtree(tmp)
                os.mkdir(tmp)
            for file_name in os.listdir(current_dir):
                if file_name.endswith(".xlsx"):
                    shutil.move(os.path.join(current_dir, file_name), tmp)

            # Report accuracy and performance
            run_report()

            parameter_file = args.parameters
            # Get change number and current delta
            parameter_handler = ParameterHandler(input_file=parameter_file)
            current_delta = int(parameter_handler.get_delta_version())
            commit_message = parameter_handler.get_commit()
            summary = parse_commit_message_contents_by_topic(
                CommitMessage.SUMMARY,
                commit_message
            )
            if summary:
                message += u"\n\n" \
                           + unicode(CommitMessage.SUMMARY) \
                           + u"\n" \
                           + summary
            description = parse_commit_message_contents_by_topic(
                CommitMessage.DESCRIPTION,
                commit_message)
            if description:
                message += unicode(CommitMessage.DESCRIPTION) \
                           + u"\n" \
                           + description

            # Get subject
            subject = subject + str(current_delta + 1)
            send_email_extra(list_to_address,
                             list_cc_address,
                             subject, message,
                             list_file_send,
                             current_dir)
        else:
            print "Missing parameters file !!!"
    else:
        # UC3: Send any
        to_address = args.to_address
        cc_address = args.cc_address
        subject = args.subject
        message = args.message
        attachments = args.attachment_file

        list_attachment = []
        attachments = attachments.split(",")
        for att in attachments:
            att = os.path.abspath(att)
            list_attachment.append(att)
        print "Sending email ..."
        EmailSender.send(to_address, cc_address, subject, message, list_attachment)
        sys.exit(0)


if __name__ == "__main__":
    main()
