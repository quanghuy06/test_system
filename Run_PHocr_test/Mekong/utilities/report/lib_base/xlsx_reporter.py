# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/07/2018
# Updated by:       Phung Dinh Tai
# Description:      Define base class for a reporter
import xlsxwriter
from abc import ABCMeta, abstractmethod
from report.lib_base.reporter import Reporter
from report.lib_base.cell_format import COLH
from report.lib_base.cell_format import Color, Align


class XlsxReporter(Reporter):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(XlsxReporter, self).__init__(**kwargs)
        # Create work book
        self.book = None
        self.line_mapping = {}
        self.column_mapping = {}

    def do_work(self):
        # Collect data
        self.collect_data()

        # Initial workbook
        self.book = xlsxwriter.Workbook(self.output_file)

        # Add sheets
        self.add_sheets()

        # Close work book
        self.book.close()

    @abstractmethod
    def add_sheets(self):
        pass

    # Calculate accuracy
    @staticmethod
    def calculate_accuracy(error, total):
        if total == 0:
            return 0
        return (float(total) - float(error)) * 100 / float(total)

    @staticmethod
    def write_cell(sheet, line, column, value, cell_format):
        """
        Write data to a cell of the work sheet

        Parameters
        ----------
        sheet: WorkSheet
            Sheet to write data
        line: int
            Index of line to write data
        column: int
            Index of column to write data
        value: str/int/float
            Data value to write to cell
        cell_format: Format
            Format of writing cell

        Returns
        -------
        None

        """
        sheet.write(line, column, value, cell_format)

    def write_line(self, sheet, line, value_array, cell_format, start_position=0, start_value=0,
                   num_elements=None):
        """
        Write a line to excel sheet where all cells use the same format

        Parameters
        ----------
        sheet: WorkSheet
            Sheet to write data
        line: int
            Line number to write data
        value_array: list
            List of cell data to write to line
        cell_format: Format
            Format for all cells on the line
        start_position: int
            Index of the cell to start writing
        start_value: int
            Index of cell to start writing in input list cells
        num_elements: int
            Number of elements to write when start_value is defined

        Returns
        -------
        None

        """
        if not num_elements:
            num_elements = len(value_array) - start_value

        for i in range(0, num_elements):
            self.write_cell(sheet=sheet, line=line, column=start_position + i,
                            value=value_array[start_value + i], cell_format=cell_format)

    def write_line_multi_format(self, sheet, line, values, formats, start_position=0):
        if len(values) != len(formats):
            raise Exception("Wrong formats line {0}".format(",".join(values)))
        for i in range(0, len(values)):
            self.write_cell(sheet=sheet, line=line, column=start_position + i, value=values[i],
                            cell_format=formats[i])

    def get_cell_format(self, align="left", font="Arial", font_size=10, font_color=None,
                        wrap_text=False, set_border=False, num_format=None, bg_color=None,
                        set_bold=False):
        fm = self.book.add_format()
        fm.set_align(alignment=align)
        fm.set_font(font_name=font)
        fm.set_font_size(font_size=font_size)
        if wrap_text:
            fm.set_text_wrap()
        if set_border:
            fm.set_border()
        if set_bold:
            fm.set_bold()
        if num_format:
            fm.set_num_format(num_format=num_format)
        if font_color:
            fm.set_color(font_color=font_color)
        if bg_color:
            fm.set_bg_color(bg_color=bg_color)
        return fm

    @staticmethod
    def get_cell_str(line_idx, col_idx):
        return "{0}{1}".format(COLH[col_idx], line_idx+1)

    def get_condition_formula(self, sheet, column, line_start, line_end, value):
        range_start = self.get_cell_str(line_idx=line_start, col_idx=column)
        range_end = self.get_cell_str(line_idx=line_end, col_idx=column)
        return "\'{sheet_name}\'!{range_start}:{range_end},{value}".format(sheet_name=sheet,
                                                                           range_start=range_start,
                                                                           range_end=range_end,
                                                                           value=value)

    def get_range_formula(self, sheet, column, line_start, line_end):
        range_start = self.get_cell_str(line_idx=line_start, col_idx=column)
        range_end = self.get_cell_str(line_idx=line_end, col_idx=column)
        return "\'{sheet_name}\'!{range_start}:{range_end}".format(sheet_name=sheet,
                                                                   range_start=range_start,
                                                                   range_end=range_end)

    @staticmethod
    def get_accuracy_formula(errors_cell, total_cell):
        return "=1-{errors}/{total}".format(errors=errors_cell, total=total_cell)

    @staticmethod
    def get_count_formula(conditions_string):
        return "=SUM(COUNTIFS({conditions}))".format(conditions=conditions_string)

    @staticmethod
    def get_sum_formula(range_string, conditions_string):
        return "=SUM(SUMIFS({range},{conditions}))".format(range=range_string,
                                                           conditions=conditions_string)

    @staticmethod
    def get_variance_formula(first_cell, second_cell):
        return "={first}-{second}".format(first=first_cell, second=second_cell)

    def add_format_for_variant_cell(self, worksheet, cell, is_increase_is_positive, in_percent):
        if is_increase_is_positive:
            positive_criteria = ">"
            negative_criteria = "<"
        else:
            positive_criteria = "<"
            negative_criteria = ">"

        worksheet.conditional_format(cell, {
            'type': 'cell',
            'criteria': positive_criteria,
            'value': 0,
            'format': self.get_format_for_variant(True, in_percent)
        })

        worksheet.conditional_format(cell, {
            'type': 'cell',
            'criteria': negative_criteria,
            'value': 0,
            'format': self.get_format_for_variant(False, in_percent)
        })

    def get_format_for_variant(self, is_positive, percent_format):
        positive_acc_format_in_percent = self.get_cell_format(set_border=True,
                                                              align=Align.RIGHT,
                                                              num_format='0.00%',
                                                              font_color=Color.GREEN,
                                                              bg_color=Color.LIGHT_GREEN)
        negative_acc_format_in_percent = self.get_cell_format(set_border=True,
                                                              align=Align.RIGHT,
                                                              font_color=Color.RED,
                                                              num_format='0.00%',
                                                              bg_color=Color.LIGHT_ORANGE)
        positive_acc_format_in_number = self.get_cell_format(set_border=True,
                                                             align=Align.RIGHT,
                                                             font_color=Color.GREEN,
                                                             num_format='#,##0',
                                                             bg_color=Color.LIGHT_GREEN)
        negative_acc_format_in_number = self.get_cell_format(set_border=True,
                                                             align=Align.RIGHT,
                                                             font_color=Color.RED,
                                                             num_format='#,##0',
                                                             bg_color=Color.LIGHT_ORANGE)
        if percent_format:
            if is_positive:
                return positive_acc_format_in_percent
            else:
                return negative_acc_format_in_percent
        else:
            if is_positive:
                return positive_acc_format_in_number
            else:
                return negative_acc_format_in_number

    def add_format_for_negative_cell_by_value(self, worksheet, cell, value,
                                              is_increase_is_negative,
                                              in_percent):
        """
        Add format for cell with condition is cell value

        Parameters
        ----------
        worksheet: worksheet working on.
        cell: current cell
        value: specific value
        in_percent

        Returns
        -------

        """
        if is_increase_is_negative:
            negative_criteria = ">"
            positive_criteria = "<"
        else:
            negative_criteria = "<"
            positive_criteria = ">"

        worksheet.conditional_format(cell, {
            'type': 'cell',
            'criteria': negative_criteria,
            'value': value,
            'format': self.get_format_for_negative_cell_by_value(False, in_percent)
        })
        worksheet.conditional_format(cell, {
            'type': 'cell',
            'criteria': positive_criteria,
            'value': value,
            'format': self.get_format_for_negative_cell_by_value(True,
                                                                 in_percent)
        })

    def get_format_for_negative_cell_by_value(self, is_positive, percent_format):
        negative_format_in_percent = self.get_cell_format(set_border=True,
                                                          align=Align.RIGHT,
                                                          font_color=Color.RED,
                                                          num_format='0.00%')
        positive_format_in_percent = self.get_cell_format(set_border=True,
                                                          align=Align.RIGHT,
                                                          font_color=Color.BLACK,
                                                          num_format='0.00%')
        negative_format_in_number = self.get_cell_format(set_border=True,
                                                         align=Align.RIGHT,
                                                         font_color=Color.RED,
                                                         num_format='#,##0')

        positive_format_in_number = self.get_cell_format(set_border=True,
                                                         align=Align.RIGHT,
                                                         font_color=Color.BLACK,
                                                         num_format='#,##0')
        if percent_format:
            if is_positive:
                return positive_format_in_percent
            else:
                return negative_format_in_percent
        else:
            if is_positive:
                return positive_format_in_number
            else:
                return negative_format_in_number
