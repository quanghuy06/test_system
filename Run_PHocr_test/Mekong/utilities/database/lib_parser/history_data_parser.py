# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      11/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from abc import ABCMeta
from database.lib_parser.tsv_parser import TsvParser
from database.lib_exporter.history_data_exporter import HDEConfiguration
from report.lib_base.history_data_informer import HistoryDataConfiguration
from baseapi.common import get_list_defined_string


class HistoryDataParser(TsvParser):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(HistoryDataParser, self).__init__(**kwargs)

    def set_up_attributes(self):
        self.header_line = 0
        # Set up list of valid headers
        self.headers_check_list = list()
        self.headers_check_list += get_list_defined_string(
            HistoryDataConfiguration.BbAccuracy)
        self.headers_check_list += get_list_defined_string(
            HistoryDataConfiguration.TextAccuracy)
        self.headers_check_list += get_list_defined_string(
            HistoryDataConfiguration.Performance)
        self.headers_check_list += get_list_defined_string(
            HistoryDataConfiguration.MemoryInfo)
        self.data = {}

    def get_header_type(self, header):
        if header == HistoryDataConfiguration.Performance.TIME:
            return float
        elif header == HDEConfiguration.TEST_NAME:
            return str
        else:
            return int
