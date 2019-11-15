# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      14/01/2019
import json
import os
from abc import ABCMeta, abstractmethod
from validate.lib_base.mekong_base import MekongBase
from validate.lib_base.spec_error import SpecError


class MekongFolder(MekongBase):
    """

    Class presents a folder data

    """

    __metaclass__ = ABCMeta

    def __init__(self, folder_path, **kwargs):
        super(MekongFolder, self).__init__(**kwargs)
        self.folder_path = folder_path

    def validate(self):
        """
        Do validate for this field.
        :return:
        None
        """
        if not self._validate_exists():
            return
        if not self._validate_empty():
            return

    def _validate_exists(self):
        """
        Implement validate this field exists or not.
        :return:
        None
        """
        is_exists = os.path.isdir(self.folder_path)
        if self.required:
            if not is_exists:
                error_msg = "Folder {} does not exists".format(self.folder_path)
                new_error = SpecError(error_msg)
                self._insert_error(new_error)
        return is_exists

    def is_empty(self):
        """
        Check this folder is empty?
        :return:
        bool
            Is this folder empty?
        """
        assert(os.path.isdir(self.folder_path))
        items_in_folder = os.listdir(self.folder_path)
        is_folder_empty = not items_in_folder
        return is_folder_empty

    def _validate_empty(self):
        """
        Validate this field is empty or not?
        :return:
        bool
            True: if this field is empty
            False: if this field not empty
        """
        is_empty = self.is_empty()
        if not self.empty_available:
            if is_empty:
                error_msg = "Can not be empty"
                new_error = SpecError(error_msg)
                self._insert_error(new_error)

        return not is_empty
