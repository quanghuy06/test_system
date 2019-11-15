# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
This module is used to draw position of elements over input image.
The purpose is for easy debugging PHOcrOffice module
"""
import os
from PIL import Image, ImageDraw, ImageFont
from .base_element import BaseElement

# Define some constant tag of PHOcr office
OCR_PAGE = "ocr_page"
OCR_TABLE = "ocr_table_mask"
OCR_CAREA = "ocr_carea"
OCR_ROW = "ocr_row"

class ElementDraw(object):
    """
    Draw box of elements over image
    """
    blank_layer = "blank_layer.png"
    output_file = "element_draw.png"
    def __init__(self, img_width, img_height, source_image=None):
        """Init"""
        self._width = img_width
        self._height = img_height
        source_img = ""
        if source_image is None:
            # Create a blank layer with A4 size
            img = Image.new('RGB', (self._width, self._height), color='white')
            img.save(ElementDraw.blank_layer)
            source_img = ElementDraw.blank_layer
        else:
            source_img = source_image
        self._source_img = Image.open(source_img)
        self._draw = ImageDraw.Draw(self._source_img)
        self._font = ImageFont.load_default()

    def __del__(self):
        """Destructor"""
        if os.path.exists(ElementDraw.blank_layer):
            os.remove(ElementDraw.blank_layer)

    def write(self, tree_element):
        """
        Save the box of element
        The main api to outside
        :return:
        """
        self.write_down_element(tree_element)
        self._source_img.save(self.output_file, "PNG")

    def _draw_text_box(self, textbox_element):
        """
        Draw boxes related with text attributes element
        :return:
        """
        textbox = BaseElement(textbox_element)
        self._draw_element(textbox)

    def _draw_table(self, table_element):
        """
        Draw boxes related with table element
        :return:
        """
        table = BaseElement(table_element)
        # Draw table box first
        self._draw_element(table)

        # Draw rows
        for row_element in table_element:
            row = BaseElement(row_element)
            self._draw_element(row)
            for col_element in row_element:
                col = BaseElement(col_element)
                self._draw_element(col)

    def _draw_element(self, base_element):
        """Draw rectangle of element"""
        self._draw.rectangle([(base_element.box.left, base_element.box.top),
                           (base_element.box.left + base_element.box.width,
                            base_element.box.top + base_element.box.height)],
                            outline='red', fill=None)

        # Write text down to photo
        text_value = base_element.tag + " " + base_element.m_id

        # Write table name to upper middle of table
        if base_element.tag == OCR_TABLE:
            self._draw.text((base_element.box.left + base_element.box.width / 2,
                            base_element.box.top - 10),
                           text_value, font=self._font, fill=255)
        # Write ocr row to lower of row
        elif base_element.tag == OCR_ROW:
            self._draw.text((base_element.box.left,
                            base_element.box.top + 5),
                           text_value, font=self._font, fill=255)
        # Write col and other to middle
        else:
            self._draw.text((base_element.box.left,
                            base_element.box.top + base_element.box.height / 2),
                           text_value, font=self._font, fill=255)

    def write_down_element(self, tree_element):
        """
        Write down the image for input element
        Can use outside
        """
        element = BaseElement(tree_element)
        input_tag = element.tag
        if input_tag == OCR_TABLE:
            self._draw_table(tree_element)
        if input_tag == OCR_CAREA:
            self._draw_text_box(tree_element)
        if input_tag == OCR_PAGE:
            for member in tree_element:
                self.write_down_element(member)
