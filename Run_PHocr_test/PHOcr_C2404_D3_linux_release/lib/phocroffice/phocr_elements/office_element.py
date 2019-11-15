# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from abc import abstractmethod, ABCMeta
import json
from phocr_shared.phocr_config import PHOcrConstant
from phocr_elements.office_object_tag import OfficeObjectTag
from phocr_shared.xml_int_parser import XmlIntParser
from phocr_shared.xml_page_direction_parser import XmlPageDirectionParser
from phocr_shared.xml_line_direction_parser import XmlLineDirectionParser
from phocr_elements.office_enum import PageDirection
from phocr_elements.office_enum import LineDirection


class OfficeElement(object):
    """
    This class is mapping from OCRElement in utility folder of phocr
    """
    __metaclass__ = ABCMeta

    def __init__(self, id_, x, y, w, h):
        self.id = id_
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.str_value = ''
        self.page_dir = None
        self.line_dir = None
        self.tag = OfficeObjectTag.UNKNOWN

    @abstractmethod
    def parse_xml(self, xml_obj):
        self.id = XmlIntParser.parse(xml_obj, 'id', required=True)
        self.x = XmlIntParser.parse(xml_obj, 'x', required=True)
        self.y = XmlIntParser.parse(xml_obj, 'y', required=True)
        self.w = XmlIntParser.parse(xml_obj, 'w', required=True)
        self.h = XmlIntParser.parse(xml_obj, 'h', required=True)
        self.page_dir = XmlPageDirectionParser.parse(
            xml_obj,
            'page_dir',
            required=False,
            default=PageDirection.HORIZONTAL
        )
        self.line_dir = XmlLineDirectionParser.parse(
            xml_obj,
            'line_dir',
            required=False,
            default=LineDirection.TOP_TO_BOTTOM
        )

    def post_process_xml(self, xml_obj):
        pass

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=2)

    def __str__(self):
        """
        Return string represent of office element
        :return:
        """
        result = 'id: ' + str(self.id) + ' [x: ' + str(self.x) + ', y: ' + \
                 str(self.y) + ', w: ' + str(self.w) + ', h: ' + str(self.h) + \
                 ']'
        return result
