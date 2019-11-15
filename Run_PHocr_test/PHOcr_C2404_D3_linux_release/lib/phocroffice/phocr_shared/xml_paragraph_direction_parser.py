# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.phocr_error import PHOcrInvalidXmlException
from phocr_shared.xml_type_parser import XmlTypeParser


class XmlParagraphDirectionParser(XmlTypeParser):
    """Parsing paragraph direction in xml"""
    DIRECTION = 'rtl'

    @classmethod
    def parse(cls, xml_obj, attribute, required=False, default=None):
        have_attribute, value = XmlTypeParser.preprocess_parse(
            xml_obj,
            attribute,
            required,
            default
        )
        if have_attribute:
            # If paragraph has direction, it must be 'rtl'.
            if value == cls.DIRECTION:
                return value
            else:
                raise PHOcrInvalidXmlException(
                    'Attribute {0} is not {1} in xml object \n {2}'.format(
                        attribute,
                        cls.DIRECTION,
                        str(xml_obj)
                    )
                )
