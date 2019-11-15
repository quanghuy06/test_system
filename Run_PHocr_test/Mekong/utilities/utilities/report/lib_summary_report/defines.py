# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/04/2017
# Last update:      12/07/2018
# Description:


class ErrorFlags(object):
    # Error type flag
    F_CRASH = "< CRASH >"
    F_GENERAL = "< GENERAL >"
    F_EXTRA = "< FAILED >"
    F_OUTPUT_OFFICE_0B = "< OUTPUT OFFICE 0B >"
    F_SYSTEM = "< TEST SYSTEM ERROR >"
    F_GOOD = "< NOT ERROR >"
    F_MISSING_OUTPUT = "< MISSING OUTPUT >"


class Threshold(object):
    # Memory peak threshold (unit: MB)
    CHANGE_MEMORY_PEAK_MB = 20
    MEMORY_PEAK_MB = 250
