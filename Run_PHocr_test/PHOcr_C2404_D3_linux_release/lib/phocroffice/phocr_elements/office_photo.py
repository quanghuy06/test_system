# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_elements.office_element import OfficeElement
from phocr_shared.phocr_error import PHOcrError, PHOcrInvalidXmlException
from phocr_elements.office_object_tag import OfficeObjectTag
from phocr_shared.xml_boolean_parser import XmlBooleanParser


class OfficePhoto(OfficeElement):
    """
    This class is mapping from OCRPhoto in utility folder of phocr
    """
    def __init__(self):
        self.path = ''
        self.inside_table = False
        self.contain_table = False
        self.intersect_with_text_in_table = False
        self.tag = OfficeObjectTag.PHOTO

    def parse_xml(self, xml_obj):
        if xml_obj.tag != 'ocr_photo':
            raise PHOcrInvalidXmlException(PHOcrError.INVALID_XML)
        OfficeElement.parse_xml(self, xml_obj)
        self.path = xml_obj.get('image')
        self.inside_table = XmlBooleanParser.parse(
            xml_obj,
            'inside_table',
            required=True
        )
        self.contain_table = XmlBooleanParser.parse(
            xml_obj,
            'contain_table',
            required=True
        )
        self.intersect_with_text_in_table = XmlBooleanParser.parse(
            xml_obj,
            'intersect_with_text_in_table',
            required=True
        )

    def shift_vertical_position(self, shift_distance):
        """
        Shift all vertical coordinate of table
        :param shift_distance: Input shift distance
        :return:
        """
        self.y += shift_distance
