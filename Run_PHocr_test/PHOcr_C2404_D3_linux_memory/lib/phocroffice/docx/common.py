# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from __future__ import division

import sys

from docx.box import *
from docx.enum.text import WD_TAB_ALIGNMENT, WD_COLOR_INDEX as WD_COLOR
from phocr_elements.office_object_tag import OfficeObjectTag
from phocr_shared.shared import Pixel, Pt
from phocr_shared.alignment import calculate_left_indent
from phocr_shared.alignment_enum import AlignmentEnum
from phocr_shared.phocr_common import PHOcrCommon, Point, Polygon, \
    TextDirection, WordDefault
from phocr_shared.object_info import ObjectInfo
import phocr_shared.statistics as math


class Common:
    """
    This class will contains methods which are used in docx_creator.py
    The purpose is serving for specific calculation relating to word document
    """

    @staticmethod
    def get_near_image(par, transformer, overlap_v, near_image, region_height):
        is_near_image = None
        if overlap_v > 0:
            if transformer.get_h(par) / overlap_v >= 1 and \
                    transformer.get_h(par) < region_height:
                if near_image == 'right':
                    is_near_image = 'right-full'
                else:
                    is_near_image = 'left-full'
            elif transformer.get_h(par) / overlap_v > 0.2:
                if near_image == 'right':
                    is_near_image = 'right'
                else:
                    is_near_image = 'left'
        return is_near_image

    @staticmethod
    def calculate_para_infor(page, par, transformer):
        par_mid = par.x + par.w / 2
        overlap_v = 0
        near_image = None
        region_height = 0
        for region in page.photos:
            photo_mid = (transformer.get_x(region)
                         + transformer.get_w(region) / 2)
            if (transformer.get_y(region) + transformer.get_h(region)
                    < transformer.get_y(par)) or \
                    (transformer.get_y(par) + transformer.get_h(par)
                     < transformer.get_y(region)):
                continue
            else:
                region_bottom = \
                    (transformer.get_y(region)
                     + transformer.get_h(region))
                par_bottom = \
                    (transformer.get_y(par)
                     + transformer.get_h(par))
                overlap_v = \
                    (min(region_bottom, par_bottom)
                     - max(transformer.get_y(region),
                           transformer.get_y(par)))
            if overlap_v > 0:
                if photo_mid <= par_mid:
                    near_image = 'right'
                else:
                    near_image = None
                region_height = transformer.get_h(region)
                break
        return overlap_v, near_image, region_height

    @staticmethod
    def get_text_angle_histogram(para, text_angle_histogram):
        # Analysis text angle
        for line in para.lines:
            text_angle = int(line.text_angle)
            if 0 <= text_angle <= 360:
                text_angle = 360 - text_angle
            else:
                text_angle = 0

            if text_angle not in text_angle_histogram:
                text_angle_histogram[text_angle] = 0
            text_angle_histogram[text_angle] += 1
        return text_angle_histogram

    @staticmethod
    def get_paragraph_array(carea, text_direction):
        paragraph_orders = []
        for para in carea.paragraphs:
            para_info = ObjectInfo(para.id, para.x, para.y, para.tag)
            paragraph_orders.append(para_info)
        if text_direction == TextDirection.TBRL:
            # Next, sort by x and reverse (DEC)
            paragraph_orders = sorted(
                paragraph_orders,
                key=lambda element_p: element_p.x,
                reverse=True
            )
        return paragraph_orders

    @staticmethod
    def smooth_indent_by_shd(
            document, par_format, start, i,
            left_indents, right_indents):
        left_id = par_format.left_indent
        if left_id is None:
            left_id = 0
        left_indents.append(left_id)
        right_id = par_format.right_indent
        if right_id is None:
            right_id = 0
        right_indents.append(right_id)
        if i == (len(document.paragraphs) - 1):
            if len(left_indents) > 1 and len(right_indents) > 1:
                left_indent = min(left_indents)
                for j in range(start, len(document.paragraphs)):
                    par_format = document.paragraphs[j].paragraph_format
                    if par_format.shd.rgb is not None:
                        par_format.left_indent = \
                            calculate_left_indent(par_format,
                                                  left_indent)
                right_indent = min(right_indents)
                for j in range(start, len(document.paragraphs)):
                    par_format = document.paragraphs[j].paragraph_format
                    if par_format.shd.rgb is not None:
                        par_format.right_indent = right_indent

    @staticmethod
    def smooth_indent_by_bg(document, start, left_indents, right_indents):
        left_indents = []
        right_indents = []
        if len(left_indents) > 1 and len(right_indents) > 1:
            left_indent = math.mean(left_indents)
            for j in range(start, len(document.paragraphs)):
                par_format = document.paragraphs[j].paragraph_format
                if par_format.shd.rgb is not None:
                    par_format.left_indent = \
                        calculate_left_indent(par_format, left_indent)
            right_indent = math.mean(right_indents)
            for j in range(start, len(document.paragraphs)):
                par_format = document.paragraphs[j].paragraph_format
                if par_format.shd.rgb is not None:
                    par_format.right_indent = right_indent

    @staticmethod
    def smooth_par_contain_background_indent(document):
        left_indents = []
        right_indents = []
        start = 0
        have_background = False
        for i in range(0, len(document.paragraphs)):
            par_format = document.paragraphs[i].paragraph_format
            if par_format.shd.rgb is not None:
                have_background = True
                Common.smooth_indent_by_shd(document, par_format, start, i,
                                            left_indents, right_indents)
            elif have_background:
                have_background = False
                start = i
                Common.smooth_indent_by_bg(document, start,
                                           left_indents, right_indents)

    @staticmethod
    def set_space_after(p, par, word, dpi, transformer,
                        next_word=None,
                        box_container=None,
                        is_same_format=None):
        """
        Set space after

        Parameters
        ----------
        p
        par
        word
        dpi
        transformer
        next_word
        box_container
        is_same_format: The word and next word is same format.
        With the condition, the space belong to the word.

        Returns
        -------

        """
        spaces_after = next_word.spaces_before
        spaces_after = 1 if spaces_after < 3 else spaces_after

        is_tap = spaces_after > 3 and AlignmentEnum.is_left(par.alignment)

        if not is_tap and is_same_format and len(p.runs) > 0:
            run = p.runs[-1]
            run.text = run.text + ' ' * spaces_after
        else:
            space = p.add_run()
            font = space.font

            # Checking for font name of space
            if word.font and len(word.font) > 0:
                font.name = word.font

            # Checking for font size of space
            if word.size and len(word.size) > 0:
                font.size = Pt(float(word.size))

            # Checking for font style of space
            if next_word is not None:
                # Checking for color space
                if (word.color is not None) and next_word.color:
                    space.font.color.rgb = PHOcrCommon.get_color(word.color)

                # Check for bold space
                if word.bold and next_word.bold:
                    space.bold = True

                # Checking for italic space
                if word.italic and next_word.italic:
                    space.italic = True

                # Checking for underline space
                if word.underline and next_word.underline:
                    space.underline = True
            # Add space
            if is_tap:
                # Only when the number of space large enough
                tab_position = Pixel(
                    (transformer.get_x(next_word)
                     - box_container.left_margin()),
                    dpi.horizontal_resolution
                )

                # If the margin of page left are OK, we will add the tab stop
                p.paragraph_format.tab_stops.add_tab_stop(
                    tab_position, WD_TAB_ALIGNMENT.LEFT)
                space.add_tab()
            else:
                space.add_text(' ' * spaces_after)

    @staticmethod
    def set_text_style_for_run(run, font_info, word_color):
        """
        Set text style for a run element.

        Parameters
        ----------
        run
        font_info
        word_color

        Returns
        -------

        """
        if font_info.bold == 'True':
            run.font.bold = True
        if font_info.italic == 'True':
            run.font.italic = True
        if font_info.underline == 'True':
            run.font.underline = True
        if word_color is not None and word_color != 'None':
            run.font.color.rgb = PHOcrCommon.get_color(word_color)
        if font_info.size == 0:
            run.font.size = Pt(WordDefault.FONT_SIZE)
        elif font_info.size > 0:
            run.font.size = Pt(font_info.size)
        run.font.name = font_info.name

    @staticmethod
    def get_anchor_paragraph(document):
        """
        Get anchor paragraph which is latest paragraph of document

        Parameters
        ----------
        document

        Returns
        -------

        """
        if len(document.paragraphs) == 0:
            # If not have any paragraph in document. Create an
            # paragraph for anchor
            p = document.add_paragraph()
        else:
            # Latest paragraph in document
            p = document.paragraphs[-1]
        return p

    @staticmethod
    def text_angle_in_block(angle, text_angle_histogram):
        """
        Calculate text angle in block using histogram of all text angle
        of paragraph

        Parameters
        ----------
        angle
        text_angle_histogram

        Returns
        -------

        """
        final_text_angle = 0
        max_count = 0
        for text_angle_key, count in text_angle_histogram.items():
            if count > max_count:
                final_text_angle = text_angle_key
                max_count = count
        if final_text_angle == 270:
            angle = 'vert270'
        elif final_text_angle == 90:
            angle = 'vert'
        elif final_text_angle == 180:
            angle = ' rot="10800000"'
        return angle

    @staticmethod
    def get_all_element_by_tag(page, expected_tag):
        """
        Get element by input tag name

        Parameters
        ----------
        page
        expected_tag

        Returns
        -------

        """
        expected_elements = []
        for region in page:
            if region.tag == expected_tag:
                expected_elements.append(region)
        return expected_elements

    @staticmethod
    def calculate_space_after_first_paragraph(
            page,
            paragraph_xml,
            margin_top):
        """
        Adding padding paragraph at head of document for space after
        by that way, we can insert table at the head of document and first
        paragraph after that

        Parameters
        ----------
        page
        paragraph_xml
        margin_top

        Returns
        -------

        """
        all_tables = page.tables
        all_tables.sort(key=lambda table: table.y)
        first_paragraph_y = paragraph_xml.y
        first_table_y = sys.maxsize

        if len(all_tables) > 0:
            first_table = all_tables[0]
            first_table_y = first_table.y

        if first_table_y > first_paragraph_y:
            target_y = first_paragraph_y
        else:
            target_y = first_table_y

        space_after = target_y - margin_top - 70
        return space_after

    # Calculate space after based on text direction
    @staticmethod
    def calculate_space_after(current_par, next_par, text_direction):
        if text_direction == TextDirection.TBRL:
            space_after = current_par.x - (next_par.x + next_par.w)
        else:
            space_after = next_par.y - (current_par.y + current_par.h)
        if space_after > 0:
            return space_after
        return 0

    # Remove paragraph in xml
    @staticmethod
    def delete_paragraph(paragraph):
        p = paragraph._element
        p.getparent().remove(p)
        p._p = p._element = None

    @staticmethod
    def add_textbox(document, textbox):
        """
        Add text box into document, by using last paragraph in document
        to be anchor

        Parameters
        ----------
        document
        textbox

        Returns
        -------

        """
        if len(document.paragraphs) > 0:
            target_anchor = document.paragraphs[-1]
        else:
            target_anchor = document.add_paragraph()
        run = target_anchor.add_run()
        run.add_textbox(textbox)

    @staticmethod
    def get_sum_vertical_overlap_area(page, box_photo):
        sum_overlap_v = 0
        for carea in page.careas:
            box_carea = Box(carea)
            if box_carea.top >= box_photo.top:
                if box_carea.bottom >= box_photo.bottom:
                    overlap_v = box_photo.bottom - box_carea.top
                else:
                    overlap_v = box_carea.h
            else:
                if box_carea.bottom <= box_photo.bottom:
                    overlap_v = box_carea.bottom - box_photo.top
                else:
                    overlap_v = box_photo.h
            if overlap_v > 0:
                sum_overlap_v += overlap_v
        return sum_overlap_v

    @staticmethod
    def get_sum_area(page, box_photo):
        sum_overlap = 0
        for carea in page.careas:
            for par in carea.paragraphs:
                for line in par.lines:
                    for word in line.words:
                        box_word = Box(word)
                        box_overlap = overlap_region(box_photo, box_word)
                        if box_overlap is not None:
                            sum_overlap += box_overlap.w * box_overlap.h
        return sum_overlap

    # Get wrap for photo
    @staticmethod
    def get_photo_wrap(element, page):
        box_photo = Box(element)
        if box_photo.w / page.w > 0.85 and box_photo.h / page.h > 0.85:
            # if the box photo overlap almost image,
            # don't wrap
            return 'wrapNone'

        # Detect format of picture
        sum_overlap_v = Common.get_sum_vertical_overlap_area(page, box_photo)
        ratio = round(sum_overlap_v / box_photo.h, 3)
        photo_wrap = 'wrapNone'
        if ratio > 0.75:
            photo_wrap = 'wrapSquare'
        sum_overlap = Common.get_sum_area(page, box_photo)
        if box_photo.w * box_photo.h > 0:
            ratio = sum_overlap / (box_photo.w * box_photo.h)
            if ratio > 0.07:
                photo_wrap = 'wrapNone'
        return photo_wrap

    # Get array of boxes of photos
    @staticmethod
    def get_photo_boxes(page):
        all_box_photo = []
        for photo in page.photos:
            box_photo = Box(photo)
            all_box_photo.append(box_photo)
        return all_box_photo

    # Get array of careas based on array of boxes of photos
    @staticmethod
    def get_carea_array_base_on_photos(page, all_box_photo):
        list_of_careas = []
        for carea in page.careas:
            if carea.is_noise or \
                    ratio_overlap_photo(carea, all_box_photo) >= 1:
                continue
            list_of_careas.append(carea)
        return list_of_careas

    # Get array of careas
    @staticmethod
    def get_carea_array(page):
        area_orders = []
        for element in page.elements:
            if element.tag == OfficeObjectTag.CAREA or \
                    element.tag == OfficeObjectTag.TABLE:
                area_infor = ObjectInfo(
                    element.id,
                    element.x,
                    element.y,
                    element.tag
                )
                area_orders.append(area_infor)
        return area_orders

    @staticmethod
    def assign_highlight(highlight_color):
        highlight_color_ = None
        if highlight_color == 'RED':
            highlight_color_ = WD_COLOR.RED
        elif highlight_color == 'GREEN':
            highlight_color_ = WD_COLOR.GREEN
        elif highlight_color == 'BLUE':
            highlight_color_ = WD_COLOR.BLUE
        elif highlight_color == 'YELLOW':
            highlight_color_ = WD_COLOR.YELLOW
        elif highlight_color == 'BRIGHT_GREEN':
            highlight_color_ = WD_COLOR.BRIGHT_GREEN
        elif highlight_color == 'DARK_BLUE':
            highlight_color_ = WD_COLOR.DARK_BLUE
        elif highlight_color == 'DARK_RED':
            highlight_color_ = WD_COLOR.DARK_RED
        elif highlight_color == 'DARK_YELLOW':
            highlight_color_ = WD_COLOR.DARK_YELLOW
        elif highlight_color == 'GRAY_25':
            highlight_color_ = WD_COLOR.GRAY_25
        elif highlight_color == 'GRAY_50':
            highlight_color_ = WD_COLOR.GRAY_50
        elif highlight_color == 'PINK':
            highlight_color_ = WD_COLOR.PINK
        elif highlight_color == 'TEAL':
            highlight_color_ = WD_COLOR.TEAL
        elif highlight_color == 'TURQUOISE':
            highlight_color_ = WD_COLOR.TURQUOISE
        elif highlight_color == 'VIOLET':
            highlight_color_ = WD_COLOR.VIOLET
        return highlight_color_

    @staticmethod
    def get_rgb_element(color_str):
        red, green, blue = color_str.split(',')
        red = int(red)
        green = int(green)
        blue = int(blue)
        return red, green, blue

    @staticmethod
    def get_min_distance(color, red, green, blue):
        red_ = int(color[0:2], 16)
        green_ = int(color[2:4], 16)
        blue_ = int(color[4:6], 16)
        min_balance = ((red_ - red) ** 2
                       + (green_ - green) ** 2
                       + (blue_ - blue) ** 2)
        return min_balance

    # Get highlight color
    @staticmethod
    def get_highlight_color(color_str):
        red, green, blue = Common.get_rgb_element(color_str)
        list_color = [
            'WHITE', 'BLACK', 'RED', 'GREEN', 'BLUE', 'YELLOW',
            'BRIGHT_GREEN', 'DARK_BLUE', 'DARK_RED', 'DARK_YELLOW',
            'GRAY_25', 'GRAY_50', 'PINK', 'TEAL', 'TURQUOISE',
            'VIOLET'
        ]
        list_color_hex = [
            '#FFFFFF', '#000000', '#FF0000', '#00FF00', '#0000FF',
            '#FFFF00', '#00FF00', '#000080', '#800000', '#808000',
            '#C0C0C0', '#808080', '#FF00FF', '#008080', '#00FFFF',
            '#800080'
        ]
        color_ = list_color_hex[0].lstrip('#')
        min_balance = Common.get_min_distance(color_, red, green, blue)
        highlight_color_index = 0
        for i in range(0, len(list_color)):
            color = list_color_hex[i].lstrip('#')
            balance = Common.get_min_distance(
                color, red, green, blue
            )
            if balance < min_balance:
                min_balance = balance
                highlight_color_index = i
        highlight_color = list_color[highlight_color_index]
        return Common.assign_highlight(highlight_color)

    # Given three collinear points p, q, r, the function checks if
    # point q lies on line segment 'pr'
    @staticmethod
    def on_segment(p, q, r):
        if min(p.x, r.x) <= q.x <= max(p.x, r.x) and \
                min(p.y, r.y) <= q.y <= max(p.y, r.y):
            return True

        return False

    # To find orientation of ordered triplet (p, q, r).
    # The function returns following values
    # 0 --> p, q and r are collinear
    # 1 --> Clockwise
    # 2 --> Counterclockwise
    @staticmethod
    def orientation(p, q, r):
        # See http://www.geeksforgeeks.org/orientation-3-ordered-points/
        # for details of below formula.
        val = (q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y)

        if val == 0:
            return 0  # collinear

        # clock or counter clock wise
        if val > 0:
            return 1
        else:
            return 2

    @staticmethod
    def do_intersect(p1, q1, p2, q2):
        # Find the four orientations needed for general and
        # special cases
        o1 = Common.orientation(p1, q1, p2)
        o2 = Common.orientation(p1, q1, q2)
        o3 = Common.orientation(p2, q2, p1)
        o4 = Common.orientation(p2, q2, q1)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special Cases
        # p1, q1 and p2 are collinear and p2 lies on segment p1q1
        if o1 == 0 and Common.on_segment(p1, p2, q1):
            return True

        # p1, q1 and p2 are collinear and q2 lies on segment p1q1
        if o2 == 0 and Common.on_segment(p1, q2, q1):
            return True

        # p2, q2 and p1 are collinear and p1 lies on segment p2q2
        if o3 == 0 and Common.on_segment(p2, p1, q2):
            return True

        # p2, q2 and q1 are collinear and q1 lies on segment p2q2
        if o4 == 0 and Common.on_segment(p2, q1, q2):
            return True

        return False  # Doesn't fall in any of the above cases

    @staticmethod
    def is_contain(p1, p2):
        p1_pos = PHOcrCommon.get_object_position(p1)
        p2_pos = PHOcrCommon.get_object_position(p2)
        if p1_pos.x <= p2_pos.x and p1_pos.y <= p2_pos.y and \
                (p1_pos.x + p1_pos.w >= p2_pos.x + p2_pos.w) and \
                (p1_pos.y + p1_pos.h >= p2_pos.y + p2_pos.h):
            return 1
        return 0

    @staticmethod
    def is_horizontal(c1, c2):
        """
        Check careas are "parallel" or not by using a line and
        check intersection points by horizontal

        Parameters
        ----------
        c1
        c2

        Returns
        -------

        """
        par_0_pos = PHOcrCommon.get_object_position(c1)
        par_1_pos = PHOcrCommon.get_object_position(c2)

        p0_polygon = Polygon(
            Point(par_0_pos.x, par_0_pos.y),
            Point(par_0_pos.x, par_0_pos.y + par_0_pos.h),
            Point(par_0_pos.x + par_0_pos.w, par_0_pos.y),
            Point(par_0_pos.x + par_0_pos.w, par_0_pos.y + par_0_pos.h)
        )
        p1_polygon = Polygon(
            Point(par_1_pos.x, par_1_pos.y),
            Point(par_1_pos.x, par_1_pos.y + par_1_pos.h),
            Point(par_1_pos.x + par_1_pos.w, par_1_pos.y),
            Point(par_1_pos.x + par_1_pos.w, par_1_pos.y + par_1_pos.h)
        )

        if par_0_pos.x > par_1_pos.x:
            delta = par_0_pos.x + par_0_pos.w
        else:
            delta = par_1_pos.x + par_1_pos.w

        min_x = min(par_0_pos.x, par_1_pos.x)
        max_y = max(par_0_pos.y, par_1_pos.y)
        min_h = min(par_0_pos.h, par_1_pos.h)
        for i in range(max_y, max_y + min_h):
            p0 = Point(min_x, i)
            q0 = Point(delta, i)
            if (
                Common.do_intersect(p0, q0, p0_polygon.p1, p0_polygon.q1) and
                Common.do_intersect(p0, q0, p0_polygon.p2, p0_polygon.q2) and
                Common.do_intersect(p0, q0, p1_polygon.p1, p1_polygon.q1) and
                Common.do_intersect(p0, q0, p1_polygon.p2, p1_polygon.q2)
            ):
                return True
        return False

    @staticmethod
    def is_vertical(c1, c2):
        """
        Check careas are "parallel" or not by using
        a line and check intersection points by vertical

        Parameters
        ----------
        c1
        c2

        Returns
        -------

        """
        # Get information of carea 1
        box_p1 = Box(c1)

        # Get information of carea 2
        box_p2 = Box(c2)

        p1_polygon = Polygon(
            Point(box_p1.x, box_p1.y),
            Point(box_p1.x + box_p1.w, box_p1.y),
            Point(box_p1.x, box_p1.y + box_p1.h),
            Point(box_p1.x + box_p1.w, box_p1.y + box_p1.h)
        )

        p2_polygon = Polygon(
            Point(box_p2.x, box_p2.y),
            Point(box_p2.x + box_p2.w, box_p2.y),
            Point(box_p2.x, box_p2.y + box_p2.h),
            Point(box_p2.x + box_p2.w, box_p2.y + box_p2.h)
        )

        max_x = max(box_p1.x, box_p2.x)
        min_y = min(box_p1.y, box_p2.y)
        min_w = min(box_p1.w, box_p2.w)
        if box_p1.y > box_p2.y:
            delta = box_p1.y + box_p1.h
        else:
            delta = box_p2.y + box_p2.h
        for i in range(max_x, max_x + min_w):
            p0 = Point(i, min_y)
            q0 = Point(i, delta)
            if (
                Common.do_intersect(p0, q0, p1_polygon.p1, p1_polygon.q1) and
                Common.do_intersect(p0, q0, p1_polygon.p2, p1_polygon.q2) and
                Common.do_intersect(p0, q0, p2_polygon.p1, p2_polygon.q1) and
                Common.do_intersect(p0, q0, p2_polygon.p2, p2_polygon.q2)
            ):
                return True
        return False

    @staticmethod
    def get_histogram(list_of_careas, layout_structure):
        # Get histograms of each careas
        histograms = {}
        for i in range(len(list_of_careas)):
            count = 0
            for j in range(len(layout_structure)):
                sub_layout = layout_structure[j]
                for k in range(len(sub_layout)):
                    if sub_layout[k] == list_of_careas[i].id:
                        count += 1
            histograms[list_of_careas[i].id] = count
        return histograms

    @staticmethod
    def get_layout_structure(list_of_careas):
        layout_structure = []
        # Get all couple of careas are parallel careas
        for i in range(len(list_of_careas)):
            sub_pars = [list_of_careas[i].id]
            for j in range(i + 1, len(list_of_careas)):
                if Common.is_horizontal(list_of_careas[i],
                                        list_of_careas[j]) or \
                                Common.is_contain(list_of_careas[i],
                                                  list_of_careas[j]) == 1:
                    sub_pars.append(list_of_careas[j].id)
            layout_structure.append(sub_pars)
        return layout_structure

    @staticmethod
    def is_complicated_page_layout(list_of_careas, debug=0):
        """
        Get shape of page layout is complicated or normal

        Parameters
        ----------
        list_of_careas
        debug

        Returns
        -------

        """
        if len(list_of_careas) <= 1:
            return False
        if len(list_of_careas) == 2:
            if Common.is_horizontal(list_of_careas[0], list_of_careas[1]):
                return True
            else:
                return False
        else:
            layout_structure = Common.get_layout_structure(list_of_careas)
            histograms = Common.get_histogram(list_of_careas, layout_structure)
            if debug > 0:
                print('layout_structure: ' + str(layout_structure))
                print('histograms: ' + str(histograms))
            for key in sorted(histograms):
                if debug > 0:
                    print('key:' + str(key) + '; value:' + str(histograms[key]))
                if histograms[key] > 1:
                    return True
            return False

    @staticmethod
    def is_long_character(line):
        """
        Check text of line have long character or not

        Parameters
        ----------
        line

        Returns
        -------

        """
        all_word = []
        long_char = ['p', 'g', 'j', 'q', 'y', 'Q']
        for word in line:
            for char in word:
                all_word.append(char.text)
        for i in range(0, len(all_word) - 1):
            if all_word[i] in long_char:
                return True
        return False

    @staticmethod
    def is_cjk_language(language):
        """
        Check current language is east asia language

        Parameters
        ----------
        language : str
            OCR language

        Returns
        -------

        """
        language_lower = language.lower()
        if (language_lower == 'chinesetraditional' or
                language_lower == 'chinesesimplified' or
                language_lower == 'japanese' or
                language_lower == 'korean'):
            return True
        return False
