# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/07/2018
# Updated by:       Phung Dinh Tai
# Description:      Define base class for a delta reporter which get data from MekongDB
from abc import ABCMeta, abstractmethod

from configs.database import SpecKeys
from database.lib_base.test_case_manager import TestCaseManager
from report.lib_base.history_data_informer import HistoryDataInformer, HistoryDataConfiguration
from report.lib_base.tags_informer import TagsInformer
from report.lib_base.xlsx_reporter import XlsxReporter


class DeltaReporter(XlsxReporter):
    __metaclass__ = ABCMeta

    def __init__(self, platform, **kwargs):
        self.platform = platform
        super(DeltaReporter, self).__init__(**kwargs)
        self.test_cases_manager = TestCaseManager()
        self.tags_informer = None
        self.phocr_test_machine_informer = None
        self.esdk_informer = None
        self.list_test_names = []
        self.deltas = []
        self.line_start_data = 0
        self.line_end_data = 0
        self.current_delta = 0
        self.list_tags = []
        self.tag_data = {}
        self.tag_headers = []
        self.ignore_tags = [SpecKeys.Tags.BUG_LIST,
                            SpecKeys.Tags.CMD_OPTION,
                            SpecKeys.Tags.DOC_NAME,
                            SpecKeys.Tags.DOC_PAGE,
                            SpecKeys.Tags.ACCURACY,
                            SpecKeys.Tags.IS_NON_INTEGRATION,
                            SpecKeys.Tags.IS_MEMCHECK_PEAK,
                            SpecKeys.Tags.IS_EXTREME_TEST]
        self.headers = []
        self.primary_conditions_string = ""

    def collect_data(self):
        self.logger.start_step("Prepare data")
        # Initial tags informer
        self.get_tags_data()
        self.tags_informer = TagsInformer(data=self.tag_data)
        # Initial history data informer
        self.get_history_data()
        self.phocr_test_machine_informer = \
            HistoryDataInformer(product=HistoryDataConfiguration.Product.PHOCR_TEST_MACHINE,
                                platform=self.platform, data=self.data)
        self.esdk_informer = \
            HistoryDataInformer(product=HistoryDataConfiguration.Product.ESDK,
                                platform=self.platform, data=self.data)
        # Get informers for history data of other products
        self.get_some_history_informers()

        # Get list of test names
        self.get_list_test_names()

        # Get delta list
        self.get_deltas_report_list()
        if self.deltas:
            self.current_delta = self.deltas[0]
        else:
            self.current_delta = 0

        # Range of data in raw data sheets
        self.line_start_data = 1
        self.line_end_data = self.line_start_data + len(self.list_test_names)
        self.list_tags = self.tags_informer.get_tags_header()
        self.tag_headers = [item for item in self.list_tags if item not in self.ignore_tags]
        self.private_headers = self.get_private_headers()
        # Headers of raw data sheet
        self.headers = self.private_headers + self.tag_headers
        # Create mapping
        self.create_mappings()
        # Get primary conditions string for collecting data
        self.primary_conditions_string = self.get_primary_conditions_string_for_all_delta()
        # Prepare some more data
        self.prepare_private_data()
        self.logger.end_step(True)

    @abstractmethod
    def get_filters(self):
        pass

    @abstractmethod
    def get_private_headers(self):
        pass

    def get_tags_data(self):
        filters = self.get_filters()
        spec_infos = self.test_cases_manager.query_by_filters(filters_str=filters, find_option={
            SpecKeys.TAGS: 1
        })
        for spec_info in spec_infos:
            self.tag_data[spec_info[SpecKeys.ID]] = spec_info[SpecKeys.TAGS]

    def get_history_data(self):
        self.data = {}
        filters = self.get_filters()
        spec_infos = self.test_cases_manager.query_by_filters(filters_str=filters, find_option={
            SpecKeys.HISTORY_DATA: 1
        })
        for spec_info in spec_infos:
            self.data[spec_info[SpecKeys.ID]] = spec_info[SpecKeys.HISTORY_DATA]

    def get_list_test_names(self):
        filters = self.get_filters()
        spec_infos = self.test_cases_manager.query_by_filters(filters_str=filters, only_id=True)
        for spec_info in spec_infos:
            self.list_test_names.append(spec_info[SpecKeys.ID])
        self.list_test_names = sorted(self.list_test_names)
        self.recheck_list_test_names()

    @abstractmethod
    def recheck_list_test_names(self):
        pass

    def create_mappings(self):
        # Line mapping
        start_line = 1
        for test_name in self.list_test_names:
            self.line_mapping[test_name] = start_line
            start_line += 1
        # Column mapping
        for i in range(0, len(self.headers)):
            self.column_mapping[self.headers[i]] = i

    def get_range_string(self, delta, header):
        column = self.column_mapping[header]
        sheet_name = self.get_delta_sheet_name(delta=delta)
        return self.get_range_formula(sheet=sheet_name, column=column,
                                      line_start=self.line_start_data, line_end=self.line_end_data)

    def get_condition_string(self, delta, header, value):
        column = self.column_mapping[header]
        sheet_name = self.get_delta_sheet_name(delta=delta)
        return self.get_condition_formula(sheet=sheet_name, column=column,
                                          line_start=self.line_start_data,
                                          line_end=self.line_end_data, value=value)

    # Create a template that real sheet name should replace "SHEET_NAME" string in template
    def get_condition_template(self, header, value):
        column = self.column_mapping[header]
        return self.get_condition_formula(sheet="SHEET_NAME", column=column,
                                          line_start=self.line_start_data,
                                          line_end=self.line_end_data, value=value)

    # Get cell reference
    def get_cell_reference(self, sheet_name, test_name, header):
        line = self.line_mapping[test_name]
        column = self.column_mapping[header]
        cell_str = self.get_cell_str(line_idx=line, col_idx=column)
        return "=\'{sheet_name}\'!{cell_str}".format(sheet_name=sheet_name, cell_str=cell_str)

    @abstractmethod
    def get_deltas_report_list(self):
        pass

    @abstractmethod
    def get_some_history_informers(self):
        pass

    @abstractmethod
    def get_delta_sheet_name(self, delta):
        pass

    @abstractmethod
    def get_primary_conditions_string_for_all_delta(self):
        pass

    @abstractmethod
    def prepare_private_data(self):
        pass
