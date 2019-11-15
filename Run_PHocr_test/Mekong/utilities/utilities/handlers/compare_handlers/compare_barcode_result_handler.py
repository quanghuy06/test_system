# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created:     12/01/2017
# Last updated:     26/07/2017
# Update by:        Phung Dinh Tai
# Description:      This script define a class for handling json compare result
import os
from abc import ABCMeta
from handlers.compare_handlers.lib_base.compare_result_handler_class import \
    CompareResultHandlerClass, CRHDLConfiguration
from configs.projects.phocr import PhocrProject
from configs.database import TestcaseConfig, SpecKeys
from handlers.test_spec_handler import TestSpecHandler


class CBCHConfiguration(object):

    # Title
    GENERAL_TITLE = "Compare barcode"
    SIMPLE_TITLE = "Barcode simple"
    COMPARE_LOCATION_TITLE = "Barcode with location"

    # Information keys
    NUM_CORRECT = "number_correct_barcodes"
    NUM_ERROR = "number_error_barcodes"
    TOTAL = "total barcodes"

    # Compare types
    T_SIMPLE = "simple"
    T_LOCATION = "location"


class CompareBarcodeHandler(CompareResultHandlerClass):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(CompareBarcodeHandler, self).__init__(**kwargs)

    def get_list_tests(self):
        list_tests = list()
        for test_name in self.data.keys():
            spec_file = os.path.join(self.test_folder, test_name, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            if spec_handler.get_component() == PhocrProject.components.BARCODE\
                    and not self.is_memory_checking(spec_handler):
                list_tests.append(test_name)
        return list_tests

    def set_title(self):
        self.title = CBCHConfiguration.GENERAL_TITLE

    # Check if change is different from reference data
    def is_barcode_changed(self, test_name, image):
        if test_name == image:
            res = self.data[test_name]
        else:
            res = self.data[test_name][CRHDLConfiguration.DETAIL_INFO][image]
        return res[CRHDLConfiguration.DIFF][CRHDLConfiguration.IS_CHANGED]

    # Reference with ground truth
    def is_ref_barcode_pass(self, test_name, image):
        if test_name == image:
            res = self.data[test_name]
        else:
            res = self.data[test_name][CRHDLConfiguration.DETAIL_INFO][image]
        return not res[CRHDLConfiguration.ORIGIN][CRHDLConfiguration.IS_CHANGED]

    # Change with ground truth
    def is_barcode_pass(self, test_name, image):
        if self.is_barcode_changed(test_name, image):
            if test_name == image:
                res = self.data[test_name]
            else:
                res = self.data[test_name][CRHDLConfiguration.DETAIL_INFO][image]
            return not res[CRHDLConfiguration.CHANGE][CRHDLConfiguration.IS_CHANGED]
        else:
            return self.is_ref_barcode_pass(test_name, image)

    # Get total error barcodes when comparing change with ground truth
    def num_error_bars(self, test_name, image):
        if test_name == image:
            res = self.data[test_name]
        else:
            res = self.data[test_name][CRHDLConfiguration.DETAIL_INFO][image]
        if self.is_barcode_changed(test_name, image):
            return res[CRHDLConfiguration.CHANGE][CBCHConfiguration.NUM_ERROR]
        else:
            return res[CRHDLConfiguration.ORIGIN][CBCHConfiguration.NUM_ERROR]

    # Get number of error barcodes when comparing reference with ground truth
    def num_ref_error_bars(self, test_name, image):
        if test_name == image:
            res = self.data[test_name]
        else:
            res = self.data[test_name][CRHDLConfiguration.DETAIL_INFO][image]
        return res[CRHDLConfiguration.ORIGIN][CBCHConfiguration.NUM_ERROR]

    # Variance number errors between change and reference
    def variance_change_vs_ref_bars(self, test_name, image):
        return self.num_error_bars(test_name, image) - \
               self.num_ref_error_bars(test_name, image)

    # Get number of barcode correct
    def num_correct_bars(self, test_name, image):
        if test_name == image:
            res = self.data[test_name]
        else:
            res = self.data[test_name][CRHDLConfiguration.DETAIL_INFO][image]
        if self.is_barcode_changed(test_name, image):
            return res[CRHDLConfiguration.CHANGE][CBCHConfiguration.NUM_CORRECT]
        else:
            return res[CRHDLConfiguration.ORIGIN][CBCHConfiguration.NUM_CORRECT]

    # Get total number of barcodes in ground truth
    def total_bars(self, test_name, image):
        if test_name == image:
            res = self.data[test_name]
        else:
            res = self.data[test_name][CRHDLConfiguration.DETAIL_INFO][image]
        return res[CBCHConfiguration.TOTAL]

    # Get list images of a test case
    def get_list_images(self, test_name):
        result = []
        res = self.data[test_name]
        if CRHDLConfiguration.DETAIL_INFO in res:
            # Test case with multiple images
            for image in res[CRHDLConfiguration.DETAIL_INFO]:
                result.append(image)
        else:
            # Test case with single image
            result.append(test_name)
        return result

    def comparison_type(self, test_name):
        return self.data[test_name][CRHDLConfiguration.TITLE]
