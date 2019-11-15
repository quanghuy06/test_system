import os

from report.lib_summary_report.bounding_box_accuracy_reporter import BbAccuracyReporter
from test.test_base import TestBase

class TestBBAccuracyReporter(TestBase):

    def test_report_normally(self):
        test_folder = os.path.join(self.overall_infor_data_dir, "spec")
        test_file = os.path.join(self.overall_infor_data_dir, 'test_result.json')
        compare_file = os.path.join(self.overall_infor_data_dir, 'compare_result.json')
        change_number = 123
        delta = 222

        # Initial reporter
        reporter = BbAccuracyReporter(test_file=test_file, compare_file=compare_file,
                                      test_folder=test_folder, change_number=change_number,
                                      delta=delta)

        # Do report
        reporter.do_work()
        output_file_name = "BoundingBoxAccuracyReport_C123_D222.xlsx"
        output_file_path = os.path.join(self.tmp_folder_path, output_file_name)
        self.assertTrue(os.path.isfile(output_file_path))
