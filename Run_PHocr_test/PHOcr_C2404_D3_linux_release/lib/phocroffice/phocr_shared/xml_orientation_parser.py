# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.text_direction import Orientation
from phocr_shared.phocr_error import PHOcrInvalidXmlException
from phocr_shared.xml_type_parser import XmlTypeParser


class XmlOrientationParser(XmlTypeParser):
    """Parsing orientation in xml"""

    @classmethod
    def parse(cls, xml_obj, attribute, required=False, default=None):
        have_attribute, value = XmlTypeParser.preprocess_parse(
            xml_obj,
            attribute,
            required,
            default
        )
        if have_attribute:
            if value == 'ORIENTATION_ERROR':
                return Orientation.ORIENTATION_ERROR
            elif value == 'ORIENTATION_PAGE_UP':
                return Orientation.ORIENTATION_PAGE_UP
            elif value == 'ORIENTATION_PAGE_RIGHT':
                return Orientation.ORIENTATION_PAGE_RIGHT
            elif value == 'ORIENTATION_PAGE_DOWN':
                return Orientation.ORIENTATION_PAGE_DOWN
            elif value == 'ORIENTATION_PAGE_LEFT':
                return Orientation.ORIENTATION_PAGE_LEFT
            else:
                raise PHOcrInvalidXmlException(
                    'Attribute {0} is not enum {1} in xml object \n {2}'.format(
                        attribute,
                        Orientation.__name__,
                        str(xml_obj)
                    )
                )
