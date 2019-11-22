# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      16/05/2017
# Last update:      16/05/2107
# Description:      This generate report which perform difference of
#                   + output bounding box file vs reference file (change_data) or ground truth file (diff_data)
#                   + reference bounding box file vs ground truth file (master_data)

import os
from error_counter import ErrorCounter
from baseapi.excel_style import *

class BookInfo:
    DEFAULT_FILE = "ComparisonReport.xls"
    LAYOUT_SUFFIX = "_0.txt"
    class WordSheet:
        RAW = "Word-Raw"
        FREQ = "Word-Frequency"
    class CharSheet:
        RAW = "Character-Raw"
        FREQ = "Character-Frequency"

class TestCaseData:
    def __init__(self, filename = "", word_data = None, char_data = None):
        self.filename = filename
        self.word_data = word_data
        self.char_data = char_data

class DetailInformationReporter:
    # Initial
    def __init__(self, src_folder = None, dest_folder = None):
        # Path file
        self.src_folder = src_folder
        self.dest_folder = dest_folder

        # Error data
        self.data = []
        self.file_list = []

        # Data is processed or not
        self.processed = False

        # Initial work book
        self.workbook = xlwt.Workbook(encoding="utf-8")

    # Get file list
    def get_file_list(self):
        if not os.path.isdir(self.src_folder):
            print "{0} : No such folder or directory".format(self.src_folder)
            return
        # Get list files which will be compared
        for fname in os.listdir(self.src_folder):
            src_file = os.path.join(self.src_folder, fname)
            if os.path.isfile(src_file) and fname.endswith(BookInfo.LAYOUT_SUFFIX):
                dest_file = os.path.join(self.dest_folder, fname)
                if os.path.isfile(dest_file):
                    self.file_list.append([src_file, dest_file])
                else:
                    print "{0} : No such file or directory".format(dest_file)

    # Set file list from outside which user will collect manual
    def SetFileList(self, file_list):
        self.file_list = file_list

    # Process data
    def Process(self):
        # Get compare data
        count = 0
        total = len(self.file_list)
        for pair in self.file_list:
            test_name = os.path.basename(pair[0])
            test_name = test_name.replace(BookInfo.LAYOUT_SUFFIX, "")
            print "[{0}/{1}] {2}".format(count, total, test_name)
            counter = ErrorCounter(pair[0], pair[1])
            self.data.append(TestCaseData(os.path.basename(pair[0]), counter.GetWordData(), counter.GetCharData()))
            count += 1

        self.processed = True

    def add_raw_word_sheet(self):

        if not self.processed:
            self.Process()

        # Add sheet
        sheet = self.workbook.add_sheet(BookInfo.WordSheet.RAW)

        start_line = 0
        for element in self.data:
            # Each element is compare data for 1 test case
            line = start_line
            # Write test name
            test_name = element.filename.replace(BookInfo.LAYOUT_SUFFIX, "")
            sheet.write(line, 0, test_name, header_style_1)

            # Header
            sheet.write(line, 1, "Changed", header_style_1)
            sheet.write(line, 2, "Origin", header_style_1)
            sheet.write(line, 4, "Insert", header_style_2)
            sheet.write(line, 6, "Delete", header_style_2)

            # Replace errors
            replace_list = element.word_data.GetReplaceList()
            line = start_line
            for error in replace_list:
                line += 1
                sheet.write(line, 1, error[0], base_style_2)
                sheet.write(line, 2, error[1], base_style_2)

            # Insert errors
            insert_list = element.word_data.GetInsertList()
            line = start_line
            for word in insert_list:
                line += 1
                sheet.write(line, 4, word, base_style_2)

            # Delete errors
            delete_list = element.word_data.GetDeleteList()
            line = start_line
            for word in delete_list:
                line += 1
                sheet.write(line, 6, word, base_style_2)

            # New start line of next test case
            start_line += max(len(replace_list), len(insert_list), len(delete_list)) + 3

    def add_raw_char_sheet(self):

        if not self.processed:
            self.Process()

        # Add sheet
        sheet = self.workbook.add_sheet(BookInfo.CharSheet.RAW)

        start_line = 0
        for element in self.data:
            # Each element is compare data for 1 test case
            line = start_line
            # Write test name
            test_name = element.filename.replace(BookInfo.LAYOUT_SUFFIX, "")
            sheet.write(line, 0, test_name, header_style_1)

            # Header
            sheet.write(line, 1, "Changed", header_style_1)
            sheet.write(line, 2, "Origin", header_style_1)
            sheet.write(line, 4, "Insert", header_style_2)
            sheet.write(line, 6, "Delete", header_style_2)

            # Replace errors
            replace_list = element.char_data.GetReplaceList()
            line = start_line
            for error in replace_list:
                line += 1
                sheet.write(line, 1, error[0], base_style_2)
                sheet.write(line, 2, error[1], base_style_2)

            # Insert errors
            insert_list = element.char_data.GetInsertList()
            line = start_line
            for char in insert_list:
                line += 1
                sheet.write(line, 4, char, base_style_2)

            # Delete errors
            delete_list = element.char_data.GetDeleteList()
            line = start_line
            for char in delete_list:
                line += 1
                sheet.write(line, 6, char, base_style_2)

            # New start line of next test case
            start_line += max(len(replace_list), len(insert_list), len(delete_list)) + 3

    def save_file(self, file_name = None):
        if not file_name:
            file_name = BookInfo.DEFAULT_FILE
        self.workbook.save(file_name)

    def Report(self, file_name = None):
        if not self.processed:
            self.Process()
        self.add_raw_word_sheet()
        self.add_raw_char_sheet()
        self.save_file(file_name)


