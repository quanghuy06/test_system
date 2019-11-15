# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      26/02/2019
from baseapi.common import get_list_defined_string
from configs.common import Platform
from validate.lib_base.mekong_enum import MekongEnum


class PlatformEnum(MekongEnum):
    """
    Present "platform" field in spec.json > tags.
    Define platform will be test
    """
    def __init__(self, **kwargs):
        super(PlatformEnum, self).__init__(**kwargs)

    def _valid_data_types(self):
        """
        Get the valid data type for platform
        :return:
        list
            list of type for platform
        """
        return [str, unicode]

    def _get_valid_values(self):
        """
        Get all valid values
        :return:
        list
            All available platform
        """
        return get_list_defined_string(Platform)
