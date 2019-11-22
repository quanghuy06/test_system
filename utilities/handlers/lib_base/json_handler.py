# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           TaiPD
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      02/07/2018
# Description:      This python script define a base class for json handlers
import os
from abc import ABCMeta, abstractmethod
from baseapi.file_access import read_json, write_json
from handlers.lib_base.file_handler import FileHandler


class JsonHandler(FileHandler):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(JsonHandler, self).__init__(**kwargs)

    def load_data(self):
        self.data = read_json(self.input_file)

    def dump(self, output_file=None):
        if not output_file:
            # Override input file
            output_file = self.input_file
        else:
            # Create parent directory
            parent_dir = os.path.dirname(output_file)
            if not os.path.isdir(parent_dir):
                os.makedirs(parent_dir)
        write_json(obj=self.data, file_name=output_file)
