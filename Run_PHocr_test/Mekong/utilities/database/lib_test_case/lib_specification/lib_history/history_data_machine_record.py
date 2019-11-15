# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      25/02/2019
from baseapi.common import get_list_defined_string
from report.lib_base.history_data_informer import HistoryDataConfiguration
from validate.lib_base.mekong_object import MekongObject
from validate.lib_base.spec_error import SpecError


class HistoryDataMachineRecord(MekongObject):
    """
    Represent a history data record for each machine.
    Example:
        {
            "1": {
              "Time execute": 1.744
            },
            "129": {
              "Time execute": 2.8250000000000002,
              "Total characters text": 1711,
              "Total errors text": 8
            }
        }
    """
    def __init__(self, **kwargs):
        super(HistoryDataMachineRecord, self).__init__(**kwargs)

    def _validate_valid_value(self):
        """
        Do nothing, all validations are implemented in _validate_custom()
        :return:
        None
        """
        pass

    def _validate_redundant(self):
        """
        Do nothing, all validations are implemented in _validate_custom()
        :return:
        None
        """
        pass

    def _validate_custom(self):
        # TODO(Huan) find better solution for this
        """
        Specific validate implement on hitory_data > abbyy_client
        Because this field has dynamic keys on the object.
        So we need to create manual validate function.
        Below is valid case of this field:
        + abbyy_client: {} -> cover by _validate_type()
        + abbyy_client: {"1": {
              "Total characters bounding box": 1711,
              "Total errors bounding box": 5
            }
        }

        We will validate following rules:
        + If there are delta history, it data not be a empty object
        + Inside a object of history object: keys must be one of following values:
            - Total characters bounding box
            - Total errors bounding box
            - Time execute
            - Total characters text
            - Total errors text

        Returns
        -------
        """
        history_valid_fields = get_list_defined_string(
            HistoryDataConfiguration.BbAccuracy)
        history_valid_fields += get_list_defined_string(
            HistoryDataConfiguration.TextAccuracy)
        history_valid_fields += get_list_defined_string(
            HistoryDataConfiguration.Performance)
        history_valid_fields += get_list_defined_string(
            HistoryDataConfiguration.MemoryInfo)

        for delta in self.json_data.keys():
            history_delta_record = self.json_data[delta]
            if not type(history_delta_record) is dict:
                error_msg = 'Data "{0}" should be type of "{1}"'.format(
                    history_delta_record, dict.__name__)
                new_error = SpecError(error_msg)
                new_error.append_field(delta)
                self._insert_error(new_error)
                continue

            # Check for empty dictionary
            if self.required and not history_delta_record:
                error_msg = 'Data "{0}" should contains at least one of "{1}"'.format(
                    history_delta_record, history_valid_fields)
                new_error = SpecError(error_msg)
                new_error.append_field(delta)
                self._insert_error(new_error)
                continue

            for field in history_delta_record.keys():
                # Is this field is one of above fields
                if field not in history_valid_fields:
                    error_msg = '"{0}" should be one of "{1}"'.format(field,
                                                                      history_valid_fields)
                    new_error = SpecError(error_msg)
                    new_error.append_field(field)
                    new_error.append_field(delta)
                    self._insert_error(new_error)
                    continue
                value = history_delta_record[field]
                if type(value) is int or type(value) is float:
                    continue
                else:
                    error_msg = '"{0}" should be type of int or float'.format(value)
                    new_error = SpecError(error_msg)
                    new_error.append_field(field)
                    new_error.append_field(delta)
                    self._insert_error(new_error)
