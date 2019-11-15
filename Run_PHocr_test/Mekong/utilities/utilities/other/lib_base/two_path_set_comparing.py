import os
import sys
import sys_path
sys_path.insert_sys_path()

from baseapi.file_access import write_line, remove_paths
from configs.jenkins import JenkinsHelper
from configs.test_result import FinalTestResult
from configs.database import TestcaseConfig
from configs.compare_result import CompareJsonKeys
from tests.lib_comparison.compare_folder_test_result import CompareFolderTestResult
from configs.compare_result import CompareResultConfig


class DPSConfiguration:
    # File name
    FILE_NAME_DEFAULT = "DifferenceBetweenTwoPathSet.txt"

    # Difference between two patch set information
    DIFFERENCE_TITLE = "****DIFFERENCE BETWEEN TWO PATH SET****"
    TC_IN_PREVIOUS_BUILD = "\n*** TEST CASE IN PREVIOUS BUILD BUT NOT IN CURRENT BUILD: ***"
    TC_IN_CURRENT_BUILD = "\n*** TEST CASE IN CURRENT BUILD BUT NOT IN PREVIOUS BUILD: ***"
    TC_IN_BOTH_BUILDS = "\n***TEST CASE IN BOTH TWO BUILDS BUT DIFFERENT: ***"


class TwoPatchSetComparing:
    def __init__(self, job_name, last_build_number, platform):
        self.job_name = job_name
        self.not_in_current = []
        self.not_in_previous = []
        self.diff_detail = {}
        self.list_differ = []
        self.last_build_str = str(last_build_number)
        self.platform = platform
        self.file_output = os.path.join(self.platform,
                                        FinalTestResult.REPORT,
                                        DPSConfiguration.FILE_NAME_DEFAULT)

    def write_line_to_file(self, line_string):
        write_line(message=line_string, file_path=self.file_output)

    def do_work(self):

        detail_compare = self.compare_two_path_set()
        if detail_compare:
            # Check and remove old file
            if os.path.isfile(self.file_output):
                remove_paths(self.file_output)

            self.write_data()

    def compare_two_path_set(self):
        current_dir = os.getcwd()
        try:
            archive_folder = JenkinsHelper.get_archive_path(self.job_name, self.last_build_str)
            # Compare results between two folder
            if not os.path.isdir(archive_folder):
                print "\tFolder {0} doesn't exists! No comparision executed".format(
                    self.last_build_str)
                return
            platform_folder = os.path.join(archive_folder, self.platform)
            if not os.path.isdir(platform_folder):
                print "\tFolder {0} doesn't exists! No comparision executed" \
                      " for platform {1}".format(platform_folder, self.platform)
                return
            previous_changed_path = os.path.join(platform_folder,
                                                 FinalTestResult.TEST,
                                                 FinalTestResult.CHANGE)
            if not os.path.isdir(previous_changed_path):
                print "\tDon't have test results for platform {0}!".format(self.platform)
                return
            previous_item = os.listdir(previous_changed_path)
            current_test_path = os.path.join(current_dir,
                                             self.platform,
                                             FinalTestResult.TEST,
                                             FinalTestResult.CHANGE)
            current_item = os.listdir(current_test_path)
            # Test case previous build but not in current build
            self.not_in_current = [item for item in previous_item if item not in current_item]
            # Test case current build but not in previous build
            self.not_in_previous = [item for item in current_item if item not in previous_item]
            # Get test case in both two build but difference
            both_input_and_output = [item for item in previous_item if item in current_item]

            for test_case in both_input_and_output:
                compare_folder_test_result = CompareFolderTestResult(previous_changed_path, test_case)
                previous_o_folder = os.path.join(previous_changed_path, test_case,
                                                 TestcaseConfig.OUTPUT_FOLDER, self.platform)
                current_o_folder = os.path.join(current_test_path, test_case,
                                                TestcaseConfig.OUTPUT_FOLDER, self.platform)
                not_in_r, not_in_o, detail_infos = \
                    compare_folder_test_result.compare_two_folder(previous_o_folder,
                                                                  current_o_folder)
                is_change = False

                self.diff_detail[CompareJsonKeys.INFO] = {}
                if not_in_r:
                    self.diff_detail[CompareJsonKeys.INFO][CompareResultConfig.NOT_IN_REFERENCE] = \
                        not_in_r
                    is_change = True
                if not_in_o:
                    self.diff_detail[CompareJsonKeys.INFO][CompareResultConfig.NOT_IN_OUTPUT] = \
                        not_in_o
                    is_change = True
                if detail_infos:
                    self.diff_detail[CompareJsonKeys.INFO][CompareResultConfig.DIFF_FILE] = \
                        detail_infos
                    for info in detail_infos:
                        if info[CompareJsonKeys.IS_CHANGE] is True:
                            is_change = True
                self.diff_detail[CompareJsonKeys.IS_CHANGE] = is_change
                if is_change:
                    self.list_differ.append(test_case)
            return self.diff_detail

        except Exception as e:
            print e
            print "\tError while compare !"
            sys.exit(0)

    def write_data(self):
        if (not self.not_in_previous) and (not self.not_in_current) and (not self.list_differ):
            print "\tThere is no difference between two patch sets on {0}!".format(self.platform)
            return
        # Write title
        self.write_line_to_file(DPSConfiguration.DIFFERENCE_TITLE)

        # Write test case in current build but not in previous build
        self.write_line_to_file(DPSConfiguration.TC_IN_CURRENT_BUILD)
        if self.not_in_previous:
            for test_case in self.not_in_previous:
                self.write_line_to_file(test_case)

        # Write test case in previous build but not in this build
        self.write_line_to_file(DPSConfiguration.TC_IN_PREVIOUS_BUILD)
        if self.not_in_current:
            for test_case in self.not_in_current:
                self.write_line_to_file(test_case)

        # Write test case in both two build but difference
        self.write_line_to_file(DPSConfiguration.TC_IN_BOTH_BUILDS)
        if self.list_differ:
            for test_case in self.list_differ:
                self.write_line_to_file(test_case)
