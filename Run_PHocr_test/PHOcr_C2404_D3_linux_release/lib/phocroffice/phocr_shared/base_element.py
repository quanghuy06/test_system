# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
This module used to easily handle element tree object
"""
import xml.etree.cElementTree as ET
from .element_aspect import ElementAspect
from .element_box import ElementBox


class BaseElement(object):
    """
    An Element class from an element tree, now it supports Pixel unit only
    """

    def __init__(self, element):

        self.element = element
        if element is not None:
            self.box = ElementBox(element)
            self.tag = str(element.tag)
            self.m_id = str(element.id)
        else:
            raise Exception('Catch None type element as input!')

    @staticmethod
    def print_element(element):
        """Print out an Element tree"""
        print(ET.tostring(element, encoding='utf8').decode())

    def __str__(self):
        """For printing BaseElement object"""
        return '%s, id: %d x: %d y: %d w: %d h:%d' % (self.tag, self.m_id,
                                                      self.box.x, self.box.y,
                                                      self.box.w, self.box.h)

    def min_value_in_aspect_of_children(self, aspect):
        """
        Find the minimum value of an Element with the input aspect
        Use when the input element tree has child elements
        Return 0 if element has no child
        :return:
        """
        min_value = 0
        child_value = 0
        child_idx = 0
        for child_element in self.element:
            child = BaseElement(child_element)
            if aspect == ElementAspect.LEFT:
                child_value = child.box.left

            elif aspect == ElementAspect.TOP:
                child_value = child.box.top

            elif aspect == ElementAspect.WIDTH:
                child_value = child.box.width

            elif aspect == ElementAspect.HEIGHT:
                child_value = child.box.height
            else:
                # Do nothing because this option invalid
                pass
            if child_idx == 0:
                min_value = child_value
            else:
                if child_value < min_value:
                    min_value = child_value
        return min_value
