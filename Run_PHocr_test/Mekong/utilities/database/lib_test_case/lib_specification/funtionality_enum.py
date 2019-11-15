# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      26/02/2019
from baseapi.common import get_list_defined_string
from configs.projects.phocr import PhocrProject
from validate.lib_base.mekong_enum import MekongEnum


class FunctionalityEnum(MekongEnum):
    """
    Present "functionalities" field in spec.json.
    Also define all valid value for functionalities
    """
    def __init__(self, **kwargs):
        super(FunctionalityEnum, self).__init__(**kwargs)

    def _valid_data_types(self):
        """
        Get the valid data type for functionality
        :return:
        list
            list of type for functionality
        """
        return [str, unicode]

    def _get_valid_values(self):
        """
        Get all valid values
        :return:
        list
            all valid values for functionality
        """
        return get_list_defined_string(PhocrProject.functionalities)
