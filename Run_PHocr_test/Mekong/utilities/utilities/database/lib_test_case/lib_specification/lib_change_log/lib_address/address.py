# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      07/01/2019
from abc import ABCMeta
from validate.lib_base.mekong_object import MekongObject
from validate.lib_base.mekong_parser import MekongParser
from validate.lib_base.mekong_string import MekongString


class Address(MekongObject):
    """
    Class presents address information for a change log record. An address
    information contain information about IP address and MAC address. A
    change log record could have more than one address because the machine
    could have multiple network interface and currently we report all of them.

    Examples
    --------

    {
        "ip": "10.116.41.96",
        "mac": "f4:8e:38:7b:06:e0"
    }

    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(Address, self).__init__(**kwargs)
        # List of required information data
        self.ip = MekongParser.generate_object_from_json(
            self._get_json_for('ip'),
            MekongString
        )
        self.mac = MekongParser.generate_object_from_json(
            self._get_json_for('mac'),
            MekongString
        )
