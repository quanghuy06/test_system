# Toshiba - TSDV
# Team:         PHOcr
# Author:       Huanlv
# Date create:  30/06/2017
# Description:  This script define executer for binary test result comparison
import os
from baseapi.common import compare_two_list_string
from baseapi.file_access import list_all_file_in_folder_recusively
from configs.common import Platform
from configs.compare_result import CompareResultConfig, CompareJsonKeys, \
    CompareMessage
from configs.database import TestcaseConfig, SpecKeys
from configs.test_result import FinalTestResult
from handlers.test_spec_handler import TestSpecHandler
from tests.lib_comparison.compare_bounding_box import CompareBoundingBox
from tests.lib_comparison.compare_office import CompareOfficeFile
from tests.lib_comparison.compare_pdf import ComparePdf
from tests.lib_comparison.compare_text_file import CompareTextFile


# Execute test for one test case
class BinaryTestCompareExecutor:
    """
    This class will compare for component "binary_test".
    Compare base on user defined output of the test case.
    """

    def __init__(self, test_folder, test_id, platform,
                 result_folder=CompareResultConfig.FOLDER_DEFAULT):
        self.test_folder = test_folder
        self.test_id = test_id
        self.test_path = os.path.join(test_folder, test_id)
        spec_file = os.path.join(test_folder, test_id, TestcaseConfig.SPEC_FILE)
        self.spec_handler = TestSpecHandler(input_file=spec_file)
        self.result_folder = os.path.join(result_folder, test_id)
        if not os.path.isdir(self.result_folder):
            os.makedirs(self.result_folder)
        self.platform = platform
        self.compare_result_for_platform_dir = os.path.join(self.result_folder,
                                                            self.platform)
        if not os.path.isdir(self.compare_result_for_platform_dir):
            os.makedirs(self.compare_result_for_platform_dir)

    def execute(self):
        """
        Do compare output files and ref_data
        Returns
        -------
        object
            compare result
        """
        # TODO (HuanLV) Create classes for generate compare result of binary_test.
        final_result = dict()
        final_result['binary_test'] = True

        output_dir = os.path.join(self.test_path, TestcaseConfig.OUTPUT_FOLDER, self.platform)
        ref_data_dir = os.path.join(self.test_path, TestcaseConfig.REF_DATA_DIR, self.platform)

        # Use Linux platform here because use linux folder for both windows and linux GT
        # apply only for ground truth for text file and bounding box file.
        # TODO(HuanLV) correct tructure of ground truth folder
        ground_truth_dir = os.path.join(self.test_path, TestcaseConfig.GROUND_TRUTH_DATA_DIR,
                                        Platform.LINUX)

        # Collect all file in ref_data folder:
        ref_data_file_list = list()
        for file_name in list_all_file_in_folder_recusively(ref_data_dir):
            ref_data_file_list.append(file_name)

        # Collect all output files
        output_file_list = list()
        for file_name in list_all_file_in_folder_recusively(output_dir):
            output_file_list.append(file_name)

        gt_file_list = list()
        for file_name in list_all_file_in_folder_recusively(ground_truth_dir):
            gt_file_list.append(file_name)

        # Get stdout.txt, stderr.txt file list
        std_file_list = list()
        std_file_list.append(FinalTestResult.Test.STDERR_FILE_NAME)
        std_file_list.append(FinalTestResult.Test.STDOUT_FILE_NAME)

        # Get comparators and output defined by user
        binary_test_information = self.spec_handler.get_binary_test_information()
        user_defined_output = \
            binary_test_information[SpecKeys.BinaryTestInformation.OUTPUT]
        user_defined_file_list = []
        comparator_map = {}
        for file_output in user_defined_output:
            file_name = str(file_output[SpecKeys.BinaryTestInformation.Output.NAME])
            user_defined_file_list.append(file_name)

            comparator_name = (file_output[SpecKeys.BinaryTestInformation.Output.COMPARATOR])
            comparator_map[file_name] = comparator_name

        same_output_user_defined, not_in_output, not_in_user_defined = \
            compare_two_list_string(output_file_list, user_defined_file_list)

        information = dict()
        information[CompareMessage.FILE_NOT_IN_OUTPUT] = not_in_output
        information[CompareMessage.FILE_NOT_IN_USER_DEFINED] = not_in_user_defined

        compare_result = dict()
        same_output_ref_data_user_defined, not_in_ref_data, not_in_output_user_defined = \
            compare_two_list_string(ref_data_file_list, same_output_user_defined)

        information[CompareMessage.FILE_NOT_IN_REF] = not_in_ref_data

        for file_name in same_output_ref_data_user_defined:
            compare_result[file_name] = dict()
            file_compare_result = dict()
            # compare
            file_in_gt_path = os.path.join(ground_truth_dir, file_name)
            file_in_output_path = os.path.join(output_dir, file_name)
            file_in_ref_data_path = os.path.join(ref_data_dir, file_name)

            comparator_name = comparator_map[file_name]
            # Because GT folder store only for bb or text file,
            # So other think will be ignore.

            file_compare_result[CompareJsonKeys.DIFF] = self.compare_2_files(file_in_output_path,
                                                                             file_in_ref_data_path,
                                                                             comparator_name,
                                                                             False,
                                                                             self.compare_result_for_platform_dir)
            file_compare_result[CompareJsonKeys.CHANGE] = self.compare_2_files(file_in_output_path,
                                                                               file_in_gt_path,
                                                                               comparator_name,
                                                                               False,
                                                                               self.compare_result_for_platform_dir)
            file_compare_result[CompareJsonKeys.ORIGIN] = self.compare_2_files(
                file_in_ref_data_path,
                file_in_gt_path,
                comparator_name,
                False,
                self.compare_result_for_platform_dir)

            compare_result[file_name]['result'] = file_compare_result

            # We will support compare for text, bb file if one is missing
            # by create empty file instead of missing file.
            # Because we need accuracy data although output file or reference file
            # missing.
        for file_name in std_file_list:
            compare_result[file_name] = dict()

            # is junk file
            compare_result[file_name]['is_std'] = True

            file_compare_result = dict()
            # compare
            file_in_output_path = os.path.join(output_dir, file_name)
            file_in_ref_data_path = os.path.join(ref_data_dir, file_name)

            comparator_name = SpecKeys.BinaryTestInformation.Output.Comparator.TEXT
            file_compare_result[CompareJsonKeys.DIFF] = self.compare_2_files(file_in_output_path,
                                                                             file_in_ref_data_path,
                                                                             comparator_name,
                                                                             False,
                                                                             self.compare_result_for_platform_dir)
            file_compare_result[CompareJsonKeys.CHANGE] = dict()
            file_compare_result[CompareJsonKeys.ORIGIN] = dict()
            compare_result[file_name]['result'] = file_compare_result

            # We will support compare for text, bb file if one is missing
            # by create empty file instead of missing file.
            # Because we need accuracy data although output file or reference file
            # missing.

        information['compare_result'] = compare_result

        # uncomment if need compare information
        # final_result['information'] = information

        # is_change = ?
        # Test case is changed when:
        #     - output has file list difference with ref_data
        #     - one of output file has accuracy/ content changed.
        is_change = False

        # is output_file list difference with ref_data file list
        if not_in_output \
                or not_in_ref_data \
                or not_in_ref_data:
            is_change = True
        elif self.is_any_files_changed_with_ref_data(compare_result):
            is_change = True

        final_result[CompareJsonKeys.IS_CHANGE] = is_change

        return final_result

    @classmethod
    def compare_2_files(cls,
                        first_file,
                        second_file,
                        comparator_name,
                        is_arabic,
                        compare_output_dir):
        """
        Compare 2 file with corresponding comparator.
        Parameters
        ----------
        first_file: string
            path to first file
        second_file: string
            path to second file
        comparator_name: string
            name of comparator
        is_arabic: bool
            Do compared files are Arabic?
        compare_output_dir: string
            directory store compare output files if have.

        Returns
        -------
        object
            Result of compare.

        """
        if not os.path.isfile(first_file) \
                or not os.path.isfile(second_file):
            return {
                CompareJsonKeys.IS_CHANGE: True
            }

        comparator_name_in_lower = comparator_name.lower()
        output_definition = SpecKeys.BinaryTestInformation.Output
        if comparator_name_in_lower == output_definition.Comparator.TEXT:
            comparator = CompareTextFile(is_arabic=is_arabic)
        elif comparator_name_in_lower == output_definition.Comparator.BOUNDING_BOX:
            comparator = CompareBoundingBox()
        elif comparator_name_in_lower == output_definition.Comparator.PDF:
            # TODO(HuanLV) separate compare pdf vs pdfa
            comparator = ComparePdf()
        elif comparator_name_in_lower == output_definition.Comparator.PDFA:
            comparator = ComparePdf()
        elif comparator_name_in_lower == output_definition.Comparator.WORD:
            comparator = CompareOfficeFile("Compare word")
        elif comparator_name_in_lower == output_definition.Comparator.EXCEL:
            comparator = CompareOfficeFile("compare excel")

        elif comparator_name_in_lower == output_definition.Comparator.PPTX:
            comparator = CompareOfficeFile("compare pptx")
        elif comparator_name_in_lower == output_definition.Comparator.IGNORE:
            return {
                CompareJsonKeys.IS_CHANGE: False
            }
        else:
            error_msg = "Does not supported comparator named {0}".format(comparator_name)
            raise Exception(error_msg)

        return comparator.compare(first_file, second_file, compare_output_dir)

    @classmethod
    def is_any_files_changed_with_ref_data(cls, compare_result):
        """
        Check compare result to determine test case is changed or not?
        Parameters
        ----------
        compare_result: dict
            compare result of the test case

        Returns
        -------
        bool
            if test case changed, return True
            else return False.

        """
        for file_name in compare_result:
            file_compare_result = compare_result[file_name]
            detail_result = file_compare_result['result']
            for pair_result in detail_result:
                if pair_result != CompareJsonKeys.DIFF:
                    continue
                if CompareJsonKeys.IS_CHANGE in detail_result[pair_result]:
                    if detail_result[pair_result][CompareJsonKeys.IS_CHANGE]:
                        return True

        return False

    @classmethod
    def is_file_change(cls, file_compare_information):
        """
        Check with compare result of 2 files, is ouput file changed or not
        Parameters
        ----------
        file_compare_information: dict
            compare result of 2 files

        Returns
        -------
        bool
            if 2 file different, return True
            else return False
        """
        return file_compare_information[CompareJsonKeys.IS_CHANGE]
