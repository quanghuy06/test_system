import unittest
import os
import shutil

from utilities.report.lib_summary_report.bounding_box_accuracy_reporter import BbAccuracyReporter


class TestBase(unittest.TestCase):

    def setUp(self):
        self.pwd = os.getcwd()
        self.tmp_folder = "output_d41d8cd98f00b204e9800998ecf8427e"
        self.tmp_folder_path = os.path.join(self.pwd, self.tmp_folder)
        self.test_dir = os.path.dirname(__file__)
        self.mekong_dir = os.path.dirname(self.test_dir)
        self.data_dir = os.path.join(self.test_dir, "data")
        self.overall_infor_data_dir = os.path.join(self.data_dir,
                                                   "test_report/overall_info_reporter")
        self.prepare_and_chdir_to_tmp_folder()

    def tearDown(self):
        self.clean_test_result()
        #os.chdir(self.pwd)

    def prepare_and_chdir_to_tmp_folder(self):
        if not os.path.isdir(self.tmp_folder_path):
            os.makedirs(self.tmp_folder_path)
        self.assertFalse(os.chdir(self.tmp_folder_path))

    def clean_test_result(self):
        os.chdir(self.pwd)
        #shutil.rmtree(self.tmp_folder_path)


