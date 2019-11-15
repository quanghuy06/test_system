# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      11/01/2019
from abc import ABCMeta, abstractmethod
from validate.lib_base.mekong_json_base import MekongJsonBase


class MekongList(MekongJsonBase):
    """

    Abstract class presents information with type list.
    For class which inherit this one, please implement these abstract class:
    + _validate_element_of_list()
    + _extract_data()

    """

    __metaclass__ = ABCMeta

    def __init__(self, element_type, **kwargs):
        super(MekongList, self).__init__(**kwargs)
        self.element_type = element_type
        self.element_list = list()

    def _valid_data_types(self):
        """
        Validate data types of this field is list
        :return:
        list
            list type
        """
        return [list]

    def _parse_data(self):
        """
        From json list data, create instances corresponding
        :return:
        None
        """
        for record in self.json_data:
            new_element = self.element_type(json_data=record,
                                            required=self.required,
                                            empty_available=self.empty_available)
            self.element_list.append(new_element)

    def _validate_custom(self):
        """
        Iterator each element in list, then call validate.
        After that, collect errors from elements in this class.
        :return:
        """
        self._parse_data()
        for element in self.element_list:
            element.validate()
            errors = element.get_errors()
            for error in errors:
                error.append_field(str(self.element_list.index(element)))
                self._insert_error(error)

    def is_empty(self):
        """
        Check is the list empty or not
        :return:
        bool
            True: the list is empty
            False: the list not empty
        """
        return not self.json_data


