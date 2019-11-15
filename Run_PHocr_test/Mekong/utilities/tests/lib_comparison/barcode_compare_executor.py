# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date create:  30/06/2017
# Last update:  02/07/2017
# Updated by:   Phung Dinh Tai
# Description:  This script define executer for Barcode result comparison
import os

from configs.compare_result import CompareJsonKeys, CompareBarcodeInfo
from configs.database import TestcaseConfig
from configs.projects.phocr import PhocrProject
from configs.test_result import FinalTestResult
from handlers.test_spec_handler import TestSpecHandler
from tests.lib_comparison.compare_barcode import CompareBarcode
from tests.lib_comparison.compare_folder_test_result import \
    CompareFolderTestResult


class BarcodeCompareExecutor:

    def __init__(self, test_folder, test_id, platform):
        test_path = os.path.join(test_folder, test_id)
        list_files = []
        self.data = []
        self.platform = platform
        self.test_folder = test_folder
        self.test_id = test_id
        for file_name in os.listdir(os.path.join(test_path,
                                                 TestcaseConfig.OUTPUT_FOLDER,
                                                 self.platform)):
            if "_barcode.csv" in file_name:
                list_files.append(file_name)
        for test_file in list_files:
            output_file = os.path.join(test_path,
                                       TestcaseConfig.OUTPUT_FOLDER,
                                       self.platform, test_file)
            ref_file = os.path.join(test_path,
                                    TestcaseConfig.REF_DATA_DIR,
                                    self.platform, test_file)
            ground_file = os.path.join(test_path,
                                       TestcaseConfig.GROUND_TRUTH_DATA_DIR,
                                       self.platform, test_file)
            self.data.append({
                "output": output_file,
                "reference": ref_file,
                "ground_truth": ground_file
            })
        spec_file = os.path.join(test_folder, test_id, TestcaseConfig.SPEC_FILE)
        self.spec_handler = TestSpecHandler(input_file=spec_file)

    def execute(self):
        bar_executor = CompareBarcode()
        # Check if "simple" in functionalities of test cases -> Compare simple
        result = None
        if PhocrProject.functionalities.BAR_SIMPLE in self.spec_handler.get_functions():
            result = bar_executor.execute(self.data,
                                          CompareBarcodeInfo.type.SIMPLE)
        else:
            # If not -> compare with barcode location
            result = bar_executor.execute(self.data,
                                          CompareBarcodeInfo.type.LOCATION)

        # TODO(Huan) This is tempolary fixed compare stdout, stderr for barcode
        # This code duplicate with phocr_compare_executor.py module.
        # refactor it later.

        # TODO(Huan) currently, result has multiple formats:
        # Example 1. result: {"detail_information": {...},
        #                      "is_changed": False,
        #                      "tile":"Barcode with location",
        #                      ...}
        # Example 2. result:
        # {'is_changed': True,
        #  'compare_reference_vs_ground_truth': {'detail_information': []},
        #  'compare_change_vs_reference': {'is_stdout_changed': True,
        #                                  'is_stderr_changed': True,
        #                                  'detail_information': {
        #                                      'right_only': [],
        #                                      'funny_files': [],
        #                                      'left_only': ['stderr.txt',
        #                                                    'stdout.txt'],
        #                                      'diff_files': []},
        #                                  'title': 'Compare folder'}}
        # currently, we ignore case example 1 with compare stdout, stdin.
        # Need to fix it later

        if not CompareJsonKeys.DIFF in result.keys():
            return result

        # Compare stderr and stdout of reference data and output data
        test_path = os.path.join(self.test_folder, self.test_id)
        o_folder = os.path.join(test_path, TestcaseConfig.OUTPUT_FOLDER,
                                self.platform)
        if not os.path.isdir(o_folder):
            os.makedirs(o_folder)
        r_folder = os.path.join(test_path, TestcaseConfig.REF_DATA_DIR,
                                self.platform)
        if not os.path.isdir(r_folder):
            os.makedirs(r_folder)

        compare_test_result = CompareFolderTestResult(self.test_folder,
                                                      self.test_id)
        is_stdout_changed = compare_test_result.is_file_changed(r_folder,
                                                                o_folder,
                                                                FinalTestResult.Test.STDOUT_FILE_NAME)
        is_stderr_changed = compare_test_result.is_file_changed(r_folder,
                                                                o_folder,
                                                                FinalTestResult.Test.STDERR_FILE_NAME)
        result[CompareJsonKeys.DIFF][
            CompareJsonKeys.IS_STDOUT_CHANGED] = is_stdout_changed
        result[CompareJsonKeys.DIFF][
            CompareJsonKeys.IS_STDERR_CHANGED] = is_stderr_changed
        if is_stdout_changed or is_stderr_changed:
            result[CompareJsonKeys.IS_CHANGE] = True

        return result
