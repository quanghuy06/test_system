# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
This module contain Logger class which help the other module logging
"""

import os
from abc import abstractmethod, ABCMeta


class OCRLogLevel(object):
    """
    Matching to enum LogLevel in PHOcr
    """
    LOG_LEVEL_OFF = 0
    LOG_LEVEL_FATAL = 1
    LOG_LEVEL_ERROR = 2
    LOG_LEVEL_WARN = 3
    LOG_LEVEL_INFOR = 4
    LOG_LEVEL_DEBUG = 5
    LOG_LEVEL_TRACE = 6
    LOG_LEVEL_ALL = 7


class OCRLogger(object):
    """
    Common API for logger
    """
    __metaclass__ = ABCMeta

    def __init__(self, debug_level):
        self._debug_level = debug_level

    @abstractmethod
    def log(self, debug_level, message):
        """
        Logging interface
        :param debug_level: debug level to log
        :param message: message to log
        :return:
        """
        pass

    def can_log(self, debug_level):
        """
        Is debug level match the condition for enable logging
        :param debug_level: debug level which are judgement
        :return: Boolean - can or can't log
        """
        return self._debug_level >= debug_level


class OCRFileLogger(OCRLogger):
    """
    Logger which log to file
    """
    def __init__(self, log_file, debug_level, working_directory):
        OCRLogger.__init__(self, debug_level)
        self._log_file = os.path.join(working_directory, log_file)
        self._clear_log_file()

    def log(self, debug_level, message):
        """
        Log message to file
        :param debug_level: level want to enable log
        :param message: message want to log
        :return:
        """
        if self.can_log(debug_level):
            with open(self._log_file, mode='a') as log_file:
                log_file.write(message)

    def _clear_log_file(self):
        """
        Remove log file if it exists
        :return:
        """
        if os.path.exists(self._log_file):
            os.remove(self._log_file)
