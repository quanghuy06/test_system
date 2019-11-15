# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_elements.office_element import OfficeElement
from phocr_shared.phocr_error import PHOcrError, PHOcrInvalidXmlException
from phocr_elements.office_line import OfficeLine
from phocr_elements.office_element_with_background import \
    OfficeElementWithBackground
from phocr_elements.office_object_tag import OfficeObjectTag
from phocr_shared.alignment_enum import AlignmentEnum
from phocr_shared.xml_alignment_parser import XmlAlignmentParser
from phocr_shared.xml_bullet_numbering_parser import XmlBulletNumberingParser
from phocr_shared.xml_paragraph_direction_parser import \
    XmlParagraphDirectionParser
from phocr_shared.xml_boolean_parser import XmlBooleanParser
from phocr_shared.xml_int_parser import XmlIntParser
from phocr_shared.xml_language_parser import XmlLanguageParser


class OfficeParagraph(OfficeElement, OfficeElementWithBackground):
    """
    This class is mapping from OCRParagraph in utility folder of phocr
    """
    def __init__(self):
        self.lines = []
        self.first_line_indent = 0
        self.line_spacing = 0
        self.left_indent = 0
        self.right_indent = 0
        self.right_padding = 0
        self.alignment = AlignmentEnum.ALIGN_LEFT
        self.space_after = 0
        self.space_before = 0
        self.is_list = False
        self.list_type = None
        self.list_name = None
        self.list_level = None
        self.start_at = -1
        self.lang = None
        self.direction = None
        self.background_color = None
        self.tag = OfficeObjectTag.PARAGRAPH

    def parse_xml(self, xml_obj):
        if xml_obj.tag != 'ocr_par':
            raise PHOcrInvalidXmlException(PHOcrError.INVALID_XML)
        OfficeElement.parse_xml(self, xml_obj)
        OfficeElementWithBackground.parse_xml(self, xml_obj)
        self.first_line_indent = XmlIntParser.parse(
            xml_obj,
            'first-line-indent',
            required=True
        )
        self.left_indent = XmlIntParser.parse(
            xml_obj,
            'left-indent',
            required=True
        )
        self.right_indent = XmlIntParser.parse(
            xml_obj,
            'right-indent',
            required=True
        )
        self.right_padding = XmlIntParser.parse(
            xml_obj,
            'right-padding',
            required=True
        )
        self.alignment = XmlAlignmentParser.parse(
            xml_obj,
            'alignment',
            required=True
        )
        self.is_list = XmlBooleanParser.parse(
            xml_obj,
            'is_list',
            required=False,
            default=False
        )
        if self.is_list:
            self.list_type = XmlBulletNumberingParser.parse(
                xml_obj,
                'list_type',
                required=False,
                default=''
            )
            self.list_name = xml_obj.get('list_name')
            self.list_level = xml_obj.get('list_level')
            self.start_at = XmlIntParser.parse(
                xml_obj,
                'start_at',
                required=False,
                default=0
            )
        self.lang = XmlLanguageParser.parse(
            xml_obj,
            'lang',
            required=False,
            default=''
        )
        self.direction = XmlParagraphDirectionParser.parse(
            xml_obj,
            'dir',
            required=False,
            default=''
        )
        for line_xml in xml_obj:
            line = OfficeLine()
            line.parse_xml(line_xml)
            self.lines.append(line)

    def recalculate_indent(self, page=None, cell=None, carea=None):
        pass

    def shift_vertical_position(self, shift_distance):
        """
        Shift all vertical coordinate of one paragraph and other elements inside
        :param shift_distance: Input shift distance
        :return:
        """
        self.y += shift_distance
        # Shift all lines inside this paragraph
        for line in self.lines:
            line.shift_vertical_position(shift_distance)
