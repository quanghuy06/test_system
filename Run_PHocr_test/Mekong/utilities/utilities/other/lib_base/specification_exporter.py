# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      14/07/2017
# Last update:      30/07/2018
# Updated by:       Le Thi Thanh
# Description:      Define class reporter for test case specification

import sys
import os
from configs.database import DbConfig, SpecHelper, SpecKeys, SpecCheckKey, \
    FilterInterfaceConfig, TestcaseConfig
from baseapi.file_access import read_json


class SpecDbExporter:
    def __init__(self):
        self.data = {}
        helper = SpecHelper()
        self.tags = helper.get_list_tags()
        self.tags_str = []
        for tag_name in sorted(self.tags.iterkeys()):
            self.tags_str.append(tag_name)

    def get_data(self, spec_list):
        for spec_obj in spec_list:
            test_id = spec_obj[SpecKeys.ID]
            self.data[test_id] = {}
            self.data[test_id][SpecKeys.COMPONENT] = spec_obj[SpecKeys.COMPONENT]
            self.data[test_id][SpecKeys.FUNCTIONALITIES] = ",".join(spec_obj[SpecKeys.FUNCTIONALITIES])
            tags = spec_obj[SpecKeys.TAGS]
            for tag_name in tags:
                self.data[test_id][tag_name] = tags[tag_name]
        return self.data

    def get_spec_list_from_test_folder(self, test_folder):
        if not os.path.isdir(test_folder):
            print "Folder {0} does not exist!".format(test_folder)
            sys.exit(1)
        spec_list = []
        for test_id in os.listdir(test_folder):
            spec_file = os.path.join(test_folder, test_id, TestcaseConfig.SPEC_FILE)
            spec_list.append(read_json(spec_file))
        return spec_list

    def export(self, file_name, test_folder):
        spec_list = self.get_spec_list_from_test_folder(test_folder)
        # Get test case specification from database
        self.get_data(spec_list)
        # Write header line
        with open(file_name, 'w') as myfile:
            head_line = "Test case ID"
            head_line += "\t" + SpecKeys.COMPONENT
            head_line += "\t" + SpecKeys.FUNCTIONALITIES
            for tag_name in self.tags_str:
                head_line += "\t{0}".format(tag_name)
            head_line += "\n"
            myfile.write(head_line)
            # Write data
            for test_id in sorted(self.data.iterkeys()):
                line = test_id
                line += "\t" + self.data[test_id][SpecKeys.COMPONENT]
                line += "\t" + self.data[test_id][SpecKeys.FUNCTIONALITIES]
                tags = self.data[test_id]
                for tag_name in self.tags_str:
                    if tag_name != SpecKeys.COMPONENT and tag_name != SpecKeys.FUNCTIONALITIES:
                        try:
                            value_type = self.tags[tag_name][SpecCheckKey.TYPE]
                            if value_type == FilterInterfaceConfig.TYPE_BOOL:
                                if tags[tag_name]:
                                    line += "\tx"
                                else:
                                    line += "\t"
                            elif value_type == FilterInterfaceConfig.TYPE_LIST:
                                line += "\t" + "|".join(tags[tag_name])
                            elif value_type == FilterInterfaceConfig.TYPE_STR:
                                line += "\t" + tags[tag_name]
                            else:
                                line += "\t" + str(tags[tag_name])
                        except:
                            line += "\t"

                line += "\n"
                myfile.write(line.encode('utf-8'))
            myfile.close()
