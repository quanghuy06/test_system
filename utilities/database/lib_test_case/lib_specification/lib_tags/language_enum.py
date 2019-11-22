# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      26/02/2019
from baseapi.common import get_list_defined_string
from configs.database import SpecKeys
from validate.lib_base.mekong_enum import MekongEnum


class LanguageEnum(MekongEnum):
    """
    Present "language" field in spec.json > tags.
    Also define all languages
    """
    def __init__(self, **kwargs):
        super(LanguageEnum, self).__init__(**kwargs)

    def _valid_data_types(self):
        """
        Get the valid data type for language
        :return:
        list
            list of type for language
        """
        return [str, unicode]

    def _get_valid_values(self):
        """
        Get all valid values
        :return:
        list
            All available languages
        """
        return get_list_defined_string(SpecKeys.Tags.Language)
