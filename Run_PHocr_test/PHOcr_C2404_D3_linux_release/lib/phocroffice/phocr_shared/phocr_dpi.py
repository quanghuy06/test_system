# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.


class PHOcrDPI(object):
    """
    Present DPI object inside PHOcr
    """
    def __init__(self, horizontal_res, vertical_res):
        self.horizontal_resolution = horizontal_res
        self.vertical_resolution = vertical_res

    def __gt__(self, other):
        if self.horizontal_resolution > other.horizontal_resolution:
            if self.vertical_resolution >= other.vertical_resolution:
                return True
        if self.vertical_resolution > other.vertical_resolution:
            if self.horizontal_resolution >= other.horizontal_resolution:
                return True
        return False

    def __lt__(self, other):
        if self.horizontal_resolution < other.horizontal_resolution:
            if self.vertical_resolution <= other.vertical_resolution:
                return True
        if self.vertical_resolution < other.vertical_resolution:
            if self.horizontal_resolution <= other.horizontal_resolution:
                return True
        return False

    def __str__(self):
        return "PHOcrDPI(" + str(self.horizontal_resolution) + ", " \
               + str(self.vertical_resolution) + ")"
