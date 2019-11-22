# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      26/02/2019
from baseapi.common import get_list_defined_string
from configs.projects.phocr import PhocrProject
from validate.lib_base.mekong_enum import MekongEnum


class ComponentEnum(MekongEnum):
    """
    Present "component" field in spec.json.
    Also define all valid value for component
    """
    def __init__(self, **kwargs):
        super(ComponentEnum, self).__init__(**kwargs)

    def _valid_data_types(self):
        """
        Get the valid data type for component
        :return:
        list
            list of type for component
        """
        return [str, unicode]

    def _get_valid_values(self):
        """
        Get all valid values
        :return:
        list
            all valid values for component
        """
        return get_list_defined_string(PhocrProject.components)
