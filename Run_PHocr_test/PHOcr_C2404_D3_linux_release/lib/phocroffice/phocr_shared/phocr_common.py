# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

import os

# Load python module path inside root folder
from phocr_shared.phocr_python_path import load_path
load_path()

from lxml import etree
import phocr_shared.statistics as math
from phocr_shared.phocr_config import PHOcrConstant
from phocr_shared.shared import RGBColor
from phocr_shared.alignment_enum import AlignmentEnum
from phocr_shared.phocr_dpi import PHOcrDPI


class DocumentType:
    DOCX = 1
    XLSX = 2
    PPTX = 3


class Rectangle:
    """Box object"""
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_area(self):
        """Get area of box"""
        return self.w * self.h

    def intersect_box(self, other):
        """Check if it intersect other box"""
        current_left = self.x
        current_top = self.y
        current_width = self.w
        current_height = self.h

        next_left = other.x
        next_top = other.y
        next_width = other.w
        next_height = other.h

        current_right = current_left + current_width - 1
        next_right = next_left + next_width - 1
        current_bottom = current_top + current_height - 1
        next_bottom = next_top + next_height - 1
        if next_bottom < current_top or current_bottom < next_top or\
                current_right < next_left or next_right < current_left:
            return False
        return True

    def contain_box(self, other):
        """Check if it contains other box"""
        if (self.x <= other.x and self.y <= other.y and
                (self.x + self.w >= other.x + other.w) and
                (self.y + self.h >= other.y + other.h)):
            return True
        return False


class Alignment:
    LEFT = 1
    RIGHT = 2
    CENTER = 3
    JUSTIFY = 4
    TOP = 5
    MIDDLE = 6
    BOTTOM = 7
    DISTRIBUTED = 8


class TextDirection:
    LRTB = 1  # Left-right-top-bottom
    TBRL = 2  # Top-bottom-right-left


class WordDefault:
    """
    Enum class to store the default font size for office output
    """
    FONT_SIZE = 11


class CoordinateTransform:
    @staticmethod
    def getX(obj, direction):
        if direction == TextDirection.LRTB:
            return obj.x
        elif direction == TextDirection.TBRL:
            return obj.y

    @staticmethod
    def getY(obj, direction):
        if direction == TextDirection.LRTB:
            return obj.y
        elif direction == TextDirection.TBRL:
            return obj.x

    @staticmethod
    def getW(obj, direction):
        if direction == TextDirection.LRTB:
            return obj.w
        elif direction == TextDirection.TBRL:
            return obj.h

    @staticmethod
    def getH(obj, direction):
        if direction == TextDirection.LRTB:
            return obj.h
        elif direction == TextDirection.TBRL:
            return obj.w


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Polygon:
    def __init__(self, p1, q1, p2, q2):
        self.p1 = p1
        self.q1 = q1
        self.p2 = p2
        self.q2 = q2


