# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      02/01/2019
import json
from abc import abstractmethod

from validate.lib_base.spec_error import SpecError


class MekongBase(object):
    """

    Abstract class - inheritance of all classes which relate to json object of
    test case's specification. This aims to store warnings and errors of
    validation of objects.

    """

    def __init__(self,
                 required=True,
                 empty_available=False):
        self._errors = list()
        self.required = required
        self.empty_available = empty_available

    def _insert_error(self, error):
        """
        Inset new error to error list
        :param error: SpecError
        New error
        :return:
        None
        """
        assert type(error) is SpecError
        self._errors.append(error)

    def add_meta_field_to_error(self, field_name):
        """
        Add field name to errors, aims to store path to the field.
        And we can use it to print useful information.
        Example:

        spec.json > tags > Language : This field can not emtpy

        :param field_name:
        :return:
        None
        """
        for error in self._errors:
            error.append_field(field_name)

    def get_errors(self):
        """
        Get all errors
        :return:
        list
            list of all errors
        """
        return self._errors

    def get_errors_in_dict(self):
        """
        Get errors in dictionary format
        :return:
        dict
            errors in dictionary format
        """
        errors = list()
        for error in self._errors:
            errors.append(error.to_dict())
        return errors

    def get_errors_in_json(self):
        """
        Get errors in json format
        :return:
        json
            errors in json format
        """
        return json.dumps(self.get_errors_in_dict(),
                          indent=4,
                          sort_keys=True)

    def print_errors(self):
        """
        Print errors to screen in json format
        :return:
        """
        print(self.get_errors_in_json())

    @abstractmethod
    def validate(self):
        """
        Do validate for this field.
        :return:
        None
        """
        pass

    @abstractmethod
    def is_empty(self):
        """
        Check this object is empty?
        :return:
        bool
            Is this object empty?
        """
        pass

    def _validate_empty(self):
        """
        Validate this object is empty or not?
        :return:
        bool
            True: if this object is empty
            False: if this object not empty
        """
        is_empty = self.is_empty()
        if not self.empty_available:
            if is_empty:
                error_msg = "Can not be empty"
                new_error = SpecError(error_msg)
                self._insert_error(new_error)

        return not is_empty

    def _get_field_instances(self):
        """
        Get all field and its object in a dictionary
        :return:
        dict
            all field object of this class in a dictionary
        """
        field_instances = dict()
        for attribute in self.__dict__.keys():
            field_object = self.__getattribute__(attribute)
            if isinstance(field_object, MekongBase):
                field_instances[attribute] = field_object
        return field_instances
