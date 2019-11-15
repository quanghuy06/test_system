# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

import phocr_shared.statistics as math
from phocr_shared.phocr_common import CoordinateTransform, TextDirection, \
    Rectangle, PHOcrCommon


class RegionType:
    """Region type"""
    NONE = 1
    TEXTLINE = 2
    TABLE = 3
    PHOTO = 4


class Box(Rectangle):
    """Box object"""
    def __init__(self, rectangle, region_type=RegionType.NONE):
        self.region_type = region_type
        Rectangle.__init__(self,
                           rectangle.x,
                           rectangle.y,
                           rectangle.w,
                           rectangle.h)

    def equal_box(self, other):
        """Check if it is equal other box"""
        if self.region_type == other.region_type and \
                self.x == other.x and self.y == other.y and \
                self.w == other.w and self.h == other.h:
            return True
        return False


class Common:
    """Common object"""
    debug = 0

    def __init__(self, debug):
        self.debug = int(debug)

    @staticmethod
    def is_parallel_boxes_by_x(box, other_box):
        """Check if two boxes are parallel by x-coordinate"""
        # Get smaller x
        min_x = min(box.x, other_box.x)
        # Get larger width
        max_w = max(box.x + box.w, other_box.x + other_box.w)
        # Traverse from minimum x to maximum x
        for i in range(min_x, max_w):
            # If we find a line which cut two boxes
            if box.x < i < box.x + box.w and\
                    other_box.x < i < other_box.x + other_box.w:
                return True
        return False

    @staticmethod
    def is_parallel_boxes_by_y(box, other_box):
        """Check if two boxes are parallel by y-coordinate"""
        # Get smaller y
        min_y = min(box.y, other_box.y)
        # Get larger height
        max_h = max(box.y + box.h, other_box.y + other_box.h)
        # Traverse from minimum y to maximum y
        for i in range(min_y, max_h):
            # If we find a line which cut two boxes
            if box.y < i < box.y + box.h and\
                    other_box.y < i < other_box.y + other_box.h:
                return True
        return False

    @staticmethod
    def is_line_by_line(par, column, text_direction):
        """Check if is line by line in paragraph of column"""
        # If space width in end line is longer than
        # width of first word in next line
        # This paragraph is line by line
        i = 0
        for line in par.lines:
            if i < len(par.lines) - 1:
                end_word_distance = \
                    (CoordinateTransform.getX(par, text_direction)
                     + CoordinateTransform.getW(par, text_direction))\
                    - (CoordinateTransform.getX(line, text_direction)
                       + CoordinateTransform.getW(line, text_direction))
                next_line = par.lines[i + 1]
                first_next_word_width = CoordinateTransform.getW(
                    next_line.words[0],
                    text_direction
                )
                if end_word_distance > first_next_word_width:
                    return True
            i += 1

        # Unless, we compare distance between width of each line in paragraph
        # and space width of it
        if len(par.lines) > 2:
            for i in range(0, len(par.lines) - 2):
                line = par.lines[i]
                line_x = CoordinateTransform.getX(line, text_direction)
                line_w = CoordinateTransform.getW(line, text_direction)
                line_right_distance = \
                    (CoordinateTransform.getX(column, text_direction)
                     + CoordinateTransform.getW(column, text_direction))\
                    - (line_x + line_w)
                next_line = par.lines[i + 1]
                next_line_w = CoordinateTransform.getW(
                    next_line,
                    text_direction
                )
                if line_right_distance > next_line_w:
                    return True
        elif len(par.lines) == 2:
            line_1 = par.lines[0]
            line_2 = par.lines[1]
            line_1_x = CoordinateTransform.getX(line_1, text_direction)
            line_1_w = CoordinateTransform.getW(line_1, text_direction)
            line_1_right_distance = \
                (CoordinateTransform.getX(column, text_direction)
                 + CoordinateTransform.getW(column, text_direction))\
                - (line_1_x + line_1_w)
            line_2_w = CoordinateTransform.getW(line_2, text_direction)
            if line_1_right_distance > line_2_w:
                return True
        return False

    @staticmethod
    def set_alignment_for_par_with_one_line(par, col, text_direction):
        alignment = 'left'
        line = par.lines[0]
        line_left_distance = \
            (CoordinateTransform.getX(line, text_direction)
             - CoordinateTransform.getX(col, text_direction))
        line_right_distance = \
            (CoordinateTransform.getX(col, text_direction)
             + CoordinateTransform.getW(col, text_direction))\
            - (CoordinateTransform.getX(line, text_direction)
               + CoordinateTransform.getW(line, text_direction))
        if line_right_distance != 0:
            ratio = round(float(line_left_distance)/line_right_distance, 3)
            if ratio < 0.8:
                alignment = 'left'
            elif ratio > 1.2:
                alignment = 'right'
            else:
                alignment = 'center'
        elif line_left_distance > 0:
            alignment = 'right'
        return alignment

    @staticmethod
    def set_alignment_for_par_with_two_lines(par, text_direction):
        alignment = 'left'
        line_1 = par.lines[0]
        line_2 = par.lines[1]
        left_distance, right_distance = \
            PHOcrCommon.get_left_and_right_distance_with_two_lines(
                line_1,
                line_2,
                text_direction
            )
        if abs(left_distance) < 20 and \
                abs(right_distance) < 20 and \
                len(par.lines[0].words) > 5:
            alignment = 'justify'
        elif abs(left_distance) > 20 and abs(right_distance) > 20:
            if abs(left_distance) < abs(right_distance):
                ratio = left_distance // right_distance
            else:
                ratio = right_distance // left_distance
            if ratio < 0 and abs(ratio) > 0.5:
                alignment = 'center'
            else:
                alignment = 'left'
        elif abs(left_distance) <= abs(right_distance):
            alignment = 'left'
        elif abs(left_distance) > abs(right_distance):
            alignment = 'right'
        return alignment

    @staticmethod
    def set_alignment_for_par_with_three_lines(par, text_direction):
        alignment = 'left'
        line_1 = par.lines[0]
        line_2 = par.lines[1]
        line_3 = par.lines[2]
        line_left_distance, line_right_distance, line_right_distance_23 = \
            PHOcrCommon.get_left_and_right_distance_with_three_lines(
                line_1,
                line_2,
                line_3,
                text_direction
            )
        if line_left_distance > 20 and line_right_distance_23 > 20:
            if line_right_distance_23 != 0:
                ratio = line_left_distance // line_right_distance_23
                if 0.5 < ratio < 1.5:
                    alignment = 'center'
        elif line_left_distance < 20 and line_right_distance < 20:
            alignment = 'justify'
        elif line_left_distance <= line_right_distance:
            alignment = 'left'
        elif line_left_distance > line_right_distance:
            alignment = 'right'
        return alignment

    @staticmethod
    def set_alignment_for_par_more_than_three_lines(par):
        alignment = 'left'
        left_positions = []
        right_positions = []
        for i in range(1, len(par.lines) - 1):
            line = par.lines[i]
            line_left = line.x
            line_right = line.x + line.w
            left_positions.append(line_left)
            right_positions.append(line_left + line_right)

        # Calculate standard deviation of left and right position
        std_left = math.stdev(left_positions)
        std_right = math.stdev(right_positions)
        if std_right == 0:
            if std_left <= 5:
                alignment = 'justify'
            elif len(par.lines) > 5:
                alignment = 'right'
            else:
                alignment = 'left'
        else:
            ratio = std_left // std_right
            if std_left < 10 and std_right < 10:
                alignment = 'justify'
            elif std_left >= 10 and std_right >= 10 and 0.5 < ratio < 1.5:
                alignment = 'center'
            elif std_left <= 10:
                alignment = 'left'
            elif std_right <= 10:
                alignment = 'right'
        return alignment

    @staticmethod
    def define_alignment(par, col):
        """Define alignment in column"""
        text_direction = TextDirection.LRTB
        alignment = 'left'
        if len(par.lines) == 1:
            alignment = Common.set_alignment_for_par_with_one_line(
                par,
                col,
                text_direction
            )
        if len(par.lines) == 2:
            alignment = Common.set_alignment_for_par_with_two_lines(
                par,
                text_direction
            )
        if len(par.lines) == 3:
            alignment = Common.set_alignment_for_par_with_three_lines(
                par,
                text_direction
            )
        if len(par.lines) > 3:
            alignment = Common.set_alignment_for_par_more_than_three_lines(par)
        return alignment

    @staticmethod
    def define_valignment(par, column):
        """Define vertical alignment in column"""
        par_top = par.y
        par_bottom = par_top + par.h
        column_top = column.y
        column_bottom = column_top + column.h

        top_distance = par_top - column_top
        bottom_distance = column_bottom - par_bottom

        if bottom_distance == 0:
            v_alignment = 'bottom'
        else:
            ratio = float(top_distance) / bottom_distance
            if ratio < 0.5:
                v_alignment = 'top'
            elif ratio > 2:
                v_alignment = 'bottom'
            else:
                v_alignment = 'vcenter'
        return v_alignment


class RGBColor(tuple):
    """
    Immutable value object defining a particular RGB color.
    """
    def __new__(cls, red, green, blue):
        msg = 'RGBColor() takes three integer values 0-255'
        for val in (red, green, blue):
            if not isinstance(val, int) or val < 0 or val > 255:
                raise ValueError(msg)
        return super(RGBColor, cls).__new__(cls, (red, green, blue))

    def __str__(self):
        """
        Return a hex string rgb value, like '3C2F80'
        """
        return '%02X%02X%02X' % self

    @classmethod
    def from_string(cls, rgb_hex_str):
        """
        Return a new instance from an RGB color hex string like ``'3C2F80'``.
        """
        red = int(rgb_hex_str[:2], 16)
        green = int(rgb_hex_str[2:4], 16)
        blue = int(rgb_hex_str[4:], 16)
        return cls(red, green, blue)
