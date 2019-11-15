# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
This module will process problems relating to table
"""

from pptx.oxml.xmlchemy import OxmlElement
from phocr_shared.shared import Pt


class TableProcessing(object):
    """
    This class will process problems relating to table
    """

    def SubElement(self, parent, tagname, **kwargs):
        element = OxmlElement(tagname)
        kwargs = sorted(kwargs.items())
        element.attrib.update(kwargs)
        parent.append(element)
        return element

    def set_fill_for_cell(self, cell, missing_edge_xml, border_width='12700'):
        """
        This function will set border for cell base on xml information

        Parameters
        ----------
        cell : Cell
            Instance of cell object in pptx library
        start_row_idx : int
            Started row index
        end_row_idx : int
            Ended row index
        col_idx : int
            Column index

        Returns
        -------

        """

        tcPr = cell._tc.get_or_add_tcPr()

        ln_l = self.SubElement(tcPr,
                               'a:lnL',
                               w=border_width,
                               cap='flat',
                               cmpd='sng',
                               algn='ctr')
        if missing_edge_xml.left_border:
            _ = self.SubElement(ln_l, 'a:noFill')
        else:
            fill_l = self.SubElement(ln_l, 'a:solidFill')
            _ = self.SubElement(fill_l, 'a:schemeClr', val='tx1')
        _ = self.SubElement(ln_l, 'a:prstDash', val='solid')
        _ = self.SubElement(ln_l, 'a:round')
        _ = self.SubElement(ln_l, 'a:headEnd', type='none', w='med', len='med')
        _ = self.SubElement(ln_l, 'a:tailEnd', type='none', w='med', len='med')

        ln_r = self.SubElement(tcPr,
                               'a:lnR',
                               w=border_width,
                               cap='flat',
                               cmpd='sng',
                               algn='ctr')
        if missing_edge_xml.right_border:
            _ = self.SubElement(ln_r, 'a:noFill')
        else:
            fill_r = self.SubElement(ln_r, 'a:solidFill')
            _ = self.SubElement(fill_r, 'a:schemeClr', val='tx1')
        _ = self.SubElement(ln_r, 'a:prstDash', val='solid')
        _ = self.SubElement(ln_r, 'a:round')
        _ = self.SubElement(ln_r, 'a:headEnd', type='none', w='med', len='med')
        _ = self.SubElement(ln_r, 'a:tailEnd', type='none', w='med', len='med')

        ln_t = self.SubElement(tcPr,
                               'a:lnT',
                               w=border_width,
                               cap='flat',
                               cmpd='sng',
                               algn='ctr')
        if missing_edge_xml.top_border:
            _ = self.SubElement(ln_t, 'a:noFill')
        else:
            fill_t = self.SubElement(ln_t, 'a:solidFill')
            _ = self.SubElement(fill_t, 'a:schemeClr', val='tx1')
        _ = self.SubElement(ln_t, 'a:prstDash', val='solid')
        _ = self.SubElement(ln_t, 'a:round')
        _ = self.SubElement(ln_t, 'a:headEnd', type='none', w='med', len='med')
        _ = self.SubElement(ln_t, 'a:tailEnd', type='none', w='med', len='med')

        ln_b = self.SubElement(tcPr,
                               'a:lnB',
                               w=border_width,
                               cap='flat',
                               cmpd='sng',
                               algn='ctr')
        if missing_edge_xml.bottom_border:
            _ = self.SubElement(ln_b, 'a:noFill')
        else:
            fill_b = self.SubElement(ln_b, 'a:solidFill')
            _ = self.SubElement(fill_b, 'a:schemeClr', val='tx1')
        _ = self.SubElement(ln_b, 'a:prstDash', val='solid')
        _ = self.SubElement(ln_b, 'a:round')
        _ = self.SubElement(ln_b, 'a:headEnd', type='none', w='med', len='med')
        _ = self.SubElement(ln_b, 'a:tailEnd', type='none', w='med', len='med')

    # Merge cells vertically
    def merge_vertically_cells(
            self,
            table,
            start_row_idx,
            end_row_idx,
            col_idx):
        """
        This function will merge vertically cells

        Parameters
        ----------
        table : Table
            Instance of table object in pptx library
        start_row_idx : int
            Started row index
        end_row_idx : int
            Ended row index
        col_idx : int
            Column index

        Returns
        -------

        """

        row_count = end_row_idx - start_row_idx + 1
        column_cells = [r.cells[col_idx] for r in table.rows][start_row_idx:]
        column_cells[0]._tc.set('rowSpan', str(row_count))
        for c in column_cells[1:]:
            c._tc.set('vMerge', '1')

    # Merge cells horizontally
    def merge_horizontally_cells(
            self,
            table,
            row_idx,
            start_col_idx,
            end_col_idx):
        """
        This function will merge horizontally cells

        Parameters
        ----------
        table : Table
            Instance of table object in pptx library
        row_idx : int
            Row index
        start_col_idx : int
            Started column index
        end_col_idx : int
            Ended column index

        Returns
        -------

        """

        col_count = end_col_idx - start_col_idx + 1
        row_cells = \
            [c for c in table.rows[row_idx].cells][start_col_idx:end_col_idx]
        row_cells[0]._tc.set('gridSpan', str(col_count))
        for c in row_cells[1:]:
            c._tc.set('hMerge', '1')

    # The workaround function to merge cells in a table
    def merge_cells(self, table, start_row_idx, end_row_idx,
                   start_col_idx, end_col_idx):
        """
        This function will merge row and cell from start to end

        Parameters
        ----------
        table : Table
            Instance of table object in pptx library
        start_row_idx : int
            Started row index
        end_row_idx : int
            Ended row index
        start_col_idx : int
            Started column index
        end_col_idx : int
            Ended column index

        Returns
        -------

        """

        for col_idx in range(start_col_idx, end_col_idx + 1):
            self.merge_vertically_cells(
                table,
                start_row_idx,
                end_row_idx,
                col_idx)
        for row_idx in range(start_row_idx, end_row_idx + 1):
            self.merge_horizontally_cells(
                table,
                row_idx,
                start_col_idx,
                end_col_idx)

    # Clear the default Font (Calibri) and Font size (18 Pt) inside Table Cell.
    def clear_table_default(self, table, num_rows, num_columns):
        """
        This function will clear default style of table in pptx library

        Parameters
        ----------
        table : Table
            Instance of table object in pptx library
        num_rows : int
            The number of rows in table
        num_columns : int
            The number of columns in table

        Returns
        -------

        """

        for i in range(num_rows):
            for j in range(num_columns):
                tb_cell = table.cell(i, j)
                tf_cell = tb_cell.text_frame
                tf_cell.clear()
                para = tf_cell.paragraphs[0]
                run = para.add_run()
                run.text = ' '
                run.font.size = Pt(1)
