# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      30/01/2019
from abc import ABCMeta

from configs.database import SpecKeys
from database.lib_test_case.lib_specification.lib_binary_test_information.lib_output.output import \
    Output
from validate.lib_base.mekong_object import MekongObject
from validate.lib_base.mekong_parser import MekongParser
from validate.lib_base.mekong_string import MekongString


class BinaryTestInformation(MekongObject):
    """
    Class presents "binary_test_information" field in spec.json
    Examples:
    "binary_test_information": {
        "binary_name": "PHOcrExample",
        "test_command": "-ocr -layout english TEST_DATA/01_0033.jpg",
        "output": [{
            "comparator": "ignore",
            "name": "01_0033.jpg.txt"
          },
          {
            "comparator": "bounding_box",
            "name": "01_0033.jpg_0.txt"
          }
        ]
    }

    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(BinaryTestInformation, self).__init__(**kwargs)
        self.name = SpecKeys.BINARY_TEST_INFORMATION
        self.empty_available = True

        # String tags
        self.binary_name = MekongParser.generate_object_from_json(
            self._get_json_for('binary_name'),
            MekongString
        )
        self.test_command = MekongParser.generate_object_from_json(
            self._get_json_for('test_command'),
            MekongString
        )
        self.output = MekongParser.generate_list_form_json(
            self._get_json_for('output'),
            Output
        )
