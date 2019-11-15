# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      02/01/2019
# Description:      Define class which presents information of specification of
#                   Mekong test case.
import json
import os
from abc import ABCMeta
from configs.database import TestcaseConfig
from validate.lib_base.mekong_base import MekongBase
from database.lib_test_case.specification import Specification
from validate.lib_base.mekong_folder import MekongFolder
from validate.lib_base.spec_error import SpecError


class MekongTestCase(MekongBase):
    """
    Class presents data for a test case. Data contains:
    - Specification of test case which store in json format file
    - Test data folder which contains input data for testing
    - Reference data folder which contains current test result of source master
    - Ground truth data folder which contains results which we expected of
    testing. This folder can be empty because currently we has no ground
    truth for pdf output or office output (docx, xlsx, pptx).

    """

    __metaclass__ = ABCMeta

    def __init__(self, test_case_path, **kwargs):
        """
        Do not parse information in constructor.

        """
        super(MekongTestCase, self).__init__(**kwargs)
        self.test_case_path = test_case_path
        self.test_case_name = os.path.basename(self.test_case_path)
        # Folders
        test_data_path = os.path.join(self.test_case_path,
                                      TestcaseConfig.TEST_DATA_DIR)
        self.test_data = MekongFolder(test_data_path,
                                      required=True,
                                      empty_available=False)

        ref_data_path = os.path.join(self.test_case_path,
                                     TestcaseConfig.REF_DATA_DIR)
        self.ref_data = MekongFolder(ref_data_path,
                                     empty_available=True,
                                     required=False)

        ground_truth_path = os.path.join(self.test_case_path,
                                         TestcaseConfig.GROUND_TRUTH_DATA_DIR)
        self.ground_truth = MekongFolder(ground_truth_path,
                                         empty_available=True,
                                         required=False)

        scripts_path = os.path.join(self.test_case_path,
                                    TestcaseConfig.SCRIPT_DIR)
        self.scripts = MekongFolder(scripts_path,
                                    empty_available=True,
                                    required=False)

        spec_path = os.path.join(self.test_case_path,
                                 TestcaseConfig.SPEC_FILE)
        with open(spec_path) as f:
            spec_json = json.loads(f.read())

        self.specification = Specification(json_data=spec_json, required=True)

    def validate(self):
        """
        Validate for folders: ground_truth, ref_data, test_data, scripts folder
        and spec.json file
        :return:
        None
        """
        field_instances = self._get_field_instances()
        candidate_fields = field_instances.keys()
        for field_name in candidate_fields:
            field_instance = field_instances[field_name]
            field_instance.validate()
            errors = field_instance.get_errors()
            for error in errors:
                error.append_field(field_name)
                self._insert_error(error)

        self._validate_rules()

    def _validate_rules(self):
        # validate name of test folder must be the same with test case id
        test_case_id = self.specification.get_data_for('_id')
        if test_case_id != self.test_case_name:
            error_msg = "Test case id {0} must be the same with test case folder {1}"
            error_msg = error_msg.format(test_case_id, self.test_case_name)
            new_error = SpecError(error_msg)
            self._insert_error(new_error)
