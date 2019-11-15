# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      12/07/2016
# Last update:      12/07/2107
# Description:      This script define some common functions that used for post integration process

# Accuracy and performance information file structure
#     Product,<value>
#     Version,<value>
#     Test case ID, Time execute, Total characters, Insert errors, Replace errors, Delete errors

# Output of parse_info(): Json object
from configs.database import SpecKeys
from database.lib_base.test_case_manager import TestCaseManager


class CsvKeys:
    PRODUCT = "product"
    VERSION = "version"
    TEST_ID = "test case id"
    TIME = "time execute"
    TOTAL_CHARS = "total characters"
    ERR_INSERT = "insert errors"
    ERR_REPLACE = "replace errors"
    ERR_DELETE = "delete errors"
    TOTAL_ERRORS = "total errors"


class AccAndPermParser:

    def __init__(self, file_path):
        self.file_path = file_path
        self.id_idx = -1
        self.time_idx = -1
        self.char_idx = -1
        self.insert_idx = -1
        self.replace_idx = -1
        self.delete_idx = -1
        self.total_errors_idx = -1
        self.strip_chars = [' ', '\n', '"', '\r', '\t']

    def strip_(self, string):
        start_index = 0
        str_len = len(string)
        end_index = str_len
        for i in range(0, str_len):
            if string[i] in self.strip_chars:
                start_index += 1
            else:
                break
        for i in range(str_len - 1, -1, -1):
            if string[i] in self.strip_chars:
                end_index -= 1
            else:
                break
        return string[start_index:end_index]

    def get_product(self):
        fp = open(self.file_path, "r")
        for i, line in enumerate(fp):
            split_str = line.split("\t")

            # This prevents save file using office software, that will put string into ""
            num_fields = len(split_str)
            for j in range(0, num_fields):
                split_str[j] = self.strip_(split_str[j])

            if split_str[0].lower() == CsvKeys.PRODUCT:
                fp.close()
                return split_str[1]
        fp.close()
        return ""

    def get_version(self):
        fp = open(self.file_path, "r")
        for i, line in enumerate(fp):
            split_str = line.split("\t")

            # This prevents save file using office software, that will put string into ""
            num_fields = len(split_str)
            for j in range(0, num_fields):
                split_str[j] = split_str[j].strip('"')

            if split_str[0].lower() == CsvKeys.VERSION:
                fp.close()
                return int(split_str[1])
        fp.close()
        return -1

    # Try to find the header line and get index of each information
    def parse_index(self):
        fp = open(self.file_path, "r")
        for i, line in enumerate(fp):
            line = line.strip()
            split_str = line.split("\t")

            # This prevents save file using office software, that will put string into ""
            num_fields = len(split_str)
            for j in range(0, num_fields):
                split_str[j] = split_str[j].strip('"')

            isHeaderLine = False
            for k in range(0, num_fields):
                if split_str[k].lower() == CsvKeys.TEST_ID:
                    isHeaderLine = True
                    self.id_idx = k
                if split_str[k].lower() == CsvKeys.TIME:
                    self.time_idx = k
                if split_str[k].lower() == CsvKeys.TOTAL_CHARS:
                    self.char_idx = k
                if split_str[k].lower() == CsvKeys.ERR_DELETE:
                    self.delete_idx = k
                if split_str[k].lower() == CsvKeys.ERR_INSERT:
                    self.insert_idx = k
                if split_str[k].lower() == CsvKeys.ERR_REPLACE:
                    self.replace_idx = k
                if split_str[k].lower() == CsvKeys.TOTAL_ERRORS:
                    self.total_errors_idx = k

            if isHeaderLine:
                return

    def parse_line(self, line):
        info = {}
        split_str = line.split("\t")

        # This prevents save file using office software, that will put string into ""
        num_fields = len(split_str)
        for i in range(0, num_fields):
            split_str[i] = split_str[i].strip('"')
            split_str[i] = split_str[i].strip('\n')

        test_id = None
        if self.id_idx >= 0 and split_str[self.id_idx]:
            test_id = split_str[self.id_idx]
        else:
            return (None, None)
        if self.time_idx >= 0 and split_str[self.time_idx]:
            info[SpecKeys.History.PERFORMANCE] = float(split_str[self.time_idx])
        if self.char_idx >= 0 and split_str[self.char_idx]:
            info[SpecKeys.History.TOTAL_CHARACTER] = int(split_str[self.char_idx])
        if self.insert_idx >= 0 and split_str[self.insert_idx]:
            info[SpecKeys.History.ERR_INSERT] = int(split_str[self.insert_idx])
        if self.replace_idx >= 0 and split_str[self.replace_idx]:
            info[SpecKeys.History.ERR_REPLACE] = int(split_str[self.replace_idx])
        if self.delete_idx >= 0 and split_str[self.delete_idx]:
            info[SpecKeys.History.ERR_DELETE] = int(split_str[self.delete_idx])
        if self.total_errors_idx >= 0 and split_str[self.total_errors_idx]:
            info[SpecKeys.History.TOTAL_ERRORS] = int(split_str[self.total_errors_idx])
        return (test_id, info)

    def parse_info(self):
        self.parse_index()
        all_info = {}
        test_case_manager = TestCaseManager()
        with open(self.file_path, "r") as myfile:
            for line in myfile.readlines():
                try:
                    test_id, info = self.parse_line(line)
                    if test_case_manager.is_test_case_on_db(test_id):
                        all_info[test_id] = info
                except:
                    pass
        myfile.close()
        return all_info
