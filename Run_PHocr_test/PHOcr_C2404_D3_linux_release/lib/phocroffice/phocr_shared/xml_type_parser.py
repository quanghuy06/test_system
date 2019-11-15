# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from abc import abstractmethod, ABCMeta
from phocr_shared.phocr_error import PHOcrError, PHOcrInvalidXmlException


class XmlTypeParser(object):
    """
    This class is mapping from OCRElement in utility folder of phocr
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def parse(cls, xml_obj, attribute, required=False, default=None):
        pass

    @classmethod
    def preprocess_parse(cls, xml_obj, attribute, required=False, default=None):
        # Check input variable
        if xml_obj is None or attribute is None:
            raise PHOcrInvalidXmlException(PHOcrError.INVALID_INPUT_VARIABLE)

        # Get attribute
        value = xml_obj.get(attribute)
        if value is None:
            have_attribute = False
        else:
            have_attribute = True
        if not have_attribute:
            if required:
                raise PHOcrInvalidXmlException(
                    'Attribute {0} is required in xml object \n {1}'.format(
                        attribute,
                        str(xml_obj)
                    )
                )
            else:
                return have_attribute, default
        return have_attribute, value
