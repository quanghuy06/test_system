# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/07/2018
# Updated by:       Phung Dinh Tai
# Description:      Define base class for a file parser
from abc import ABCMeta, abstractmethod
from baseapi.log_manager import Logger


class FileParser(object):

    __metaclass__ = ABCMeta

    def __init__(self, input_file, log_enable=True):
        self.input_file = input_file
        self.work_good = True
        self.data = None
        self.meta_data = None
        self.logger = Logger(log_disable=(not log_enable))

    @abstractmethod
    def pre_process(self):
        pass

    @abstractmethod
    def load_meta_data(self):
        pass

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def handle_data(self):
        pass

    def do_work(self):
        # Pre-process file, raw data
        self.pre_process()

        # Load meta data if exist
        self.load_meta_data()

        # Load data
        self.load_data()

        # Handle raw data for final used data
        self.handle_data()
