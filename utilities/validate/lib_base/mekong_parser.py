# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      26/02/2019
from validate.lib_base.mekong_list import MekongList


class MekongParser(object):
    """
    Class to create MekongBase object from json data.
    """
    @staticmethod
    def generate_object_from_json(json_data,
                                  class_name,
                                  required=True,
                                  empty_available=False):
        """
        Generate MekongBase object from json data for
        MekongInt, MekongFloat, MekongObject, MekongString
        :param json_data: data of the field
        :param class_name: name of instance need to create
        :param required: is this field required
        :param empty_available: is this field can empty
        :return:
        MekongBase
            instance of class_name
        """
        field_object = class_name(json_data=json_data,
                                  required=required,
                                  empty_available=empty_available)
        return field_object

    @staticmethod
    def generate_list_form_json(json_data,
                                class_name,
                                required=True,
                                empty_available=False):
        """
        Generate MekongList object. With this function, we can create
        whatever list we want by specify class_name.
        "class_name" can be MekongInt, MekongFloat, MekongObject, MekongString
        And we can create list of int, list of float, list of object,
        list of string corresponding.
        :param json_data: data of the field
        :param class_name: name of instance need to create
        :param required: is this field required
        :param empty_available: is this field can empty
        :return:
        MekongList
            instance of MekongList
        """
        element_list = MekongList(class_name,
                                  json_data=json_data,
                                  required=required,
                                  empty_available=empty_available)
        return element_list
