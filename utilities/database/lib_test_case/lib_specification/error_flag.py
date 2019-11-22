# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      02/01/2019
from abc import ABCMeta
from validate.lib_base.mekong_object import MekongObject
from validate.lib_base.mekong_bool import MekongBool
from validate.lib_base.mekong_parser import MekongParser


class ErrorFlag(MekongObject):
    """

    Class presents test case is error or not at the moment on different
    platforms.

    Examples
    --------
    This is example of json object of error flag field in test case's
    specification:
    {
        "linux" : True,
        "windows" : False
    }
    .
    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(ErrorFlag, self).__init__(**kwargs)
        self.linux = MekongParser.generate_object_from_json(
            self._get_json_for('linux'),
            MekongBool)
        self.windows = MekongParser.generate_object_from_json(
            self._get_json_for('windows'),
            MekongBool)
