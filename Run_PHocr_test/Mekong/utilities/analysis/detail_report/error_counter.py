# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      16/05/2017
# Last update:      16/05/2107
# Description:      Compare bounding box 2 files

from data_parser import TextLayoutParser

class ErrorData:
    # Initial class
    def __init__(self):
        self.correct_list = []
        self.replace_list = []
        self.insert_list = []
        self.delete_list = []
        self.total_elements = 0

    # @return: List string
    def GetCorrectList(self):
        result = []
        for element in self.correct_list:
            result.append(element.content)
        return result

    # @return: List string
    def GetInsertList(self):
        result = []
        for element in self.insert_list:
            result.append(element.content)
        return result

    # @return: List string
    def GetDeleteList(self):
        result = []
        for element in self.delete_list:
            result.append(element.content)
        return result

    # @return: 2-D array, [<src_element>,<dest_element>]
    def GetReplaceList(self):
        result = []
        for element in self.replace_list:
            result.append([element.content, element.replace])
        return result

class ErrorCounter:
    # Initial
    # This compare source file vs destination file
    def __init__(self, src_file, dest_file):
        # Path to layout text files
        self.src = src_file
        self.dest = dest_file
        # Initial text layout parsers
        self.src_parser = TextLayoutParser(src_file)
        self.dest_parser = TextLayoutParser(dest_file)
        # Word data
        self.word_data = ErrorData()
        self.src_word_list = []
        self.dest_word_list = []
        self.word_counted = False
        # Character data
        self.char_data = ErrorData()
        self.src_char_list = []
        self.dest_char_list = []
        self.char_counted = False

    def WordCount(self):
        self.src_word_list = self.src_parser.GetWordList()
        self.dest_word_list = self.dest_parser.GetWordList()
        self.word_data.total_elements = len(self.dest_word_list)
        # Get list of: correct, replace and insert
        for sword in self.src_word_list:
            founded = False

            for dword in self.dest_word_list:
                if sword.IsSamePlace(dword):
                    founded = True
                    if sword.content == dword.content:
                        # Correct
                        self.word_data.correct_list.append(sword)
                    else:
                        # Replace error
                        sword.replace = dword.content
                        self.word_data.replace_list.append(sword)
                    break

            if not founded:
                # Insert error
                self.word_data.insert_list.append(sword)

        # Get list of: delete
        for dword in self.dest_word_list:
            founded = False

            for sword in self.src_word_list:
                if dword.IsSamePlace(sword):
                    founded = True
                    break

            if not founded:
                # Delete error
                self.word_data.delete_list.append(dword)
        self.word_counted = True

    def CharCount(self):
        self.src_char_list = self.src_parser.GetCharacterList()
        self.dest_char_list = self.dest_parser.GetCharacterList()
        self.char_data.total_elements = len(self.dest_char_list)
        # Get list of: correct, replace and insert
        for schar in self.src_char_list:
            founded = False

            for dchar in self.dest_char_list:
                if schar.IsSamePlace(dchar):
                    founded = True
                    if schar.content == dchar.content:
                        # Correct
                        self.char_data.correct_list.append(schar)
                    else:
                        # Replace error
                        schar.replace = dchar.content
                        self.char_data.replace_list.append(schar)
                    break

            if not founded:
                # Insert error
                self.char_data.insert_list.append(schar)

        # Get list of: delete
        for dchar in self.dest_char_list:
            founded = False

            for schar in self.src_char_list:
                if dchar.IsSamePlace(schar):
                    founded = True
                    break

            if not founded:
                # Delete error
                self.char_data.delete_list.append(dchar)
        self.char_counted = True

    def Count(self):
        self.WordCount()
        self.CharCount()

    def GetWordData(self):
        if not self.word_counted:
            self.WordCount()
        return self.word_data

    def GetCharData(self):
        if not self.char_counted:
            self.CharCount()
        return self.char_data
