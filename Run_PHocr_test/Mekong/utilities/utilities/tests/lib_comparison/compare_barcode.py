# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date create:      21/04/2017
# Last update:      03/07/2017
# Updated by:       Phung Dinh Tai
# Description:      This script define class for executing barcode result comparison
import os
import filecmp
from configs.compare_result import *
from tests.lib_comparison.barcode import Barcode
from baseapi.rect import Rectange


class CompareBarcode:

    def __init__(self):
        self.title = CompareResultConfig.TITLE_CMP_BARCODE

    # Check style of line
    @staticmethod
    def check_style(line):
        arr = line.split(",")
        if len(arr) == 2:
            return arr
        if len(arr) == 6:
            for i in range(2, 6):
                arr[i] = arr[i].strip()
                if not arr[i].isdigit():
                    return []
            return arr
        else:
            return []

    # Get data lines from file. Return list of data lines
    def get_data(self, src_file):
        if not os.path.isfile(src_file):
            return []
        result = []
        with open(src_file, 'r') as my_file:
            for line in my_file:
                arr = self.check_style(line)
                # Get data simple
                if len(arr) == 2:
                    barcode = Barcode(arr[0], arr[1])
                    result.append(barcode)
                # Get data with location
                if len(arr) == 6:
                    barcode = Barcode(arr[0], arr[1])
                    barcode.bbox = Rectange(arr[2], arr[3], arr[4], arr[5])
                    result.append(barcode)
        return result

    # Compare 2 files. Note that 2 file maybe is the same even if order of lines are different.
    @staticmethod
    def compare_2_file_location(src_bars, base_bars):
        result = dict()
        result[CompareBarcodeInfo.TITLE] = CompareBarcodeInfo.Title.LOCATION
        correct = []  # Same location, same barcode
        replace = []  # Same location, different barcode
        insert = []  # In base, not in src
        delete = []  # In src, not in base
        # Get compare result type : correct, replace, delete
        for barcode in src_bars:
            not_found = True
            for base in base_bars:
                cmp_res = barcode.compare_location_with(base)
                if cmp_res == BarcodeCmpType.location.CORRECT:
                    correct.append(barcode.to_string())
                    not_found = False
                    break
                if cmp_res == BarcodeCmpType.location.REPLACE:
                    replace.append(barcode.to_string())
                    not_found = False
                    break
            if not_found:
                delete.append(barcode.to_string())
        # Get compare result type : insert
        if len(correct) + len(replace) < len(base_bars):
            for barcode in base_bars:
                founded = False
                for base in src_bars:
                    cmp_res = barcode.compare_location_with(base)
                    founded = cmp_res == BarcodeCmpType.location.CORRECT or \
                        cmp_res == BarcodeCmpType.location.REPLACE
                    if founded:
                        break
                if not founded:
                    insert.append(barcode.to_string())
        is_change = False
        # Update to final result
        result[CompareBarcodeInfo.DETAIL] = {}
        if len(correct) > 0:
            result[CompareBarcodeInfo.DETAIL][BarcodeCmpType.location.CORRECT] = correct
        if len(replace) > 0:
            result[CompareBarcodeInfo.DETAIL][BarcodeCmpType.location.REPLACE] = replace
            is_change = True
        if len(insert) > 0:
            result[CompareBarcodeInfo.DETAIL][BarcodeCmpType.location.INSERT] = insert
            is_change = True
        if len(delete) > 0:
            result[CompareBarcodeInfo.DETAIL][BarcodeCmpType.location.DELETE] = delete
            is_change = True
        result[CompareBarcodeInfo.IS_CHANGE] = is_change
        result[CompareBarcodeInfo.NUM_CORRECT] = len(correct)
        # Number errors = REPLACE + INSERT + DELETE
        result[CompareBarcodeInfo.NUM_ERROR] = len(replace) + len(insert) + len(delete)
        return result

    # Compare 2 files. Note that 2 file maybe is the same even if order of lines are different.
    @staticmethod
    def compare_2_file_simple(src_bars, base_bars):
        result = dict()
        result[CompareBarcodeInfo.TITLE] = CompareBarcodeInfo.Title.SIMPLE
        type_1 = []  # Same format, same content
        type_2 = []  # Same format, different content
        type_3 = []  # Different format, same content
        type_4 = []  # In src, not in base
        type_5 = []  # In base, not in src
        # Get compare result type 1, 2, 3, 4
        for barcode in src_bars:
            not_found = True
            for base in base_bars:
                cmp_res = barcode.compare_with(base)
                if cmp_res == BarcodeCmpType.simple.TYPE_1:
                    # Correct
                    type_1.append(barcode.to_string())
                    not_found = False
                    break
                if cmp_res == BarcodeCmpType.simple.TYPE_2:
                    type_2.append(barcode.to_string())
                    not_found = False
                    break
                if cmp_res == BarcodeCmpType.simple.TYPE_3:
                    type_3.append(barcode.to_string())
                    not_found = False
                    break
            if not_found:
                type_4.append(barcode.to_string())
        # Get compare result type 5
        if len(base_bars) > len(src_bars):
            founded = False
            for barcode in base_bars:
                for base in src_bars:
                    cmp_res = barcode.compare_with(base)
                    founded = cmp_res == BarcodeCmpType.simple.TYPE_1 \
                        or cmp_res == BarcodeCmpType.simple.TYPE_2 \
                        or cmp_res == BarcodeCmpType.simple.TYPE_3
                    if founded:
                        break
                if not founded:
                    type_5.append(barcode.to_string())
        is_change = False
        # Update to final result
        result[CompareBarcodeInfo.DETAIL] = {}
        if len(type_1) > 0:
            result[CompareBarcodeInfo.DETAIL][BarcodeCmpType.simple.TYPE_1] = type_1
        if len(type_2) > 0:
            result[CompareBarcodeInfo.DETAIL][BarcodeCmpType.simple.TYPE_2] = type_2
            is_change = True
        if len(type_3) > 0:
            result[CompareBarcodeInfo.DETAIL][BarcodeCmpType.simple.TYPE_3] = type_3
            is_change = True
        if len(type_4) > 0:
            result[CompareBarcodeInfo.DETAIL][BarcodeCmpType.simple.TYPE_4] = type_4
            is_change = True
        if len(type_5) > 0:
            result[CompareBarcodeInfo.DETAIL][BarcodeCmpType.simple.TYPE_5] = type_5
            is_change = True
        result[CompareBarcodeInfo.IS_CHANGE] = is_change
        result[CompareBarcodeInfo.NUM_CORRECT] = len(type_1)
        # Number errors = type_2 + type_3 + type_4 + type_5
        result[CompareBarcodeInfo.NUM_ERROR] = len(type_2) + len(type_3) + len(type_4) + len(type_5)
        return result

    # Execute comparision for one data set
    def execute_one(self, out_file, ref_file, ground_file, compare_type):
        result = {}
        output_data = self.get_data(out_file)
        ref_data = self.get_data(ref_file)
        ground_data = self.get_data(ground_file)
        # Get total number of barcodes in ground truth
        total_barcodes = len(ground_data)
        result[CompareBarcodeInfo.TOTAL] = total_barcodes
        # Compare barcode simple
        if compare_type == CompareBarcodeInfo.type.SIMPLE:
            # Compare change with reference
            # Compare 2 file to identify if 2 file change before compare bounding box
            if filecmp.cmp(out_file, ref_file):
                cmp_diff = dict()
                cmp_diff[CompareBarcodeInfo.IS_CHANGE] = False
            else:
                cmp_diff = self.compare_2_file_simple(output_data, ref_data)
            result[CompareBarcodeInfo.DIFF] = cmp_diff
            result[CompareBarcodeInfo.IS_CHANGE] = cmp_diff[CompareBarcodeInfo.IS_CHANGE]
            # Compare reference data with ground truth data
            result[CompareBarcodeInfo.ORIGIN] =\
                self.compare_2_file_simple(ref_data, ground_data)
            result[CompareBarcodeInfo.TITLE] = CompareBarcodeInfo.Title.SIMPLE
            # If current result is not change compare with reference data, not need to compare
            # ground truth. Otherwise, compare output and reference with ground truth data
            if cmp_diff[CompareBarcodeInfo.IS_CHANGE]:
                # Compare output with ground truth data
                result[CompareBarcodeInfo.CHANGE] =\
                    self.compare_2_file_simple(output_data, ground_data)
                result[CompareBarcodeInfo.NUM_CORRECT] = result[CompareBarcodeInfo.CHANGE][
                    CompareBarcodeInfo.NUM_CORRECT]
            else:
                result[CompareBarcodeInfo.NUM_CORRECT] = result[CompareBarcodeInfo.ORIGIN][
                    CompareBarcodeInfo.NUM_CORRECT]
        if compare_type == CompareBarcodeInfo.type.LOCATION:
            # Compare change with reference
            # Compare 2 file to identify if 2 file change before compare bounding box
            if filecmp.cmp(out_file, ref_file):
                cmp_diff = dict()
                cmp_diff[CompareBarcodeInfo.IS_CHANGE] = False
            else:
                cmp_diff = self.compare_2_file_location(output_data, ref_data)
            result[CompareBarcodeInfo.DIFF] = cmp_diff
            result[CompareBarcodeInfo.IS_CHANGE] = cmp_diff[CompareBarcodeInfo.IS_CHANGE]
            # Compare reference data with ground truth data
            result[CompareBarcodeInfo.ORIGIN] =\
                self.compare_2_file_location(ref_data, ground_data)
            result[CompareBarcodeInfo.TITLE] = CompareBarcodeInfo.Title.SIMPLE
            # If current result is not change compare with reference data, not need to
            # compare ground truth
            # Otherwise, compare output and reference with ground truth data
            if cmp_diff[CompareBarcodeInfo.IS_CHANGE]:
                # Compare output with ground truth data
                result[CompareBarcodeInfo.CHANGE] =\
                    self.compare_2_file_location(output_data, ground_data)
                result[CompareBarcodeInfo.NUM_CORRECT] = result[CompareBarcodeInfo.CHANGE][
                    CompareBarcodeInfo.NUM_CORRECT]
            else:
                result[CompareBarcodeInfo.NUM_CORRECT] = result[CompareBarcodeInfo.ORIGIN][
                    CompareBarcodeInfo.NUM_CORRECT]
        return result

    # Execute comparidion with multiple set of (output, reference, ground truth)
    # data is a list of triple sets
    def execute(self, data, compare_type):
        if not data:
            return {}
        if len(data) == 1:
            data_set = data[0]
            return self.execute_one(data_set[CompareBarcodeData.OUTPUT],
                                    data_set[CompareBarcodeData.REF],
                                    data_set[CompareBarcodeData.GROUND],
                                    compare_type)
        else:
            result = dict()
            result[CompareBarcodeInfo.DETAIL] = {}
            result[CompareBarcodeInfo.IS_CHANGE] = False
            num_correct = 0
            total_barcodes = 0
            index = 1
            if compare_type == CompareBarcodeInfo.type.SIMPLE:
                result[CompareBarcodeInfo.TITLE] = CompareBarcodeInfo.Title.SIMPLE
            else:
                result[CompareBarcodeInfo.TITLE] = CompareBarcodeInfo.Title.LOCATION
            total = len(data)
            for data_set in data:
                out_file = data_set[CompareBarcodeData.OUTPUT]
                ref_file = data_set[CompareBarcodeData.REF]
                ground_file = data_set[CompareBarcodeData.GROUND]
                file_name = os.path.basename(out_file)
                test_name = file_name.replace("_barcode.csv", '')
                print "   {0}/{1} {2}".format(index, total, test_name)
                if os.path.exists(out_file) and os.path.exists(ref_file):
                    result_set = self.execute_one(out_file,
                                                  ref_file,
                                                  ground_file,
                                                  compare_type)
                    num_correct += result_set[CompareBarcodeInfo.NUM_CORRECT]
                    total_barcodes += result_set[CompareBarcodeInfo.TOTAL]
                    if result_set[CompareBarcodeInfo.IS_CHANGE]:
                        result[CompareBarcodeInfo.IS_CHANGE] = True
                    result[CompareBarcodeInfo.DETAIL][test_name] = result_set
                else:
                    result[CompareBarcodeInfo.IS_CHANGE] = True
                    result_set = dict()
                    result_set[CompareBarcodeInfo.IS_CHANGE] = True
                    if (not os.path.exists(out_file))\
                            and (not os.path.exists(ref_file)):
                        result_set[
                            CompareBarcodeInfo.NOT_IN_OUTPUT_AND_REF] = True
                    elif not os.path.exists(ref_file):
                        result_set[CompareBarcodeInfo.OUTPUT_ONLY] = True
                    else:
                        result_set[CompareBarcodeInfo.REF_ONLY] = True
                    result[CompareBarcodeInfo.DETAIL][test_name] = result_set
                index += 1
            result[CompareBarcodeInfo.NUM_CORRECT] = num_correct
            result[CompareBarcodeInfo.TOTAL] = total_barcodes
            return result
