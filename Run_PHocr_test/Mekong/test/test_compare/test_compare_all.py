import os
import filecmp
import shutil
from test.test_base import TestBase
from utilities.tests.compare_all import CompareAll


class Object(object):
    pass


class TestCompareAll(TestBase):

    def get_test_result_name(self):
        return "test_result.json"

    def get_compare_output_name(self):
        return "compare_result.json"

    def run_test_with_folder(self, data_path, platform):
        pwd = os.getcwd()
        data_abs_path = os.path.join(self.data_dir, data_path)
        compare_result_folder = os.path.join(self.tmp_folder_path, data_path)
        if os.path.isdir(compare_result_folder):
            shutil.rmtree(compare_result_folder)
        os.makedirs(compare_result_folder)
        os.chdir(compare_result_folder)
        test_folder = os.path.join(data_abs_path, "TESTS")
        result_json = os.path.join(data_abs_path, self.get_test_result_name())
        output_folder = os.path.join(compare_result_folder, "compare_output")

        cmp_executor = CompareAll(test_folder=test_folder,
                                  platform=platform,
                                  test_result=result_json,
                                  output_folder=output_folder)
        cmp_executor.do_work()

        output_file = os.path.join(compare_result_folder, self.get_compare_output_name())
        ground_truth_file = os.path.join(data_abs_path,
                                         "ground_truth",
                                         self.get_compare_output_name())

        is_same_with_gt = filecmp.cmp(output_file, ground_truth_file, False)
        self.assertTrue(is_same_with_gt)

    def test_compare_bb_on_linux(self):
        data_path = "test_compare/test_compare_all/compare_bb"
        platform = "linux"
        self.run_test_with_folder(data_path, platform)

    def test_compare_docx_on_linux(self):
        data_path = "test_compare/test_compare_all/compare_docx"
        platform = "linux"
        self.run_test_with_folder(data_path, platform)

    def test_compare_xlsx_on_linux(self):
        data_path = "test_compare/test_compare_all/compare_xlsx"
        platform = "linux"
        self.run_test_with_folder(data_path, platform)

    def test_compare_pptx_on_linux(self):
        data_path = "test_compare/test_compare_all/compare_pptx"
        platform = "linux"
        self.run_test_with_folder(data_path, platform)

    def test_compare_txt_on_linux(self):
        data_path = "test_compare/test_compare_all/compare_text"
        platform = "linux"
        self.run_test_with_folder(data_path, platform)

    def test_compare_pdf_on_linux(self):
        data_path = "test_compare/test_compare_all/compare_pdf"
        platform = "linux"
        self.run_test_with_folder(data_path, platform)

    def test_compare_std_on_linux(self):
        data_path = "test_compare/test_compare_all/compare_std"
        platform = "linux"
        self.run_test_with_folder(data_path, platform)

    def test_compare_junk_files_on_linux(self):
        data_path = "test_compare/test_compare_all/junk_files"
        platform = "linux"
        self.run_test_with_folder(data_path, platform)


    def test_compare_bb_on_windows(self):
        data_path = "test_compare/test_compare_all/windows/compare_bb"
        platform = "windows"
        self.run_test_with_folder(data_path, platform)