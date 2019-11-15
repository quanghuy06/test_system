# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/09/2019
# Description:      This script define available updates for data which is used for testing on
#                   virtual machines
from enum import Enum


class DataUpdatesAvailable(Enum):
    """
    Enum class define type of data available for updating
    """
    PHOCR_TRAINED_DATA = 1
    PYTHON_PORTABLE = 2
    VALGRIND_MEKONG = 3


def get_update_option(data_type):
    """
    Convert data type from enum to arguments option in command line. This help us to create
    command line of workers_manager.py to run on a node when we manage nodes from master.

    Parameters
    ----------
    data_type : DataUpdatesAvailable
        Type of data need to be updated in enum.

    Returns
    -------
    str
        Option of command line to update data package. Return empty string in case there is no
        action to be done.

    """
    if data_type == DataUpdatesAvailable.PHOCR_TRAINED_DATA:
        return "--update-training-data"
    if data_type == DataUpdatesAvailable.PYTHON_PORTABLE:
        return "--update-python-portable"
    if data_type == DataUpdatesAvailable.VALGRIND_MEKONG:
        return "--update-valgrind"
    return ""
