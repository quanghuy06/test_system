# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class OfficeElementWithBackground(object):
    """
    This class is mapping from OCRElementWithBackground
    in utility folder of phocr
    """
    def __init__(self):
        self.have_background_color = False
        self.background_color = None

    def parse_xml(self, xml_obj):
        self.background_color = xml_obj.get('background_color')
        if self.background_color is not None:
            self.have_background_color = True
