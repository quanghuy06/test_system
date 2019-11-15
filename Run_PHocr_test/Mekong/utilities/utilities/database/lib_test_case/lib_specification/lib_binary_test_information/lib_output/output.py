# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      30/01/2019
from abc import ABCMeta

from database.lib_test_case.lib_specification.lib_binary_test_information.lib_output.comparator_enum import \
    ComparatorEnum
from validate.lib_base.mekong_object import MekongObject
from validate.lib_base.mekong_parser import MekongParser
from validate.lib_base.mekong_string import MekongString


class Output(MekongObject):
    """
    Class presents output information for a output record.

    Examples
    --------
    {
        "comparator": "bounding_box",
        "name": "01_0033.jpg_0.txt"
    }

    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(Output, self).__init__(**kwargs)
        self.comparator = MekongParser.generate_object_from_json(
            self._get_json_for('comparator'),
            ComparatorEnum
        )
        self.name = MekongParser.generate_object_from_json(
            self._get_json_for('name'),
            MekongString
        )
