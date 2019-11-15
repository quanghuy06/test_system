# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      04/01/2019
from abc import ABCMeta

from database.lib_test_case.lib_specification.lib_history.history_data_platform_record import \
    HistoryDataPlatformRecord
from validate.lib_base.mekong_object import MekongObject
from validate.lib_base.mekong_parser import MekongParser


class HistoryData(MekongObject):
    """
    Present "history_data" field in spec.json file.
    """

    def __init__(self, **kwargs):
        super(HistoryData, self).__init__(**kwargs)
        self.linux = MekongParser.generate_object_from_json(
            self._get_json_for('linux'),
            HistoryDataPlatformRecord)
        self.windows = MekongParser.generate_object_from_json(
            self._get_json_for('windows'),
            HistoryDataPlatformRecord)
