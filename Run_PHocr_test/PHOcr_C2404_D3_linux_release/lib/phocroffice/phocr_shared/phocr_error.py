# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
Class and Enumeration which related to error
"""


class PHOcrError(object):
    """
    Define errors when executing
    """
    INVALID_XML = 'XML object is invalid!'
    INVALID_OUTPUT_FORMAT = 'Output format is invalid!'
    MISSING_OUTPUT_FORMAT = 'Output format is docx, xlsx, pptx or all!'
    INVALID_INPUT_VARIABLE = 'Input variable is invalid!'


class PHOcrInvalidXmlException(Exception):
    pass
