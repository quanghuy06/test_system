# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class PhotoWrap(object):
    NONE = 0
    IN_LINE_WITH_TEXT = 1
    SQUARE = 2
    TIGHT = 3
    THROUGH = 4
    TOP_AND_BOTTOM = 5
    BEHIND_TEXT = 6
    IN_FRONT_OF_TEXT = 7


def convert_photo_wrap(wrap_str):
    wrap_enum = PhotoWrap.NONE
    if wrap_str == 'NONE':
        wrap_enum = PhotoWrap.NONE
    elif wrap_str == 'IN_LINE_WITH_TEXT':
        wrap_enum = PhotoWrap.IN_LINE_WITH_TEXT
    elif wrap_str == 'SQUARE':
        wrap_enum = PhotoWrap.SQUARE
    elif wrap_str == 'TIGHT':
        wrap_enum = PhotoWrap.TIGHT
    elif wrap_str == 'THROUGH':
        wrap_enum = PhotoWrap.THROUGH
    elif wrap_str == 'TOP_AND_BOTTOM':
        wrap_enum = PhotoWrap.TOP_AND_BOTTOM
    elif wrap_str == 'BEHIND_TEXT':
        wrap_enum = PhotoWrap.BEHIND_TEXT
    elif wrap_str == 'IN_FRONT_OF_TEXT':
        wrap_enum = PhotoWrap.IN_FRONT_OF_TEXT
    return wrap_enum


class PageDirection(object):
    """
    Related to WritingDirection of OCREngine, the value are the same
    with reference enum
    """
    HORIZONTAL = 0
    VERTICAL = 1


def convert_page_direction(page_dir_str):
    page_dir_enum = PageDirection.HORIZONTAL
    if page_dir_str is None or len(page_dir_str) == 0:
        return None
    if page_dir_str == 'HORIZONTAL':
        page_dir_enum = PageDirection.HORIZONTAL
    elif page_dir_str == 'VERTICAL':
        page_dir_enum = PageDirection.VERTICAL
    return page_dir_enum


class LineDirection(object):
    """
    Related to TextlineOrder of OCREngine, the value are the same
    with reference enum
    """
    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1
    TOP_TO_BOTTOM = 2


def convert_line_direction(line_dir_str):
    line_dir_enum = LineDirection.TOP_TO_BOTTOM
    if line_dir_str is None or len(line_dir_str) == 0:
        return None
    if line_dir_str == 'LEFT_TO_RIGHT':
        line_dir_enum = LineDirection.LEFT_TO_RIGHT
    elif line_dir_str == 'RIGHT_TO_LEFT':
        line_dir_enum = LineDirection.RIGHT_TO_LEFT
    elif line_dir_str == 'TOP_TO_BOTTOM':
        line_dir_enum = LineDirection.TOP_TO_BOTTOM
    return line_dir_enum


class CommonDirection(object):
    """
    Common direction for using in multiple purpose
    """
    ALL = 0
    VERTICAL = 1
    HORIZONTAL = 2
