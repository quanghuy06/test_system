# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.box_attribute import BoxAttribute


class PhotoAttribute(BoxAttribute):
    def __init__(self, dpi, x, y, w, h, path, wrap, inside_table=False):
        super(PhotoAttribute, self).__init__(dpi, x, y, w, h)
        self.path = path
        self.wrap = wrap
        self.inside_table = inside_table
