# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/01/2019
from database.lib_test_case.lib_specification.lib_history.history_data_machine_record import \
    HistoryDataMachineRecord
from validate.lib_base.mekong_object import MekongObject
from validate.lib_base.mekong_parser import MekongParser


class HistoryDataPlatformRecord(MekongObject):
    """
        Represent a history data record for each machine.
        Example:
            {
                "abbyy_client": {},
                "esdk": {},
                "phocr_on_board": {},
                "phocr_test_machine": {},
                "tesseract": {}
            }
        """
    def __init__(self, **kwargs):
        super(HistoryDataPlatformRecord, self).__init__(**kwargs)
        self.abbyy_client = MekongParser.generate_object_from_json(
            self._get_json_for('abbyy_client'),
            HistoryDataMachineRecord,
            True,
            True)
        self.esdk = MekongParser.generate_object_from_json(
            self._get_json_for('esdk'),
            HistoryDataMachineRecord,
            True,
            True)
        self.phocr_on_board = MekongParser.generate_object_from_json(
            self._get_json_for('phocr_on_board'),
            HistoryDataMachineRecord,
            True,
            True)
        self.phocr_test_machine = MekongParser.generate_object_from_json(
            self._get_json_for('phocr_test_machine'),
            HistoryDataMachineRecord,
            True,
            True)
        self.tesseract = MekongParser.generate_object_from_json(
            self._get_json_for('tesseract'),
            HistoryDataMachineRecord,
            True,
            True)
