# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      19/07/2018
# Description:

from handlers.parameters_handler import ParameterHandler
from manager.lib_distribution.filter_parser import parse_filters_message
from configs.database import SpecKeys, SpecHelper
from database.lib_base.test_case_manager import TestCaseManager
from configs.projects.phocr import PhocrProject
from configs.projects.hanoi import HanoiProject
from database.lib_base.collection_util import FilterExtraction, FilterInterfaceConfig


class CommitMessageValidator:
    def __init__(self, parameters):
        self.parameters = parameters
        self.parameters_handler = ParameterHandler(input_file=self.parameters)
        self.db_helper = SpecHelper()
        self.tc_manager = TestCaseManager()
        self.extractor = FilterExtraction()
        self.list_delimiter = [FilterInterfaceConfig.LIST_DELIMITER,
                          FilterInterfaceConfig.AND_DELIMITER,
                          FilterInterfaceConfig.OR_DELIMITER]

    # Get list functions
    def get_list_function(self, func_str):
        phocr_funcs = []
        barcode_funcs = []
        list_str = self.extractor.extract_list_con(func_str, self.list_delimiter)
        for con_str in list_str:
            if con_str not in self.list_delimiter:
                # Check function is phocr's function or barcode's function
                functionlities = self.db_helper.get_list_functionality()
                phocr_funcs = functionlities[PhocrProject.PRODUCT][
                    PhocrProject.components.DEFAULT]
                barcode_funcs = functionlities[PhocrProject.PRODUCT][
                    PhocrProject.components.BARCODE]
        list_funcs = phocr_funcs + barcode_funcs
        return list_funcs

    # Get list string which are not tag
    def get_list_not_tags(self, tags_str):
        list_delimiter = [FilterInterfaceConfig.AND_DELIMITER,
                          FilterInterfaceConfig.OR_DELIMITER]
        list_con = self.extractor.extract_list_con(tags_str, list_delimiter)
        list_not_tag = []
        for con_str in list_con:
            if con_str not in list_delimiter:
                key, value = self.extractor.extract_tag_value(con_str)
                check_key_value = self.db_helper.is_valid_tag(key, value)
                if not check_key_value or check_key_value is None:
                    list_not_tag.append(key)
        return list_not_tag

    # Check information in message is correct or not
    def is_valid_info(self, str, list_value):
        delimiter_split = " "
        for delimiter in self.list_delimiter:
            if delimiter in str:
                delimiter_split = delimiter
        list_value_lower = []
        for value in list_value:
            list_value_lower.append(value.lower())
        list_error = []
        for key in str.split(delimiter_split):
            if key not in list_value_lower:
                list_error.append(key)
        if list_error:
            print "{0} are/is incorrect!".format(list_error)
            return False
        else:
            return True

    def check_filter_commit(self):
        is_message_good = True
        # Get filter commit message
        commit_message = self.parameters_handler.get_commit()
        filter_commit = parse_filters_message(commit_message)
        # Check filter commit message
        if not filter_commit:
            print "There is no filtering in the message!"
            return is_message_good
        for key in filter_commit:
            if key == SpecKeys.ID:
                ids_str = filter_commit[SpecKeys.ID]
                # Check if ID is wrong -> exit system
                ids_not_exist = []
                for id_str in ids_str.split(","):
                    if not self.tc_manager.is_test_case_on_db(id_str):
                        ids_not_exist.append(id_str)
                if ids_not_exist:
                    print "\nTest case {0} doesn't exist!!!\n" \
                          "".format(ids_not_exist)
                    is_message_good = False
                else:
                    is_message_good = True

            if key == SpecKeys.PRODUCT:
                pro_str = filter_commit[SpecKeys.PRODUCT]
                list_product = self.db_helper.get_list_product()
                is_message_good = self.is_valid_info(pro_str, list_product)

            if key == SpecKeys.COMPONENT:
                com_str = filter_commit[SpecKeys.COMPONENT]
                list_component = self.db_helper.get_list_component()
                # Get PHOcr components
                phocr_component = []
                for phocr_com in list_component[PhocrProject.PRODUCT]:
                    phocr_component.append(phocr_com.lower())
                # Get HaNoi components
                hanoi_component = []
                for hanoi_com in list_component[HanoiProject.PRODUCT]:
                    hanoi_component.append(hanoi_com.lower())
                all_components = phocr_component + hanoi_component
                is_message_good = self.is_valid_info(com_str, all_components)

            if key == SpecKeys.FUNCTIONALITIES:
                func_str = filter_commit[SpecKeys.FUNCTIONALITIES]
                list_funcs = self.get_list_function(func_str)
                is_message_good = self.is_valid_info(func_str, list_funcs)

            if key == SpecKeys.TAGS:
                tags_str = filter_commit[SpecKeys.TAGS]
                list_not_tag = self.get_list_not_tags(tags_str)
                if list_not_tag:
                    print "\nTags/Tag {0} are/is incorrect!!!" \
                          "\n".format(list_not_tag)
                    is_message_good = False
                else:
                    is_message_good = True
        return is_message_good
