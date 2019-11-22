# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      27/02/2019
from baseapi.common import get_list_defined_string
from configs.database import SpecKeys
from configs.projects.phocr import PhocrProject
from validate.lib_base.mekong_enum import MekongEnum


class ComparatorEnum(MekongEnum):
    """
    Present "comparator" field in spec.json > binary_test_information > output.
    Also define all valid values for comparator
    """
    def __init__(self, **kwargs):
        super(ComparatorEnum, self).__init__(**kwargs)

    def _valid_data_types(self):
        """
        Get the valid data type for comparator
        :return:
        list
            list of type for comparator
        """
        return [str, unicode]

    def _get_valid_values(self):
        """
        Get all valid values
        :return:
        list
            all valid values for component
        """
        return get_list_defined_string(
            SpecKeys.BinaryTestInformation.Output.Comparator
        )
