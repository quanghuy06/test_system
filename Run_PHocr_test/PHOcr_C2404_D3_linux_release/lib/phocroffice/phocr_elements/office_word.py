# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_elements.office_element import OfficeElement
from phocr_elements.office_element_with_highlight import \
    OfficeElementWithHighlight
from phocr_elements.office_object_tag import OfficeObjectTag
from phocr_shared.phocr_error import PHOcrError, PHOcrInvalidXmlException
from phocr_shared.xml_boolean_parser import XmlBooleanParser
from phocr_shared.xml_int_parser import XmlIntParser
from phocr_shared.xml_language_parser import XmlLanguageParser
from phocr_shared.xml_paragraph_direction_parser import \
    XmlParagraphDirectionParser


class OfficeCharacter(OfficeElement):
    """
    This class is mapping from OCRCharacter in utility folder of phocr
    """
    def __init__(self):
        self.value = ''
        self.tag = OfficeObjectTag.CHARACTER

    def parse_xml(self, xml_obj):
        if xml_obj.tag != 'ocr_character':
            raise PHOcrInvalidXmlException(PHOcrError.INVALID_XML)
        OfficeElement.parse_xml(self, xml_obj)
        self.value = xml_obj.get('value')

    def shift_vertical_position(self, shift_distance):
        """
        Shift all vertical coordinate of one character
        :param shift_distance: Input shift distance
        :return:
        """
        self.y += shift_distance


class OfficeWord(OfficeElement, OfficeElementWithHighlight):
    """
    This class is mapping from OCRWord in utility folder of phocr
    """
    def __init__(self):
        self.characters = []
        self.value = ''
        self.font = None
        self.wfont = 0.0
        self.size = None
        self.bold = False
        self.italic = False
        self.underline = False
        self.spaces_before = 0
        self.lang = ''
        self.direction = ''
        self.numeric = False
        self.monospace = None
        self.serif = None
        self.smallcaps = None
        self.tag = OfficeObjectTag.WORD

    def parse_xml(self, xml_obj):
        if xml_obj.tag != 'ocr_word':
            raise PHOcrInvalidXmlException(PHOcrError.INVALID_XML)
        OfficeElement.parse_xml(self, xml_obj)
        OfficeElementWithHighlight.parse_xml(self, xml_obj)
        self.value = u'{0}'.format(xml_obj.get('value'))
        self.font = xml_obj.get('x_font')
        self.wfont = XmlIntParser.parse(
            xml_obj,
            'x_wconf',
            required=True
        )
        self.size = xml_obj.get('x_fsize')
        self.spaces_before = XmlIntParser.parse(
            xml_obj,
            'spaces_before',
            required=True
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
        self.numeric = XmlBooleanParser.parse(
            xml_obj,
            'numeric',
            required=False,
            default=False
        )
        self.monospace = XmlBooleanParser.parse(
            xml_obj,
            'monospace',
            required=False,
            default=False
        )
        self.serif = XmlBooleanParser.parse(
            xml_obj,
            'serif',
            required=False,
            default=False
        )
        self.smallcaps = XmlBooleanParser.parse(
            xml_obj,
            'smallcaps',
            required=False,
            default=False
        )
        self.bold = XmlBooleanParser.parse(
            xml_obj,
            'bold',
            required=False,
            default=False
        )
        self.italic = XmlBooleanParser.parse(
            xml_obj,
            'italic',
            required=False,
            default=False
        )
        self.underline = XmlBooleanParser.parse(
            xml_obj,
            'underline',
            required=False,
            default=False
        )
        for character_xml in xml_obj:
            character = OfficeCharacter()
            character.parse_xml(character_xml)
            self.characters.append(character)

    def shift_vertical_position(self, shift_distance):
        """
        Shift all vertical coordinate of one word and other elements inside it
        :param shift_distance: Input shift distance
        :return:
        """
        self.y += shift_distance
        # Shift all characters inside word
        for character in self.characters:
            character.shift_vertical_position(shift_distance)
