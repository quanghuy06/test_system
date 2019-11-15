import unittest
import os
import shutil

from report.lib_summary_report.overall_information_reporter import OverallInformationReporter


class TestOverallInfoReporter(unittest.TestCase):
    def test_report_normally(self):

        script_dir = os.path.dirname(__file__)
        data_dir = os.path.join(os.path.dirname(script_dir), "data")
        overall_infor_data_dir = os.path.join(data_dir, "report/overall_info_reporter")
        test_folder = os.path.join(overall_infor_data_dir, "spec")
        test_file = os.path.join(overall_infor_data_dir, 'test_result.json')
        compare_file = os.path.join(overall_infor_data_dir, 'compare_result.json')

        tmp_folder = "output_d41d8cd98f00b204e9800998ecf8427e"
        pwd = os.getcwd()
        tmp_folder_path = os.path.join(pwd, tmp_folder)
        if os.path.isdir(tmp_folder_path):
            shutil.rmtree(tmp_folder_path)
        os.makedirs(tmp_folder_path)
        os.chdir(tmp_folder_path)

        # Initial reporter
        platform = "linux"
        reporter = OverallInformationReporter(test_file=test_file, test_folder=test_folder,
                                              error_folder=None, compare_file=compare_file,
                                              platform=platform)

        # Do report
        reporter.do_work()
        output_file_name = "OverallInformation.txt"
        output_file_path = os.path.join(tmp_folder_path, output_file_name)
        self.assertTrue(os.path.isfile(output_file_path))

        #post process
        # Delete tmp folder
        os.chdir(pwd)
        shutil.rmtree(tmp_folder_path)