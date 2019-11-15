# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.alignment_enum import AlignmentEnum
from phocr_shared.phocr_error import PHOcrInvalidXmlException
from phocr_shared.xml_type_parser import XmlTypeParser


class XmlAlignmentParser(XmlTypeParser):
    """Parsing alignment in xml"""

    @classmethod
    def parse(cls, xml_obj, attribute, required=False, default=None):
        have_attribute, value = XmlTypeParser.preprocess_parse(
            xml_obj,
            attribute,
            required,
            default
        )
        if have_attribute:
            if value == 'NONE':
                return AlignmentEnum.NONE
            elif value == 'LEFT':
                return AlignmentEnum.ALIGN_LEFT
            elif value == 'RIGHT':
                return AlignmentEnum.ALIGN_RIGHT
            elif value == 'CENTER':
                return AlignmentEnum.ALIGN_CENTER
            elif value == 'JUSTIFY':
                return AlignmentEnum.ALIGN_JUSTIFY
            elif value == 'JUSTIFY_FULL':
                return AlignmentEnum.ALIGN_JUSTIFY_FULL
            else:
                raise PHOcrInvalidXmlException(
                    'Attribute {0} is not enum {1} in xml object \n {2}'.format(
                        attribute,
                        AlignmentEnum.__name__,
                        str(xml_obj)
                    )
                )
