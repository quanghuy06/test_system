# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      09/07/2018
# Updated by:       Phung Dinh Tai
# Description:      Define base class for a tsv reporter
import os
from abc import ABCMeta, abstractmethod
from report.lib_base.reporter import Reporter
from baseapi.file_access import write_line, remove_paths


class TsvReporter(Reporter):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(TsvReporter, self).__init__(**kwargs)
        self.headers = []
        self.list_test_names = []

    @abstractmethod
    def get_line_data(self, test_name):
        return []

    @staticmethod
    def get_line_string(line_data):
        for i in range(0, len(line_data)):
            if type(line_data[i]) is not unicode:
                line_data[i] = str(line_data[i])
        return "\t".join(line_data)

    def do_work(self):
        # Collect data
        self.collect_data()

        if os.path.isfile(self.output_file):
            remove_paths(self.output_file)

        dir_name = os.path.dirname(self.output_file)
        if dir_name and not os.path.isdir(dir_name):
            os.makedirs(dir_name)

        write_data = self.get_line_string(line_data=self.headers)

        # Write data
        for test_name in self.list_test_names:
            line_data = self.get_line_data(test_name=test_name)
            write_data += "\n"
            write_data += self.get_line_string(line_data=line_data)

        # Write headers
        with open(self.output_file, 'w') as my_file:
            my_file.write(write_data.encode('utf-8'))
            my_file.close()
