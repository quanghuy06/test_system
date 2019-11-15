# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_elements.office_element import OfficeElement
from phocr_shared.phocr_error import PHOcrError, PHOcrInvalidXmlException
from phocr_elements.office_object_tag import OfficeObjectTag
from phocr_elements.office_word import OfficeWord
from phocr_shared.xml_int_parser import XmlIntParser
from phocr_shared.xml_float_parser import XmlFloatParser


class OfficeLine(OfficeElement):
    """
    This class is mapping from OCRLine in utility folder of phocr
    """
    def __init__(self):
        self.words = []
        self.text_angle = -1.0
        self.baseline = 0.0
        self.x_height = 0
        self.x_size = 0.0
        self.x_descenders = 0.0
        self.x_ascenders = 0.0
        self.tag = OfficeObjectTag.LINE

    def length(self):
        return len(self.words)

    def parse_xml(self, xml_obj):
        if xml_obj.tag != 'ocr_line':
            raise PHOcrInvalidXmlException(PHOcrError.INVALID_XML)
        OfficeElement.parse_xml(self, xml_obj)
        self.text_angle = XmlFloatParser.parse(
            xml_obj,
            'text_angle',
            required=True
        )
        self.baseline = XmlFloatParser.parse(
            xml_obj,
            'baseline',
            required=True
        )
        self.x_height = XmlIntParser.parse(
            xml_obj,
            'x_height',
            required=True
        )
        self.x_size = XmlFloatParser.parse(
            xml_obj,
            'x_size',
            required=True
        )
        self.x_descenders = XmlFloatParser.parse(
            xml_obj,
            'x_descenders',
            required=True
        )
        self.x_ascenders = XmlFloatParser.parse(
            xml_obj,
            'x_ascenders',
            required=True
        )
        for word_xml in xml_obj:
            word = OfficeWord()
            word.parse_xml(word_xml)
            self.words.append(word)

    def shift_vertical_position(self, shift_distance):
        """
        Shift all vertical coordinate of line and other elements inside it
        :param shift_distance: Input shift distance
        :return:
        """
        self.y += shift_distance
        # Shift all word inside line
        for word in self.words:
            word.shift_vertical_position(shift_distance)
