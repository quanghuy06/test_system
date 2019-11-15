# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/07/2018
# Updated by:       Phung Dinh Tai
# Description:      Define base class for a reporter
from abc import ABCMeta, abstractmethod
from baseapi.log_manager import Logger


class Reporter(object):

    __metaclass__ = ABCMeta

    def __init__(self, output_file=None, log_enable=True):
        self.output_file = output_file
        self.output_file_set = False
        if self.output_file:
            self.output_file_set = True
        self.data = None
        self.title = None
        self.work_good = True
        self.logger = Logger(log_disable=(not log_enable))

    @abstractmethod
    def collect_data(self):
        pass

    @abstractmethod
    def do_work(self):
        pass
