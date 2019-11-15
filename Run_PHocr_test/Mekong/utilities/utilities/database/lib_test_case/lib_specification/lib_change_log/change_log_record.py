# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      07/01/2019
from abc import ABCMeta

from database.lib_test_case.lib_specification.lib_change_log.lib_address.address import \
    Address
from validate.lib_base.mekong_object import MekongObject
from validate.lib_base.mekong_parser import MekongParser
from validate.lib_base.mekong_string import MekongString


class ChangeLogRecord(MekongObject):
    """
    Class presents change log record.

    Examples
    --------

    {
        "address": [
            {
                "ip": "127.0.0.1",
                "mac": "00:00:00:00:00:00"
            },
            {
                "ip": "10.116.41.34",
                "mac": "08:00:27:51:8f:48"
            }
        ],
        "changed_log": "Update NonIT tag. Updated parts: spec.json",
        "time": "11-12-2018 13:55",
        "user": "manager"
    }

    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(ChangeLogRecord, self).__init__(**kwargs)
        # Required information
        self.user = MekongParser.generate_object_from_json(
            self._get_json_for('user'),
            MekongString
        )
        self.time = MekongParser.generate_object_from_json(
            self._get_json_for('time'),
            MekongString
        )
        self.changed_log = MekongParser.generate_object_from_json(
            self._get_json_for('changed_log'),
            MekongString
        )
        self.address = MekongParser.generate_list_form_json(
            self._get_json_for('address'),
            Address
        )
