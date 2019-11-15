# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from phocr_shared.shared import Pixel
from phocr_shared.box_attribute import BoxAttribute


class TableAttribute(BoxAttribute):
    def __init__(
            self, dpi, num_rows, num_cols, x, y, w, h,
            column_width_arr, column_height_arr, table_paras, style=None):
        super(TableAttribute, self).__init__(dpi, x, y, w, h)
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.column_width_arr = column_width_arr
        self.column_height_arr = column_height_arr
        self.table_paras = table_paras
        self.style = style

    def get_column_width_at_index(self, index):
        return Pixel(self.column_width_arr[index], self._dpi.horizontal_resolution).twips

    def get_row_height_at_index(self, index):
        return Pixel(self.column_height_arr[index], self._dpi.vertical_resolution).twips
