# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
This module will define the enumeration for direction
"""


class WritingDirection(object):
    """
    Matching with WritingDirection enum in PHOcr
    """
    WRITING_DIRECTION_ERROR = -1
    WRITING_DIRECTION_LEFT_TO_RIGHT = 0
    WRITING_DIRECTION_RIGHT_TO_LEFT = 1
    WRITING_DIRECTION_TOP_TO_BOTTOM = 2


def convert_writing_direction(writing_dir):
    writing_dir_enum = WritingDirection.WRITING_DIRECTION_LEFT_TO_RIGHT
    if writing_dir == -1:
        writing_dir_enum = WritingDirection.WRITING_DIRECTION_ERROR
    elif writing_dir == 0:
        writing_dir_enum = WritingDirection.WRITING_DIRECTION_LEFT_TO_RIGHT
    elif writing_dir == 1:
        writing_dir_enum = WritingDirection.WRITING_DIRECTION_RIGHT_TO_LEFT
    elif writing_dir == 2:
        writing_dir_enum = WritingDirection.WRITING_DIRECTION_TOP_TO_BOTTOM
    return writing_dir_enum


class TextlineOrder(object):
    """
    Matching with TextlineOrder enum in PHOcr
    """
    TEXTLINE_ORDER_LEFT_TO_RIGHT = 0
    TEXTLINE_ORDER_RIGHT_TO_LEFT = 1
    TEXTLINE_ORDER_TOP_TO_BOTTOM = 2


def convert_textline_order(textline_order):
    textline_order_enum = TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM
    if textline_order == 0:
        textline_order_enum = TextlineOrder.TEXTLINE_ORDER_LEFT_TO_RIGHT
    elif textline_order == 1:
        textline_order_enum = TextlineOrder.TEXTLINE_ORDER_RIGHT_TO_LEFT
    elif textline_order == 2:
        textline_order_enum = TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM
    return textline_order_enum


class Orientation(object):
    """
    Matching with Orientation enum in PHOcr
    """
    ORIENTATION_ERROR = -1
    ORIENTATION_PAGE_UP = 0
    ORIENTATION_PAGE_RIGHT = 1
    ORIENTATION_PAGE_DOWN = 2
    ORIENTATION_PAGE_LEFT = 3


def convert_orientation(orientation):
    orientation_enum = Orientation.ORIENTATION_PAGE_UP
    if orientation == 0:
        orientation_enum = Orientation.ORIENTATION_PAGE_UP
    elif orientation == 1:
        orientation_enum = Orientation.ORIENTATION_PAGE_RIGHT
    elif orientation == 2:
        orientation_enum = Orientation.ORIENTATION_PAGE_DOWN
    elif orientation == 3:
        orientation_enum = Orientation.ORIENTATION_PAGE_LEFT
    return orientation_enum


class OrientationTransformer(object):
    """
    This class will transform x, y, w, h of box element which contain
    orientation information
    """

    def __init__(self):
        self.orientation_ = Orientation.ORIENTATION_PAGE_LEFT
        self.writing_direction_ = WritingDirection.WRITING_DIRECTION_LEFT_TO_RIGHT
        self.text_line_order_ = TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM

    @property
    def orientation(self):
        """
        Current orientation configuration
        :return:
        """
        return self.orientation_

    @orientation.setter
    def orientation(self, value):
        """
        Setter for orientation configuration
        :param value:
        :return:
        """
        self.orientation_ = value

    @property
    def writing_direction(self):
        """
        Current writing direction configuration
        :return:
        """
        return self.writing_direction_

    @writing_direction.setter
    def writing_direction(self, value):
        """
        Setter for writing direction configuration
        :param value:
        :return:
        """
        self.writing_direction_ = value

    @property
    def text_line_order(self):
        """
        Current text line order configuration
        :return:
        """
        return self.text_line_order_

    @text_line_order.setter
    def text_line_order(self, value):
        """
        Setter for text line order configuration
        :param value:
        :return:
        """
        self.text_line_order_ = value

    def get_x(self, box_element):
        """
        :param box_element: contain function get('x') get('y')
        :return: int value
        """
        if self.text_line_order_ == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
            return box_element.x
        else:
            return box_element.y

    def get_y(self, box_element):
        """
        :param box_element: contain function get('x') get('y')
        :return:
        """
        if self.text_line_order_ == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
            return box_element.y
        else:
            return box_element.x

    def get_w(self, box_element):
        """
        :param box_element: contain function get('w') get('h')
        :return:
        """
        if self.text_line_order_ == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
            return box_element.w
        else:
            return box_element.h

    def get_h(self, box_element):
        """
        :param box_element: contain function get('w') get('h')
        :return:
        """
        if self.text_line_order_ == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
            return box_element.h
        else:
            return box_element.w


def get_transformed_margin_left(page):
    """
    Get left margin of current processing page using text line order
    :return:
    """
    if page['text_line_order'] == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
        return page['margin_left']
    elif page['text_line_order'] == TextlineOrder.TEXTLINE_ORDER_RIGHT_TO_LEFT:
        return page['margin_top']
    elif page['text_line_order'] == TextlineOrder.TEXTLINE_ORDER_LEFT_TO_RIGHT:
        return page['margin_bottom']


def get_transformed_margin_right(page):
    """
    Get right margin of current processing page using text line order
    :param page: dicts contain key
        'text_line_order'
        'margin_right' 'margin_bottom' 'margin_top'
    :return:
    """
    if page['text_line_order'] == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
        return page['margin_right']
    elif page['text_line_order'] == TextlineOrder.TEXTLINE_ORDER_RIGHT_TO_LEFT:
        return page['margin_bottom']
    elif page['text_line_order'] == TextlineOrder.TEXTLINE_ORDER_LEFT_TO_RIGHT:
        return page['margin_top']


def get_transformed_width(page):
    """
    Get width of page using text line order
    :param page: dicts contain key 'text_line_order' 'width' 'height'
    :return:
    """
    if page['text_line_order'] == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
        return page['width']
    else:
        return page['height']


def get_transformed_x(page, data):
    """
    Get x using text line order
    :param page: dicts contain key 'text_line_order'
    :param data: dicst contain key 'x' and 'y'
    :return:
    """
    if page['text_line_order'] == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
        return data.x
    else:
        return data.y


def get_transformed_y(page, data):
    """
    Get y using text line order
    :param page: dicts contain key 'text_line_order'
    :param data: dicst contain key 'x' and 'y'
    :return:
    """
    if page['text_line_order'] == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
        return data.y
    else:
        return data.x


def get_transformed_w(page, data):
    """
    Get w using text line order
    :param page: dicts contain key 'text_line_order'
    :param data: dicts contain key 'w' and 'h'
    :return:
    """
    if page['text_line_order'] == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
        return data.w
    else:
        return data.h


def get_transformed_h(page, data):
    """
    Get h using text line order
    :param page: dicts contain key 'text_line_order'
    :param data: dicts contain key 'w' and 'h'
    :return:
    """
    if page['text_line_order'] == TextlineOrder.TEXTLINE_ORDER_TOP_TO_BOTTOM:
        return data.h
    else:
        return data.w
