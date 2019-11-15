# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
This module for calculate alignment of all office modules
"""

# Enumeration in this module
from phocr_shared.alignment_enum import AlignmentEnum
from phocr_shared.text_direction import get_transformed_x, get_transformed_w, \
    get_transformed_margin_left, get_transformed_width, \
    get_transformed_margin_right

# Data from docx, pptx and xlsx
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.base import EnumValue as DOCXEnum
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
from pptx.enum.base import EnumValue as PPTXEnum


def _default_alignment_docx():
    """
    Return default alignment of text
    :return:
    """
    return WD_PARAGRAPH_ALIGNMENT.LEFT


def _default_alignment_pptx():
    """
    Return default alignment of text
    :return:
    """
    return PP_PARAGRAPH_ALIGNMENT.LEFT


def get_alignment_from_str(alignment_str):
    """
    Transfer alignment from string to enum (PHOcrEnum.h)
    :param alignment_str:
    :return:
    """
    if alignment_str == AlignmentEnum.ALIGN_LEFT:
        alignment_enum = WD_PARAGRAPH_ALIGNMENT.LEFT
    elif alignment_str == AlignmentEnum.ALIGN_RIGHT:
        alignment_enum = WD_PARAGRAPH_ALIGNMENT.RIGHT
    elif alignment_str == AlignmentEnum.ALIGN_CENTER:
        alignment_enum = WD_PARAGRAPH_ALIGNMENT.CENTER
    elif alignment_str == AlignmentEnum.ALIGN_JUSTIFY or \
            alignment_str == AlignmentEnum.ALIGN_JUSTIFY_FULL:
        alignment_enum = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    else:
        alignment_enum = _default_alignment_docx()
    return alignment_enum


def string_to_alignment_docx(alignment_str):
    """
    Convert alignment string from xml data to alignment enums
    :param alignment_str:
    :param recommend_alignment:
    :param inside_textbox:
    :return:
    """
    assert isinstance(alignment_str, str)
    alignment_str = alignment_str.lower()
    if alignment_str == AlignmentEnum.NONE:
        alignment_enum = _default_alignment_docx()
    else:
        alignment_enum = get_alignment_from_str(alignment_str)

    return alignment_enum


def string_to_alignment_pptx(alignment_str):
    """
    Convert alignment string from xml data to alignment enums
    :param alignment_str:
    :return:
    """
    assert isinstance(alignment_str, str)
    alignment_str = alignment_str.lower()
    if alignment_str == AlignmentEnum.NONE:
        alignment_enum = _default_alignment_pptx()
    elif alignment_str == AlignmentEnum.ALIGN_LEFT:
        alignment_enum = PP_PARAGRAPH_ALIGNMENT.LEFT
    elif alignment_str == AlignmentEnum.ALIGN_RIGHT:
        alignment_enum = PP_PARAGRAPH_ALIGNMENT.RIGHT
    elif alignment_str == AlignmentEnum.ALIGN_CENTER:
        alignment_enum = PP_PARAGRAPH_ALIGNMENT.CENTER
    elif alignment_str == AlignmentEnum.ALIGN_JUSTIFY:
        alignment_enum = PP_PARAGRAPH_ALIGNMENT.JUSTIFY
    else:
        alignment_enum = _default_alignment_pptx()

    return alignment_enum


def _get_enum(alignment):
    """
    Get alignment object corresponding with input alignment type
    :param alignment:
    :return:
    """
    if isinstance(alignment, DOCXEnum):
        return WD_PARAGRAPH_ALIGNMENT
    elif isinstance(alignment, PPTXEnum):
        return PP_PARAGRAPH_ALIGNMENT
    else:
        return WD_PARAGRAPH_ALIGNMENT


def is_left_align(alignment):
    """
    Is this left alignment (for all office modules)
    :param alignment:
    :return:
    """
    alignment_enum = _get_enum(alignment)
    return alignment == alignment_enum.LEFT


def is_right_align(alignment):
    """
    Is this right alignment (for all office modules)
    :param alignment:
    :return:
    """
    alignment_enum = _get_enum(alignment)
    return alignment == alignment_enum.RIGHT


def is_center_align(alignment):
    """
    Is this center alignment (for all office modules)
    :param alignment:
    :return:
    """
    alignment_enum = _get_enum(alignment)
    return alignment == alignment_enum.CENTER


def is_justify_align(alignment):
    """
    Is this justify alignment (for all office modules)
    :param alignment:
    :return:
    """
    alignment_enum = _get_enum(alignment)
    return alignment == alignment_enum.JUSTIFY


def _get_line_str(line):
    """
    Get string of line
    :param line:
    :return:
    """
    data = []
    for word in line:
        data.append(word.get('value'))
    return ' '.join(data)


def analysis_indent(office_paragraph, xml_paragraph, dpi, converter,
                    block=None,
                    page=None):
    """
    Analysis indentation for
    return tuple (left_indent, right_indent, first_line_indent)
    :param office_paragraph:
    :param xml_paragraph:
    :param dpi:
    :param converter:
    :param inside_textbox:
    :param block:
    :param page: dict like this:
    {
        'margin_left': self.margin_left,
        'margin_right': self.margin_right,
        'margin_top': self.margin_top,
        'margin_bottom': self.margin_bottom,
        'width': Pixel(self.width).inches
    }
    -- all measurement in emu
    :return:
    """

    first_line_indent = 0
    is_left = is_left_align(office_paragraph.alignment)
    is_justify = is_justify_align(office_paragraph.alignment)
    is_right = is_right_align(office_paragraph.alignment)
    is_center = is_center_align(office_paragraph.alignment)
    left_indent = converter(xml_paragraph.left_indent, dpi.horizontal_resolution).emu
    right_indent = converter(xml_paragraph.right_indent, dpi.horizontal_resolution).emu

    if is_left or is_justify or is_right:
        # First line indent
        first_line_indent = \
            converter(xml_paragraph.first_line_indent, dpi.horizontal_resolution).emu

    # Apply indentation into paragraph when it not inside of text box
    if block is not None and page is not None:
        block_x = int(get_transformed_x(page, block))
        block_right = block_x + int(get_transformed_w(page, block)) - 1
        left_indent += (converter(block_x, dpi.horizontal_resolution).emu
                        - get_transformed_margin_left(page))

        block_right_margin = (get_transformed_width(page)
                              - get_transformed_margin_right(page)
                              - converter(block_right, dpi.horizontal_resolution).emu)

        if len(xml_paragraph.lines) > 1 or is_right or is_center:
            # We only set right indent for paragraph have more than two lines
            # if only one line, don't need to set right indent
            right_indent += block_right_margin

    return left_indent, right_indent, first_line_indent


def indent_one_line_paragraph(paragraph_xml,
                              left_indent, right_indent,
                              position_transformer,
                              pixel_converter):
    """
    With one line paragraph_xml, we should not eliminate the
    right when align left and vice versa
    :param pixel_converter: Convert pixel to emu
    :param position_transformer:
    :param paragraph_xml: paragraph_xml which need to correct
    :param left_indent: current left indent
    :param right_indent: current right indent
    :return: tuple (left_indent, right_indent) after correct
    """
    if len(paragraph_xml.lines) == 1:
        alignment = paragraph_xml.alignment.lower()
        width = int(position_transformer.get_w(paragraph_xml))
        reduce_width = pixel_converter(width / 2).emu
        if alignment == AlignmentEnum.ALIGN_LEFT:
            right_indent -= reduce_width
        elif alignment == AlignmentEnum.ALIGN_RIGHT:
            left_indent -= reduce_width
        left_indent = max(0, left_indent)
        right_indent = max(0, right_indent)

    return left_indent, right_indent


def calculate_left_indent(par_format, left_indent):
    """
    When hanging, the python docx will set the left indent is
    -first_line_indent --> it is the issue of python docx.
    This code will reset the left indent
    :param par_format: format object of paragraph
    :param left_indent: original left indent from calculating in analysis_indent
    of alignment.py module
    :return:
    """
    is_hanging = par_format.first_line_indent < 0
    if is_hanging:
        left_indent -= par_format.first_line_indent
    return left_indent
