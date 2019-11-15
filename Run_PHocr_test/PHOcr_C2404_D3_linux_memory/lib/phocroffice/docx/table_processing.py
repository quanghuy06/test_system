# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
This module will process problems relating to table
"""

from phocr_shared.phocr_common import PHOcrCommon


class TableProcessing(object):
    """
    This class will process problems relating to table
    """

    @staticmethod
    def is_single_carea_cell(cell_xml):
        """
        This function will return background color if this is single cell

        Parameters
        ----------
        cell_xml : int
            Xml information of cell

        Returns
        -------

        """
        if len(cell_xml.careas) != 1:
            return
        carea = cell_xml.careas[0]
        par_xml = carea.paragraphs[0]
        background_color = par_xml.background_color
        if background_color is not None:
            return background_color
        return

    @staticmethod
    def assign_cell_color(cell_info, column_xml):
        """
        This function will set background color for cell

        Parameters
        ----------
        cell_info : Cell
            Instance of cell object in pptx library
        column_xml : int
            Xml information of cell

        Returns
        -------

        """

        cell_background_color = column_xml.highlight_color
        white_background_color = '255, 255, 255'
        if cell_background_color is None:
            cell_background_color = TableProcessing.is_single_carea_cell(
                column_xml
            )
            if cell_background_color is None:
                cell_background_color = white_background_color
        cell_rgb = str(PHOcrCommon.get_color(cell_background_color))
        cell_info.add_background_color(cell_rgb)

    @staticmethod
    def generate_border_info_for_cell(element):
        """
        Generate xml for cell having a missing edge

        Parameters
        ----------
        element

        Returns
        -------

        """
        border_info = '       <w:tcBorders>\n'
        if element.left_border:
            border_info += '         <w:left w:val="nil"/>\n'
        if element.right_border:
            border_info += '         <w:right w:val="nil"/>\n'
        if element.top_border:
            border_info += '         <w:top w:val="nil"/>\n'
        if element.bottom_border:
            border_info += '         <w:bottom w:val="nil"/>\n'
        border_info += '       </w:tcBorders>\n'

        return border_info
