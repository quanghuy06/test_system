# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_elements.office_element import OfficeElement
from phocr_elements.office_element_with_background import \
    OfficeElementWithBackground
from phocr_shared.phocr_error import PHOcrError, PHOcrInvalidXmlException
from phocr_elements.office_paragraph import OfficeParagraph
from phocr_elements.office_object_tag import OfficeObjectTag
from phocr_shared.xml_page_direction_parser import XmlPageDirectionParser
from phocr_shared.xml_line_direction_parser import XmlLineDirectionParser
from phocr_shared.xml_boolean_parser import XmlBooleanParser
from phocr_shared.xml_int_parser import XmlIntParser


class OfficeCarea(OfficeElement, OfficeElementWithBackground):
    """
    This class is mapping from OCRCarea in utility folder of phocr
    """
    def __init__(self):
        self.paragraphs = []
        self.writing_direction = None
        self.textline_order = None
        self.right_padding = 0
        self.is_noise = False
        self.background_color = ''
        self.tag = OfficeObjectTag.CAREA

    def parse_xml(self, xml_obj):
        if xml_obj.tag != 'ocr_carea':
            raise PHOcrInvalidXmlException(PHOcrError.INVALID_XML)
        OfficeElement.parse_xml(self, xml_obj)
        OfficeElementWithBackground.parse_xml(self, xml_obj)
        self.writing_direction = XmlPageDirectionParser.parse(
            xml_obj,
            'writing_direction',
            required=True
        )
        self.textline_order = XmlLineDirectionParser.parse(
            xml_obj,
            'textline_order',
            required=True
        )
        self.is_noise = XmlBooleanParser.parse(
            xml_obj,
            'is_noise',
            required=True
        )
        self.right_padding = XmlIntParser.parse(
            xml_obj,
            'right-padding',
            required=True
        )
        for paragraph_xml in xml_obj:
            paragraph = OfficeParagraph()
            paragraph.parse_xml(paragraph_xml)
            self.paragraphs.append(paragraph)

    def shift_vertical_position(self, shift_distance):
        """
        Shift all vertical coordinate of one content area and other elements
        inside it
        :param shift_distance: Input shift distance
        :return:
        """
        self.y += shift_distance
        for paragraph in self.paragraphs:
            paragraph.shift_vertical_position(shift_distance)
