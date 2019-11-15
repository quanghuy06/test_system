# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
BoxContainer is structure like:
Parent box
    Child box

Parent can be whole page box
    Child box can be
        - writing area
        - text box
        - table cell box
"""


class BoxContainer(object):
    """
    Container for describe page setting
    """

    def __init__(self, box, parent_box, is_whole_page_box=False):
        self._box = box
        self._parent_box = parent_box
        self._is_whole_page_box = is_whole_page_box

    def right_margin(self):
        """
        Margin from box to parent box
        :return:
        """
        return self._parent_box.right_px - self._box.right_px

    def left_margin(self):
        """
        Margin from box to parent box
        :return:
        """
        return self._box.left_px - self._parent_box.left_px

    def top_margin(self):
        """
        Margin from box to parent box
        :return:
        """
        return self._box.top_px - self._parent_box.top_px

    def bottom_margin(self):
        """
        Margin from box to parent box
        :return:
        """
        return self._parent_box.bottom_px - self._box.bottom_px

    @property
    def is_whole_page_box(self):
        """
        This container is for whole page or child of page
        :return:
        """
        return self._is_whole_page_box

    @property
    def x(self):
        """
        Child x by emu
        :return:
        """
        return self._box.x

    @property
    def y(self):
        """
        Child y by emu
        :return:
        """
        return self._box.y

    @property
    def w(self):
        """
        Child width by emu
        :return:
        """
        return self._box.w

    @property
    def h(self):
        """
        Child height by emu
        :return:
        """
        return self._box.h

    @property
    def parent_w_px(self):
        """
        Parent width by pixel
        :return:
        """
        return self._parent_box.w_px

    @property
    def parent_h_px(self):
        """
        Parent height by pixel
        :return:
        """
        return self._parent_box.h_px
