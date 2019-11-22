# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created:     31/07/2017
# Last update:      03/08/2017
# Updated by:       Phung Dinh Tai
# Description:      This script is used to define class for files in pdf format comparison
import sys_path
sys_path.insert_sys_path()

import os
import filecmp
import traceback
from baseapi.file_access import remove_paths
from configs.compare_result import CompareResultConfig, CompareJsonKeys

class Flags:
    WRONG_TIMESTAMP = "Wrong timestamp format"
    CONTENT_CHANGE = "Content change"
    TIMESTAMP_CHANGE = "Timestamp changed"

# Key is parent tag to search
# Value is tags that will be replaced
TopTagSearches = {
    "x:xmpmeta" : ["xmp:CreateDate", "xmp:ModifyDate", "xmp:MetadataDate", "xmpMM:DocumentID", "xmpMM:InstanceID"]
}

BottomSearches = ["/ID", "/ModDate", "/CreationDate"]

TimestampTags = ["xmp:CreateDate", "xmp:ModifyDate", "xmp:MetadataDate", "/ModDate", "/CreationDate"]

def getStartTag(tag):
    return "<" + tag

def getFullStartTag(tag):
    return "<" + tag + ">"

def getEndTag(tag):
    return "</" + tag + ">"

def getEmptyTag(tag):
    return "<" + tag + "></" + tag + ">\n"

def getSpacesString (num):
    str = ""
    for i in range(0, num):
        str += " "
    return str

class ComparePdf:

    def __init__(self):
        self.title = CompareResultConfig.TITLE_CMP_PDFA

    def change_working_dir(self, working_dir):
        # Change current directory before run real test
        if not os.path.exists(working_dir):
            os.makedirs(working_dir)
        os.chdir(working_dir)

    def is_timestamp_tag(self, tag):
        if tag in TimestampTags:
            return True
        else:
            return False

    def get_tag_value(self, tag, line):
        tag = tag.strip()
        startTag = getFullStartTag(tag)
        endTag = getEndTag(tag)
        si = line.find(startTag) + len(startTag)
        ei = line.find(endTag)
        return line[si:ei]

    def get_tag_obj(self, tag, line):
        tag = tag.strip()
        str_len = len(line)
        si = line.find(tag) + len(tag)
        value_str = line[si:str_len]
        return value_str.strip()

    # 2017-08-03T08:15:50+07:00
    def check_timestamps_xml(self, str):
        try:
            str = str.strip()
            if len(str) != 25:
                return False
            str_split = str.split('T')
            # Parse date string
            date_str = str_split[0]
            date_split = date_str.split('-')
            for elm in date_split:
                int(elm)
            # Parse time string
            t_split = str_split[1].split('+')
            time_str = t_split[0]
            time_split = time_str.split(':')
            for elm in time_split:
                int(elm)
            # Parse time zone string
            tz_str = t_split[1]
            tz_split = tz_str.split(':')
            for elm in tz_split:
                int(elm)
            return True
        except:
            return False

    # (D:20170803081550+07'00)
    def check_timestamps_obj(self, str):
        try:
            str = str.strip()
            str_len = len(str)
            if str_len != 24:
                return False
            if str[0] != '(':
                return False
            if str[2] != ':':
                return False
            if str[str_len - 1] != ')':
                return False
            date_str = str[3:11]
            int(date_str)
            time_str = str[11:17]
            int(time_str)
            if str[17] != '+':
                return False
            tz_str = str[-6:str_len - 1]
            tz_split = tz_str.split('\'')
            for elm in tz_split:
                int(elm)
            return True
        except:
            return False

    def remove_time_stamps(self, input_file, output_file):
        with open(input_file, 'rb') as myfile:
            source = myfile.readlines()

        time_stamps_correct = True
        # Top search
        cnt_line = 0
        for line in source:
            for ptag in TopTagSearches:
                endTag = getEndTag(ptag)
                tags = []
                for elm in TopTagSearches[ptag]:
                    tags.append(elm)
                for tag in tags:
                    if tag in line:
                        # Check timestamp format
                        if self.is_timestamp_tag(tag):
                            timestamp = self.get_tag_value(tag, line)
                            if not self.check_timestamps_xml(timestamp):
                                time_stamps_correct = False
                        source[cnt_line] = getSpacesString(line.find('<')) + getEmptyTag(tag)
                        tags.remove(tag)
                if ((endTag in line) or (not tags)):
                    break
            cnt_line += 1
        myfile.close()
        # Bottom search
        cnt_line = len(source) - 1
        infos = []
        for elm in BottomSearches:
            infos.append(elm)
        for counter in range(cnt_line, -1, -1):
            line = source[counter]
            for info_tag in infos:
                if info_tag in line:
                    # Check timestamp format
                    if self.is_timestamp_tag(info_tag):
                        timestamp = self.get_tag_obj(info_tag, line)
                        if not self.check_timestamps_obj(timestamp):
                            time_stamps_correct = False
                    source[counter] = getSpacesString(line.find('/')) + info_tag + "\n"
                    infos.remove(info_tag)
            if (not infos) or ("endstream" in line):
                break
        # Write output file
        with open(output_file, "wb") as myfile:
            myfile.writelines(source)
        return time_stamps_correct

    def compare(self, src_file, dest_file, result_folder = None):
        src_file = os.path.abspath(src_file)
        dest_file = os.path.abspath(dest_file)
        curr_dir = os.getcwd()  # Directory run this scripts
        working_dir = 'e7968b1d-19c6-43d8-bc07-d203ab12a4be'
        result = {}
        result[CompareJsonKeys.FILE] = os.path.basename(src_file)
        result[CompareJsonKeys.TITLE] = self.title
        try:
            self.change_working_dir(working_dir)
            csf = "source.pdf"
            dsf = "destination.pdf"

            # Remove timestamps source file
            src_time_stamp_correct = self.remove_time_stamps(src_file, csf)

            # Remove timestamps destination file
            dest_timestamp_correct = self.remove_time_stamps(dest_file, dsf)

            info = list()
            if not src_time_stamp_correct:
                info.append(Flags.WRONG_TIMESTAMP)

            result[CompareJsonKeys.IS_CHANGE] = False

            is_timestamp_changed = \
                src_time_stamp_correct != dest_timestamp_correct
            if is_timestamp_changed:
                # Before and after
                result[CompareJsonKeys.IS_CHANGE] = True
                info.append(Flags.TIMESTAMP_CHANGE)

            is_content_changed = not filecmp.cmp(csf, dsf)
            if is_content_changed:
                result[CompareJsonKeys.IS_CHANGE] = True
                info.append(Flags.CONTENT_CHANGE)
            result[CompareJsonKeys.CONTENT] = ", ".join(info)

            return result
        except:
            tb = traceback.format_exc()
            return {
                CompareJsonKeys.IS_CHANGE : True,
                "Traceback": tb
            }
        finally:
            self.change_working_dir(curr_dir)
            remove_paths(working_dir)
