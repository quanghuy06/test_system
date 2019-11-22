import os
import argparse
import sys_path
sys_path.insert_sys_path()
from configs.jenkins import JenkinsHelper
from configs.common import SupportedPlatform
from configs.test_result import FinalTestResult
from baseapi.file_access import suffix_file, copy_a_path
from configs.json_key import ParametersJson
from handlers.parameters_handler import ParameterHandler


class ITToPostProcessRemover:
    def __init__(self, job_name, build_number):
        self.achieve_path = JenkinsHelper.get_archive_path(job_name, build_number)
        self.parameter = os.path.join(self.achieve_path,
                                      FinalTestResult.INFO,
                                      ParametersJson.DEFAULT_NAME)
        self.parameter_handler = ParameterHandler(input_file=self.parameter)
        self.change_number = self.parameter_handler.get_change_number()
        self.delta_version = self.parameter_handler.get_delta_version()

    def get_report_files(self, list_file, dest_path):
        """
        Get file report file from IT result to post process.

        """
        suffix = "C{0}_D{1}".format(self.change_number, self.delta_version)
        for file_name in list_file:
            file_name = suffix_file(file_name, suffix)
            for platform in SupportedPlatform:
                platform_folder = os.path.join(self.achieve_path, platform)
                report_folder = os.path.join(platform_folder,
                                             FinalTestResult.REPORT)

                report_file_path = os.path.join(report_folder,
                                                file_name)
                # Copy file report to destination path
                copy_a_path(report_file_path,
                            os.path.join(dest_path, file_name))


def parse_argument():
    parser = argparse.ArgumentParser(
        description='Get data which is archived on Jenkin')
    parser.add_argument('-j', "--job-name",
                        required=True,
                        help="Jenkins job name")
    parser.add_argument('-b', "--build-number",
                        required=True,
                        help="Jenkins build number will contain reference data")
    return parser.parse_args()


def main():
    args = parse_argument()
    it_to_post_process_remover = ITToPostProcessRemover(args.job_name,
                                                        args.build_number)
    list_report_file_name_default = [FinalTestResult.FILE_REPORT_TEXT_ACCURACY]

    it_to_post_process_remover.get_report_files(list_report_file_name_default,
                                                os.getcwd())


if __name__ == "__main__":
    main()
