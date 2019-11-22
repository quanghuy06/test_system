# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           TaiPD
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      02/07/2018
# Description:
from abc import ABCMeta, abstractmethod


class FileHandler(object):

    __metaclass__ = ABCMeta

    def __init__(self, input_file=None):
        self.input_file = input_file
        self.data = None
        self.load_data()

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def dump(self, output_file):
        pass
