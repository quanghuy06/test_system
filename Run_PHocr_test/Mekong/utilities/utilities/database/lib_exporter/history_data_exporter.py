# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from abc import ABCMeta

from configs.database import SpecKeys
from database.lib_base.test_case_manager import TestCaseManager
from report.lib_base.history_data_informer import HistoryDataInformer
from report.lib_base.tsv_reporter import TsvReporter


class HDEConfiguration(object):

    TEST_NAME = "Test case"
    FILE_DEFAULT = "HistoryData.tsv"


class HistoryDataExporter(TsvReporter):

    __metaclass__ = ABCMeta

    def __init__(self, platform, product, version, filters=None, **kwargs):
        super(HistoryDataExporter, self).__init__(**kwargs)
        self.platform = platform
        self.product = product
        self.version = version
        if not self.output_file_set:
            self.output_file = HDEConfiguration.FILE_DEFAULT
        self.filters = filters
        if not self.filters:
            self.filters = {}
        self.history_informer = HistoryDataInformer(product=self.product,
                                                    platform=self.platform)
        self.test_case_manager = TestCaseManager()
        self.headers = []
        self.list_test_names = []

    def collect_data(self):
        # Get list test names
        self.get_data_filter()

        # Get header
        self.headers = [HDEConfiguration.TEST_NAME]
        self.headers += HistoryDataInformer.get_bb_accuracy_headers()
        self.headers += HistoryDataInformer.get_text_accuracy_headers()
        self.headers += HistoryDataInformer.get_performance_headers()
        self.headers += HistoryDataInformer.get_memory_peak_header()

    def get_data_filter(self):
        spec_infos = self.test_case_manager.query_by_filters(self.filters, find_option={
            SpecKeys.ID: 1,
            SpecKeys.HISTORY_DATA: 1
        })
        self.data = {}
        for spec_info in spec_infos:
            test_name = spec_info[SpecKeys.ID]
            self.list_test_names.append(test_name)
            self.data[test_name] = {}
            self.data[test_name] = spec_info[SpecKeys.HISTORY_DATA]
        self.list_test_names = sorted(self.list_test_names)

    def get_line_data(self, test_name):
        line_data = list()
        line_data.append(test_name)
        line_data += self.history_informer.get_bb_accuracy(test_id=test_name,
                                                           delta=self.version)
        line_data += self.history_informer.get_text_accuracy(test_id=test_name,
                                                             delta=self.version)
        line_data.append(self.history_informer.get_time(test_id=test_name,
                                                        delta=self.version))
        line_data.append(
            self.history_informer.get_memory_peak(test_id=test_name,
                                                  delta=self.version))
        return line_data
