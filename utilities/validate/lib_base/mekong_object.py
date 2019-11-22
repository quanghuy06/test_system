# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      11/01/2019
from abc import ABCMeta, abstractmethod
from validate.lib_base.mekong_json_base import MekongJsonBase
from validate.lib_base.spec_error import SpecError


class MekongObject(MekongJsonBase):
    """

    Abstract class presents information with type MekongObject and contain
    some of object members in it. Member objects of an ObjectContainer is
    specific such as a computer should have it's name, ip, user name,... We
    access to object information by using '.' operator.

    Examples
    --------
    A machine has it's information store by json object like this

    {
        'ip' : '192.168.1.1',
        'user_name' : 'test'
    }

    For this data block, we should have machine's information as an objects
    container. In this case machine information object contain 3 data object
    members: name, ip, user name. Each member should be a string object.

    machine_information (objects container)
        |__ ip (string object)
        |__ user_name (string object)

    To access data such as ip, we have:
    machine_information.ip.value()

    Notes
    -----
    Please distinguish between ObjectsContainer with ObjectsList

    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(MekongObject, self).__init__(**kwargs)

    def _valid_data_types(self):
        """
        Get valid data type for object data
        :return:
        list
            dict type
        """
        return [dict]

    def is_empty(self):
        """
        Check is the object empty or not
        :return:
        bool
            True: the object is empty
            False: the object not empty
        """
        return not self.json_data

    def _validate_custom(self):
        """
        Validate redundant fields in this object,
        and validate for each field in the object.
        Collect all errors into this object
        :return:
        None
        """
        self._validate_redundant()
        self._validate_for_fields()

    def _validate_for_fields(self):
        """

        :return:
        """
        field_instances = self._get_field_instances()
        candidate_fields = field_instances.keys()
        for field_name in candidate_fields:
            field_instance = field_instances[field_name]
            field_instance.validate()
            errors = field_instance.get_errors()
            for error in errors:
                error.append_field(field_name)
                self._insert_error(error)

    def _validate_redundant(self):
        """
        Find the redundant data for the object.
        Add all redundant to error list
        :return:
        None
        """
        field_instances = self._get_field_instances()
        candidate_fields = field_instances.keys()
        for field in self.json_data.keys():
            if field not in candidate_fields:
                error_msg = "Redundant field"
                new_error = SpecError(error_msg)
                new_error.append_field(field)
                self._insert_error(new_error)

    def get_field_names(self):
        """
        Get all fields in the object.
        Also it is all fields in spec.json file
        :return:
        list
            list of fields
        """
        return self.__dict__.keys()

    def _get_json_for(self, field):
        """
        Get json data for a field
        :param field:
        Name of field
        :return:
        json
            json data of the field
        """
        if self.json_data is None \
                or type(self.json_data) not in self._valid_data_types() \
                or field not in self.json_data.keys():
            return None
        else:
            json_data = self.json_data[field]

        return json_data

    def get_data_for(self, field):
        field_instances = self._get_field_instances()
        if field in field_instances:
            return field_instances[field].to_json()

        error_msg = "Class {0} does not have field {1}"
        error_msg = error_msg.format(__name__, field)
        raise Exception(error_msg)

