# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date create:  30/06/2017
# Last update:  22/01/2018
# Updated by:   Phung Dinh Tai
# Description:  This script define executer for PHOcr result comparison
import os
from baseapi.common import get_files_in_folder, compare_two_list_string
from baseapi.file_access import remove_paths
from configs.common import Platform
from configs.compare_result import CompareResultConfig, CompareJsonKeys, \
    CompareMessage
from configs.database import TestcaseConfig, SpecKeys
from configs.projects.phocr import PhocrProject
from configs.test_result import FinalTestResult
from handlers.test_spec_handler import TestSpecHandler
from tests.lib_comparison.compare_bounding_box import CompareBoundingBox
from tests.lib_comparison.compare_folder import CompareFolder
from tests.lib_comparison.compare_office import CompareOfficeFile
from tests.lib_comparison.compare_pdf import ComparePdf
from tests.lib_comparison.compare_text_file import CompareTextFile
from tests.lib_comparison.compare_folder_test_result import CompareFolderTestResult


# Execute test for one test case
class PhocrCompareExecutor:

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

    @staticmethod
    def compare_files_list_in_two_folder(src_folder, des_folder, ext_list):
        files_src = get_files_in_folder(src_folder, ext_list)
        files_dest = get_files_in_folder(des_folder, ext_list)
        return compare_two_list_string(files_src, files_dest)

    @staticmethod
    def is_valid_extension(file_name, ext_list, ignore_ext_list):
        if ignore_ext_list:
            for ext in ignore_ext_list:
                if file_name.endswith(ext):
                    return False
        for ext in ext_list:
            if file_name.endswith(ext):
                return True

    def compare_files_in_two_folder(self, src_folder, des_folder, ext_list, worker,
                                    ignore_ext_list=None):
        same, not_in_s, not_in_d = self.compare_files_list_in_two_folder(src_folder,
                                                                         des_folder,
                                                                         None)
        detail_info_list = []

        if not os.path.isdir(self.result_folder):
            os.makedirs(self.result_folder)

        for f in same:
            if self.is_valid_extension(f, ext_list, ignore_ext_list):
                s_file = os.path.join(src_folder, f)
                d_file = os.path.join(des_folder, f)
                detail_info_list.append(worker.compare(s_file, d_file, self.result_folder))
        return not_in_s, not_in_d, detail_info_list

    def compare_using_worker(self, o_folder, r_folder, g_folder, ext_list, worker, is_changed,
                             ignore_ext_list=None):
        result = {}
        is_output_formatting_compare = \
            worker.title == CompareResultConfig.TITLE_CMP_EXCEL \
            or worker.title == CompareResultConfig.TITLE_CMP_DOCX \
            or worker.title == CompareResultConfig.TITLE_CMP_PDFA \
            or worker.title == CompareResultConfig.TITLE_CMP_PPTX
        if is_output_formatting_compare:
            not_in_o, not_in_r, detail_info_list = \
                self.compare_files_in_two_folder(o_folder, r_folder, ext_list, worker,
                                                 ignore_ext_list)

            result = dict()
            result[CompareJsonKeys.IS_CHANGE] = False
            if not_in_o:
                result[CompareMessage.FILE_NOT_IN_OUTPUT] = not_in_o
                result[CompareJsonKeys.IS_CHANGE] = True
            if not_in_r:
                result[CompareMessage.FILE_NOT_IN_REF] = not_in_r
                result[CompareJsonKeys.IS_CHANGE] = True
            result[CompareJsonKeys.OFFICE_INFO] = detail_info_list
            for info in detail_info_list:
                if info[CompareJsonKeys.IS_CHANGE]:
                    result[CompareJsonKeys.IS_CHANGE] = True
                    break

        # Always compare reference with ground truth
        if worker.title == CompareResultConfig.TITLE_CMP_BB:
            worker.html_suffix = CompareResultConfig.HTML_ORIGIN_SUFFIX
        is_accuracy_compare = \
            worker.title == CompareResultConfig.TITLE_CMP_TEXT \
            or worker.title == CompareResultConfig.TITLE_CMP_BB
        if is_accuracy_compare:
            # Check if files not in reference data => temporary create an empty file for comparing
            # and we should remove after that
            same, not_in_r_0, not_in_g_0 =\
                self.compare_files_list_in_two_folder(r_folder, g_folder, ext_list)
            for f in not_in_r_0:
                r_file = os.path.join(r_folder, f)
                with open(r_file, "w") as my_file:
                    my_file.write("")
                    my_file.close()
            for f in not_in_g_0:
                g_file = os.path.join(g_folder, f)
                with open(g_file, "w") as my_file:
                    my_file.write("")
                    my_file.close()

            # Execute comparing files in two folders
            not_in_r, not_in_g, ref_detail_info_list =\
                self.compare_files_in_two_folder(r_folder, g_folder, ext_list, worker,
                                                 ignore_ext_list)
            result[CompareJsonKeys.ORIGIN] = {}

            result[CompareJsonKeys.ORIGIN][CompareJsonKeys.INFO] = ref_detail_info_list
            for cmp_info in ref_detail_info_list:
                if cmp_info[CompareJsonKeys.IS_CHANGE]:
                    result[CompareJsonKeys.ORIGIN][CompareJsonKeys.IS_CHANGE] = True
                    break

            is_bb_changed = False
            is_diff_file = False
            if is_changed:
                # Check if output is different from reference data or not
                # Compare text files of output vs reference data
                worker.html_suffix = CompareResultConfig.HTML_DIFF_SUFFIX
                not_in_o, not_in_r, detail_info_list =\
                    self.compare_files_in_two_folder(o_folder, r_folder, ext_list, worker,
                                                     ignore_ext_list)
                result[CompareJsonKeys.DIFF] = {}
                if not_in_o:
                    result[CompareJsonKeys.DIFF][CompareMessage.FILE_NOT_IN_OUTPUT] = not_in_o
                    is_diff_file = True
                if not_in_r:
                    result[CompareJsonKeys.DIFF][CompareMessage.FILE_NOT_IN_REF] = not_in_r
                    is_diff_file = True

                for cmp_info in detail_info_list:
                    if cmp_info[CompareJsonKeys.IS_CHANGE]:
                        is_bb_changed = True
                        break
                if not is_bb_changed and not is_diff_file:
                    result[CompareJsonKeys.DIFF][CompareJsonKeys.INFO] = []
                    result[CompareJsonKeys.DIFF][CompareJsonKeys.IS_CHANGE] = False
                else:
                    result[CompareJsonKeys.DIFF][CompareJsonKeys.INFO] = detail_info_list
                    result[CompareJsonKeys.DIFF][CompareJsonKeys.IS_CHANGE] = True

            if is_bb_changed:
                result[CompareJsonKeys.DIFF][CompareJsonKeys.IS_CHANGE] = True
                # Compare text files of output vs ground truth data
                worker.html_suffix = CompareResultConfig.HTML_CHANGE_SUFFIX
                # Check if files not in reference data => temporary create an empty file for
                # comparing and we should remove after that
                same, not_in_o_0, not_in_g_0 = \
                    self.compare_files_list_in_two_folder(o_folder, g_folder, ext_list)
                for f in not_in_o_0:
                    o_file = os.path.join(o_folder, f)
                    with open(o_file, "w") as my_file:
                        my_file.write("")
                        my_file.close()
                # Execute compare files
                not_in_o, not_in_g, detail_info_list =\
                    self.compare_files_in_two_folder(o_folder, g_folder, ext_list, worker,
                                                     ignore_ext_list)

                # Remove temporary files
                for f in not_in_o_0:
                    o_file = os.path.join(o_folder, f)
                    remove_paths(o_file)

                result[CompareJsonKeys.CHANGE] = {}
                result[CompareJsonKeys.CHANGE][CompareJsonKeys.IS_CHANGE] = False

                if not_in_o_0:
                    result[CompareJsonKeys.CHANGE][CompareMessage.FILE_NOT_IN_OUTPUT] = \
                        not_in_o_0
                    result[CompareJsonKeys.CHANGE][CompareJsonKeys.IS_CHANGE] = True

                if not_in_g_0:
                    result[CompareJsonKeys.CHANGE][CompareMessage.FILE_NOT_IN_GT] = \
                        not_in_g_0
                    result[CompareJsonKeys.CHANGE][CompareJsonKeys.IS_CHANGE] = True

                result[CompareJsonKeys.CHANGE][CompareJsonKeys.INFO] = detail_info_list
                for cmp_info in detail_info_list:
                    if cmp_info[CompareJsonKeys.IS_CHANGE]:
                        result[CompareJsonKeys.CHANGE][CompareJsonKeys.IS_CHANGE] = True
                        break

            # Remove temporary files
            for f in not_in_r_0:
                r_file = os.path.join(r_folder, f)
                remove_paths(r_file)
            for f in not_in_g_0:
                g_file = os.path.join(g_folder, f)
                remove_paths(g_file)
        return result

    @staticmethod
    def get_detail_errors(detail_info_list):
        total_chars = 0
        total_errors = 0
        insert_errors = 0
        replace_errors = 0
        delete_errors = 0
        result = {}
        for cmp_info in detail_info_list:
            total_chars += cmp_info[CompareJsonKeys.TOTAL_CHARACTER]
            total_errors += cmp_info[CompareJsonKeys.TOTAL_ERROR]
            insert_errors += cmp_info[CompareJsonKeys.INSERT_ERR]
            replace_errors += cmp_info[CompareJsonKeys.REPLACE_ERR]
            delete_errors += cmp_info[CompareJsonKeys.DELETE_ERR]
        result[CompareJsonKeys.TOTAL_CHARACTER] = total_chars
        result[CompareJsonKeys.TOTAL_ERROR] = total_errors
        result[CompareJsonKeys.INSERT_ERR] = insert_errors
        result[CompareJsonKeys.REPLACE_ERR] = replace_errors
        result[CompareJsonKeys.DELETE_ERR] = delete_errors
        return result

    @staticmethod
    def get_errors(detail_info_list):
        total_chars = 0
        total_errors = 0
        result = {}
        for cmp_info in detail_info_list:
            total_chars += cmp_info[CompareJsonKeys.TOTAL_CHARACTER]
            total_errors += cmp_info[CompareJsonKeys.TOTAL_ERROR]
        result[CompareJsonKeys.TOTAL_CHARACTER] = total_chars
        result[CompareJsonKeys.TOTAL_ERROR] = total_errors
        return result

    def execute(self):
        # Get functions of current test case
        functions = self.spec_handler.get_functions()

        # Check if current output is different from reference data or not by compare folder
        # If not change, only compare file between reference data and ground truth data to get
        # current accuracy
        # If change, compare file between: output vs reference, output vs ground truth,
        # reference vs ground truth
        worker = CompareFolder()
        result = {}
        self.result_folder = os.path.join(self.result_folder, self.platform)
        o_folder = os.path.join(self.test_path, TestcaseConfig.OUTPUT_FOLDER, self.platform)
        if not os.path.isdir(o_folder):
            os.makedirs(o_folder)
        r_folder = os.path.join(self.test_path, TestcaseConfig.REF_DATA_DIR, self.platform)
        if not os.path.isdir(r_folder):
            os.makedirs(r_folder)
        g_folder = os.path.join(self.test_path, TestcaseConfig.GROUND_TRUTH_DATA_DIR,
                                Platform.LINUX)
        if not os.path.isdir(g_folder):
            os.makedirs(g_folder)
        fd_cmp_o_vs_r = worker.compare(o_folder, r_folder)
        result[CompareJsonKeys.IS_CHANGE] = fd_cmp_o_vs_r[CompareJsonKeys.IS_CHANGE]
        result[CompareJsonKeys.ORIGIN] = {}
        result[CompareJsonKeys.ORIGIN][CompareJsonKeys.INFO] = []
        result[CompareJsonKeys.DIFF] = {}
        result[CompareJsonKeys.DIFF][CompareJsonKeys.INFO] = []
        result[CompareJsonKeys.CHANGE] = {}
        result[CompareJsonKeys.CHANGE][CompareJsonKeys.INFO] = []
        is_compare_folder = True

        from baseapi.common import get_lower
        lower_functionalities = get_lower(functions)
        # Check if have functionality export text file -> Compare text file
        if PhocrProject.functionalities.EXPORT_TXT in lower_functionalities:
            is_compare_folder = False
            print CompareResultConfig.TITLE_CMP_TEXT
            # Compare text files of reference data vs ground truth data
            ext_list = [CompareResultConfig.TXT_SUFFIX]
            language_lower = [x.lower() for x in self.spec_handler.get_tag(
                    tag=SpecKeys.Tags.LANGS)]
            is_arabic = "arabic" in language_lower

            bb_ext_list = []
            for i in range(0, 100):
                bb_ext_list.append("_{0}.txt".format(i))

            text_worker = CompareTextFile(is_arabic)
            text_cmp_result =\
                self.compare_using_worker(o_folder, r_folder, g_folder,
                                          ext_list, text_worker,
                                          fd_cmp_o_vs_r[CompareJsonKeys.IS_CHANGE],
                                          ignore_ext_list=bb_ext_list)
            if CompareJsonKeys.DIFF in text_cmp_result.keys():
                for cmp_info in text_cmp_result[CompareJsonKeys.DIFF][CompareJsonKeys.INFO]:
                    result[CompareJsonKeys.DIFF][CompareJsonKeys.INFO].append(cmp_info)
                errors = self.get_errors(text_cmp_result[CompareJsonKeys.DIFF][
                                             CompareJsonKeys.INFO])
                for key in errors:
                    result[CompareJsonKeys.DIFF][key] = errors[key]

            if CompareJsonKeys.CHANGE in text_cmp_result.keys():
                for cmp_info in text_cmp_result[CompareJsonKeys.CHANGE][CompareJsonKeys.INFO]:
                    result[CompareJsonKeys.CHANGE][CompareJsonKeys.INFO].append(cmp_info)
                errors = self.get_errors(text_cmp_result[CompareJsonKeys.CHANGE][
                                             CompareJsonKeys.INFO])
                for key in errors:
                    result[CompareJsonKeys.CHANGE][key] = errors[key]

            if CompareJsonKeys.ORIGIN in text_cmp_result.keys():
                for cmp_info in text_cmp_result[CompareJsonKeys.ORIGIN][CompareJsonKeys.INFO]:
                    result[CompareJsonKeys.ORIGIN][CompareJsonKeys.INFO].append(cmp_info)
                errors = self.get_errors(text_cmp_result[CompareJsonKeys.ORIGIN][
                                             CompareJsonKeys.INFO])
                for key in errors:
                    result[CompareJsonKeys.ORIGIN][key] = errors[key]

        # Check if have functionality export text layout -> Compare bounding box
        if PhocrProject.functionalities.TEXT_LAYOUT in lower_functionalities:
            is_compare_folder = False
            print CompareResultConfig.TITLE_CMP_BB
            # Compare text files of reference data vs ground truth data
            language_lower = [x.lower() for x in self.spec_handler.get_tag(
                    tag=SpecKeys.Tags.LANGS)]
            is_arabic = "arabic" in language_lower
            ext_list = []
            for i in range(0, 100):
                ext_list.append("_{0}.txt".format(i))
            bb_worker = CompareBoundingBox(is_arabic=is_arabic)
            bb_cmp_result =\
                self.compare_using_worker(o_folder, r_folder, g_folder,
                                          ext_list, bb_worker,
                                          fd_cmp_o_vs_r[CompareJsonKeys.IS_CHANGE])
            # Export compare result for reference with ground truth
            for cmp_info in bb_cmp_result[CompareJsonKeys.ORIGIN][CompareJsonKeys.INFO]:
                result[CompareJsonKeys.ORIGIN][CompareJsonKeys.INFO].append(cmp_info)
            errors = self.get_detail_errors(bb_cmp_result[CompareJsonKeys.ORIGIN][
                                                CompareJsonKeys.INFO])
            for key in errors:
                result[CompareJsonKeys.ORIGIN][key] = errors[key]
            # Try to export compare result for change with reference data
            if CompareJsonKeys.DIFF in bb_cmp_result.keys():
                if bb_cmp_result[CompareJsonKeys.DIFF][CompareJsonKeys.INFO]:
                    for cmp_info in bb_cmp_result[CompareJsonKeys.DIFF][CompareJsonKeys.INFO]:
                        result[CompareJsonKeys.DIFF][
                            CompareJsonKeys.INFO].append(cmp_info)
                    errors = self.get_detail_errors(
                        bb_cmp_result[CompareJsonKeys.DIFF][
                            CompareJsonKeys.INFO])
                    for key in errors:
                        result[CompareJsonKeys.DIFF][key] = errors[key]

            # Try to export compare result for change with ground truth data
            if CompareJsonKeys.CHANGE in bb_cmp_result.keys():
                for cmp_info in bb_cmp_result[CompareJsonKeys.CHANGE][CompareJsonKeys.INFO]:
                    result[CompareJsonKeys.CHANGE][CompareJsonKeys.INFO].append(cmp_info)
                errors = self.get_detail_errors(bb_cmp_result[CompareJsonKeys.CHANGE][
                                                    CompareJsonKeys.INFO])
                for key in errors:
                    result[CompareJsonKeys.CHANGE][key] = errors[key]

        # Office files compare results
        is_cmp_office = False
        ext_list = []
        title = "Compare office"
        if PhocrProject.functionalities.EXPORT_EXCEL in lower_functionalities:
            print CompareResultConfig.TITLE_CMP_EXCEL
            ext_list.append(".xlsx")
            title = CompareResultConfig.TITLE_CMP_EXCEL
            is_cmp_office = True
        if PhocrProject.functionalities.EXPORT_DOCX in lower_functionalities:
            print CompareResultConfig.TITLE_CMP_DOCX
            ext_list.append(".docx")
            title = CompareResultConfig.TITLE_CMP_DOCX
            is_cmp_office = True
        if PhocrProject.functionalities.EXPORT_PPTX in lower_functionalities:
            print CompareResultConfig.TITLE_CMP_PPTX
            ext_list.append(".pptx")
            title = CompareResultConfig.TITLE_CMP_PPTX
            is_cmp_office = True
        if is_cmp_office:
            is_compare_folder = False
            office_worker = CompareOfficeFile(title)
            office_cmp_result = self.compare_using_worker(o_folder, r_folder, g_folder,
                                                          ext_list, office_worker,
                                                          fd_cmp_o_vs_r[CompareJsonKeys.IS_CHANGE])
            office_cmp_result[CompareJsonKeys.TITLE] = title
            result[CompareJsonKeys.DIFF][CompareJsonKeys.INFO].append(office_cmp_result)

        # PDF/A files compare result
        if PhocrProject.functionalities.EXPORT_PDFA in lower_functionalities \
                or PhocrProject.functionalities.EXPORT_PDFA_BIN in lower_functionalities \
                or PhocrProject.functionalities.EXPORT_PDFA_HALFTONE in lower_functionalities \
                or PhocrProject.functionalities.EXPORT_PDFA_PHOTO_HALFTONE in lower_functionalities \
                or PhocrProject.functionalities.NO_OCR_PDF in lower_functionalities:
            is_compare_folder = False
            print CompareResultConfig.TITLE_CMP_PDFA
            ext_list = [".pdf"]
            pdfa_worker = ComparePdf()
            pdfa_cmp_result = self.compare_using_worker(o_folder, r_folder, g_folder,
                                                        ext_list, pdfa_worker,
                                                        fd_cmp_o_vs_r[CompareJsonKeys.IS_CHANGE])
            pdfa_cmp_result[CompareJsonKeys.TITLE] = CompareResultConfig.TITLE_CMP_PDFA
            result[CompareJsonKeys.DIFF][CompareJsonKeys.INFO].append(pdfa_cmp_result)
        # Check if output is changed with reference data
        if not is_compare_folder:
            result[CompareJsonKeys.IS_CHANGE] = False
            for cmp_info in result[CompareJsonKeys.DIFF][CompareJsonKeys.INFO]:
                if cmp_info[CompareJsonKeys.IS_CHANGE]:
                    result[CompareJsonKeys.IS_CHANGE] = True
                    break
        else:
            print CompareResultConfig.TITLE_CMP_FOLDER
            result[CompareJsonKeys.DIFF][CompareJsonKeys.TITLE] = \
                CompareResultConfig.TITLE_CMP_FOLDER
            result[CompareJsonKeys.DIFF][CompareJsonKeys.INFO] = fd_cmp_o_vs_r[CompareJsonKeys.INFO]

        # Compare stderr and stdout of reference data and output data
        compare_test_result = CompareFolderTestResult(self.test_folder, self.test_id)
        is_stdout_changed = compare_test_result.is_file_changed(r_folder, o_folder,
                                                                FinalTestResult.Test.STDOUT_FILE_NAME)
        is_stderr_changed = compare_test_result.is_file_changed(r_folder, o_folder,
                                                                FinalTestResult.Test.STDERR_FILE_NAME)
        result[CompareJsonKeys.DIFF][CompareJsonKeys.IS_STDOUT_CHANGED] = is_stdout_changed
        result[CompareJsonKeys.DIFF][CompareJsonKeys.IS_STDERR_CHANGED] = is_stderr_changed
        if is_stdout_changed or is_stderr_changed:
            result[CompareJsonKeys.IS_CHANGE] = True
        # If output not change with reference, delete compare result between output with reference
        # and output with ground truth
        if result[CompareJsonKeys.IS_CHANGE] is False:
            del result[CompareJsonKeys.CHANGE]
            del result[CompareJsonKeys.DIFF]
        is_change_result_exist = CompareJsonKeys.CHANGE in result \
            and len(result[CompareJsonKeys.CHANGE][CompareJsonKeys.INFO]) == 0
        if is_change_result_exist:
            del result[CompareJsonKeys.CHANGE]

        return result