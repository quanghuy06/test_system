# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class OCRBox:
    def __init__(self, dpi, x, y, w, h, pixel_converter):
        """
        Box element

        Parameters
        ----------
        dpi
        x
        y
        w
        h
        pixel_converter
        """
        self._pixel_converter = pixel_converter
        self._dpi = dpi
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    def __str__(self):
        return 'x: {x}, y: {y}, w: {w}, h: {h}'.format(
            x=self.x_px, y=self.y_px, w=self.w_px, h=self.h_px
        )

    @classmethod
    def from_xml_element(cls, element, dpi, converter):
        try:
            return OCRBox(dpi,
                          element.x, element.y,
                          element.w, element.h,
                          converter)
        except Exception:
            return None

    @property
    def x(self):
        return self._pixel_converter(self._x, self._dpi.horizontal_resolution)

    @property
    def y(self):
        return self._pixel_converter(self._y, self._dpi.vertical_resolution)

    @property
    def w(self):
        return self._pixel_converter(self._w, self._dpi.horizontal_resolution)

    @property
    def h(self):
        return self._pixel_converter(self._h, self._dpi.vertical_resolution)

    @property
    def right(self):
        return self.x + self.w

    @property
    def bottom(self):
        return self.y + self.h

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

    @property
    def x_px(self):
        return self._x

    @property
    def y_px(self):
        return self._y

    @property
    def w_px(self):
        return self._w

    @property
    def h_px(self):
        return self._h

    @property
    def right_px(self):
        return self._x + self._w - 1

    @property
    def bottom_px(self):
        return self._y + self._h - 1

    @property
    def top_px(self):
        return self.y_px

    @property
    def left_px(self):
        return self.x_px
