# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from abc import ABCMeta

from baseapi.common import format_string
from configs.database import SpecKeys
from database.lib_base.test_case_manager import TestCaseManager
from report.lib_base.tags_informer import TagsInformer
from report.lib_base.tsv_reporter import TsvReporter


class SIEConfiguration(object):

    TEST_NAME = "Test case"
    FILE_DEFAULT = "SpecInfoDb.tsv"


class SpecInfoExporter(TsvReporter):

    __metaclass__ = ABCMeta

    def __init__(self, filters=None, **kwargs):
        super(SpecInfoExporter, self).__init__(**kwargs)
        if not self.output_file_set:
            self.output_file = SIEConfiguration.FILE_DEFAULT
        self.filters = filters
        if not self.filters:
            self.filters = {}
        self.test_case_manager = TestCaseManager()
        self.tags_informer = TagsInformer()
        self.tags_data = {}
        self.base_data = {}

    def collect_data(self):
        # Get list test names
        self.get_data_filter()

        # Initial data for tags informer
        self.tags_informer.data = self.tags_data

        # Get header
        self.headers = [SIEConfiguration.TEST_NAME, SpecKeys.PRODUCT, SpecKeys.COMPONENT,
                        SpecKeys.FUNCTIONALITIES]
        self.headers += self.tags_informer.get_tags_header()

    def get_data_filter(self):
        spec_infos = self.test_case_manager.query_by_filters(self.filters, find_option={
            SpecKeys.ID: 1,
            SpecKeys.PRODUCT: 1,
            SpecKeys.COMPONENT:1,
            SpecKeys.FUNCTIONALITIES: 1,
            SpecKeys.TAGS: 1
        })
        for spec_info in spec_infos:
            test_name = spec_info[SpecKeys.ID]
            self.list_test_names.append(test_name)
            self.tags_data[test_name] = spec_info[SpecKeys.TAGS]
            self.base_data[test_name] = {}
            self.base_data[test_name][SpecKeys.PRODUCT] = spec_info[SpecKeys.PRODUCT]
            self.base_data[test_name][SpecKeys.COMPONENT] = spec_info[SpecKeys.COMPONENT]
            self.base_data[test_name][SpecKeys.FUNCTIONALITIES] = spec_info[
                SpecKeys.FUNCTIONALITIES]
        self.list_test_names = sorted(self.list_test_names)

    def get_line_data(self, test_name):
        line_data = list()
        line_data.append(test_name)
        line_data.append(format_string(self.base_data[test_name][SpecKeys.PRODUCT]))
        line_data.append(format_string(self.base_data[test_name][SpecKeys.COMPONENT]))
        line_data.append(format_string(self.base_data[test_name][SpecKeys.FUNCTIONALITIES]))
        line_data += self.tags_informer.get_tags_value(test_id=test_name)
        return line_data
