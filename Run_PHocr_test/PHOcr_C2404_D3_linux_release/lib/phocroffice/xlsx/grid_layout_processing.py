# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
This module will build a grid layout base on information from xml
"""

from __future__ import division

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

from xlsx.common import Box, Common, Rectangle, RegionType
from phocr_shared.phocr_config import PHOcrConstant
from phocr_shared.phocr_common import PHOcrCommon, TextDirection
from phocr_shared.base_element import BaseElement
from phocr_shared.element_draw import ElementDraw
from phocr_shared.phocr_error import PHOcrError
from phocr_shared.phocr_dpi import PHOcrDPI


class GridLayoutProcessing(object):
    """
    Processing to generate grid layout
    """

    # The distance threshold for tiny row and column
    TINY_DISTANCE = 12

    def __init__(self, worksheet, export_one_sheet,
                 number_horizontal_pages, number_vertical_pages, debug=0):
        self.worksheet = worksheet
        self.debug = int(debug)
        self.width = 0
        self.height = 0
        self.text_direction = TextDirection.LRTB
        # We'll use this threshold to merge rows/columns which are very close
        self.min_distance = 20
        # Default dpi for processing
        self.dpi = PHOcrDPI(PHOcrConstant.DEFAULT_DPI, PHOcrConstant.DEFAULT_DPI)
        # Init value
        self.column_width = PHOcrConstant.ORIGINAL_COLUMN_WIDTH
        self.column_pixel = PHOcrConstant.DEFAULT_COLUMN_PIXELS
        self.row_height = PHOcrConstant.ORIGINAL_ROW_HEIGHT
        self.row_pixel = PHOcrConstant.DEFAULT_ROW_PIXELS
        # We need to convert value (x, y, w, h)
        # because default dpi of library is only 96dpi
        self.scale = float(96 / self.dpi.vertical_resolution)
        self.export_one_sheet = export_one_sheet
        # Number of horizontal page
        self.no_horizontal_pages = number_horizontal_pages
        # Number of vertical page
        self.no_vertical_pages = number_vertical_pages

        # Standard paper code corresponding with the standard paper size in
        # MS Office
        self.paper_code = 0

        # Paper orientation
        self.paper_orientation = ""

        # Flag to check if page is standard paper size
        self.is_using_standard_size = True

    def create_layout(self, page):
        """Create layout for page"""
        # Get dpi
        self.dpi = PHOcrCommon.get_dpi(page.dpi)

        # Re-calculate scale factor
        self.scale = float(96 / self.dpi.vertical_resolution)
        self.x_height = page.x_height
        self.width = page.w
        self.height = page.h
        self.box_map = []

        # Get standard paper size information (XLSX only need paper size name
        # and the flag to check that we standardize successfully)
        self.is_using_standard_size = page.is_using_standard_size
        self.paper_orientation = page.paper_orientation
        if self.is_using_standard_size:
            self.paper_code = page.paper_code

        # If we found layout is Chinese or Japanese
        writing_direction = page.writing_direction
        textline_order = page.textline_order
        if writing_direction == 2 and textline_order == 1:
            self.text_direction = TextDirection.TBRL

        self.pre_process_xml(page)
        self.pre_process_region(page)
        self.build_grid(page)

    def reset_value(self, element):
        """Scale coordinates basing on dpi"""
        # Convert value
        scaled_x = int(element.x * self.scale)
        scaled_y = int(element.y * self.scale)
        scaled_w = int((element.x + element.w) * self.scale)
        scaled_h = int((element.y + element.h) * self.scale)
        rectangle = Rectangle(scaled_x, scaled_y, scaled_w, scaled_h)
        return rectangle

    def extract_xml(self, element, region_type=RegionType.NONE):
        """Extract information from xml and save into array"""
        rectangle = self.reset_value(element)
        # Add into box trace
        temp_rectangle = Rectangle(rectangle.x,
                                   rectangle.y,
                                   rectangle.w - rectangle.x,
                                   rectangle.h - rectangle.y)
        box = Box(temp_rectangle, region_type)
        self.box_trace.append(box)
        # Add data into x_grid_layout and y_grid_layout
        self.x_grid_layout.append(rectangle.x)
        self.x_grid_layout.append(rectangle.w)
        self.y_grid_layout.append(rectangle.y)
        self.y_grid_layout.append(rectangle.h)

    def extract_xml_for_carea(self, element):
        """Extract information of text from xml"""
        # Loop over each paragraph in content area
        for paragraph in element.paragraphs:
            # Loop over each line of paragraph
            for line in paragraph.lines:
                temp_box = Box(Rectangle(line.x, line.y, line.w, line.h),
                               RegionType.TEXTLINE)
                for obj in self.box_map:
                    if temp_box.equal_box(obj['old_box']):
                        temp_box = obj['new_box']
                        break
                # Scale value
                scaled_x = int(line.x * self.scale)
                scaled_y = int(temp_box.y * self.scale)
                scaled_w = int((line.x + temp_box.w) * self.scale)
                scaled_h = int((temp_box.y + temp_box.h) * self.scale)
                # Add into box trace
                box = Box(Rectangle(scaled_x,
                                    scaled_y,
                                    scaled_w - scaled_x,
                                    scaled_h - scaled_y),
                          RegionType.TEXTLINE)
                self.box_trace.append(box)
                # Add data into x_grid_layout and y_grid_layout
                self.x_grid_layout.append(scaled_x)
                self.x_grid_layout.append(scaled_w)
                self.y_grid_layout.append(scaled_y)
                self.y_grid_layout.append(scaled_h)

    def extract_xml_for_table(self, table):
        """Extract information of table from xml"""
        # Check carefully if input xml is ok
        if table.num_rows <= 0 or table.num_cells <= 0:
            raise ValueError(PHOcrError.INVALID_XML)
        for row in table.rows:
            for column in row.cells:
                self.extract_xml(column, RegionType.TABLE)

    def extract_xml_for_photo(self, photo):
        """Extract information of photo from xml"""
        # Only add photo if it is bigger than threshold.
        # Here threshold is x_height
        # But we'll need to modify this threshold in the future if necessary
        if PHOcrCommon.is_photo_ok(photo.h, photo.w, self.x_height):
            self.extract_xml(photo, RegionType.PHOTO)

    def add_element_to_list(self, element, region_type):
        """Add box into list"""
        rectangle = Rectangle(element.x, element.y, element.w, element.h)
        # Add into box trace
        box = Box(rectangle, region_type)
        self.box_trace.append(box)

    def pre_process_by_horizontal(self):
        """Pre-processing by horizontal"""
        # Sort by x-coordinate
        self.box_trace = sorted(self.box_trace,
                                key=lambda e: e.x,
                                reverse=False)
        # Next, traverse each box
        for i in range(len(self.box_trace)):
            box = self.box_trace[i]
            # If this box is text-line
            if box.region_type != RegionType.TEXTLINE:
                self.box_map.append({
                    'old_box': box,
                    'new_box': box
                })
                continue
            is_paralleled = False
            for j in range(i + 1, len(self.box_trace)):
                next_box = self.box_trace[j]
                # Ignore if matching below conditions
                if box.intersect_box(next_box) or \
                        box.contain_box(next_box) or \
                        box.equal_box(next_box):
                    continue
                if Common.is_parallel_boxes_by_y(box, next_box):
                    is_found = False
                    for obj in self.box_map:
                        if box.equal_box(obj['old_box']):
                            is_found = True
                            break
                    if not is_found:
                        # Extend width of current box to start of other box
                        new_rectangle = Rectangle(box.x,
                                                  box.y,
                                                  next_box.x - box.x,
                                                  box.h)
                        new_box = Box(new_rectangle, box.region_type)
                        self.box_map.append({
                            'old_box': box,
                            'new_box': new_box
                        })
                    is_paralleled = True
                    break
            if not is_paralleled:
                is_found = False
                for obj in self.box_map:
                    if box.equal_box(obj['old_box']):
                        is_found = True
                        break
                if not is_found:
                    # Extend width of current box to width of image
                    new_rectangle = Rectangle(box.x,
                                              box.y,
                                              self.width - box.x,
                                              box.h)
                    new_box = Box(new_rectangle, box.region_type)
                    self.box_map.append({
                        'old_box': box,
                        'new_box': new_box
                    })

    def pre_process_by_vertical(self):
        """Pre-processing by vertical"""
        # Sort by y-coordinate
        self.box_trace = sorted(self.box_trace,
                                key=lambda e: (e.y + e.h),
                                reverse=True)
        # Next, traverse each box
        for i in range(len(self.box_trace)):
            box = self.box_trace[i]
            # If this box is text-line
            if box.region_type != RegionType.TEXTLINE:
                self.box_map.append({
                    'old_box': box,
                    'new_box': box
                })
                continue
            is_paralleled = False
            for j in range(i + 1, len(self.box_trace)):
                next_box = self.box_trace[j]
                # Ignore if matching below conditions
                if box.intersect_box(next_box) or \
                        box.contain_box(next_box) or \
                        box.equal_box(next_box):
                    continue
                if Common.is_parallel_boxes_by_x(box, next_box):
                    next_box_height = next_box.y + next_box.h
                    is_found = False
                    k = 0
                    for obj in self.box_map:
                        if box.equal_box(obj['new_box']):
                            self.box_map[k]['new_box'].h = \
                                (self.box_map[k]['new_box'].h
                                 + self.box_map[k]['new_box'].y
                                 - next_box_height)
                            self.box_map[k]['new_box'].y = next_box_height
                            is_found = True
                            break
                        k += 1
                    if not is_found:
                        new_rectangle = Rectangle(
                            box.x,
                            next_box_height,
                            box.w,
                            box.h + box.y - next_box_height)
                        new_box = Box(new_rectangle, box.region_type)
                        self.box_map.append({
                            'old_box': box,
                            'new_box': new_box
                        })
                    is_paralleled = True
                    break
            if not is_paralleled:
                is_found = False
                k = 0
                for obj in self.box_map:
                    if box.equal_box(obj['new_box']):
                        self.box_map[k]['new_box'].h = \
                            (self.box_map[k]['new_box'].h
                             + self.box_map[k]['new_box'].y)
                        self.box_map[k]['new_box'].y = 0
                        is_found = True
                        break
                    k += 1
                if not is_found:
                    new_rectangle = Rectangle(box.x, 0, box.w, box.h + box.y)
                    new_box = Box(new_rectangle, box.region_type)
                    self.box_map.append({
                        'old_box': box,
                        'new_box': new_box
                    })

    def debug_infor_boxes(self):
        """Print debug information"""
        from PIL import Image, ImageDraw
        white = (255, 255, 255)
        box_map_image = Image.new('RGB', [self.width, self.height], white)
        box_map_draw = ImageDraw.Draw(box_map_image)
        box_len = len(self.box_map)
        for i in range(box_len):
            box = self.box_map[i]
            box_map_draw.rectangle(((box['new_box'].x, box['new_box'].y),
                                    (box['new_box'].x + box['new_box'].w,
                                     box['new_box'].y + box['new_box'].h)),
                                   outline='red')
        box_map_image.save('box_map.png')
        box_trace_image = Image.new('RGB', [self.width, self.height], white)
        box_trace_draw = ImageDraw.Draw(box_trace_image)
        box_len = len(self.box_trace)
        for i in range(box_len):
            box = self.box_trace[i]
            box_trace_draw.rectangle(((box.x, box.y),
                                      (box.x + box.w,
                                       box.y + box.h)),
                                     outline='red')
        box_trace_image.save('box_trace.png')

    def add_text_to_list(self, page):
        """Add text to list"""
        # Find all content area
        for carea in page.careas:
            for paragraph in carea.paragraphs:
                for line in paragraph.lines:
                    self.add_element_to_list(line, RegionType.TEXTLINE)

    def add_photo_to_list(self, page):
        """Add photo to list"""
        # Find all photos
        for photo in page.photos:
            if PHOcrCommon.is_photo_ok(photo.h, photo.w, self.x_height):
                self.add_element_to_list(photo, RegionType.PHOTO)

    def add_table_to_list(self, page):
        """Add table to list"""
        # Find all tables
        for table in page.tables:
            # Check carefully if input xml is ok
            if table.num_rows <= 0 or table.num_cells <= 0:
                raise ValueError(PHOcrError.INVALID_XML)
            for row in table.rows:
                for column in row.cells:
                    self.add_element_to_list(column, RegionType.TABLE)

    def pre_process_region(self, page):
        """Pre-processing for regions to extends about x and y-coordinate"""
        # Traverse each page to extend region
        # Firstly, store information of box of regions
        self.box_trace = []
        self.box_map = []
        self.add_text_to_list(page)
        self.add_table_to_list(page)
        if self.debug > 0:
            from PIL import Image, ImageDraw
            white = (255, 255, 255)
            box_trace_image = Image.new('RGB', [self.width, self.height], white)
            box_trace_draw = ImageDraw.Draw(box_trace_image)
            box_len = len(self.box_trace)
            for i in range(box_len):
                box = self.box_trace[i]
                box_trace_draw.rectangle(((box.x, box.y),
                                          (box.x + box.w,
                                           box.y + box.h)),
                                         outline='red')
            box_trace_image.save('box_trace_initial.png')
        self.pre_process_by_horizontal()
        self.box_trace = []
        for obj in self.box_map:
            self.box_trace.append(obj['new_box'])
        self.pre_process_by_vertical()
        if self.debug > 0:
            self.debug_infor_boxes()
        self.box_trace = []

    @classmethod
    def refine_coordinate_case_1(cls, current_line, next_line):
        """Refine coordinate in case 1"""
        current_x = current_line.x
        current_y = current_line.y
        current_w = current_line.w
        next_x = next_line.x
        next_y = next_line.y
        next_w = next_line.w
        next_h = next_line.h
        # Case 1:
        #       __________
        #  ____|__________|___
        # |    |__________|   |
        # |                   |
        # |                   |
        # |___________________|
        # Smaller is current box, larger is next box
        if next_x <= current_x <= next_x + next_w and \
                next_x <= current_x + current_w <= next_x + next_w:
            if current_y < next_y:
                current_line.h = next_y - current_y
            else:
                next_line.h = current_y - next_h
        elif current_x <= next_x <= current_x + current_w and \
                current_x <= next_x + next_w <= current_x + current_w:
            # Smaller is next box, larger is current box
            if next_y < current_y:
                next_line.h = current_y - next_y
            else:
                current_line.h = next_y - current_y

    @classmethod
    def refine_coordinate_case_2(cls, current_line, next_line):
        """Refine coordinate in case 2"""
        current_x = current_line.x
        current_y = current_line.y
        current_h = current_line.h
        next_x = next_line.x
        next_y = next_line.y
        next_h = next_line.h
        if next_y <= current_y <= next_y + next_h and \
                next_y <= current_y + current_h <= next_y + next_h:
            # Case 2:
            #  ___________________
            # |               ____|_____
            # |              |    |     |
            # |              |    |     |
            # |              |____|_____|
            # |                   |
            # |___________________|
            # Smaller is current box, larger is next box
            if next_x < current_x:
                next_line.w = current_x - next_x
            else:
                current_line.w = next_x - current_x
        elif current_y <= next_y <= current_y + current_h and \
                current_y <= next_y + next_h <= current_y + current_h:
            # Smaller is next box, larger is current box
            if current_x < next_x:
                current_line.w = next_x - current_x
            else:
                next_line.w = current_x - next_x

    @classmethod
    def refine_coordinate_case_3(cls, current_line, next_line):
        """Refine coordinate in case 3"""
        current_x = current_line.x
        current_y = current_line.y
        current_w = current_line.w
        current_h = current_line.h
        next_x = next_line.x
        next_y = next_line.y
        next_w = next_line.w
        next_h = next_line.h
        # Case 3: Remaining cases
        if current_y < next_y:
            horizontal_distance = current_x + current_w - next_x
            vertical_distance = current_y + current_h - next_y
            if horizontal_distance > vertical_distance:
                current_line.h = next_y - current_y
            else:
                current_line.w = next_x - current_x
        else:
            horizontal_distance = next_x + next_w - current_x
            vertical_distance = next_y + next_h - current_y
            if horizontal_distance > vertical_distance:
                next_line.h = current_y - next_y
            else:
                next_line.w = current_x - next_x

    def refine_coordinate(self, current_line, next_line):
        """Refine coordinates of objects if they are overlapped"""
        current_x = current_line.x
        current_y = current_line.y
        current_w = current_line.w
        current_h = current_line.h
        current_rect = Rectangle(current_x, current_y, current_w, current_h)
        current_box = Box(current_rect)

        next_x = next_line.x
        next_y = next_line.y
        next_w = next_line.w
        next_h = next_line.h
        next_rect = Rectangle(next_x, next_y, next_w, next_h)
        next_box = Box(next_rect)
        # If two boxes are overlapped
        # We'll re-modify coordinates
        if current_box.contain_box(next_box) or \
                next_box.contain_box(current_box):
            return
        if current_box.intersect_box(next_box):
            # Case 1:
            #       __________
            #  ____|__________|___
            # |    |__________|   |
            # |                   |
            # |                   |
            # |___________________|
            # Smaller is current box, larger is next box
            if (next_x <= current_x <= next_x + next_w and
                next_x <= current_x + current_w <= next_x + next_w) or \
                    (current_x <= next_x <= current_x + current_w and
                     current_x <= next_x + next_w <= current_x + current_w):
                self.refine_coordinate_case_1(current_line, next_line)
            elif (next_y <= current_y <= next_y + next_h and
                  next_y <= current_y + current_h <= next_y + next_h) or \
                    (current_y <= next_y <= current_y + current_h and
                     current_y <= next_y + next_h <= current_y + current_h):
                self.refine_coordinate_case_2(current_line, next_line)
            else:
                self.refine_coordinate_case_3(current_line, next_line)

    def reset_left(self, current_line, next_line):
        """Reset left if possible"""
        line_x = current_line.x
        next_line_x = next_line.x
        if abs(line_x - next_line_x) <= self.min_distance:
            min_x = min(line_x, next_line_x)
            next_line.x = min_x
            current_line.x = min_x

    def pre_process_xml_by_x(self, ocr_lines):
        """Pre-processing by x-coordinate"""
        # Check to re-set x-coordinate
        for i in range(len(ocr_lines) - 1):
            current_line = ocr_lines[i]
            for j in range(i + 1, len(ocr_lines)):
                next_line = ocr_lines[j]
                self.reset_left(current_line, next_line)

    def reset_width(self, current_line, next_line):
        """Reset width if possible"""
        line_x = current_line.x
        line_w = current_line.w
        line_width = line_x + line_w
        next_line_x = next_line.x
        next_line_w = next_line.w
        next_line_width = next_line_x + next_line_w
        if abs(line_width - next_line_width) <= self.min_distance:
            min_x = min(line_width, next_line_width)
            next_line.w = min_x - next_line_x
            current_line.w = min_x - line_x

    def pre_process_xml_by_w(self, ocr_lines):
        """Pre-processing by w-coordinate"""
        # Check to re-set w-coordinate
        for i in range(len(ocr_lines) - 1):
            current_line = ocr_lines[i]
            for j in range(i + 1, len(ocr_lines)):
                next_line = ocr_lines[j]
                self.reset_width(current_line, next_line)

    def reset_top(self, current_line, next_line):
        """Reset top if possible"""
        line_y = current_line.y
        next_line_y = next_line.y
        if abs(line_y - next_line_y) <= self.min_distance:
            min_y = min(line_y, next_line_y)
            next_line.y = min_y
            current_line.y = min_y

    def reset_bottom(self, current_line, next_line):
        """Reset height if possible"""
        line_y = current_line.y
        line_h = current_line.h
        line_bottom = line_y + line_h
        next_line_y = next_line.y
        next_line_h = next_line.h
        next_line_bottom = next_line_y + next_line_h
        if abs(line_bottom - next_line_bottom) <= self.min_distance:
            min_h = min(line_bottom, next_line_bottom)
            next_line.h = min_h - next_line_y
            current_line.h = min_h - line_y

    def pre_process_xml_by_y(self, ocr_lines):
        """Pre-processing by y-coordinate"""
        # Check to re-set y-coordinate
        for i in range(len(ocr_lines) - 1):
            current_line = ocr_lines[i]
            for j in range(i + 1, len(ocr_lines)):
                next_line = ocr_lines[j]
                self.reset_top(current_line, next_line)

    def reset_height(self, current_line, next_line):
        """Reset height if possible"""
        line_y = current_line.y
        line_h = current_line.h
        line_height = line_y + line_h
        next_line_y = next_line.y
        next_line_h = next_line.h
        next_line_height = next_line_y + next_line_h
        if abs(line_height - next_line_height) <= self.min_distance:
            min_h = min(line_height, next_line_height)
            next_line.h = min_h - next_line_y
            current_line.h = min_h - line_y

    def pre_process_xml_by_h(self, ocr_lines):
        """Pre-processing by h-coordinate"""
        # Check to re-set h-coordinate
        for i in range(len(ocr_lines) - 1):
            current_line = ocr_lines[i]
            for j in range(i + 1, len(ocr_lines)):
                next_line = ocr_lines[j]
                self.reset_bottom(current_line, next_line)

    def pre_process_xml_with_table(self, column, other):
        """Pre-processing other object with column"""
        column_width = column.x + column.w
        column_height = column.y + column.h
        other_width = other.x + other.w
        other_height = other.y + other.h
        # Reset x-coordinate if it is very close column of table
        if abs(column.x - other.x) <= self.min_distance:
            other.w = other_width - column.x
            other.x = column.x
        elif abs(column_width - other.x) <= self.min_distance:
            other.w = other_width - column_width
            other.x = column_width
        # Reset y-coordinate if it is very close column of table
        if abs(column.y - other.y) <= self.min_distance:
            other.h = other_height - column.y
            other.y = column.y
        elif abs(column_height - other.y) <= self.min_distance:
            other.h = other_height - column_height
            other.y = column_height
        # Reset w-coordinate if it is very close column of table
        if abs(column.x - other_width) <= self.min_distance:
            other.w = column.x - other.x
        elif abs(column_width - other_width) <= self.min_distance:
            other.w = column_width - other.x
        # Reset h-coordinate if it is very close column of table
        if abs(column.y - other_height) <= self.min_distance:
            other.h = column.y - other.y
        elif abs(column_height - other_height) <= self.min_distance:
            other.h = column_height - other.y

    def pre_process_xml_between_column(self, current_column, next_column):
        """Pre-processing between columns"""
        self.check_horizontal_position(current_column, next_column)

        # Check bottom of current column and bottom of next column
        self.check_bottom_and_bottom(current_column, next_column)

        # Check top of current column and top of next column
        self.check_top_and_top(current_column, next_column)

    @classmethod
    def check_horizontal_position(cls, current_col, next_col):
        """Check horizontal position between two cells"""
        current_shape = BaseElement(current_col)
        next_shape = BaseElement(next_col)
        curr_left = current_shape.box.left
        next_left = next_shape.box.left

        # Set x-coordinate follow the maximum value if they're closed
        if abs(curr_left - next_left) <= GridLayoutProcessing.TINY_DISTANCE:
            # For simple implementation, only set the x- value at this point
            # and synchronize table position later
            min_left = min(curr_left, next_left)
            current_col.x = min_left
            next_col.x = min_left

    @classmethod
    def check_bottom_and_bottom(cls, current_col, next_col):
        """Check bottom position of this column and bottom pos of next column"""
        current_shape = BaseElement(current_col)
        next_shape = BaseElement(next_col)
        curr_bottom = current_shape.box.bottom
        curr_top = current_shape.box.top
        next_bottom = next_shape.box.bottom
        next_top = next_shape.box.top
        if 0 < abs(curr_bottom - next_bottom) <= \
                GridLayoutProcessing.TINY_DISTANCE:
            max_bottom = max(curr_bottom, next_bottom)
            current_col.h = max_bottom - curr_top
            next_col.h = max_bottom - next_top

    @classmethod
    def check_top_and_top(cls, current_col, next_col):
        """Check top position of this column and top position of next column"""
        current_shape = BaseElement(current_col)
        next_shape = BaseElement(next_col)
        curr_bottom = current_shape.box.bottom
        curr_top = current_shape.box.top
        next_bottom = next_shape.box.bottom
        next_top = next_shape.box.top
        if 0 < abs(curr_top - next_top) <= GridLayoutProcessing.TINY_DISTANCE:
            min_top = min(curr_top, next_top)
            current_col.y = min_top
            current_col.h = curr_bottom - min_top
            next_col.y = min_top
            next_col.h = next_bottom - min_top

    @staticmethod
    def update_table_xml(table):
        """
        Update table xml to match the x and w value after change it's
        value
        """
        # Update cells in horizontal direction
        GridLayoutProcessing.update_cell_horizontal(table)

        # Update cells in vertical direction
        GridLayoutProcessing.update_cell_vertical(table)

        # Update table bounding box
        GridLayoutProcessing.update_table_bb(table)

    @staticmethod
    def update_cell_horizontal(table):
        """Update the width of each cell to match data after previous process"""
        for row in table.rows:
            row_right = row.x + row.w
            col_idx = 0
            for col in row.cells:
                # If this is first column of row, then we must set
                # x-coordinate for this row
                if col_idx < len(row.cells) - 1:
                    next_col = row.cells[col_idx + 1]
                    width = next_col.x - col.x
                    col.w = width
                else:
                    col.w = row_right - col.x
                col_idx += 1

    @staticmethod
    def update_cell_vertical(table):
        """Update table cell in vertical direction from top down"""
        row_idx = 0
        rows = table.rows
        for row in rows:
            next_row = rows[row_idx + 1] if row_idx < len(rows) - 1 else None
            # Find max bottom in row
            max_bottom_with_row_span = 0
            max_bottom = 0
            for col in row.cells:
                col_bottom = col.y + col.h
                if col_bottom > max_bottom_with_row_span:
                    max_bottom_with_row_span = col_bottom
            for col in row.cells:
                col_bottom = col.y + col.h
                if col.row_span > 1:
                    continue
                if col_bottom > max_bottom:
                    max_bottom = col_bottom

            # If this row has only column with row span
            if max_bottom == 0 and max_bottom_with_row_span > 0:
                max_bottom = max_bottom_with_row_span

            # Update height for column in row
            for col in row.cells:
                if col.row_span == 1:
                    col.h = max_bottom - col.y
                row.h = max_bottom_with_row_span - col.y
                if next_row is not None:
                    if not GridLayoutProcessing.is_approximate_horizontal(
                            row,
                            next_row):
                        next_row.y = max_bottom
                        for next_col in next_row.cells:
                            next_col.y = next_row.y
            row_idx += 1

    @staticmethod
    def update_table_bb(table):
        """Used to update the table bounding box"""
        min_left = 0
        min_top = 0
        max_bottom = 0
        max_right = 0
        row_idx = 0
        for row in table.rows:
            row_ = BaseElement(row)
            if row_idx == 0:
                min_left = row_.box.left
                min_top = row_.box.top
            if row_.box.left < min_left:
                min_left = row_.box.left
            if row_.box.top < min_top:
                min_top = row_.box.top
            if row_.box.bottom > max_bottom:
                max_bottom = row_.box.bottom
            if row_.box.right > max_right:
                max_right = row_.box.right
            row_idx += 1
        table_ = BaseElement(table)
        table_.box.left = min_left
        table_.box.top = min_top
        table_.box.width = max_right - min_left
        table_.box.height = max_bottom - min_top

    @staticmethod
    def is_approximate_horizontal(first_row, second_row):
        """
        Check first and second is nearby in position

        Parameters
        ----------
        first_row
        second_row

        Returns
        -------

        """
        distance_threshold = 10
        first = BaseElement(first_row)
        second = BaseElement(second_row)
        if abs(first.box.top - second.box.top) < distance_threshold and \
                abs(first.box.bottom - second.box.bottom) < distance_threshold:
            return True
        else:
            return False

    @classmethod
    def update_last_col_position(cls, table, next_table):
        """Used to enhance the position of last column between table"""
        # Find the maximum right of each table
        max_right_list = [0, 0]
        for row in table.rows:
            last_col = BaseElement(row.cells[len(row.cells) - 1])
            last_col_right = last_col.box.right
            if last_col_right > max_right_list[0]:
                max_right_list[0] = last_col_right
        for row in next_table.rows:
            last_col = BaseElement(row.cells[len(row.cells) - 1])
            last_col_right = last_col.box.right
            if last_col_right > max_right_list[1]:
                max_right_list[1] = last_col_right

        # Set the value for each column
        max_right = max(max_right_list)
        if 0 < abs(max_right_list[0] - max_right_list[1]) \
                <= GridLayoutProcessing.TINY_DISTANCE:
            if max_right_list[0] > max_right_list[1]:
                # Set right value for next_table
                for row in next_table.rows:
                    last_col = BaseElement(row.cells[len(row.cells) - 1])
                    last_col_right = last_col.box.right
                    if 0 < abs(last_col_right - max_right) \
                            <= GridLayoutProcessing.TINY_DISTANCE:
                        last_col.box.right = max_right

            else:
                # Set right value for last columns in table
                for row in table.rows:
                    last_col = BaseElement(row.cells[len(row.cells) - 1])
                    last_col_right = last_col.box.right
                    if 0 < abs(last_col_right - max_right) \
                            <= GridLayoutProcessing.TINY_DISTANCE:
                        last_col.box.right = max_right

    def pre_process_between_tables(self, current_table, next_table):
        """Pre-processing between table"""
        for current_row in current_table.rows:
            for current_column in current_row.cells:
                for next_row in next_table.rows:
                    for next_column in next_row.cells:
                        self.pre_process_xml_between_column(current_column,
                                                            next_column)

    def pre_process_xml_base_on_table(self, ocr_tables, ocr_lines):
        """Pre-processing other objects basing on tables"""
        for i in range(len(ocr_tables) - 1):
            current_table = ocr_tables[i]
            for j in range(i + 1, len(ocr_tables)):
                next_table = ocr_tables[j]
                self.pre_process_between_tables(current_table, next_table)

                # Update table xml to match the position of table after
                # assigning value for column
                GridLayoutProcessing.update_table_xml(current_table)
                GridLayoutProcessing.update_table_xml(next_table)
                self.update_last_col_position(current_table, next_table)
        for table in ocr_tables:
            for row in table.rows:
                for column in row.cells:
                    for line in ocr_lines:
                        self.pre_process_xml_with_table(column, line)

    def pre_process_xml_with_line(self, line, other):
        """Pre-processing other object basing on line"""
        line_width = line.x + line.w
        line_height = line.y + line.h
        other_width = other.x + other.w
        other_height = other.y + other.h
        # Reset x-coordinate if it is very close line of table
        if abs(line.x - other.x) <= self.min_distance:
            other.w = other_width - line.x
            other.x = line.x
        elif abs(line_width - other.x) <= self.min_distance:
            other.w = other_width - line_width
            other.x = line_width
        # Reset y-coordinate if it is very close line of table
        if abs(line.y - other.y) <= self.min_distance:
            other.h = other_height - line.y
            other.y = line.y
        elif abs(line_height - other.y) <= self.min_distance:
            other.h = other_height - line_height
            other.y = line_height

    def pre_process_xml_base_on_line(self, ocr_lines, ocr_photos):
        """Pre-processing other objects basing on lines"""
        for line in ocr_lines:
            for photo in ocr_photos:
                # Only add photo if it is bigger than threshold
                if PHOcrCommon.is_photo_ok(photo.h, photo.w, self.x_height):
                    self.pre_process_xml_with_line(line, photo)

    def pre_process_xml(self, page):
        """
        Pre-processing .xml file to refine x, y, w, h of objects
        Here, we'll combine if they are very close (<= threshold)
        """
        # Find all content areas
        lines = []
        # Store all lines
        for carea in page.careas:
            for paragraph in carea.paragraphs:
                for line in paragraph.lines:
                    lines.append(line)
        # Check overlapped boxes to refine x, y, w, h
        for i in range(len(lines)):
            for j in range(i + 1, len(lines)):
                self.refine_coordinate(lines[i], lines[j])
            for table in page.tables:
                self.refine_coordinate(lines[i], table)

        # Base on columns in table to refine x, y, w, h
        if len(page.tables) > 0:
            self.pre_process_xml_base_on_table(page.tables, lines)

        # Debug table position after updating them
        if self.debug:
            print("After update table xml")
            draw = ElementDraw(self.width, self.height)
            for table in page.tables:
                draw.write(table)

        # Combine very close x-coordinate to reduce small columns
        self.pre_process_xml_by_x(lines)
        # Combine very close w-coordinate to reduce small columns
        self.pre_process_xml_by_w(lines)
        # Combine very close y-coordinate to reduce small rows
        self.pre_process_xml_by_y(lines)
        # Combine very close h-coordinate to reduce small rows
        self.pre_process_xml_by_h(lines)
        if self.debug > 0:
            from xml.etree.ElementTree import ElementTree
            tree = ElementTree(page)
            tree.write(open('debug.xml', 'wb'))

    def get_page_layout(self, page_obj):
        """
        Get layout of page
        We only care about content area and table
        With photo, it's not only easy to place but also update position
        """
        # We will build grid layout basing on x-coordinate and y-coordinate

        for carea in page_obj.careas:
            self.extract_xml_for_carea(carea)
        for table in page_obj.tables:
            self.extract_xml_for_table(table)

        # Remove duplicated elements and sort by ASC
        self.x_grid_layout = sorted(list(set(self.x_grid_layout)))
        self.y_grid_layout = sorted(list(set(self.y_grid_layout)))
        # Check overlapped blocks
        self.get_overlapped_box()

    def get_overlapped_box(self):
        """Get overlapped boxes from xml to fix error when opening .xlsx file"""
        box_len = len(self.box_trace)
        for i in range(box_len):
            previous_box = self.box_trace[i]
            if previous_box.region_type == RegionType.PHOTO or \
                    previous_box.region_type == RegionType.TABLE:
                continue
            for j in range(i + 1, box_len):
                next_box = self.box_trace[j]
                if next_box.region_type == RegionType.PHOTO or \
                        next_box.region_type == RegionType.TABLE:
                    continue
                # If found two boxes are intersected or contained each other
                # We'll save infor of smaller box to ignore it
                if previous_box.intersect_box(next_box) or \
                        previous_box.contain_box(next_box) or \
                        next_box.contain_box(previous_box):
                    if previous_box.get_area() > next_box.get_area():
                        self.overlapped_trace_arr.append(next_box)
                    else:
                        self.overlapped_trace_arr.append(previous_box)

    def get_row_height(self, y_distance):
        """Get height of row"""
        row_height = 0
        # Get row position
        i = 0
        for obj in self.y_grid_layout_map:
            if obj['value'] == y_distance and \
                    i < len(self.y_grid_layout_map) - 1:
                row_height = self.y_grid_layout_map[i + 1]['height']
                break
            i += 1
        return row_height

    def get_coordinate_of_line(self, line):
        """Get coordinate of line"""
        line_rectangle = Rectangle(line.x, line.y, line.w, line.h)
        temp_box = Box(line_rectangle, RegionType.TEXTLINE)
        for obj in self.box_map:
            if temp_box.equal_box(obj['old_box']):
                temp_box = obj['new_box']
                break
        # Convert value
        x_distance = int(line.x * self.scale)
        y_distance = int(temp_box.y * self.scale)
        w_distance = int((line.x + temp_box.w) * self.scale)
        h_distance = int((temp_box.y + temp_box.h) * self.scale)
        rectangle = Rectangle(x_distance, y_distance, w_distance, h_distance)
        return rectangle

    def get_line_position(self, line):
        """Get position of line"""
        is_ignored = False
        rectangle = self.get_coordinate_of_line(line)
        # Check line is overlapped or not
        is_overlapped = False
        for obj in self.overlapped_trace_arr:
            if obj.x == rectangle.x and obj.y == rectangle.y:
                is_overlapped = True
                break
        # Ignore overlapped line with bigger area
        if is_overlapped:
            is_ignored = True
        row_height = self.get_row_height(rectangle.y)
        (row, column, width, height) = self.get_cell_position(rectangle)
        if height == row or column == width:
            is_ignored = True
        return is_ignored, row_height, row, column, width, height

    def get_carea_str(self, carea):
        """
        Get carea string which concat from all paragraph inside

        Parameters
        ----------
        carea

        Returns
        -------

        """
        result = ''
        for paragraph in carea:
            result += self.get_paragraph_str(paragraph) + '\n'
        return result

    @classmethod
    def get_paragraph_str(cls, paragraph):
        """
        Get paragraph string which concat from all line inside

        Parameters
        ----------
        paragraph

        Returns
        -------

        """
        paragraph_str = ''
        for line in paragraph:
            for word in line:
                paragraph_str += word.get('value') + ' '
            paragraph_str += '\n'
        return paragraph_str

    def find_containing_cell(self, element):
        """Find the nearby cell and offset with it"""
        photo_x_scaled = element.x * self.scale
        photo_y_scaled = element.y * self.scale
        x_offset = photo_x_scaled
        y_offset = photo_y_scaled

        # Find nearest smaller in the grid compare with the left of element
        start_col = 0
        start_row = 0
        nearest_col_value = 0
        nearest_row_value = 0
        for col_value in self.x_grid_layout:
            if col_value < photo_x_scaled:
                nearest_col_value = col_value
                start_col += 1
            else:
                break
        x_offset -= nearest_col_value
        for row_value in self.y_grid_layout:
            if row_value < photo_y_scaled:
                nearest_row_value = row_value
                start_row += 1
            else:
                break
        y_offset -= nearest_row_value
        return start_col, start_row, x_offset, y_offset

    def get_cell_position(self, rectangle):
        """Get position of cell basing on coordinates"""
        # Get cell position
        row = 0
        column = 0
        # Get column position
        for obj in self.x_grid_layout_map:
            if obj['value'] == rectangle.x:
                column = obj['column']
                break
        # Get row position
        for obj in self.y_grid_layout_map:
            if obj['value'] == rectangle.y:
                row = obj['row']
                break
        width = 0
        height = 0
        # Get width position
        for obj in self.x_grid_layout_map:
            if obj['value'] == rectangle.w:
                width = obj['column']
                break
        # Get height position
        for obj in self.y_grid_layout_map:
            if obj['value'] == rectangle.h:
                height = obj['row']
                break
        return row, column, width, height

    def get_cell_information(self, element):
        """Get information of cell"""
        rectangle = self.reset_value(element)
        (row, column, width, height) = self.get_cell_position(rectangle)
        return row, column, width, height

    def setup_page(self, row, column):
        """Set page setup"""
        # Add distance between last element and width (height) of page
        page_width = int(self.width * self.scale)
        page_height = int(self.height * self.scale)

        # Set standard paper size and orientation for worksheet
        if self.is_using_standard_size:
            self.worksheet.set_paper(self.paper_code)
            if self.paper_orientation == "portrait":
                self.worksheet.set_portrait()
            elif self.paper_orientation == "landscape":
                self.worksheet.set_landscape()
            else:
                pass
        else:
            if self.height > self.width:
                self.worksheet.set_portrait()
            else:
                self.worksheet.set_landscape()

        # Get right margin
        right_mar = page_width - self.x_grid_layout[-1]
        # Get bottom margin
        bottom_mar = page_height - self.y_grid_layout[-1]
        # Get width of last column
        last_width = self._pixel_to_column_width(right_mar)
        self.worksheet.set_column(column, column, last_width)
        column += 1
        # Get height of last row
        last_height = bottom_mar * self.row_height / self.row_pixel
        self.worksheet.set_row(row, last_height)
        row += 1
        self.last_row = row - 1
        self.last_column = column - 1
        # Set print area
        self.worksheet.print_area(0, 0, self.last_row, self.last_column)
        # After set print area, we need to re-set default margin into 0
        self.worksheet.set_margins(0, 0, 0, 0)
        # Default hide printed gridlines only.
        # If you want to hide screen and printed gridlines,
        # please use "worksheet.hide_gridlines(2)"
        self.worksheet.hide_gridlines()

        # This setting is used for print the sheet. At here we know exactly how
        # many page inside this sheet, so that we can apply the setting for this
        # sheet to ensure it prints correctly.
        # Default, only one page is exported in one sheet. Only when we export
        # multiple page in one sheet, we must fit to page
        no_horizontal_pages = 1
        no_vertical_pages = 1
        if self.export_one_sheet:
            no_horizontal_pages = self.no_horizontal_pages
            no_vertical_pages = self.no_vertical_pages
        self.worksheet.fit_to_pages(no_vertical_pages, no_horizontal_pages)

    def build_grid(self, page):
        """Build grid layout"""
        # Re-set value
        self.column_width = self.worksheet.original_col_width
        self.column_pixel = self.worksheet.default_col_pixels
        self.row_height = self.worksheet.original_row_height
        self.row_pixel = self.worksheet.default_row_pixels
        self.x_grid_layout = []
        self.y_grid_layout = []
        self.x_grid_layout_map = []
        self.y_grid_layout_map = []
        self.box_trace = []
        self.overlapped_trace_arr = []
        self.box_trace = []
        # We will generate grid layout
        self.get_page_layout(page)
        # Base on x and y position to set
        # width, height for column, row in grid layout
        # and store column, row position
        row = 0
        column = 0
        previous_x = 0
        previous_y = 0
        for i in self.x_grid_layout:
            j = i - previous_x
            column_width = self._pixel_to_column_width(j)
            self.worksheet.set_column(column, column, column_width)
            x_map = {
                'value': i,
                'column': column + 1
            }
            self.x_grid_layout_map.append(x_map)
            previous_x = i
            column += 1
        for i in self.y_grid_layout:
            j = i - previous_y
            row_height = j * self.row_height / self.row_pixel
            self.worksheet.set_row(row, row_height)
            y_map = {
                'value': i,
                'height': row_height,
                'row': row + 1
            }
            self.y_grid_layout_map.append(y_map)
            previous_y = i
            row += 1
        if row > 0 and column > 0:
            self.setup_page(row, column)

    @classmethod
    def _pixel_to_column_width(cls, pixel):
        """
        Translate from pixel (scaled to 96 dpi) to column width in excel

        Parameters
        ----------
        pixel : float
            Input pixel

        Returns
        -------
        float
            column width which we can call worksheet.set_column

        Examples
        --------
        >>> column_width = self._pixel_to_column_width(pixel)
        >>> worksheet.set_column(column_start, column_end, column_width)

        """
        return pixel / cls._column_width_per_pixel_ratio(pixel)

    @classmethod
    def _column_width_per_pixel_ratio(cls, pixel):
        """
        Get ratio of width per pixel in excel. In excel, the translation
        between column width and pixel are not the constant value. It is
        one curve. After calculation, the curve is one 6 polynomial curve
        following is discrete data. The equation are interpolated from
        the discrete
            Pixel   Ratio
            64      7.591933571
            109     7.42506812
            210     7.169682485
            246     7.144931746
            339     7.105428631
            397     7.089285714
            440     7.080785323
            488     7.072463768
            537     7.065789474
            628     7.056179775
            708     7.049686349
            785     7.044781477
            843     7.042018211
            912     7.038666358
            953     7.036845603
            994     7.035175879
            1075    7.03257883

        When the pixel > 1100, this function will return default value
        7.031899252 because when pixel greater, the ratio are the same

        Parameters
        ----------
        pixel : float
            input pixel value

        Returns
        -------
        float
            Ratio width per pixel

        """

        if pixel > 1100:
            return 7.031899252

        return 8.0189013920533192e+000 \
            + -8.2797089967432801e-003 * (pixel**1) \
            + 3.0335602961293948e-005 * (pixel**2) \
            + -5.8159565539538695e-008 * (pixel**3) \
            + 6.0532510526859907e-011 * (pixel**4) \
            + -3.2386125538946733e-014 * (pixel**5) \
            + 6.9745071535767235e-018 * (pixel**6)
