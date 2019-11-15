# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      02/01/2019
from abc import ABCMeta

from validate.lib_base.mekong_float import MekongFloat
from validate.lib_base.mekong_object import MekongObject
from validate.lib_base.mekong_float_non_negative import MekongFloatNonNegative
from configs.database import SpecKeys
from configs.common import Platform
from validate.lib_base.mekong_parser import MekongParser


class Weights(MekongObject):
    """

    Class presents time of the latest testing of the test case. This will be
    referenced to distribution test cases between machines.

    Examples
    --------
    This is example of json object of weight field in test case's
    specification:
    {
        "linux" : 1.234232,
        "windows" : 2.323142
    }
    This values is updated automatically by test system. For the first time of
    test case creation, these values should be set by a suitable value.
    .
    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(Weights, self).__init__(**kwargs)
        self.linux = MekongParser.generate_object_from_json(
            self._get_json_for("linux"),
            MekongFloatNonNegative)
        self.windows = MekongParser.generate_object_from_json(
            self._get_json_for("windows"),
            MekongFloatNonNegative)
