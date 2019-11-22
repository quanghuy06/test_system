# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      21/01/2019
from abc import ABCMeta
from validate.lib_base.mekong_int import MekongInt
from validate.lib_base.spec_error import SpecError


class MekongIntNonNegative(MekongInt):
    """

    Class presents information with type int and value is non negative value

    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(MekongIntNonNegative, self).__init__(**kwargs)

    def _validate_custom(self):
        """
        Validate for non negative number
        :return:
        bool
            True: If this field is non negative number
            False: This field is negative number
        """
        if int(self.json_data) < 0:
            error_msg = "'{0}' should be non negative number" \
                        "".format(self.json_data)
            new_error = SpecError(error_msg)
            self._insert_error(new_error)

