# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      20/07/2017
# Last update:      01/08/2018
# Editor:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Description:      Parse tags information from tsv file
import sys_path
sys_path.insert_sys_path()

from configs.database import SpecHelper, SpecKeys


class TagsTsvParser:

    def __init__(self, tsv_file):
        self.file = tsv_file
        helper = SpecHelper()
        self.tag_list = helper.get_list_tags()
        # Initial column index
        for tag_name in self.tag_list:
            self.tag_list[tag_name]["columnidx"] = -1
        self.data = {}
        self.header_line_idx = -1
        self.component_col_idx = -1
        self.functionality_col_idx = -1

    def parse_index(self):
        fp = open(self.file, "r")
        for i, line in enumerate(fp):
            line = line.strip()
            split_str = line.split("\t")

            # This prevents save file using office software, that will put string into ""
            num_fields = len(split_str)
            for j in range(0, num_fields):
                split_str[j] = split_str[j].strip('"')

            num_fields = len(split_str)
            isHeaderLine = False
            if split_str[0].lower() == "test case id":
                isHeaderLine = True
                self.header_line_idx = i
            if isHeaderLine:
                for k in range(1, num_fields):
                    if split_str[k].lower() == SpecKeys.COMPONENT.lower():
                        self.component_col_idx = k
                        continue
                    if split_str[k].lower() == SpecKeys.FUNCTIONALITIES.lower():
                        self.functionality_col_idx = k
                        continue
                    for tag_name in self.tag_list:
                        if split_str[k].lower() == tag_name.lower():
                            self.tag_list[tag_name]["columnidx"] = k
                            break
        fp.close()

    def parse_data(self):
        fp = open(self.file, "r")
        for i, line in enumerate(fp):
            line = line.strip('\n')
            split_str = line.split("\t")

            # This prevents save file using office software, that will put string into ""
            num_fields = len(split_str)
            for j in range(0, num_fields):
                split_str[j] = split_str[j].strip('"')

            if i > self.header_line_idx:
                # Get test id
                test_id = split_str[0]
                self.data[test_id] = {}
                # Get component value
                if self.component_col_idx > 0:
                    self.data[test_id][SpecKeys.COMPONENT] = split_str[self.component_col_idx]
                # Get functionality value
                if self.functionality_col_idx > 0:
                    self.data[test_id][SpecKeys.FUNCTIONALITIES] = split_str[self.functionality_col_idx]
                # Get tags
                for tag_name in self.tag_list:
                    tag_idx = self.tag_list[tag_name]["columnidx"]
                    if tag_idx >= 1:
                        self.data[test_id][tag_name] = split_str[tag_idx]
        fp.close()

    def get_data(self):
        self.parse_index()
        self.parse_data()
        return self.data
