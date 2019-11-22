# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created:     02/07/2017
# Last updated:     02/07/2017
# Update by:        Phung Dinh Tai
# Description:      This script define a class for auto select executer to execute
#                   comparison base on test case specification
import os

from configs.database import TestcaseConfig, SpecKeys
from configs.projects.hanoi import HanoiProject
from configs.projects.phocr import PhocrProject
from handlers.test_spec_handler import TestSpecHandler
from tests.lib_comparison.barcode_compare_executor import BarcodeCompareExecutor
from tests.lib_comparison.binary_test_compare_executor import BinaryTestCompareExecutor
from tests.lib_comparison.hanoi_compare_executor import HanoiCompareExecutor
from tests.lib_comparison.memcheck_compare_executor import MemCheckCompareExecutor
from tests.lib_comparison.phocr_compare_executor import PhocrCompareExecutor


class AutoComparisonExecutor:

    def __init__(self, test_folder, test_id, platform):

        self.test_folder = test_folder
        self.test_id = test_id
        self.platform = platform

        # Initial handler for specification
        spec_file = os.path.join(test_folder, test_id, TestcaseConfig.SPEC_FILE)
        self.spec_handler = TestSpecHandler(input_file=spec_file)

    def run(self):

        if self.spec_handler.get_tag(SpecKeys.Tags.IS_MEMCHECK):
            auto_executor = MemCheckCompareExecutor(self.test_folder, self.test_id)
            return auto_executor.execute()

        # PHOcr project
        if self.spec_handler.get_product() == PhocrProject.PRODUCT:

            # PHOcrExe test runner
            if self.spec_handler.get_component() == PhocrProject.components.DEFAULT:
                auto_executor = PhocrCompareExecutor(self.test_folder, self.test_id, self.platform)
                return auto_executor.execute()

            # Barcode test runner
            if self.spec_handler.get_component() == PhocrProject.components.BARCODE:
                auto_executor = BarcodeCompareExecutor(self.test_folder, self.test_id,
                                                       self.platform)
                return auto_executor.execute()

            if self.spec_handler.get_component() == PhocrProject.components.BINARY_TEST:
                auto_executor = BinaryTestCompareExecutor(self.test_folder,
                                                          self.test_id,
                                                          self.platform)
                return auto_executor.execute()

        # Hanoi project
        if self.spec_handler.get_product() == HanoiProject.PRODUCT:
            auto_executor = HanoiCompareExecutor(self.test_folder, self.test_id, self.platform)
            return auto_executor.execute()
