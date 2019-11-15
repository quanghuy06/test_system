# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class OfficeObjectTag(object):
    """
    This class shows us objects which are used in phocr to export to
    output formatting
    """
    UNKNOWN = -1
    PAGE = 0
    TABLE = 1
    ROW = 2
    CELL = 3
    CAREA = 4
    PARAGRAPH = 5
    LINE = 6
    WORD = 7
    CHARACTER = 8
    PHOTO = 9
