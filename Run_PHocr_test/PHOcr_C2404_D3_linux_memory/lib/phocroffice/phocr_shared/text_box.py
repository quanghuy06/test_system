# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
This module for supporting textbox generation in all office format
"""
from phocr_shared.text_direction import TextlineOrder
from phocr_shared.alignment_enum import AlignmentEnum


class CommonDirection(object):
    """
    Common direction for using in multiple purpose
    """
    ALL = 0
    VERTICAL = 1
    HORIZONTAL = 2


def _common_alignment_of_carea(carea):
    """
    If all paragraph have the same alignment,
    return that alignment
    Else, return None

    Parameters
    ----------
    carea

    Returns
    -------

    """
    if len(carea.paragraphs) == 0:
        return None

    first_alignment = carea.paragraphs[0].alignment.lower()
    for paragraph in carea.paragraphs:
        curr_alignment = paragraph.alignment.lower()
        if curr_alignment != first_alignment:
            return None
    return first_alignment


def _is_all_paragraph_one_line(carea):
    """
    Is all paragraph inside of carea is one line

    Parameters
    ----------
    carea

    Returns
    -------

    """
    is_one_line = True
    for paragraph in carea.paragraphs:
        if len(paragraph.lines) != 1:
            is_one_line = False
    return is_one_line


def calculate_text_box_size(carea):
    """
    With one line text box, the width will be bigger,
    it will make layout better

    Parameters
    ----------
    carea

    Returns
    -------

    """

    textline_order = carea.textline_order
    alignment = _common_alignment_of_carea(carea)

    if ((_is_all_paragraph_one_line(carea)) and
        (alignment is not None)):

        # Calculate padding size
        if textline_order == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
            size_depend = carea.w
        else:
            size_depend = carea.h
        adding_size = float(size_depend) * 0.33

        if alignment == AlignmentEnum.ALIGN_CENTER:
            reduce_start = adding_size / 2
        elif alignment == AlignmentEnum.ALIGN_RIGHT:
            reduce_start = adding_size
        else:
            reduce_start = 0

        if textline_order == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
            carea.w += adding_size
            carea.x -= reduce_start
        else:
            carea.h += adding_size
            carea.y -= reduce_start

    return carea.x, carea.y, carea.w, carea.h


def element_overlap_area(element1, element2, axis=CommonDirection.ALL):
    """
    Refer function boxOverlapRegion in PHOcr

    Parameters
    ----------
    element1
    element2
    axis

    Returns
    -------

    """
    left_1 = element1.x
    width_1 = element1.w
    top_1 = element1.y
    height_1 = element1.h
    left_2 = element2.x
    width_2 = element2.w
    top_2 = element2.y
    height_2 = element2.h
    right_1 = left_1 + width_1 - 1
    right_2 = left_2 + width_2 - 1
    bottom_1 = top_1 + height_1 - 1
    bottom_2 = top_2 + height_2 - 1
    if bottom_2 < top_1 or \
            bottom_1 < top_2 or \
            right_1 < left_2 or \
            right_2 < left_1:
        return 0

    left_target = max(left_1, left_2)
    top_target = max(top_1, top_2)
    right_target = min(right_1, right_2)
    bottom_target = min(bottom_1, bottom_2)
    if axis == CommonDirection.ALL:
        return (right_target - left_target + 1) * \
               (bottom_target - top_target + 1)
    elif axis == CommonDirection.HORIZONTAL:
        return right_target - left_target + 1
    elif axis == CommonDirection.VERTICAL:
        return bottom_target - top_target + 1
    else:
        raise ValueError('Axis should be instance of CommonDirection')