class PHOcrCommon:
    @staticmethod
    def get_dpi(page_dpi):
        """
        Get dpi of page

        Parameters
        ----------
        page_dpi : int
            Resolution of page

        Returns
        -------

        """
        if PHOcrDPI(PHOcrConstant.MIN_CREDIBLE_RESOLUTION, PHOcrConstant.MIN_CREDIBLE_RESOLUTION) \
                < page_dpi < PHOcrDPI(PHOcrConstant.MAX_CREDIBLE_RESOLUTION, PHOcrConstant.MAX_CREDIBLE_RESOLUTION):
            return page_dpi

        return PHOcrDPI(PHOcrConstant.DEFAULT_DPI, PHOcrConstant.DEFAULT_DPI)

    @staticmethod
    def get_color(color_str):
        """
        Get color based on rgb

        Parameters
        ----------
        color_str : str
            RGB color with type is string

        Returns
        -------

        """
        red, green, blue = color_str.split(',')
        return RGBColor(int(red), int(green), int(blue))

    @staticmethod
    def remove_ouliner(array, ratio):
        """
        Remove outlier of array data

        Parameters
        ----------
        array
        ratio

        Returns
        -------

        """
        mean_duration = math.mean(array)
        std_dev_one_test = math.stdev(array)

        def drop_outliers(x):
            """
            This function will check to drop outliers

            Parameters
            ----------
            x : float

            Returns
            -------
            x : float

            """
            if abs(x - mean_duration) <= ratio * std_dev_one_test:
                return x

        # Warning when use: return filter(drop_outliers, array)
        return [item for item in array if drop_outliers(item)]

    @staticmethod
    def separate_array(array, mode):
        """
        Saparate array data to 2 region to re-calculate std

        Parameters
        ----------
        array
        mode

        Returns
        -------

        """
        mean_value = math.mean(array)
        array_lower = []
        array_higher = []
        for element in array:
            if element <= mean_value:
                array_lower.append(element)
            else:
                array_higher.append(element)
        if mode == 1:
            return array_lower
        elif mode == 2:
            return array_higher

    @staticmethod
    def get_object_position(element):
        rectangle = Rectangle(element.x, element.y, element.w, element.h)
        return rectangle

    @staticmethod
    def calculate_baseline_different(
            current_line,
            next_line,
            text_direction,
            document_type):
        """
        Calculate base_line is distance between base line of 2 continue lines
        2 lines maybe place in same or different paragraph

        Parameters
        ----------
        current_line
        next_line
        text_direction
        document_type

        Returns
        -------

        """
        if text_direction != TextDirection.TBRL:
            baseline = int(next_line.baseline) - int(current_line.baseline)
        else:
            # TODO(phuchm): baseline is base on "baseline" attribue with DOCX
            # and x-coordinate with PPTX
            # it should be consistent, please fix it later
            if document_type == DocumentType.DOCX:
                baseline = (int(next_line.baseline)
                            - int(current_line.baseline))
            else:  # document_type == DocumentType.PPTX
                baseline = current_line.x - next_line.x

        return baseline

    @staticmethod
    def calculate_line_spacing(par, text_direction, document_type):
        """
        Calculate baseline of paragraph by calculating
        average of baseline between each 2 frequent line

        Parameters
        ----------
        par
        text_direction
        document_type

        Returns
        -------

        """
        baseline_arr = []
        i = 0
        if len(par.lines) > 2:
            for line in par.lines:
                if i <= len(par.lines) - 2:
                    next_line = par.lines[i + 1]
                    baseline_ = PHOcrCommon.calculate_baseline_different(
                        line,
                        next_line,
                        text_direction,
                        document_type
                    )
                    baseline_arr.append(baseline_)
                i += 1
            sum_baseline = 0
            for bl in baseline_arr:
                sum_baseline += bl
            # TODO(phuchm): sum_baseline is int with DOCX and float with PPTX
            # it should be consistent, please fix it later
            if document_type == DocumentType.DOCX:
                baseline = int(round(sum_baseline / (len(par.lines) - 1), 5))
            else:  # document_type == DocumentType.PPTX
                baseline = round(float(sum_baseline) / (len(par.lines) - 1), 5)
        else:
            baseline = PHOcrCommon.calculate_baseline_different(
                par.lines[0],
                par.lines[1],
                text_direction,
                document_type
            )
        if baseline > 0:
            return baseline
        else:
            return 0

    @staticmethod
    def escape(s, quot=None, amp=None, apos=None):
        """
        Escape string in XML

        Parameters
        ----------
        s
        quot
        amp
        apos

        Returns
        -------

        """
        # Must be done first if enabled!
        if amp:
            s = s.replace('&', '&amp;')
        s = s.replace('<', '&lt;')
        s = s.replace('>', '&gt;')
        if quot:
            s = s.replace('"', '&quot;')
        if apos:
            s = s.replace('\'', '&apos;')
        return s

    @staticmethod
    def parse_xml_file(path_to_xml_file):
        """
        Parse XML file

        Parameters
        ----------
        path_to_xml_file : str
            Path to .xml file

        Returns
        -------

        """
        if not os.path.exists(path_to_xml_file):
            raise Exception('Path "' + path_to_xml_file + '" does not exist!')

        tree = None

        with open(path_to_xml_file, encoding='utf8', errors='ignore') as f:
            data_file = f.read()
            parser = etree.XMLParser(
                ns_clean=True,
                recover=True,
                encoding='utf-8'
            )
            tree = etree.fromstring(data_file, parser=parser)

        return tree

    @staticmethod
    def is_photo_ok(photo_h, photo_w, x_height):
        """
        Compare size of photo with x_height

        Parameters
        ----------
        photo_h
        photo_w
        x_height

        Returns
        -------

        """
        photo_area = photo_w * photo_h
        return \
            (photo_w >= x_height and photo_h >= x_height) or \
            (photo_area > x_height * x_height)

    @staticmethod
    def remove_file(file_path):
        """
        Remove a file if exist

        Parameters
        ----------
        file_path : str
            Path to file

        Returns
        -------

        """
        if os.path.exists(file_path):
            os.remove(file_path)

    @staticmethod
    def is_numbering(par, text_direction, x_height):
        # Check numbering
        is_numbering = False
        if 2 <= len(par.lines) < 5:
            count = 0
            for i in range(1, len(par.lines)):
                line = par.lines[i]
                if len(par.lines[0].words) > 1:
                    if abs(CoordinateTransform.getX(
                            par.lines[0].words[1],
                            text_direction)
                           - CoordinateTransform.getX(line, text_direction)) <=\
                            x_height / 2:
                        count += 1
            if count / len(par.lines) >= 0.5:
                is_numbering = True
        return is_numbering

    @staticmethod
    def get_std_left(left_positions):
        std_left = math.stdev(left_positions)
        if std_left > 30:
            ratio = 1.5
            # Separate array to 2 regions, to avoid case that
            # 1 paragraph wrap beside image
            left_positions_lower = PHOcrCommon.separate_array(
                left_positions, 1)
            left_positions_higher = PHOcrCommon.separate_array(
                left_positions,
                2
            )
            if len(left_positions_lower) >= 2 and \
                    len(left_positions_higher) >= 2:
                std_left_lower = math.stdev(left_positions_lower)
                std_left_higher = math.stdev(left_positions_higher)
                if std_left_lower < 5 and std_left_higher < 5:
                    std_left = \
                        (std_left_higher + std_left_lower) / 2
                    left_positions = left_positions_lower
                else:
                    left_positions = PHOcrCommon.remove_ouliner(
                        left_positions,
                        ratio
                    )
                    std_left = math.stdev(left_positions)
            else:
                left_positions = PHOcrCommon.remove_ouliner(
                    left_positions, ratio)
                std_left = math.stdev(left_positions)
        else:
            # Remove ouliner if array have more than 5 element
            left_positions = PHOcrCommon.remove_ouliner(
                left_positions,
                2
            )
            std_left = math.stdev(left_positions)
        return std_left

    @staticmethod
    def get_std_right(right_positions):
        # Same with left position
        std_right = math.stdev(right_positions)
        if std_right > 30:
            ratio = 1.5
            right_positions_lower = PHOcrCommon.separate_array(
                right_positions,
                1
            )
            right_positions_higher = PHOcrCommon.separate_array(
                right_positions,
                2
            )
            if len(right_positions_lower) >= 2 and \
                    len(right_positions_higher) >= 2:
                std_right_lower = math.stdev(right_positions_lower)
                std_right_higher = math.stdev(
                    right_positions_higher
                )
                if std_right_lower < 5 and std_right_higher < 5:
                    std_right = (std_right_higher + std_right_lower) / 2
                    right_positions = right_positions_higher
                else:
                    right_positions = PHOcrCommon.remove_ouliner(
                        right_positions,
                        ratio
                    )
                    std_right = math.stdev(right_positions)
            else:
                right_positions = PHOcrCommon.remove_ouliner(
                    right_positions,
                    ratio
                )
                std_right = math.stdev(right_positions)
        else:
            right_positions = PHOcrCommon.remove_ouliner(
                right_positions, 2)
            std_right = math.stdev(right_positions)
        return std_right

    @staticmethod
    def get_alignment_base_on_std_left_and_right(par, std_left, std_right):
        alignment = AlignmentEnum.ALIGN_LEFT
        if std_right == 0:
            if std_left <= 5:
                alignment = AlignmentEnum.ALIGN_JUSTIFY
            elif len(par.lines) > 5:
                alignment = AlignmentEnum.ALIGN_RIGHT
            else:
                alignment = AlignmentEnum.ALIGN_LEFT
        else:
            ratio = std_left / std_right
            if std_left <= 5 and std_right <= 5:
                alignment = AlignmentEnum.ALIGN_JUSTIFY
            elif std_left >= 5 and std_right >= 5 and 0.5 < ratio < 1.5:
                alignment = AlignmentEnum.ALIGN_CENTER
            elif std_left <= 5:
                alignment = AlignmentEnum.ALIGN_LEFT
            elif std_right <= 5:
                alignment = AlignmentEnum.ALIGN_RIGHT
        return alignment

    @staticmethod
    def get_alignment_for_par_more_than_three_lines(
            par, text_direction,
            left_positions, right_positions):
        alignment = AlignmentEnum.ALIGN_LEFT
        # If number of lines in paragraph > 3, we'll use standard deviation
        # to calculate alignment of paragraph
        if len(par.lines) > 3:
            for i in range(1, len(par.lines) - 1):
                line = par.lines[i]
                line_left = CoordinateTransform.getX(line, text_direction)
                line_right = CoordinateTransform.getW(line, text_direction)
                left_positions.append(line_left)
                right_positions.append(line_left + line_right)

            # Use standard deviation of left and right position
            # to define alignment
            if len(left_positions) >= 5 and len(right_positions) >= 5:
                std_left = PHOcrCommon.get_std_left(left_positions)
                # Same with left position
                std_right = PHOcrCommon.get_std_right(right_positions)
            else:
                std_left = math.stdev(left_positions)
                std_right = math.stdev(right_positions)
            alignment = PHOcrCommon.get_alignment_base_on_std_left_and_right(
                par,
                std_left,
                std_right
            )
        return alignment

    @staticmethod
    def get_left_and_right_distance_with_two_lines(
            line_1, line_2, text_direction):
        left_distance = \
            (CoordinateTransform.getX(line_1, text_direction)
             - CoordinateTransform.getX(line_2, text_direction))
        right_distance = \
            (CoordinateTransform.getX(line_1, text_direction)
             + CoordinateTransform.getW(line_1, text_direction)
             - (CoordinateTransform.getX(line_2, text_direction)
                + CoordinateTransform.getW(line_2, text_direction)))
        return left_distance, right_distance

    @staticmethod
    def get_left_and_right_distance_with_three_lines(
            line_1, line_2, line_3, text_direction):
        line_left_distance = \
            abs(CoordinateTransform.getX(line_3, text_direction)
                - CoordinateTransform.getX(line_2, text_direction))
        line_right_distance = \
            abs((CoordinateTransform.getX(line_2, text_direction)
                 + CoordinateTransform.getW(line_2, text_direction))
                - (CoordinateTransform.getX(line_1, text_direction)
                   + CoordinateTransform.getW(line_1, text_direction)))
        line_right_distance_23 = \
            abs((CoordinateTransform.getX(line_2, text_direction)
                 + CoordinateTransform.getW(line_2, text_direction))
                - (CoordinateTransform.getX(line_3, text_direction)
                   + CoordinateTransform.getW(line_3, text_direction)))
        return line_left_distance, line_right_distance, line_right_distance_23

    @staticmethod
    def get_alignment_for_par_with_three_lines(par, text_direction, x_height):
        alignment = AlignmentEnum.ALIGN_LEFT
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
        if line_left_distance > x_height and line_right_distance_23 > x_height:
            if line_right_distance_23 != 0:
                ratio = line_left_distance / line_right_distance_23
                if 0.5 < ratio < 1.5:
                    alignment = AlignmentEnum.ALIGN_CENTER
        elif line_left_distance < x_height and line_right_distance < x_height:
            alignment = AlignmentEnum.ALIGN_JUSTIFY
        elif line_left_distance <= line_right_distance:
            alignment = AlignmentEnum.ALIGN_LEFT
        elif line_left_distance > line_right_distance:
            alignment = AlignmentEnum.ALIGN_RIGHT
        return alignment

    @staticmethod
    def get_alignment_for_par_with_two_lines(par, text_direction, x_height):
        alignment = AlignmentEnum.ALIGN_LEFT
        line_1 = par.lines[0]
        line_2 = par.lines[1]
        left_distance, right_distance = \
            PHOcrCommon.get_left_and_right_distance_with_two_lines(
                line_1,
                line_2,
                text_direction
            )
        if abs(left_distance) < x_height and \
                abs(right_distance) < x_height and \
                len(par.lines[0].words) > 5:
            alignment = AlignmentEnum.ALIGN_JUSTIFY
        elif abs(left_distance) > x_height and abs(right_distance) > x_height:
            if abs(left_distance) < abs(right_distance):
                ratio = left_distance / right_distance
            else:
                ratio = right_distance / left_distance
            if ratio < 0 and abs(ratio) > 0.5:
                alignment = AlignmentEnum.ALIGN_CENTER
            else:
                alignment = AlignmentEnum.ALIGN_LEFT
        elif abs(left_distance) <= abs(right_distance):
            alignment = AlignmentEnum.ALIGN_LEFT
        elif abs(left_distance) > abs(right_distance):
            alignment = AlignmentEnum.ALIGN_RIGHT
        return alignment

    @staticmethod
    def get_alignment_for_par_with_one_line(par, text_direction):
        alignment = AlignmentEnum.ALIGN_LEFT
        par_x = CoordinateTransform.getX(par, text_direction)
        par_w = CoordinateTransform.getW(par, text_direction)
        line = par.lines[0]
        line_left_distance = \
            CoordinateTransform.getX(line, text_direction) - par_x
        line_right_distance = \
            (par_x + par_w
             - (CoordinateTransform.getX(line, text_direction)
                + CoordinateTransform.getW(line, text_direction)))
        if line_right_distance != 0:
            ratio = round(float(line_left_distance) / line_right_distance, 3)
            if ratio < 0.8:
                alignment = AlignmentEnum.ALIGN_LEFT
            elif ratio > 1.2:
                alignment = AlignmentEnum.ALIGN_RIGHT
            else:
                alignment = AlignmentEnum.ALIGN_CENTER
        # If right_ratio = 0 and left_ratio > 0
        elif line_left_distance > 0:
            alignment = AlignmentEnum.ALIGN_RIGHT
        return alignment

    @staticmethod
    def get_paragraph_alignment(par, text_direction, x_height):
        """
        Calculate alignment style for paragraph

        Parameters
        ----------
        par
        text_direction
        x_height

        Returns
        -------

        """
        # Check style of paragraph
        alignment = AlignmentEnum.ALIGN_LEFT
        left_positions = []
        right_positions = []

        # Check numbering
        is_numbering = PHOcrCommon.is_numbering(par, text_direction, x_height)
        if is_numbering:
            return alignment
        else:
            # If number of lines in paragraph > 3, we'll use standard deviation
            # to calculate alignment of paragraph
            if len(par.lines) > 3:
                alignment = \
                    PHOcrCommon.get_alignment_for_par_more_than_three_lines(
                        par, text_direction,
                        left_positions, right_positions
                    )
            if len(par.lines) == 3:
                alignment = PHOcrCommon.get_alignment_for_par_with_three_lines(
                    par, text_direction, x_height
                )
            if len(par.lines) == 2:
                alignment = PHOcrCommon.get_alignment_for_par_with_two_lines(
                    par, text_direction, x_height
                )
            if len(par.lines) == 1:
                alignment = PHOcrCommon.get_alignment_for_par_with_one_line(
                    par, text_direction
                )
        return alignment

    @staticmethod
    def get_width_and_height(table, x_lines, y_lines):
        no_table_cols = table.num_cells
        no_table_rows = table.num_rows
        # Assign width and height of presented column
        for row in table.rows:
            for column in row.cells:
                left = column.x
                top = column.y

                if x_lines[column.id - 1] > left or x_lines[column.id - 1] < 0:
                    x_lines[column.id - 1] = left
                x_lines[column.id - 1] = left

                if y_lines[row.id - 1] > top or y_lines[row.id - 1] < 0:
                    y_lines[row.id - 1] = top
                y_lines[row.id - 1] = top

                if column.id == no_table_cols:
                    x_lines[column.id] = left + column.w

                if row.id == no_table_rows:
                    y_lines[row.id] = top + column.h

    @staticmethod
    def assign_width_and_height(
            table,
            x_lines, y_lines,
            col_width_arr, col_height_arr):
        small_width = 30
        init_value = -1
        no_table_cols = table.num_cells
        no_table_rows = table.num_rows
        for i in range(no_table_cols):
            if x_lines[i + 1] == init_value or x_lines[i] == init_value:
                col_width_arr[i] = 100
            else:
                col_width_arr[i] = x_lines[i + 1] - x_lines[i]
            col_width_arr[i] = max(small_width, col_width_arr[i])

        for i in range(no_table_rows):
            if y_lines[i + 1] == init_value or y_lines[i] == init_value:
                col_height_arr[i] = 100
            else:
                col_height_arr[i] = y_lines[i + 1] - y_lines[i]

    @staticmethod
    def get_columns_size(table):
        init_value = -1
        no_table_cols = table.num_cells
        no_table_rows = table.num_rows
        col_width_arr = [init_value] * no_table_cols
        col_height_arr = [init_value] * no_table_rows
        x_lines = [init_value] * (no_table_cols + 1)
        y_lines = [init_value] * (no_table_rows + 1)
        PHOcrCommon.get_width_and_height(table, x_lines, y_lines)
        PHOcrCommon.assign_width_and_height(table,
                                            x_lines, y_lines,
                                            col_width_arr, col_height_arr)
        return col_width_arr, col_height_arr
