# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.phocr_error import PHOcrInvalidXmlException
from phocr_shared.xml_type_parser import XmlTypeParser


class XmlBooleanParser(XmlTypeParser):
    """Parsing boolean type in xml"""

    @classmethod
    def parse(cls, xml_obj, attribute, required=False, default=None):
        have_attribute, value = XmlTypeParser.preprocess_parse(
            xml_obj,
            attribute,
            required,
            default
        )
        if have_attribute:
            if value == 'True':
                return True
            elif value == 'False':
                return False
            else:
                raise PHOcrInvalidXmlException(
                    'Attribute {0} is not type {1} in xml object \n {2}'.format(
                        attribute,
                        bool.__name__,
                        str(xml_obj)
                    )
                )
