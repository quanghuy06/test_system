# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      02/01/2019
# Description:      Define class which presents information of specification of
#                   Mekong test case.
import os
from abc import ABCMeta
from baseapi.common import get_list_defined_string
from configs.database import SpecKeys
from configs.projects.phocr import PhocrProject
from database.lib_test_case.lib_specification.binary_test_information import \
    BinaryTestInformation
from database.lib_test_case.lib_specification.component_enum import \
    ComponentEnum
from database.lib_test_case.lib_specification.funtionality_enum import \
    FunctionalityEnum
from database.lib_test_case.lib_specification.lib_change_log.change_log_record import \
    ChangeLogRecord
from database.lib_test_case.lib_specification.product_enum import ProductEnum
from validate.lib_base.mekong_float_non_negative import MekongFloatNonNegative
from validate.lib_base.mekong_string import MekongString
from validate.lib_base.mekong_bool import MekongBool
from validate.lib_base.mekong_object import MekongObject
from validate.lib_base.mekong_parser import MekongParser

from database.lib_test_case.lib_specification.weights \
    import Weights
from database.lib_test_case.lib_specification.error_flag \
    import ErrorFlag
from database.lib_test_case.lib_specification.tags \
    import Tags
from database.lib_test_case.lib_specification.history_data \
    import HistoryData
from validate.lib_base.spec_error import SpecError


class Specification(MekongObject):
    """

    Class presents information of test case's specification

    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        """
        Do not parse information in constructor.

        """
        super(Specification, self).__init__(**kwargs)
        self._id = MekongParser.generate_object_from_json(
            self._get_json_for('_id'),
            MekongString)
        self.component = MekongParser.generate_object_from_json(
            self._get_json_for('component'),
            ComponentEnum)
        self.binary_test_information = MekongParser.generate_object_from_json(
            self._get_json_for('binary_test_information'),
            BinaryTestInformation,
            required=False,
            empty_available=True
        )
        self.product = MekongParser.generate_object_from_json(
            self._get_json_for('product'),
            ProductEnum)
        self.enable = MekongParser.generate_object_from_json(
            self._get_json_for('enable'),
            MekongBool)
        self.error_flags = MekongParser.generate_object_from_json(
            self._get_json_for('error_flags'),
            ErrorFlag)

        self.functionalities = MekongParser.generate_list_form_json(
            self._get_json_for('functionalities'),
            FunctionalityEnum,
            empty_available=True)
        self.history_data = MekongParser.generate_object_from_json(
            self._get_json_for('history_data'),
            HistoryData)
        self.tags = MekongParser.generate_object_from_json(
            self._get_json_for('tags'),
            Tags)
        self.weight = MekongParser.generate_object_from_json(
            self._get_json_for("weight"),
            MekongFloatNonNegative,
            required=False,
            empty_available=False)
        self.weights = MekongParser.generate_object_from_json(
            self._get_json_for("weights"),
            Weights)
        self.changed_log = MekongParser.generate_list_form_json(
            self._get_json_for('changed_log'),
            ChangeLogRecord,
            empty_available=True,
            required=False
        )

    def _validate_rules(self):
        # If component is "binary_test",
        # field "binary_test_information" must not be empty
        component = self.component.to_json()
        if component == PhocrProject.components.BINARY_TEST:
            if self.binary_test_information.get_errors():
                return
            if self.binary_test_information.is_empty():
                error_msg = "Can not be empty"
                new_error = SpecError(error_msg)
                new_error.append_field(SpecKeys.BINARY_TEST_INFORMATION)
                self._insert_error(new_error)
                return

            # Field functionality must empty.
            if self.functionalities.get_errors():
                return
            if not self.functionalities.is_empty():
                error_msg = "This test case run with component 'binary_test'. " \
                            "So 'functionalities' field must be empty"
                new_error = SpecError(error_msg)
                new_error.append_field(SpecKeys.FUNCTIONALITIES)
                self._insert_error(new_error)
                return
