# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      22/02/2019

from validate.lib_base.mekong_json_base import MekongJsonBase

from abc import ABCMeta

__metaclass__ = ABCMeta


class MekongString(MekongJsonBase):
    """
    Class present string type in json.
    """
    def __init__(self, **kwargs):
        super(MekongString, self).__init__(**kwargs)

    def _valid_data_types(self):
        """
        Check is data type of string
        :return:
        bool
            Does data of this field is type of string
        """
        return [str, unicode]

    def _validate_custom(self):
        """
        Do nothing
        :return:
        None
        """
        pass

    def is_empty(self):
        """
        Check this string is empty or not.
        :return:
        bool
            is this string empty?
        """

        return not self.json_data
