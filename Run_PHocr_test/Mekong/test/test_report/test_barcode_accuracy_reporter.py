import os
import sys_path
sys_path.insert_sys_path()

from report.lib_summary_report.barcode_accuracy_reporter import BarcodeAccuracyReporter
from test.test_base import TestBase

class TestBarcodeAccuracyReporter(TestBase):

    def test_report_normally(self):

        test_folder = os.path.join(self.overall_infor_data_dir, "spec")
        test_file = os.path.join(self.overall_infor_data_dir, 'test_result.json')
        compare_file = os.path.join(self.overall_infor_data_dir, 'compare_result.json')

        # Initial reporter
        reporter = BarcodeAccuracyReporter(test_file=test_file, compare_file=compare_file,
                                      test_folder=test_folder)

        # Do report
        reporter.do_work()
        output_file_name = "BarcodeAccuracyReport.xlsx"
        output_file_path = os.path.join(self.tmp_folder_path, output_file_name)
        self.assertTrue(os.path.isfile(output_file_path))