# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class PHOcrConstant(object):
    """
    Default dpi
    """
    DEFAULT_DPI = 300

    """
    Minimum believable resolution. Used as a default if there is no other
    information, as it is safer to under-estimate than over-estimate.
    """
    MIN_CREDIBLE_RESOLUTION = 70

    """
    Maximum believable resolution.
    """
    MAX_CREDIBLE_RESOLUTION = 2400

    """
    Default width of column by inch
    """
    ORIGINAL_COLUMN_WIDTH = 8.43

    """
    Default width of column by pixel
    """
    DEFAULT_COLUMN_PIXELS = 64

    """
    Default height of row by inch
    """
    ORIGINAL_ROW_HEIGHT = 15

    """
    Default height of row by pixel
    """
    DEFAULT_ROW_PIXELS = 20
