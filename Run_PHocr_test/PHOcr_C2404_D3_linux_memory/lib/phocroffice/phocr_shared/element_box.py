# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
The basic box
"""


class ElementBox(object):
    """Basic Box element class"""
    def __init__(self, element):
        """
        Init ElementBox with one element tree object
        :param element:
        """
        if element is not None:
            self.element = element
            self.x = element.x
            self.y = element.y
            self.w = element.w
            self.h = element.h
        else:
            raise Exception('Catch None type element as input!')

    @property
    def left(self):
        """Left value of ElementBox"""
        return self.x

    @left.getter
    def left(self):
        """Get left of ElementBox"""
        return self.x

    @left.setter
    def left(self, value):
        """Set the left of ElementBox"""
        self.x = value
        self.element.x = value

    @property
    def top(self):
        """Top value of ElementBox"""
        return self.y

    @top.getter
    def top(self):
        """Get left of ElementBox"""
        return self.y

    @top.setter
    def top(self, value):
        """Set the left of ElementBox"""
        self.y = value
        self.element.y = value

    @property
    def width(self):
        """Get width of ElementBox"""
        return self.w

    @width.getter
    def width(self):
        """Get left of ElementBox"""
        return self.w

    @width.setter
    def width(self, value):
        """Set the left of ElementBox"""
        self.w = value
        self.element.w = value

    @property
    def height(self):
        """Get height of ElementBox"""
        return self.h

    @height.getter
    def height(self):
        """Get left of ElementBox"""
        return self.h

    @height.setter
    def height(self, value):
        """Set the left of ElementBox"""
        self.h = value
        self.element.h = value

    @property
    def right(self):
        """Get right of ElementBox"""
        return self.left + self.width

    @right.getter
    def right(self):
        """Get left of ElementBox"""
        return self.left + self.width

    @right.setter
    def right(self, value):
        """Set the left of ElementBox"""
        new_width = value - self.left
        self.w = new_width
        self.element.w = new_width

    @property
    def bottom(self):
        """Get bottom of ElementBox"""
        return self.top + self.height

    @bottom.getter
    def bottom(self):
        """Get left of ElementBox"""
        return self.top + self.height

    @bottom.setter
    def bottom(self, value):
        """Set the left of ElementBox"""
        new_height = value - self.left
        self.h = new_height
        self.element.h = new_height
