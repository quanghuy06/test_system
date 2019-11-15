# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.phocr_config import PHOcrConstant
from phocr_elements.office_element import OfficeElement
from phocr_elements.office_carea import OfficeCarea
from phocr_elements.office_table import OfficeTable
from phocr_elements.office_photo import OfficePhoto
from phocr_shared.phocr_error import PHOcrError, PHOcrInvalidXmlException
from phocr_elements.office_object_tag import OfficeObjectTag
from phocr_shared.xml_orientation_parser import XmlOrientationParser
from phocr_shared.xml_writing_direction_parser import XmlWritingDirectionParser
from phocr_shared.xml_textline_direction_parser import \
    XmlTextlineDirectionParser
from phocr_shared.xml_int_parser import XmlIntParser
from phocr_shared.xml_float_parser import XmlFloatParser
from phocr_shared.text_direction import Orientation, \
    WritingDirection, TextlineOrder
from phocr_shared.paper_code_mapper import PaperCodeMapper
from phocr_shared.phocr_dpi import PHOcrDPI


class OfficePage(OfficeElement):
    """
    This class is mapping from OCRPage in utility folder of phocr
    """

    # Original paper size
    ORIGINAL_PAPER_SIZE = "original"
    # First paper size
    FIRST_PAPER_SIZE = "1stPage"

    def __init__(self):
        self.careas = []
        self.tables = []
        self.photos = []
        self.elements = []
        self.orientation = Orientation.ORIENTATION_PAGE_UP
        self.writing_direction = \
            WritingDirection.WRITING_DIRECTION_LEFT_TO_RIGHT
        self.textline_order = TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM
        self.title = ''
        self.deskew_angle = 0.0
        self.x_height = 0

        # Standard name of this paper size (A4, A3, Letter...)
        self.paper_name = ""

        # Code point of paper size corresponding with paper name, pass to
        # MS Office XML structure to set the paper size
        self.paper_code = 0

        # Standard width in Inch unit
        self.paper_width = 0

        # Standard height in Inch unit
        self.paper_height = 0

        # Orientation of standard paper
        self.paper_orientation = ""

        # Flag to check if page is standardized paper size
        self.is_using_standard_size = True
        self.baseline = 0
        self.dpi = PHOcrDPI(PHOcrConstant.DEFAULT_DPI, PHOcrConstant.DEFAULT_DPI)
        self.left_margin = 0
        self.right_margin = 0
        self.top_margin = 0
        self.bottom_margin = 0
        self.tag = OfficeObjectTag.PAGE

    def empty(self):
        if len(self.elements) == 0:
            return True
        return False

    def parse_xml(self, xml_obj):
        if xml_obj.tag != 'ocr_page':
            raise PHOcrInvalidXmlException(PHOcrError.INVALID_XML)
        OfficeElement.parse_xml(self, xml_obj)
        self.orientation = XmlOrientationParser.parse(
            xml_obj,
            'orientation',
            required=True
        )
        self.writing_direction = XmlWritingDirectionParser.parse(
            xml_obj,
            'writing_direction',
            required=True
        )
        self.textline_order = XmlTextlineDirectionParser.parse(
            xml_obj,
            'textline_order',
            required=True
        )
        self.deskew_angle = XmlFloatParser.parse(
            xml_obj,
            'deskew_angle',
            required=True
        )
        self.title = xml_obj.get('title')
        self.x_height = XmlIntParser.parse(
            xml_obj,
            'x_height',
            required=True
        )

        # Parse paper size information from XML file
        self.paper_name = xml_obj.get('paper_size')
        if self.paper_name == OfficePage.ORIGINAL_PAPER_SIZE or\
                self.paper_name == OfficePage.FIRST_PAPER_SIZE:
            self.is_using_standard_size = False
        else:
            self.paper_code = PaperCodeMapper.get_paper_code(self.paper_name)
        self.paper_orientation = xml_obj.get('paper_orientation')
        self.paper_width = XmlFloatParser.parse(
            xml_obj,
            'paper_width',
            required=True
        )
        self.paper_height = XmlFloatParser.parse(
            xml_obj,
            'paper_height',
            required=True
        )
        self.baseline = XmlIntParser.parse(
            xml_obj,
            'baseline',
            required=True
        )
        horizontal_dpi = XmlIntParser.parse(
            xml_obj,
            'horizontal_dpi',
            required=True
        )
        vertical_dpi = XmlIntParser.parse(
            xml_obj,
            'vertical_dpi',
            required=True
        )
        self.dpi = PHOcrDPI(horizontal_dpi, vertical_dpi)
        self.left_margin = XmlIntParser.parse(
            xml_obj,
            'margin_left',
            required=True
        )
        self.right_margin = XmlIntParser.parse(
            xml_obj,
            'margin_right',
            required=True
        )
        self.top_margin = XmlIntParser.parse(
            xml_obj,
            'margin_top',
            required=True
        )
        self.bottom_margin = XmlIntParser.parse(
            xml_obj,
            'margin_bottom',
            required=True
        )
        for obj_xml in xml_obj:
            if obj_xml.tag == 'ocr_carea':
                carea = OfficeCarea()
                carea.parse_xml(obj_xml)
                self.careas.append(carea)
                self.elements.append(carea)
            if obj_xml.tag == 'ocr_table_mask':
                table = OfficeTable()
                table.parse_xml(obj_xml)
                self.tables.append(table)
                self.elements.append(table)
            if obj_xml.tag == 'ocr_photo':
                photo = OfficePhoto()
                photo.parse_xml(obj_xml)
                self.photos.append(photo)
                self.elements.append(photo)

    def shift_vertical_position(self, shift_distance):
        """
        Shift all vertical coordinate of page and other elements inside page a
        shift distance
        :param shift_distance: The distance that we want to shift
        :return:
        """
        self.y += shift_distance
        # Shift all content areas inside page
        for content_area in self.careas:
            content_area.shift_vertical_position(shift_distance)
        # Shift all photos inside page
        for photo in self.photos:
            photo.shift_vertical_position(shift_distance)
        # Shift all tables inside page
        for table in self.tables:
            table.shift_vertical_position(shift_distance)

    def add_carea(self, carea):
        """
        Add one or a list of content areas to current page
        :param carea:
        :return:
        """
        self.careas.extend(carea)

    def add_table(self, table):
        """
        Add one or a list of table to current page
        :param table:
        :return:
        """
        self.tables.extend(table)

    def add_photo(self, photo):
        """
        Add one or a list of photos to current page
        :param photo:
        :return:
        """
        self.photos.extend(photo)
