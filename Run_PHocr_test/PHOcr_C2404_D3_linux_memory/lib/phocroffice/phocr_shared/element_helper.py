# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
Helper related to xml element which belong lxml
"""


def paragraph_to_string(paragraph):
    """
    Return string of PHOcr paragraph by travel all lines and words inside
    :param paragraph: input paragraph xml which is instance of lxml element
    :return: content string of paragraph
    """
    result = ''
    for line in paragraph.lines:
        for word in line.words:
            result += word.value + ' '
        result += '\n'
    return result


def carea_to_string(carea):
    """
    Return strong of PHOcr carea
    :param carea:
    :return:
    """
    result = ''
    for paragraph in carea.paragraphs:
        result += paragraph_to_string(paragraph)
    return result
