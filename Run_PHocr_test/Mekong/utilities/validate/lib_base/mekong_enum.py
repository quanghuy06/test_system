# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      22/02/2019

from validate.lib_base.mekong_json_base import MekongJsonBase
from validate.lib_base.spec_error import SpecError
from abc import ABCMeta,abstractmethod

__metaclass__ = ABCMeta


class MekongEnum(MekongJsonBase):
    """
    Class present abstract "enum" type.
    """
    def __init__(self, **kwargs):
        super(MekongEnum, self).__init__(**kwargs)

    def _validate_custom(self):
        """
        Implement abstract method for enum type.
        In enum, data will check is in valid values
        :return:
        None
        """
        self._validate_valid_value()

    @abstractmethod
    def _get_valid_values(self):
        """
        Abstract method to get valid values.
        Each derived class will have it's own valid values
        :return:
        list
            list of valid values
        """
        pass

    def _validate_valid_value(self):
        """
        Check is this data exists in valid values
        If data does not exists in valid values,
        a error will be added to self._errors list.
        :return:
        None
        """
        valid_values = self._get_valid_values()
        if not valid_values:
            return
        if self.json_data not in valid_values:
            error_msg = "'{0}' should be one of {1}".format(self.json_data, valid_values)
            new_error = SpecError(error_msg)
            self._insert_error(new_error)

    def is_empty(self):
        """
        Check this string is empty or not.
        :return:
        bool
            is this string empty?
        """

        return not self.json_data
