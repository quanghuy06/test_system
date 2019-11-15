# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.phocr_error import PHOcrInvalidXmlException
from phocr_shared.xml_type_parser import XmlTypeParser
from phocr_shared.phocr_supported_languages import PHOcrSupportedLanguages


class XmlLanguageParser(XmlTypeParser):
    """Parsing language in xml"""

    @classmethod
    def parse(cls, xml_obj, attribute, required=False, default=None):
        have_attribute, value = XmlTypeParser.preprocess_parse(
            xml_obj,
            attribute,
            required,
            default
        )
        if have_attribute:
            if value in PHOcrSupportedLanguages.LANGUAGES:
                return value
            else:
                raise PHOcrInvalidXmlException(
                    'Language {0} is not in {1} in xml object \n {2}'.format(
                        value,
                        PHOcrSupportedLanguages.__name__,
                        str(xml_obj)
                    )
                )
