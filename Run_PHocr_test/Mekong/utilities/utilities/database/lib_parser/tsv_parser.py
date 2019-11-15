# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Updated by:       Phung Dinh Tai
# Description:      Define base class for a tsv file parser
import codecs
from abc import ABCMeta, abstractmethod
from file_parser import FileParser


class TsvParser(FileParser):

    __metaclass__ = ABCMeta

    def __init__(self, header_line=0, **kwargs):
        self.header_line = header_line
        super(TsvParser, self).__init__(**kwargs)
        self.lines = []
        self.meta_headers = []
        self.meta_mappings = {}
        self.headers = []
        self.headers_check_list = []
        self.list_labels = []
        self.line_mappings = {}
        self.column_mappings = {}
        # Because user can open and edit file with option "Quoted field as text" so
        # these are list characters will be ignore when update history data
        self.list_strip = ' "\n'

    # Pre-process data
    def pre_process(self):
        # Initial attributes
        self.set_up_attributes()

        # Read raw data
        self.read_lines()

        # Create mappings
        self.create_mappings()

    @abstractmethod
    def set_up_attributes(self):
        pass

    # Pre-process to load raw data
    def read_lines(self):
        my_file = codecs.open(filename=self.input_file, mode="r", encoding='utf-8')
        lines = my_file.readlines()
        for line in lines:
            self.lines.append(line.split("\t"))

    def create_mappings(self):
        # Create meta data header mapping
        for header in self.meta_headers:
            for i in range(0, len(self.lines)):
                line_data = self.lines[i].strip(self.list_strip)
                if line_data[0] == header:
                    self.meta_mappings[header] = i

        # Create column mapping
        header_line_data = self.lines[self.header_line]
        for i in range(0, len(header_line_data)):
            header = header_line_data[i].strip(self.list_strip)
            if header in self.headers_check_list:
                self.column_mappings[header] = i
                self.headers.append(header)

        # Create line mapping
        for i in range(self.header_line+1, len(self.lines)):
            line_data = self.lines[i]
            label = line_data[0].strip(self.list_strip)
            self.line_mappings[label] = i
            self.list_labels.append(label)

    def get_line_data(self, label):
        return self.lines[self.line_mappings[label]]

    def get_cell_data(self, label, header):
        line_data = self.get_line_data(label=label)
        col_idx = self.column_mappings[header]
        return line_data[col_idx].strip(self.list_strip)

    def get_meta_data(self, meta_header):
        line_data = self.lines[self.meta_mappings[meta_header]]
        if len(line_data) == 1:
            return None
        else:
            return line_data[1]

    def load_meta_data(self):
        self.meta_data = {}
        for i in range(0, self.header_line):
            line_data = self.lines[i].strip(self.list_strip)
            if not line_data:
                continue
            meta_header = line_data[0].strip(self.list_strip)
            if meta_header in self.meta_headers:
                if len(line_data) < 2:
                    meta_value = None
                else:
                    meta_value = line_data[1]
                self.meta_data[meta_header] = meta_value

    def load_data(self):
        for header in self.headers:
            self.data[header] = {}
            for test_name in self.list_labels:
                if test_name:
                    self.data[header][test_name] = self.get_cell_data(label=test_name, header=header)

    def handle_data(self):
        # Re-type data
        for header in self.data:
            data = self.data[header]
            data_type = self.get_header_type(header=header)
            for test_name in data:
                data[test_name] = self.correct_value_type(value_string=data[test_name],
                                                          value_type=data_type)

    @staticmethod
    def correct_value_type(value_string, value_type):
        if (not value_string) and ((value_type is int) or (value_type is float)):
            return None
        if value_type is str:
            return str(value_string)
        elif value_type is bool:
            if value_string.lower() == "x":
                return True
            else:
                return False
        elif value_type is int:
            return int(value_string)
        elif value_type is float:
            return float(value_string)
        elif value_type is list:
            return value_string.split(",")
        elif value_type is unicode:
            if type(value_string) is unicode:
                return value_string
            else:
                return str(value_string)
        else:
            raise Exception("Value type {0} is not defined".format(value_type))

    @abstractmethod
    def get_header_type(self, header):
        pass
