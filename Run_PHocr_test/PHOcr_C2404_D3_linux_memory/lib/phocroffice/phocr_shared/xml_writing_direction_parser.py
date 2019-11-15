# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.text_direction import WritingDirection
from phocr_shared.phocr_error import PHOcrInvalidXmlException
from phocr_shared.xml_type_parser import XmlTypeParser


class XmlWritingDirectionParser(XmlTypeParser):
    """Parsing writing direction in xml"""

    @classmethod
    def parse(cls, xml_obj, attribute, required=False, default=None):
        have_attribute, value = XmlTypeParser.preprocess_parse(
            xml_obj,
            attribute,
            required,
            default
        )
        if have_attribute:
            if value == 'WRITING_DIRECTION_ERROR':
                return WritingDirection.WRITING_DIRECTION_ERROR
            elif value == 'WRITING_DIRECTION_LEFT_TO_RIGHT':
                return WritingDirection.WRITING_DIRECTION_LEFT_TO_RIGHT
            elif value == 'WRITING_DIRECTION_RIGHT_TO_LEFT':
                return WritingDirection.WRITING_DIRECTION_RIGHT_TO_LEFT
            elif value == 'WRITING_DIRECTION_TOP_TO_BOTTOM':
                return WritingDirection.WRITING_DIRECTION_TOP_TO_BOTTOM
            else:
                raise PHOcrInvalidXmlException(
                    'Attribute {0} is not enum {1} in xml object \n {2}'.format(
                        attribute,
                        WritingDirection.__name__,
                        str(xml_obj)
                    )
                )
