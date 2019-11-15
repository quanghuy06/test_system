# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from __future__ import division

import warnings
warnings.filterwarnings('ignore', category=DeprecationWarning)

import os

import xlsx
from xlsx.common import Common
from xlsx.grid_layout_processing import GridLayoutProcessing
from phocr_shared.phocr_common import PHOcrCommon, TextDirection, DocumentType
from phocr_shared.logger import OCRLogLevel
from base_office_creator import BaseOfficeCreator


class XlsxCreator(BaseOfficeCreator):
    """Creator to generate .xlsx file"""

    def __init__(self, filename, language, debug, working_directory):
        """Constructor"""
        super(XlsxCreator, self).__init__(language, working_directory, debug)
        self.document_type = DocumentType.XLSX
        self.output_file = filename + ".xlsx"
        self.text_direction = TextDirection.LRTB

        # Layout processing
        self.layout_processing = None
        self.x_height = 0

        # Contain data for resolve conflict of merge range in worksheet
        self._merge_range_work_sheet = {}

        # Export in one sheet flag
        self.export_one_sheet = False

    @classmethod
    def convert_rgb_to_hex(cls, rgb):
        """Convert RGB to hex"""
        return '%02x%02x%02x' % rgb

    def convert_color_to_rgb(self, color):
        """Convert color to RGB"""
        red, green, blue = color.split(',')
        rgb = self.convert_rgb_to_hex((int(red), int(green), int(blue)))
        return rgb

    def set_space_after(self,
                        workbook,
                        word,
                        next_word=None,
                        result=None):
        """Set space-after"""
        if str(word.value[-1]) == '\xe3\x80\x82':  # Punctuation in Japanese
            return

        word_format = workbook.add_format()
        if word.font and len(word.font) > 0:
            word_format.set_font_name(word.font)
        if word.size and int(float(word.size)) > 0:
            word_format.set_font_size(int(float(word.size)))
        # Checking for font style of space
        if next_word is not None:
            # Checking for color space
            if word.color is not None:
                rgb = self.convert_color_to_rgb(word.color)
                word_format.set_font_hex_color('#' + str(rgb))
            if word.bold:
                word_format.set_bold(True)
            if word.italic:
                word_format.set_italic(True)
            # Checking for underline space
            if word.underline and next_word.underline:
                word_format.set_underline(True)
        # Add space
        result.append(word_format)
        num_spaces_after = max(next_word.spaces_before, 1)
        result.append(' ' * num_spaces_after)

    def generate_word(
            self,
            workbook,
            word,
            length=1,
            index=1,
            end_line=False,
            next_word=None,
            result=None):
        """Generate a word into MS Excel Document representation"""
        word_format = workbook.add_format()
        if word.highlight_color is not None:
            rgb = self.convert_color_to_rgb(word.highlight_color)
            word_format.set_bg_hex_color('#' + str(rgb))
        if word.color is not None:
            rgb = self.convert_color_to_rgb(word.color)
            word_format.set_font_hex_color('#' + str(rgb))
        if word.font and len(word.font) > 0:
            word_format.set_font_name(word.font)
        if word.size and int(float(word.size)) > 0:
            word_format.set_font_size(int(float(word.size)))
        if word.bold:
            word_format.set_bold(True)
        if word.italic:
            word_format.set_italic(True)
        if word.underline:
            word_format.set_underline(True)
        result.append(word_format)
        if end_line:
            result.append(word.value + '\n')
        else:
            result.append(word.value)
        if index < length:
            self.set_space_after(workbook, word, next_word, result)

    def generate_table(self, workbook, worksheet, table_obj):
        """Generate a table into MS Excel Document representation"""
        for row in table_obj.rows:
            for column in row.cells:
                (row_pos, column_pos, width_pos, height_pos) = \
                    self.layout_processing.get_cell_information(column)
                if row_pos == height_pos or column_pos == width_pos:
                    continue
                formatter = workbook.add_format({
                    'border_color': 'black',
                    'border': 1
                })
                if height_pos - 1 > row_pos or width_pos - 1 > column_pos:
                    self.merge_range(
                        worksheet,
                        row_pos, column_pos,
                        height_pos - 1, width_pos - 1,
                        '', formatter
                    )
                else:
                    worksheet.write_string(row_pos, column_pos, '', formatter)

                # Set background for the table cell
                self.set_cell_background(column, formatter)

                # Assign elements for the table cell
                for sub_carea in column.careas:
                    result = self.generate_carea_in_cell(workbook,
                                                         column,
                                                         sub_carea,
                                                         formatter)
                    result.append(formatter)
                    worksheet.write_rich_string(row_pos,
                                                column_pos,
                                                *result)
                for sub_table in column.tables:
                    self.generate_table(workbook, worksheet, sub_table)
                for sub_photo in column.photos:
                    if not sub_photo.intersect_with_text_in_table:
                        self.generate_photo(worksheet, sub_photo)
                self.get_missing_border(column, formatter)

    def set_cell_background(self, column_xml, formatter):
        """
        Set the background color for table cell having no word
        or just one paragraph
        If word in the paragraph or there are multi paragraphs in the cell,
        not set same background color for them because they might have
        different color

        Parameters
        ----------
        column_xml
        formatter

        Returns
        -------

        """
        cell_background_color = column_xml.highlight_color
        if cell_background_color is not None:
            cell_bg_hex_color = PHOcrCommon.get_color(cell_background_color)
            formatter.set_bg_color(str(cell_bg_hex_color))

        count = 0
        for carea_xml in column_xml.careas:
            for par_xml in carea_xml.paragraphs:
                cell_background_color = par_xml.background_color
                count += 1

        if count == 1 and cell_background_color is not None:
            cell_bg_hex_color = PHOcrCommon.get_color(cell_background_color)
            formatter.set_bg_color(str(cell_bg_hex_color))

    @staticmethod
    def get_missing_border(missing_edge_xml, formatter):
        """Check to set border for cell of table"""
        if missing_edge_xml.left_border:
            formatter.set_left(0)
        else:
            formatter.set_left(1)
        if missing_edge_xml.right_border:
            formatter.set_right(0)
        else:
            formatter.set_right(1)
        if missing_edge_xml.top_border:
            formatter.set_top(0)
        else:
            formatter.set_top(1)
        if missing_edge_xml.bottom_border:
            formatter.set_bottom(0)
        else:
            formatter.set_bottom(1)

    def set_alignment_for_para_in_cell(self, column, paragraph, formatter):
        # Calculate horizontal alignment
        alignment = Common.define_alignment(paragraph, column)
        if alignment == 'left' or alignment == 'justify':
            distance = abs(paragraph.x - column.x)
            indent = int(
                round(distance / self.layout_processing.min_distance) / 2
            )
            if indent > 0:
                indent += 1
            formatter.set_indent(indent)
        formatter.set_align(alignment)

        # Calculate vertical alignment
        vertical_alignment = Common.define_valignment(paragraph, column)
        formatter.set_align(vertical_alignment)

    def generate_line_of_para_in_cell(
            self,
            workbook,
            paragraph,
            result,
            is_line_by_line=False):
        line_num = 1
        for line in paragraph.lines:
            index = 1
            for word in line.words:
                adding_end_line = False
                is_end_of_line = index == len(line.words)
                not_last_line = \
                    not (line_num == len(paragraph.lines) and
                         len(paragraph.lines) > 1)
                if is_line_by_line and is_end_of_line and not_last_line:
                    adding_end_line = True
                next_word = None
                if index < len(line.words):
                    next_word = line.words[index]
                self.generate_word(workbook,
                                   word,
                                   len(line.words),
                                   index,
                                   adding_end_line,
                                   next_word,
                                   result)
                index += 1
            line_num += 1

    def generate_carea_in_cell(self, workbook,
                               column, carea, formatter):
        """Generate text in cell of table"""
        result = []
        par_num = 1
        # Number of line will decide that whether or not wrap text
        # inside of cell
        number_of_lines = 0
        # Note: Re-calculate format for cell contain carea
        # Because formatter for cell, therefore, we can't calculate for
        # last paragraph, please re-calculate when cell contain one carea
        for paragraph in carea.paragraphs:
            number_of_lines += len(paragraph.lines)
            is_line_by_line = Common.is_line_by_line(paragraph,
                                                     column,
                                                     TextDirection.TBRL)
            if len(paragraph.lines) == 1 and \
                    par_num != len(carea.paragraphs) > 1:
                is_line_by_line = True
            self.set_alignment_for_para_in_cell(column, paragraph, formatter)

            self.generate_line_of_para_in_cell(workbook, paragraph,
                                               result, is_line_by_line)
            par_num += 1
        if number_of_lines > 1:
            formatter.set_text_wrap()
        return result

    def generate_line(self, workbook, line_obj):
        """Generate line"""
        result = []
        index = 1
        is_end_line = False
        for word in line_obj.words:
            next_word = None
            if index < len(line_obj.words):
                next_word = line_obj.words[index]
            else:
                # If last word in line
                is_end_line = True
            self.generate_word(workbook,
                               word,
                               line_obj.length(),
                               index,
                               is_end_line,
                               next_word,
                               result)
            index += 1
        return result

    def generate_carea(self, workbook, worksheet, carea_obj):
        """Generate a content area into MS Excel Document representation"""
        # Loop over each paragraph in content area
        for paragraph in carea_obj.paragraphs:
            # Loop over each line in paragraph
            for line in paragraph.lines:
                (is_ignored, row_height, row, column, width, height) = \
                    self.layout_processing.get_line_position(line)
                if is_ignored:
                    continue
                # Add data into cell
                result = self.generate_line(workbook, line)
                # Add format
                line_format = workbook.add_format()
                line_format.set_align('left')
                # if text is vertical, set line format is vertical text
                if carea_obj.writing_direction == TextDirection.LRTB:
                    line_format.set_rotation(270)
                if 0 < row_height <= self.layout_processing.row_height:
                    line_format.set_valign('vcenter')
                else:
                    line_format.set_valign('bottom')
                # In case language is Japanese or Chinese
                # and writing direction is from top to bottom
                if self.text_direction == TextDirection.TBRL:
                    # Use wrap text
                    line_format.set_text_wrap()
                if height - 1 > row or width - 1 > column:
                    self.merge_range(
                        worksheet,
                        row, column,
                        height - 1, width - 1,
                        '', line_format
                    )
                text_angle = int(line.text_angle)
                if text_angle != -1:  # If rotated
                    line_format.set_rotation(text_angle)
                result.append(line_format)
                worksheet.write_rich_string(row, column, *result)

    def generate_photo(self, worksheet, photo_obj):
        """Generate a photo into MS Excel Document representation"""
        # Only add photo if it is bigger than threshold
        if PHOcrCommon.is_photo_ok(photo_obj.h, photo_obj.w, self.x_height):
            # Find the nearest cell and offset too
            start_col, start_row, x_offset, y_offset = \
                self.layout_processing.find_containing_cell(photo_obj)

            # Set photo position offset with the nearest top-left cell
            # positioning= 3 mean that picture will don't move or size with cell
            absolute_photo_path = os.path.join(self.working_directory, photo_obj.path)
            worksheet.insert_image(
                start_row,
                start_col,
                absolute_photo_path,
                {
                    'x_offset': x_offset,
                    'y_offset': y_offset,
                    'positioning': 3
                }
            )

    def generate_page_layout(self, workbook, worksheet, page_obj):
        """Generate layout for page"""
        for table in page_obj.tables:
            self.generate_table(workbook, worksheet, table)
        for photo in page_obj.photos:
            if not photo.intersect_with_text_in_table:
                self.generate_photo(worksheet, photo)
        for carea in page_obj.careas:
            self.generate_carea(workbook, worksheet, carea)

    def generate_document(self, office_obj):
        # Create a workbook and add a worksheet.
        workbook = xlsx.Workbook(self.output_file)
        # Process for export excel document in only one sheet
        if self.export_one_sheet:
            office_obj.create_one_page()

        try:
            # Traverse each page
            for page in office_obj.pages:
                worksheet = workbook.add_worksheet()

                # Check to ignore empty page, we only create empty sheet
                if page.empty():
                    continue

                self.x_height = page.x_height
                # Call processor for grid layout
                self.layout_processing = GridLayoutProcessing(
                    worksheet,
                    self.export_one_sheet,
                    office_obj.number_horizontal_pages,
                    office_obj.number_vertical_pages,
                    self.debug
                )
                self.layout_processing.create_layout(page)

                # We'll generate layout of page basing on grid layout
                self.generate_page_layout(workbook, worksheet, page)
            # Save the file
            workbook.close()
        except Exception as ex:
            # Save the file
            workbook.close()

            # Logging error
            self.error_logger.log(
                OCRLogLevel.LOG_LEVEL_ERROR,
                'Error occurred. Arguments {0}.'.format(ex.args)
            )
            raise

    def merge_range(self,
                    worksheet,
                    start_row, start_column,
                    end_row, end_column,
                    data, formatter):
        """
        Merge range in worksheet, this function will check conflict before merge

        Parameters
        ----------
        worksheet
        start_row
        start_column
        end_row
        end_column
        data
        formatter

        Returns
        -------

        """

        # Checking conflict with merge range call before
        is_there_conflict = False
        if worksheet not in self._merge_range_work_sheet:
            self._merge_range_work_sheet[worksheet] = {}
        worksheet_merge_object = self._merge_range_work_sheet[worksheet]

        for row_index in range(start_row, end_row + 1):
            if row_index not in worksheet_merge_object:
                worksheet_merge_object[row_index] = {}
            row_object = worksheet_merge_object[row_index]
            for column_index in range(start_column, end_column + 1):
                if column_index not in row_object:
                    row_object[column_index] = True
                else:
                    is_there_conflict = True
                    break
            if is_there_conflict:
                break

        # If not conflict, merge input range
        if not is_there_conflict:
            worksheet.merge_range(
                start_row, start_column,
                end_row, end_column,
                data, formatter
            )
