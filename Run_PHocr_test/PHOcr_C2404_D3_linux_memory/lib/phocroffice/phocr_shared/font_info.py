# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class FontInfo(object):
    """
    Class FontInfo to store any information of a font,
    include: font name, font size, bold, italic, underline
    """
    def __init__(self, word):
        if word is not None:
            self.name = word.font
            self.size = float(word.size)
            self.bold = word.bold
            self.italic = word.italic
            self.underline = word.underline
        else:
            self.name = None
            self.size = None
            self.bold = None
            self.italic = None
            self.underline = None
