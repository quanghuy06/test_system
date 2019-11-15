# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from configs.database import SpecKeys
from database.lib_base.test_case_manager import TestCaseManager


class HistoryDataConfiguration(object):

    class Product(object):
        PHOCR_TEST_MACHINE = "phocr_test_machine"
        PHOCR_ON_BOARD = "phocr_on_board"
        ESDK = "esdk"
        ABBYY_CLIENT = "abbyy_client"
        TESSERACT = "tesseract"

    class BbAccuracy(object):
        TOTAL_CHARACTERS = "Total characters bounding box"
        TOTAL_ERRORS = "Total errors bounding box"
        INSERT_ERRORS = "Insert errors bounding box"
        DELETE_ERRORS = "Delete errors bounding box"
        REPLACE_ERRORS = "Replace errors bounding box"

    class TextAccuracy(object):
        TOTAL_CHARACTERS = "Total characters text"
        TOTAL_ERRORS = "Total errors text"
        DELETE_ERRORS = "Delete errors text"
        INSERT_ERRORS = "Insert errors text"
        REPLACE_ERRORS = "Replace errors text"

    class Performance(object):
        TIME = "Time execute"

    class MemoryInfo(object):
        PEAK_INFO = "Memory peak"


class HistoryDataInformer(object):

    def __init__(self, product, platform, data=None, report_title=None):
        self.product = product
        self.platform = platform
        self.test_cases_manager = TestCaseManager()
        self.data = data
        self.report_title = report_title

    def get_history_data(self):
        self.data = {}
        filters = {}
        spec_infos = self.test_cases_manager.query_by_filters(filters_str=filters, find_option={
            SpecKeys.HISTORY_DATA: 1
        })
        for spec_info in spec_infos:
            self.data[spec_info[SpecKeys.ID]] = spec_info[SpecKeys.HISTORY_DATA]

    @staticmethod
    def get_bb_accuracy_headers():
        return [HistoryDataConfiguration.BbAccuracy.DELETE_ERRORS,
                HistoryDataConfiguration.BbAccuracy.INSERT_ERRORS,
                HistoryDataConfiguration.BbAccuracy.REPLACE_ERRORS,
                HistoryDataConfiguration.BbAccuracy.TOTAL_ERRORS,
                HistoryDataConfiguration.BbAccuracy.TOTAL_CHARACTERS]

    @staticmethod
    def get_text_accuracy_headers():
        return [HistoryDataConfiguration.TextAccuracy.DELETE_ERRORS,
                HistoryDataConfiguration.TextAccuracy.INSERT_ERRORS,
                HistoryDataConfiguration.TextAccuracy.REPLACE_ERRORS,
                HistoryDataConfiguration.TextAccuracy.TOTAL_ERRORS,
                HistoryDataConfiguration.TextAccuracy.TOTAL_CHARACTERS]

    @staticmethod
    def get_performance_headers():
        return [HistoryDataConfiguration.Performance.TIME]

    @staticmethod
    def get_memory_peak_header():
        return [HistoryDataConfiguration.MemoryInfo.PEAK_INFO]

    def get_list_deltas_of_test(self, test_id):
        if self.data:
            history_data = self.data[test_id][self.platform]
        else:
            history_data = self.test_cases_manager.get_history_data(
                test_id=test_id, platform=self.platform)
        if not history_data:
            return []
        # Get data of product
        if self.product in history_data.keys():
            product_data = history_data[self.product]
        else:
            return []
        deltas = []
        for key in product_data.keys():
            deltas.append(key)
        for i in range(0, len(deltas)):
            deltas[i] = int(deltas[i])
        return sorted(deltas, reverse=True)

    def get_list_deltas(self):
        if not self.data:
            return []
        list_deltas = []
        for test_id in self.data:
            test_deltas = self.get_list_deltas_of_test(test_id=test_id)
            for delta in test_deltas:
                if delta not in list_deltas:
                    list_deltas.append(delta)
        for i in range(0, len(list_deltas)):
            list_deltas[i] = int(list_deltas[i])
        return sorted(list_deltas, reverse=True)

    def get_data_delta(self, test_id, delta):
        if self.data:
            history_data = self.data[test_id][self.platform]
        else:
            history_data = self.test_cases_manager.get_history_data(
                test_id=test_id, platform=self.platform)
        if history_data is None:
            return None
        # Get data of product
        if self.product in history_data.keys():
            product_data = history_data[self.product]
        else:
            return None
        if product_data:
            # Get data of delta version
            delta_string = str(delta)
            if delta_string in product_data.keys():
                delta_data = product_data[delta_string]
            else:
                delta_data = None
            return delta_data
        else:
            return None

    # Get bounding box accuracy information
    def get_bb_accuracy(self, test_id, delta):
        bb_accuracy_info = []
        delta_data = self.get_data_delta(test_id=test_id, delta=delta)
        # Export values
        for header in self.get_bb_accuracy_headers():
            if not delta_data:
                bb_accuracy_info.append("")
            elif header in delta_data.keys():
                bb_accuracy_info.append(delta_data[header])
            else:
                bb_accuracy_info.append("")
        return bb_accuracy_info

    # Get total bounding box errors
    def get_bb_total_errors(self, test_id, delta):
        delta_data = self.get_data_delta(test_id=test_id, delta=delta)
        if not delta_data:
            return ""
        else:
            return delta_data[HistoryDataConfiguration.BbAccuracy.TOTAL_ERRORS]

    # Get text accuracy information
    def get_text_accuracy(self, test_id, delta):
        text_accuracy_info = []
        delta_data = self.get_data_delta(test_id=test_id, delta=delta)
        # Export values
        for header in self.get_text_accuracy_headers():
            if not delta_data:
                text_accuracy_info.append("")
            elif header in delta_data.keys():
                text_accuracy_info.append(delta_data[header])
            else:
                text_accuracy_info.append(None)
        return text_accuracy_info

    # Get total text errors
    def get_text_total_errors(self, test_id, delta):
        delta_data = self.get_data_delta(test_id=test_id, delta=delta)
        if not delta_data:
            return ""
        elif HistoryDataConfiguration.TextAccuracy.TOTAL_ERRORS not in delta_data:
            return ""
        else:
            return delta_data[HistoryDataConfiguration.TextAccuracy.TOTAL_ERRORS]

    # Get text accuracy information
    def get_time(self, test_id, delta):
        delta_data = self.get_data_delta(test_id=test_id, delta=delta)
        if not delta_data:
            return ""
        if HistoryDataConfiguration.Performance.TIME in delta_data:
            return delta_data[HistoryDataConfiguration.Performance.TIME]
        else:
            return ""

    def get_memory_peak(self, test_id, delta):
        """
        Get memory peak information

        Parameters
        ----------
        test_id: test case name.
        delta: delta which need to get memory peak information.

        Returns
        -------
        int: memory peak information.

        """
        delta_data = self.get_data_delta(test_id, delta)
        if not delta_data:
            return ""
        if HistoryDataConfiguration.MemoryInfo.PEAK_INFO in delta_data:
            return delta_data[HistoryDataConfiguration.MemoryInfo.PEAK_INFO]
        else:
            return ""
