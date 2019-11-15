# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      11/01/2019
from abc import ABCMeta
from validate.lib_base.mekong_json_base import MekongJsonBase


class MekongFloat(MekongJsonBase):
    """

    Class presents a history information with type float

    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(MekongFloat, self).__init__(**kwargs)

    def _valid_data_types(self):
        """
        Get valid type of float data
        :return:
        list
            float type
        """
        return [float]

    def is_empty(self):
        """
        This field always not empty
        :return:
        bool
            False: this field is not empty
        """
        return False