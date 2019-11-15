# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_elements.office_element import OfficeElement
from phocr_elements.office_carea import OfficeCarea
from phocr_elements.office_photo import OfficePhoto
from phocr_shared.phocr_error import PHOcrError, PHOcrInvalidXmlException
from phocr_elements.office_object_tag import OfficeObjectTag
from phocr_elements.office_element_with_highlight import \
    OfficeElementWithHighlight
from phocr_shared.xml_boolean_parser import XmlBooleanParser
from phocr_shared.xml_int_parser import XmlIntParser


class OfficeBorder(object):
    def __init__(self, missing, color, thickness):
        self.missing = missing
        self.color = color
        self.thickness = thickness


class OfficeCell(OfficeElement, OfficeElementWithHighlight):
    """
    This class is mapping from OCRCell in utility folder of phocr
    """
    def __init__(self):
        self.careas = []
        self.tables = []
        self.photos = []
        self.elements = []
        self.left_border = False
        self.right_border = False
        self.top_border = False
        self.bottom_border = False
        self.col_span = 1
        self.row_span = 1
        self.tag = OfficeObjectTag.CELL

    def length(self):
        return len(self.elements)

    def empty(self):
        if self.length() == 0:
            return True
        return False

    def parse_xml(self, xml_obj):
        if xml_obj.tag != 'ocr_column':
            raise PHOcrInvalidXmlException(PHOcrError.INVALID_XML)
        OfficeElement.parse_xml(self, xml_obj)
        OfficeElementWithHighlight.parse_xml(self, xml_obj)
        self.col_span = XmlIntParser.parse(
            xml_obj,
            'col_span',
            required=True
        )
        self.row_span = XmlIntParser.parse(
            xml_obj,
            'row_span',
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
            if obj_xml.tag == 'missing_edge':
                self.left_border = XmlBooleanParser.parse(
                    obj_xml,
                    'left',
                    required=False,
                    default=False
                )
                self.right_border = XmlBooleanParser.parse(
                    obj_xml,
                    'right',
                    required=False,
                    default=False
                )
                self.top_border = XmlBooleanParser.parse(
                    obj_xml,
                    'top',
                    required=False,
                    default=False
                )
                self.bottom_border = XmlBooleanParser.parse(
                    obj_xml,
                    'bottom',
                    required=False,
                    default=False
                )

    def shift_vertical_position(self, shift_distance):
        """
        Shift a cell in vertical coordinate
        :param shift_distance:
        :return:
        """
        self.y += shift_distance
        # Shift vertical coordinate of all elements
        for element in self.elements:
            element.shift_vertical_position()


class OfficeRow(OfficeElement):
    """
    This class is mapping from OCRRow in utility folder of phocr
    """
    def __init__(self):
        self.cells = []
        self.num_cols = 1
        self.tag = OfficeObjectTag.ROW

    def parse_xml(self, xml_obj):
        if xml_obj.tag != 'ocr_row':
            raise PHOcrInvalidXmlException(PHOcrError.INVALID_XML)
        OfficeElement.parse_xml(self, xml_obj)
        self.num_cols = XmlIntParser.parse(xml_obj, 'num_cols', required=True)
        for cell_xml in xml_obj:
            cell = OfficeCell()
            cell.parse_xml(cell_xml)
            self.cells.append(cell)

    def shift_vertical_position(self, shift_distance):
        """
        Shift all vertical coordinate of row
        :param shift_distance: Input shift distance
        :return:
        """
        self.y += shift_distance
        # Shift all cell inside row
        for cell in self.cells:
            cell.shift_vertical_position(shift_distance)


class OfficeTable(OfficeElement):
    """
    This class is mapping from OCRTable in utility folder of phocr
    """
    def __init__(self):
        self.rows = []
        self.num_rows = 1
        self.num_cells = 1
        self.tag = OfficeObjectTag.TABLE

    def parse_xml(self, xml_obj):
        if xml_obj.tag != 'ocr_table_mask':
            raise PHOcrInvalidXmlException(PHOcrError.INVALID_XML)
        OfficeElement.parse_xml(self, xml_obj)
        self.num_cells = XmlIntParser.parse(xml_obj, 'col', required=True)
        self.num_rows = XmlIntParser.parse(xml_obj, 'row', required=True)
        for row_xml in xml_obj:
            row = OfficeRow()
            row.parse_xml(row_xml)
            self.rows.append(row)

    def shift_vertical_position(self, shift_distance):
        """
        Shift all vertical coordinate of table and other elements inside
        :param shift_distance:
        :return:
        """
        self.y += shift_distance
        # Shift all row
        for row in self.rows:
            row.shift_vertical_position(shift_distance)
