# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from abc import ABCMeta
from database.lib_parser.spec_info_parser import SpecInfoParser
from database.lib_updater.database_updater import DatabaseUpdater
from configs.database import SpecKeys
from report.lib_base.tags_informer import TagsInformer


class SpecInfoUpdater(DatabaseUpdater):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(SpecInfoUpdater, self).__init__(**kwargs)
        self.data_parser = None

    def get_data(self):
        self.data_parser = SpecInfoParser(input_file=self.input_file)
        self.data_parser.do_work()

    def update_data(self):
        # Check to update product information
        self.update_base_info()

        # Update tags value
        self.update_tag_value()

    def update_base_info(self):
        headers = [SpecKeys.PRODUCT, SpecKeys.COMPONENT, SpecKeys.FUNCTIONALITIES]
        for header in headers:
            if header in self.data_parser.data:
                data = self.data_parser.data[header]
                for test_name in data:
                    new_value = data[test_name]
                    if new_value is None:
                        continue
                    self.test_case_manager.update_spec_by_field(test_id=test_name,
                                                                field_name=header,
                                                                new_value=new_value)
                    if test_name not in self.updated_test_cases:
                        self.updated_test_cases.append(test_name)

    def update_tag_value(self):
        tag_headers = TagsInformer.get_tags_header()
        for header in tag_headers:
            if header in self.data_parser.data:
                data = self.data_parser.data[header]
                for test_name in data:
                    new_value = data[test_name]
                    if new_value is None:
                        continue
                    self.test_case_manager.update_tag(test_id=test_name, tag_name=header,
                                                      value=new_value)
                    if test_name not in self.updated_test_cases:
                        self.updated_test_cases.append(test_name)
