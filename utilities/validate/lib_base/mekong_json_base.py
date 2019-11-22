# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      02/01/2019
import json
from abc import abstractmethod

from validate.lib_base.mekong_base import MekongBase
from validate.lib_base.spec_error import SpecError


class MekongJsonBase(MekongBase):
    """

    Abstract class - inheritance of all classes which relate to json object of
    test case's specification. This aims to store warnings and errors of
    validation of objects.

    """

    def __init__(self, json_data, **kwargs):
        super(MekongJsonBase, self).__init__(**kwargs)
        self.json_data = json_data

    @abstractmethod
    def _valid_data_types(self):
        """
        Abstract to get all valid data types
        :return:
        list
            all valid data types
        """
        pass

    @abstractmethod
    def _validate_custom(self):
        """
        Abstract method used for implement special validations for each type of
        data.
        :return:
        None
        """
        pass

    @abstractmethod
    def _validate_rules(self):
        """
        Abstract method used for implement special validations for each type of
        data.
        :return:
        None
        """
        pass

    def validate(self):
        """
        Do validate for this field.
        :return:
        None
        """
        if not self._validate_exists():
            return
        if not self._validate_type():
            return
        if not self._validate_empty():
            return

        self._validate_custom()
        self._validate_rules()

    def _validate_exists(self):
        """
        Implement validate this field exists or not.
        :return:
        None
        """
        is_exists = not self.json_data is None
        if self.required:
            if not is_exists:
                error_msg = "Missing this required field"
                new_error = SpecError(error_msg)
                self._insert_error(new_error)
        return is_exists

    def _validate_type(self):
        """
        Implement validate type of this field is correct?
        :return:
        bool
            True: if type of data correct with valid types
            False: type of data not correct with valid types.
        """
        valid_data_types = self._valid_data_types()
        is_valid_type = type(self.json_data) in valid_data_types
        if not is_valid_type:
            valid_data_types_str = [name.__name__ for name in valid_data_types]
            error_msg = "Data {0} should be type of {1}".format(self.json_data,
                                                                valid_data_types_str)
            new_error = SpecError(error_msg)
            self._insert_error(new_error)
        return is_valid_type

    def to_json(self):
        return self.json_data
