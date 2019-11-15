# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      18/07/2018
# Updated by:       Phung Dinh Tai
# Description:
import io
import platform
from junit_xml import TestSuite, TestCase
from abc import ABCMeta
from report.lib_base.reporter import Reporter
from handlers.test_result_handler import TestResultHandler
from handlers.compare_handlers.compare_result_handler import CompareResultHandler
from report.lib_summary_report.defines import ErrorFlags


class JXRConfiguration(object):
    FILE_NAME_DEFAULT = "test_result.xml"
    OUTPUT_CHANGED = "Output changed"
    TEST_SUITE = "MekongTestSystem"


class JunitXmlReporter(Reporter):

    __metaclass__ = ABCMeta

    def __init__(self, test_file, compare_file, **kwargs):
        self.test_file = test_file
        self.compare_file = compare_file
        super(JunitXmlReporter, self).__init__(**kwargs)
        if not self.output_file_set:
            self.output_file = JXRConfiguration.FILE_NAME_DEFAULT
        self.changed_list = []
        self.not_changed_list = []
        self.error_list = []

        # Set up handler for test result
        self.test_result_handler = TestResultHandler(input_file=self.test_file)

        # Set up handler for compare result
        self.cmp_result_handler = CompareResultHandler(input_file=compare_file)

    def collect_data(self):
        # Get error list tests
        self.error_list = self.test_result_handler.get_list_error_tests()
        # Get changed list tests
        test_list = self.cmp_result_handler.get_list_changed_tests()
        for test_name in test_list:
            if test_name not in self.error_list:
                self.changed_list.append(test_name)
        # Get not changed list tests
        test_list = self.cmp_result_handler.get_list_not_changed_tests()
        for test_name in test_list:
            if test_name not in self.error_list:
                self.not_changed_list.append(test_name)

    def do_work(self):

        # Collect data
        self.collect_data()

        # List of test cases
        test_cases = []
        plf = platform.platform()
        plf = plf.replace('.', '-')

        test_list = self.error_list + self.changed_list + self.not_changed_list
        # Add error test case
        for test_name in test_list:
            tc = TestCase(test_name, plf, self.test_result_handler.get_time(test_name),
                          self.test_result_handler.get_std_out(test_name),
                          self.test_result_handler.get_std_err(test_name))

            # Check if test case is error
            if test_name in self.error_list:
                tc.add_error_info(self.test_result_handler.get_exit_code(test_name))
                if self.test_result_handler.get_exit_code(test_name) < 0:
                    error_flag = ErrorFlags.F_CRASH
                else:
                    error_flag = ErrorFlags.F_GENERAL
                tc.add_failure_info(error_flag)

            # Check if test case is change
            if test_name in self.changed_list:
                failure_info = JXRConfiguration.OUTPUT_CHANGED + "\n"
                tc.add_failure_info(failure_info)

            # Append test cases to list
            test_cases.append(tc)

        ts = TestSuite(JXRConfiguration.TEST_SUITE, test_cases)

        with io.open(self.output_file, 'w+', encoding='utf8') as f:
            xml_str = TestSuite.to_xml_string([ts])
            f.write(unicode(xml_str))
