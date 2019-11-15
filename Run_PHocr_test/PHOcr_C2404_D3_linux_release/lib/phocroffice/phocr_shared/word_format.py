# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
from phocr_shared.phocr_common import PHOcrCommon
from docx.common import Common

class WordFormat(object):
    """
    This class handle word element get from element tree
    """
    def __init__(self, word):
        if word is not None:
            self.id = word.id
            self.color = word.color
            self.highlight_color = word.highlight_color
            self.spaces_before = word.spaces_before
            self.font_name = word.font
            self.font_size = word.size
            self.value = word.value
            self.bold = word.bold
            self.italic = word.italic
            self.underline = word.underline
        else:
            self.id = None
            self.color = None
            self.highlight_color = None
            self.spaces_before = None
            self.font_name = None
            self.font_size = None
            self.value = None
            self.bold = None
            self.italic = None
            self.underline = None

    def is_same_color(self, word):
        """
        Checking the word has same color with this word
        Same color or (or different a small value)
        Parameters
        ----------
        word is WordProperty

        Returns True if the word has same color with this word.
        -------
        """
        color = self.color
        if color is not None:
            color = PHOcrCommon.get_color(self.color)
            color = (color[0], color[1], color[2])

        color_word = word.color
        if color_word is not None:
            color_word = PHOcrCommon.get_color(word.color)
            color_word = (color_word[0], color_word[1], color_word[2])

        same_color = False
        if color == color_word:
            same_color = True
        else:
            if color is not None and color_word is not None:
                r1, g1, b1 = color
                r2, g2, b2 = color_word
                dr, dg, db = (abs(r2 - r1), abs(g2 - g1), abs(b2 - b1))
                if all([dr < 20, dg < 20, db < 20]):
                    same_color = True
        return same_color

    def is_same_highlight_color(self, word):
        """
        Checking the word has same highlight color with this word

        Parameters
        ----------
        word is WordProperty

        Returns True if the word has same highlight color with this word.
        -------
        """
        highlight = None
        if self.highlight_color is not None:
            highlight = Common.get_highlight_color(self.highlight_color)

        highlight_word = None
        if word.highlight_color is not None:
            highlight_word = Common.get_highlight_color(word.highlight_color)
        same_highlight = highlight == highlight_word
        return same_highlight

    def is_same_bold(self, word):
        """
        Checking the word has same bold with this word

        Parameters
        ----------
        word is WordProperty

        Returns True if the word has same bold with this word.
        -------
        """
        same_bold = self.bold == word.bold
        return same_bold

    def is_same_italic(self, word):
        """
        Checking the word has same italic with this word

        Parameters
        ----------
        word is WordProperty

        Returns True if the word has same italic with this word.
        -------
        """
        same_italic = self.italic == word.italic
        return same_italic

    def is_same_underline(self, word):
        """
        Checking the word has same underline with this word

        Parameters
        ----------
        word is WordProperty

        Returns True if the word has same underline with this word.
        -------
        """
        same_underline = self.underline == word.underline
        return same_underline

    def is_same_font_size(self, word):
        """
        Checking the word has same font size with this word

        Parameters
        ----------
        word is WordProperty

        Returns True if the word has same font size with this word.
        -------
        """
        same_font_size = self.font_size == word.font_size
        return same_font_size

    def is_same_font_name(self, word):
        """
        Checking the word has same font name with this word

        Parameters
        ----------
        word is WordProperty

        Returns True if the word has same font name with this word.
        -------
        """
        same_font_name = self.font_name = word.font_name
        return same_font_name

    def is_same_format(self, word):
        """
        Checking the word has same format with this word
        Two words information have same format:
        - same color (or different a small value)
        - same highlight color
        - same bold, italic and underline
        - same font size and font name

        Parameters
        ----------
        word is WordProperty

        Returns True if the word has same format with this word.
        -------
        """
        same_format = all([
            self.is_same_color(word),
            self.is_same_highlight_color(word),
            self.is_same_bold(word),
            self.is_same_italic(word),
            self.is_same_underline(word),
            self.is_same_font_size(word),
            self.is_same_font_name(word)
        ])
        return same_format
