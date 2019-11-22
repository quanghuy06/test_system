# Toshiba - TSDV
# Project:      PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created: 27/06/2017
# Last update:  30/06/2017
# Updated by:   Phung Dinh Tai
# Description:  This define a class to handler json object of test case specification
from abc import ABCMeta
from configs.database import SpecKeys
from configs.projects.phocr import PhocrProject
from handlers.lib_base.json_handler import JsonHandler


class TestSpecHandler(JsonHandler):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(TestSpecHandler, self).__init__(**kwargs)

    # Get id of test case
    def get_id(self):
        return self.data[SpecKeys.ID]

    # Get error flags
    def get_error_flag(self, platform):
        return self.data[SpecKeys.ERROR_FLAGS][platform]

    # Check if test case has a tag or not
    def has_tag(self, tag_name):
        if tag_name in self.data[SpecKeys.TAGS]:
            return True
        else:
            return False

    # Get value of a tag
    def get_tag(self, tag):
        if self.has_tag(tag):
            return self.data[SpecKeys.TAGS][tag]
        else:
            return None

    # Add a tag
    def add_tag(self, key, value):
        if self.has_tag(key):
            print "Tag {0} has already existed!".format(key)
        else:
            self.data[SpecKeys.TAGS][key] = value
            self.save()

    # Update a tag
    def update_tag(self, key, value):
        if self.has_tag(key):
            self.data[SpecKeys.TAGS][key] = value
        else:
            print "Tag {0} does not exist!".format(key)

    # Get list of functionalities
    def get_functions(self):
        return self.data[SpecKeys.FUNCTIONALITIES]

    # Set functionalities
    def set_functions(self, value):
        self.data[SpecKeys.FUNCTIONALITIES] = value

    # Check if output is  output formatting
    def is_output_formatting(self):
        output_formatting_functions = [PhocrProject.functionalities.EXPORT_DOCX,
                                       PhocrProject.functionalities.EXPORT_EXCEL,
                                       PhocrProject.functionalities.EXPORT_PPTX,
                                       PhocrProject.functionalities.EXPORT_PDF,
                                       PhocrProject.functionalities.EXPORT_PDFA,
                                       PhocrProject.functionalities.EXPORT_PDFA_BIN,
                                       PhocrProject.functionalities.EXPORT_PDFA_HALFTONE,
                                       PhocrProject.functionalities.EXPORT_PDFA_PHOTO_HALFTONE,
                                       PhocrProject.functionalities.NO_OCR_PDF,
                                       PhocrProject.HN_functionalities.OUTPUT_FORMATS,
                                       PhocrProject.HN_functionalities.WORKFOLOW]
        functions = self.get_functions()
        for func in functions:
            if func in output_formatting_functions:
                return True
        return False

    # Get product of test case
    def get_product(self):
        return self.data[SpecKeys.PRODUCT]

    # Get component
    def get_component(self):
        return self.data[SpecKeys.COMPONENT]

    # Set component
    def set_component(self, value):
        self.data[SpecKeys.COMPONENT] = value

    # Get weight of test case
    def get_weight(self, platform):
        if (SpecKeys.WEIGHTS not in self.data.keys()) or \
                (platform not in self.data[SpecKeys.WEIGHTS]):
            # The first time test case is not updated weight for platform
            return 1
        else:
            return self.data[SpecKeys.WEIGHTS][platform]

    def get_history_data(self, platform):
        """
        Get history data information

        Parameters
        ----------
        platform: str
             Platform want to get the data

        Returns
        -------
        dict: history data information

        """
        if (SpecKeys.HISTORY_DATA not in self.data.keys()) or\
                (platform not in self.data[SpecKeys.HISTORY_DATA]):
            return ""
        else:
            return self.data[SpecKeys.HISTORY_DATA][platform]

    def get_product_info(self, platform, product):
        """
        Get information of product, it can be phocr_test_machine,
        phocr_on_board ...

        Parameters
        ----------
        platform: str
             Platform that we want to check
        product: str
             Product that we want to get the data, product maybe one of
             phocr_test_machine, phocr_on_board ...

        Returns
        -------
        dict: product information.

        """
        history_data = self.get_history_data(platform=platform)
        if history_data:
            if product not in history_data:
                return ""
            else:
                return history_data[product]
        else:
            return ""

    def get_list_delta(self, platform, product):
        """
        Get list delta correspond with platform and product that test case has

        Parameters
        ----------
        platform: str
             Platform we want to get the data
        product: str
             Product that we want to get the data, product can be one of
             phocr_test_machine, phocr_on_board ...

        Returns
        -------
        list: List delta that test case has correspond with platform and product
        """
        list_deltas = list()
        product_data = self.get_product_info(platform=platform, product=product)
        if product_data:
            for key in product_data.keys():
                list_deltas.append(key)
            for i in range(0, len(list_deltas)):
                list_deltas[i] = int(list_deltas[i])
            list_deltas = sorted(list_deltas, reverse=True)
        return list_deltas

    def get_max_delta(self, platform, product):
        """
        Get the latest delta of that test case has information correspond
        with product and platform.

        Parameters
        ----------
        platform: str
            Platform that we want to get the data.
        product: str
            Product that we want to get the data, it can be one of
            phocr_test_machine, phocr_on_board ...

        Returns
        -------
        int: max delta

        """
        list_deltas = self.get_list_delta(platform=platform, product=product)
        if list_deltas:
            return max(list_deltas)
        else:
            return None

    def get_delta_info(self, platform, delta, product):
        """
        Get information corresponding with delta

        Parameters
        ----------
        platform: str
             Platform that we want to check
        delta: int
             Delta that we want to get data.'
        product: str
             Product that we want to get the data, it can be phocr_test_machine,
        phocr_on_board ...

        Returns
        -------

        """
        product_data = self.get_product_info(platform=platform, product=product)
        if product_data:
            if str(delta) not in product_data:
                return ""
            else:
                delta_str = str(delta)
                return product_data[delta_str]
        else:
            return ""

    def get_mem_peak_info(self, platform, delta, product):
        """
        Get memory peak information

        Parameters
        ----------
        platform: str
             Platform that we want to get data.
        delta: int
             Delta that we want to get data
        product: str
             Product that we want to get the data, it can be phocr_test_machine,
             phocr_on_board ...

        Returns
        -------
        int: Memory peak information of test case
        """
        delta_data = self.get_delta_info(platform=platform,
                                         delta=delta,
                                         product=product)
        if delta_data:
            if SpecKeys.History_data.PEAK_INFO not in delta_data:
                return 0
            else:
                return int(delta_data[SpecKeys.History_data.PEAK_INFO])
        else:
            return 0

    def get_binary_test_information(self):
        """
        Get data in field "binary_test_information" in spec.json
        Returns
        -------
        dict:
            data inside field "binary_test_information"

        """
        return self.data[SpecKeys.BINARY_TEST_INFORMATION]

    def get_output(self):
        """
        Get data in field "output" in spec.json
        Returns
        -------
        list
            data inside field "output"

        """
        return self.data[SpecKeys.OUTPUT]


    # Save updated specs
    def save(self, target_file=None):
        if not target_file:
            target_file = self.input_file
        self.dump(output_file=target_file)

    # Update specification
    def update_spec(self, force_spec_info):
        for key in force_spec_info:
            if key == SpecKeys.TAGS:
                new_tag_info = force_spec_info[key]
                for tag_name in new_tag_info:
                    if self.has_tag(tag_name):
                        self.update_tag(tag_name, new_tag_info[tag_name])
                    else:
                        self.add_tag(tag_name, new_tag_info[tag_name])
    # TODO (Thanh) : Implement for other spec key

    def force_spec(self, force_spec_info):
        self.update_spec(force_spec_info)
        self.save(self.input_file)

    def update_execute_time_for_test_case(self, platform, ratio):
        self.data[SpecKeys.WEIGHTS][platform] = \
            self.get_weight(platform) * ratio
        self.save(self.input_file)
