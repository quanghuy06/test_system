# encoding: utf-8

"""
DrawingML objects related to color, ColorFormat being the most prominent.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..oxml.simpletypes import ST_HexColorAuto
from phocr_shared.shared import ElementProxy


class ShadingBackground(ElementProxy):
    """
    Provides access to color settings such as RGB color, theme color, and
    luminance adjustments.
    """

    __slots__ = ()

    def __init__(self, pPr_parent):
        super(ShadingBackground, self).__init__(pPr_parent)

    @property
    def rgb(self):
        """
        An |RGBColor| value or |None| if no RGB color is specified.

        When :attr:`type` is `MSO_COLOR_TYPE.RGB`, the value of this property
        will always be an |RGBColor| value. It may also be an |RGBColor|
        value if :attr:`type` is `MSO_COLOR_TYPE.THEME`, as Word writes the
        current value of a theme color when one is assigned. In that case,
        the RGB value should be interpreted as no more than a good guess
        however, as the theme color takes precedence at rendering time. Its
        value is |None| whenever :attr:`type` is either |None| or
        `MSO_COLOR_TYPE.AUTO`.

        Assigning an |RGBColor| value causes :attr:`type` to become
        `MSO_COLOR_TYPE.RGB` and any theme color is removed. Assigning |None|
        causes any color to be removed such that the effective color is
        inherited from the style hierarchy.
        """
        shd = self._shd
        if shd is None:
            return None
        if shd.fill == ST_HexColorAuto.AUTO:
            return None
        return shd.fill

    @rgb.setter
    def rgb(self, value):
        if value is None and self._shd is None:
            return
        pPr = self._element.get_or_add_pPr()
        pPr._remove_shd()
        if value is not None:
            pPr.get_or_add_shd().fill = value

    @property
    def _shd(self):
        """
        Return `w:pPr/w:shd` or |None| if not present. Helper to factor out
        repetitive element access.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.shd
