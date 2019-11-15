# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.box_attribute import BoxAttribute


class TextBoxAttribute(BoxAttribute):
    """
    Contain information of textbox as position, paragraphs and angle
    """
    def __init__(self, dpi, x, y, w, h, paragraphs, angle=''):
        super(TextBoxAttribute, self).__init__(dpi, x, y, w, h)
        self.paragraphs = paragraphs
        self.angle = angle
