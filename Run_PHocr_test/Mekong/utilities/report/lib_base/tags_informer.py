# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from baseapi.common import format_string
from configs.database import SpecKeys, SpecChecking
from database.lib_base.test_case_manager import TestCaseManager


class TagsInformer(object):

    def __init__(self, data=None):
        self.test_cases_manager = TestCaseManager()
        self.data = data

    @staticmethod
    def get_tags_header():
        tags_defined = SpecChecking[SpecKeys.TAGS]
        return sorted(tags_defined.iterkeys())

    def get_tags_value(self, test_id, list_tags=None):
        tags_value = []
        if list_tags:
            list_all_tags = list_tags
        else:
            list_all_tags = self.get_tags_header()
        for tag_name in list_all_tags:
            if self.data:
                if tag_name in self.data[test_id].keys():
                    tag_value = self.data[test_id][tag_name]
                else:
                    tag_value = None
            else:
                tag_value = self.test_cases_manager.get_tag(test_id=test_id,
                                                            tag_name=tag_name)
            tags_value.append(format_string(tag_value))
        return tags_value
