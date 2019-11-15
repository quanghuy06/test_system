# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class WordProperty(object):
    """
    This class handle word element get from element tree
    """
    def __init__(self, word):
        if word is not None:
            self.id = word.id
            self.x = word.x
            self.y = word.y
            self.w = word.w
            self.h = word.h
            self.color = str(word.color)
            self.highlight_color = str(word.highlight_color)
            self.spaces_before = word.spaces_before
            self.x_wconf = float(word.wfont)
            self.font_name = str(word.font)
            self.font_size = float(word.size)
            self.value = word.value
            self.bold = word.bold
            self.italic = word.italic
            self.underline = word.underline
        else:
            self.id = None
            self.x = None
            self.y = None
            self.w = None
            self.h = None
            self.color = None
            self.highlight_color = None
            self.spaces_before = None
            self.x_wconf = None
            self.font_name = None
            self.font_size = None
            self.value = None
            self.bold = None
            self.italic = None
            self.underline = None
