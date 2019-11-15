# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class OfficeElementWithHighlight(object):
    """
    This class is mapping from OCRElementWithHighlight
    in utility folder of phocr
    """
    def __init__(self):
        self.have_highlight_color = False
        self.highlight_color = None
        self.have_color = False
        self.color = None

    def parse_xml(self, xml_obj):
        self.highlight_color = xml_obj.get('highlight_color')
        if self.highlight_color is not None:
            self.have_highlight_color = True
        self.color = xml_obj.get('color')
        if self.color is not None:
            self.have_color = True
