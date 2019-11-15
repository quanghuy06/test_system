# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.shared import Pixel


class BoxAttribute(object):
    """
    Box attribute is default x, y, w, h in Pixel
    Additional, box attribute also provide twips measurement value for box size
    """
    def __init__(self, dpi, x, y, w, h):
        self._dpi = dpi
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    @property
    def x(self):
        return Pixel(self._x, self._dpi.horizontal_resolution)

    @property
    def y(self):
        return Pixel(self._y, self._dpi.vertical_resolution)

    @property
    def w(self):
        return Pixel(self._w, self._dpi.horizontal_resolution)

    @property
    def h(self):
        return Pixel(self._h, self._dpi.vertical_resolution)

    @property
    def x_twips(self):
        return self.x.twips

    @property
    def y_twips(self):
        return self.y.twips

    @property
    def w_twips(self):
        return self.w.twips

    @property
    def h_tTwips(self):
        return self.h.twips
