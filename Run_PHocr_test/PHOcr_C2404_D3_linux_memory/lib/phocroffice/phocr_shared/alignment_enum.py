# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
Enumeration which related to alignment
"""


class AlignmentEnum(object):
    """
    Matched with alignment enum in PHOcr with file PHOcrEnum.h
    """
    NONE = 'none'
    ALIGN_LEFT = 'left'
    ALIGN_RIGHT = 'right'
    ALIGN_CENTER = 'center'
    ALIGN_JUSTIFY = 'justify'
    ALIGN_JUSTIFY_FULL = 'justify_full'

    @classmethod
    def is_left(cls, alignment):
        """
        Is alignment left
        :param alignment:
        :return:
        """
        return str(alignment).lower() == cls.ALIGN_LEFT

    @classmethod
    def is_right(cls, alignment):
        """
        Is alignment right
        :param alignment:
        :return:
        """
        return str(alignment).lower() == cls.ALIGN_RIGHT

    @classmethod
    def is_center(cls, alignment):
        """
        Is alignment center
        :param alignment:
        :return:
        """
        return str(alignment).lower() == cls.ALIGN_CENTER

    @classmethod
    def is_justify(cls, alignment):
        """
        Is alignment justified
        :param alignment:
        :return:
        """
        return \
            str(alignment).lower() == cls.ALIGN_JUSTIFY or \
            str(alignment).lower() == cls.ALIGN_JUSTIFY_FULL

