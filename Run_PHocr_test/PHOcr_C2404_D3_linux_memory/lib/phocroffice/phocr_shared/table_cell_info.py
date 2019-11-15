# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class TableCellInfo(object):
    """
    Contain strings of character areas and
    missing border of a cell in the table
    """
    def __init__(self, careas, border_info, background_color):
        """
        Parameters
        ----------
        careas
            Character areas xml information
        border_info
            Missing edge xml information
        background_color
            Background color information

        Returns
        -------

        """
        self.careas = careas
        self.border_info = border_info
        self.background_color = background_color

    def add_carea_for_cell(self, carea):
        """
        Add character area into cell to export this information
        to xml file later

        Parameters
        ----------
        carea
            added character area

        Returns
        -------

        """
        self.careas += carea

    def add_border_for_cell(self, border_info):
        """
        Add missing border into cell to export this information
        to xml file later

        Parameters
        ----------
        border_info
            added missing border information

        Returns
        -------

        """
        self.border_info += border_info

    def add_background_color(self, background_color):
        """
        Add background color into cell to export this information
        to xml file later

        Parameters
        ----------
        background_color
            added background color information

        Returns
        -------

        """
        self.background_color = background_color
