# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created:     12/01/2017
# Last updated:     26/07/2017
# Update by:        Phung Dinh Tai
# Description:      This script define a class for handling json compare result
from abc import ABCMeta
from handlers.compare_handlers.lib_base.compare_result_handler_class import \
    CompareResultHandlerClass


class CompareResultHandler(CompareResultHandlerClass):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(CompareResultHandler, self).__init__(**kwargs)

    def get_list_tests(self):
        return sorted(self.data.keys())

    def set_title(self):
        pass
