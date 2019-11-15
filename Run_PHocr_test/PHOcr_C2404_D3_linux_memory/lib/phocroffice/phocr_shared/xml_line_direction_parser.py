# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_elements.office_enum import LineDirection
from phocr_shared.phocr_error import PHOcrInvalidXmlException
from phocr_shared.xml_type_parser import XmlTypeParser


class XmlLineDirectionParser(XmlTypeParser):
    """Parsing line direction in xml"""

    @classmethod
    def parse(cls, xml_obj, attribute, required=False, default=None):
        have_attribute, value = XmlTypeParser.preprocess_parse(
            xml_obj,
            attribute,
            required,
            default
        )
        if have_attribute:
            if value == 'LEFT_TO_RIGHT':
                return LineDirection.LEFT_TO_RIGHT
            elif value == 'RIGHT_TO_LEFT':
                return LineDirection.RIGHT_TO_LEFT
            elif value == 'TOP_TO_BOTTOM':
                return LineDirection.TOP_TO_BOTTOM
            else:
                raise PHOcrInvalidXmlException(
                    'Attribute {0} is not enum {1} in xml object \n {2}'.format(
                        attribute,
                        LineDirection.__name__,
                        str(xml_obj)
                    )
                )
