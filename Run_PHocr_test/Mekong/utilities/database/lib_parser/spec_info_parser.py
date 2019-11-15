# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Updated by:       Phung Dinh Tai
# Description:      Define base class for a tsv file parser
from abc import ABCMeta
from database.lib_parser.tsv_parser import TsvParser
from database.lib_exporter.spec_info_exporter import SIEConfiguration
from configs.database import SpecKeys, SpecHelper, FilterInterfaceConfig
from report.lib_base.tags_informer import TagsInformer


class SpecInfoParser(TsvParser):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(SpecInfoParser, self).__init__(**kwargs)

    def set_up_attributes(self):
        self.header_line = 0
        # Set up list of valid headers
        self.headers_check_list = [SpecKeys.PRODUCT, SpecKeys.COMPONENT, SpecKeys.FUNCTIONALITIES]
        self.headers_check_list += TagsInformer.get_tags_header()
        self.data = {}

    def get_header_type(self, header):
        if header == SpecKeys.PRODUCT:
            return str
        elif header == SpecKeys.COMPONENT:
            return str
        elif header == SpecKeys.FUNCTIONALITIES:
            return list
        elif header == SIEConfiguration.TEST_NAME:
            return str
        else:
            # Tag type
            return self.get_tag_real_type(tag_name=header)

    @staticmethod
    def get_tag_real_type(tag_name):
        if tag_name == SpecKeys.Tags.DOC_NAME:
            return unicode
        tag_type = SpecHelper.get_tag_type(tag_name=tag_name)
        if tag_type is None:
            return str
        elif tag_type == FilterInterfaceConfig.TYPE_BOOL:
            return bool
        elif tag_type == FilterInterfaceConfig.TYPE_FLOAT:
            return float
        elif tag_type == FilterInterfaceConfig.TYPE_INT:
            return int
        elif tag_type == FilterInterfaceConfig.TYPE_STR:
            return str
        elif tag_type == FilterInterfaceConfig.TYPE_LIST:
            return list
        else:
            return str
