# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
This class to easy to calculate coordinates of box that get from xml file
"""


class Box:
    def __init__(self, element=None):
        if element is not None:
            self.x = element.x
            self.y = element.y
            self.w = element.w
            self.h = element.h
            self.left = self.x
            self.right = self.x + self.w - 1
            self.top = self.y
            self.bottom = self.y + self.h - 1
        else:
            self.x = 0
            self.y = 0
            self.w = 0
            self.h = 0
            self.left = self.x
            self.right = self.x + self.w - 1
            self.top = self.y
            self.bottom = self.y + self.h - 1

    @staticmethod
    def from_xml(xml_elm):
        box = Box()
        box.set_coordinates(xml_elm.x, xml_elm.y, xml_elm.w, xml_elm.h)
        return box

    def set_coordinates(self, x_, y_, w_, h_):
        self.x = x_
        self.y = y_
        self.w = w_
        self.h = h_
        self.left = x_
        self.right = x_ + w_ - 1
        self.top = y_
        self.bottom = y_ + h_ - 1


def overlap_region(box1, box2):
    if box1 is None or box2 is None:
        return None
    if box2.bottom < box1.top or \
            box1.bottom < box2.top or \
            box1.right < box2.left or \
            box2.right < box1.left:
        return None
    left = max(box1.left, box2.left)
    right = min(box1.right, box2.right)
    top = max(box1.top, box2.top)
    bottom = min(box1.bottom, box2.bottom)

    box = Box()
    box.set_coordinates(left, top, right - left + 1, bottom - top + 1)
    return box


def is_overlap_region(box1, box2):
    overlap_box = overlap_region(box1, box2)
    if overlap_box is not None:
        return True
    else:
        return False


def is_equal_box(box1, box2):
    if box1.left == box2.left and \
            box1.right == box2.right and \
            box1.top == box2.top and \
            box1.right == box2.right:
        return True
    else:
        return False


def ratio_overlap_photo(carea, photo_array):
    sum_area = 0
    par_area = 0
    for par in carea.paragraphs:
        for line in par.lines:
            for word in line.words:
                for char in word.characters:
                    box_char = Box(char)
                    par_area += (box_char.w * box_char.h)
                    for box_photo in photo_array:
                        box_overlap = overlap_region(box_char, box_photo)
                        if box_overlap is not None:
                            sum_area += (box_overlap.w * box_overlap.h)
    ratio = float(sum_area) / par_area
    return ratio
