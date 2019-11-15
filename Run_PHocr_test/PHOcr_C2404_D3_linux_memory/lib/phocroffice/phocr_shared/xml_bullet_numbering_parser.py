# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.bullets_and_numberings import BULLET_NUMBERING
from phocr_shared.phocr_error import PHOcrInvalidXmlException
from phocr_shared.xml_type_parser import XmlTypeParser


class XmlBulletNumberingParser(XmlTypeParser):
    """Parsing type of bullet and numbering in xml"""

    @classmethod
    def parse(cls, xml_obj, attribute, required=False, default=None):
        have_attribute, value = XmlTypeParser.preprocess_parse(
            xml_obj,
            attribute,
            required,
            default
        )
        if have_attribute:
            if value == 'BULLET':
                return BULLET_NUMBERING.BULLET
            elif value == 'NUMBERING':
                return BULLET_NUMBERING.NUMBERING
            else:
                raise PHOcrInvalidXmlException(
                    'Attribute {0} is not type {1} in xml object \n {2}'.format(
                        attribute,
                        BULLET_NUMBERING.__name__,
                        str(xml_obj)
                    )
                )
