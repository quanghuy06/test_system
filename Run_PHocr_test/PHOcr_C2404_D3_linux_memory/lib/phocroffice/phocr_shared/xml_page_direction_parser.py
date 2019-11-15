# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_elements.office_enum import PageDirection
from phocr_shared.phocr_error import PHOcrInvalidXmlException
from phocr_shared.xml_type_parser import XmlTypeParser


class XmlPageDirectionParser(XmlTypeParser):
    """Parsing page direction in xml"""

    @classmethod
    def parse(cls, xml_obj, attribute, required=False, default=None):
        have_attribute, value = XmlTypeParser.preprocess_parse(
            xml_obj,
            attribute,
            required,
            default
        )
        if have_attribute:
            if value == 'HORIZONTAL':
                return PageDirection.HORIZONTAL
            elif value == 'VERTICAL':
                return PageDirection.VERTICAL
            else:
                raise PHOcrInvalidXmlException(
                    'Attribute {0} is not enum {1} in xml object \n {2}'.format(
                        attribute,
                        PageDirection.__name__,
                        str(xml_obj)
                    )
                )
