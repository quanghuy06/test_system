# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Updated by:       Phung Dinh Tai
# Description:
import os
from abc import ABCMeta
from database.lib_updater.database_updater import DatabaseUpdater
from configs.jenkins import JenkinsHelper
from configs.test_result import FinalTestResult
from configs.common import SupportedPlatform
from configs.database import TestcaseConfig, SpecKeys
from baseapi.file_access import copy_paths, remove_paths
from configs.test_result import TestResultConfig
from configs.compare_result import CompareResultConfig
from report.lib_errors_report.bb_error_types_reporter import \
    BB_ERROR_TYPES_REPORT_NAME_DEFAULT
from report.lib_errors_report.text_error_types_reporter import \
    TEXT_ERROR_TYPES_REPORT_NAME_DEFAULT
from report.lib_memory_report.mem_peak_tsv_reporter import \
    MEM_PEAK_TSV_FILE_NAME_DEFAULT
from report.lib_base.history_data_informer import HistoryDataConfiguration

from database.lib_updater.weight_updater import WeightUpdater
from database.lib_updater.error_flag_updater import ErrorFlagUpdater
from database.lib_updater.history_data_updater import HistoryDataUpdater


class JenkinsPostItUpdater(DatabaseUpdater):

    __metaclass__ = ABCMeta

    KEY_UPDATED = " Updated parts: "

    def __init__(self, job_name, build_number, delta_version, change_number, archive_folder, **kwargs):
        self.job_name = job_name
        self.build_number = build_number
        self.delta_version = delta_version
        # Because the report file use previous delta.
        # So to get the file name of report file, we need to decrease
        # the delta version
        self.previous_delta = str(int(delta_version) - 1)
        self.change_number = change_number

        # We use this option to support running on local machine.
        if not archive_folder:
            self.archive_folder = JenkinsHelper.get_archive_path(self.job_name, self.build_number)
        else:
            self.archive_folder = archive_folder
        super(JenkinsPostItUpdater, self).__init__(**kwargs)
        self.changed_tests_folder = FinalTestResult.CHANGE
        self.status_need_to_be_updated = [FinalTestResult.CHANGE, FinalTestResult.ERROR]
        self.list_updaters = []

        # This map store information for each test case with files is updated.
        # Example:
        # [
        #   { "test_case": "01_0033",
        #     "updated_fields": [
        #       "error_flag",
        #       "history_data",
        #       "ref_data"
        #     ]
        #   },
        #   {"test_case": "02_0281",
        #     "updated_fields": [
        #       "error_flag"
        #     ]
        #   }
        # ]
        #
        # This information will be used to write changed log for test cases.
        self.updated_test_case_info_map = []

    def get_data(self):
        # Prepare data to update
        # All of test case that has status changed and error are combined into a folder to
        # prepare for updating reference data
        if os.path.isdir(self.changed_tests_folder):
            remove_paths(self.changed_tests_folder)
        os.makedirs(self.changed_tests_folder)

        # Copy output that change on a platform into combined folders
        for platform in SupportedPlatform:
            need_updated = []
            for f in self.status_need_to_be_updated:
                need_updated.append(os.path.join(self.archive_folder, platform,
                                                 FinalTestResult.TEST, f))
            for f in need_updated:
                if os.path.isdir(f):
                    for test_name in os.listdir(f):
                        # Copy output result of this platform to combined folder
                        src_folder = os.path.join(f, test_name, TestcaseConfig.OUTPUT_FOLDER,
                                                  platform)
                        des_folder = os.path.join(self.changed_tests_folder, test_name,
                                                  TestcaseConfig.OUTPUT_FOLDER)
                        platform_output_folder = os.path.join(des_folder, platform)
                        if not os.path.isdir(des_folder):
                            os.makedirs(des_folder)

                        # WARNING: a test cases can appear on poth change and error list,
                        # so we need to check if output is copied, do not continue copy.
                        if os.path.isdir(src_folder) and not os.path.isdir(platform_output_folder):
                            copy_paths(paths=src_folder, des=des_folder)

        # For a test case, it can changed/error on a platform but not changed in others. So for
        # platforms where test case output not changed, we'll copy reference of platform into
        # combined folder for this test case.
        for test_name in os.listdir(self.changed_tests_folder):
            output_folder = os.path.join(self.changed_tests_folder, test_name,
                                         TestcaseConfig.OUTPUT_FOLDER)
            for platform in SupportedPlatform:
                platform_folder = os.path.join(output_folder, platform)
                if not os.path.isdir(platform_folder):
                    # If output of a platform do not exist for a platform, find and copy it from
                    # original reference data into output folder in combined folder
                    test_orig_dir = self.find_original_test_folder(test_name=test_name)
                    if test_orig_dir is not None:
                        ref_folder = os.path.join(test_orig_dir, TestcaseConfig.REF_DATA_DIR,
                                                  platform)
                        if os.path.isdir(ref_folder):
                            copy_paths(ref_folder, output_folder)
                    # If test case has no reference data for the platform, make an empty directory
                    platform_output = os.path.join(output_folder, platform)
                    if not os.path.isdir(platform_folder):
                        os.makedirs(platform_output)

    def update_data(self):
        # Update reference data
        self.update_reference_data()

        self._append_updated_test_cases_to_map(
            self.updated_test_cases, TestcaseConfig.REF_DATA_DIR
        )

        # Update other information
        self.update_other_information_for_each_platform()

    def update_other_information_for_each_platform(self):
        for platform in SupportedPlatform:
            platform_folder = os.path.join(self.archive_folder, platform)
            test_file = os.path.join(platform_folder, FinalTestResult.TEST,
                                     TestResultConfig.FILE_DEFAULT)
            compare_file = os.path.join(platform_folder, FinalTestResult.TEST,
                                        CompareResultConfig.FILE_DEFAULT)
            bb_errors_file = \
                self.get_file_update_path(platform_folder,
                                          BB_ERROR_TYPES_REPORT_NAME_DEFAULT)
            text_errors_file = \
                self.get_file_update_path(platform_folder,
                                          TEXT_ERROR_TYPES_REPORT_NAME_DEFAULT)
            mem_peak_file = \
                self.get_file_update_path(platform_folder,
                                          MEM_PEAK_TSV_FILE_NAME_DEFAULT)

            self.update_weight(test_file, platform)
            self.update_error_flag(test_file, compare_file, platform)
            self.update_history_data(bb_errors_file,
                                     text_errors_file,
                                     mem_peak_file,
                                     HistoryDataConfiguration.Product.PHOCR_TEST_MACHINE,
                                     platform, self.delta_version)

    def get_file_update_path(self, platform_folder, file_name):
        """
        Get file path which used for update history data.

        Parameters
        ----------
        platform_folder: str
            Path to folder with name is one of supported platform
        file_name: str
            File name what we want to get the path.

        Returns
        -------
        str: Path to the specific file

        """
        suffix = ""
        if self.change_number:
            suffix = "_C{change}_D{delta}".format(change=self.change_number,
                                                  delta=self.previous_delta)
        full_file_name = file_name.format(suffix=suffix)
        file_path = os.path.join(platform_folder,
                                 FinalTestResult.REPORT,
                                 full_file_name)

        return file_path

    def find_original_test_folder(self, test_name):
        possible_dirs = []
        for platform in SupportedPlatform:
            final_test_folder = os.path.join(self.archive_folder, platform, FinalTestResult.TEST)
            for f in self.status_need_to_be_updated:
                possible_dirs.append(os.path.join(final_test_folder, f))
        for f in possible_dirs:
            test_folder = os.path.join(f, test_name)
            if os.path.isdir(test_folder):
                return test_folder
        return None

    def update_reference_data(self):
        # After combine all output, it's time to update reference data
        for test_name in os.listdir(self.changed_tests_folder):
            output_folder = os.path.join(self.changed_tests_folder, test_name,
                                         TestcaseConfig.OUTPUT_FOLDER)
            self.test_case_manager.update_reference_data(ref_folder=output_folder,
                                                         test_id=test_name)
            if test_name not in self.updated_test_cases:
                self.updated_test_cases.append(test_name)

    def update_weight(self, test_result_file, platform):
        weight_updater = WeightUpdater(username=self.username, password=self.password,
                                       input_file=test_result_file, platform=platform)
        weight_updater.do_work()

        self._append_updated_test_cases_to_map(
            weight_updater.get_updated_test_cases(), SpecKeys.WEIGHTS
        )

    def update_error_flag(self, test_result_file, compare_result_file, platform):
        error_flag_updater = ErrorFlagUpdater(username=self.username, password=self.password,
                                              input_file=test_result_file,
                                              platform=platform,
                                              compare_file=compare_result_file)
        error_flag_updater.do_work()

        self._append_updated_test_cases_to_map(
            error_flag_updater.get_updated_test_cases(), SpecKeys.ERROR_FLAGS
        )

    def update_history_data(self, bb_error_file, text_error_file,
                            mem_peak_file, product, platform, delta_version):
        bb_error_updater = HistoryDataUpdater(username=self.username,
                                              password=self.password,
                                              input_file=bb_error_file,
                                              product=product,
                                              platform=platform,
                                              version=delta_version)
        bb_error_updater.do_work()

        text_error_updater = HistoryDataUpdater(username=self.username,
                                                password=self.password,
                                                input_file=text_error_file,
                                                product=product,
                                                platform=platform,
                                                version=delta_version)
        text_error_updater.do_work()

        # Update memory peak information
        mem_peak_updater = HistoryDataUpdater(username=self.username,
                                              password=self.password,
                                              input_file=mem_peak_file,
                                              product=product,
                                              platform=platform,
                                              version=delta_version)
        mem_peak_updater.do_work()

        self._append_updated_test_cases_to_map(
            bb_error_updater.get_updated_test_cases(), SpecKeys.HISTORY_DATA
        )
        self._append_updated_test_cases_to_map(
            text_error_updater.get_updated_test_cases(), SpecKeys.HISTORY_DATA
        )

    def _append_updated_test_cases_to_map(self, test_case_ids, updated_field):
        """
        Append changed test cases with name of updated field to map.

        :param test_case_ids: list
            List of test case ids which have changed
        :param updated_field: str
            Name of the field that test cases has changed
        :return:
        None
        """
        for test_case_id in test_case_ids:
            test_case_id_unicode = unicode(test_case_id)

            # Check is there test_case_id in updated info map:
            current_test_case_info = next(
                (test_case_info for index, test_case_info in enumerate(self.updated_test_case_info_map)
                 if test_case_id_unicode == test_case_info[SpecKeys.ID]), None
            )
            if current_test_case_info is not None:
                if updated_field not in current_test_case_info['updated_fields']:
                    current_test_case_info['updated_fields'].append(updated_field)
            else:
                new_test_case_info = {SpecKeys.ID: test_case_id_unicode,
                                      "updated_fields": [updated_field]}
                self.updated_test_case_info_map.append(new_test_case_info)

    def add_changed_log_for_updated_test_cases(self, changed_log):
        """
        This function add changed log for changed test cases after post IT.
        Overide base function because this class have difference works
        when add changed log for test cases. Each test case need to collect
        list of updated fields then add to changed log of that test case.

        :param changed_log: str
            The base changed log of post IT for a test case
        :return:
        None
        """
        for test_case_info in self.updated_test_case_info_map:
            updated_fields = test_case_info["updated_fields"]
            updated_fields_description = ", ".join(updated_fields)
            test_case_id = test_case_info[SpecKeys.ID]
            appended_changed_log = changed_log + ". " + self.KEY_UPDATED + " " + updated_fields_description
            self.test_case_manager.add_new_changed_log(test_case_id, appended_changed_log)