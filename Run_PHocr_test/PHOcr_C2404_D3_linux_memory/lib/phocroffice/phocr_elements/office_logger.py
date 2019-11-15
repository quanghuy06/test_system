# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

import os
from abc import abstractmethod, ABCMeta


class OfficeLogLevel(object):
    """
    This class shows us levels for debugging
    """
    LOG_LEVEL_OFF = 0
    LOG_LEVEL_FATAL = 1
    LOG_LEVEL_ERROR = 2
    LOG_LEVEL_WARN = 3
    LOG_LEVEL_INFOR = 4
    LOG_LEVEL_DEBUG = 5
    LOG_LEVEL_TRACE = 6
    LOG_LEVEL_ALL = 7


class OfficeLogger(object):
    """
    Common API for logger
    """
    __metaclass__ = ABCMeta

    def __init__(self, debug_level):
        self.debug_level = debug_level

    @abstractmethod
    def log(self, debug_level, message):
        """
        Logging interface

        Parameters
        ----------
        debug_level : int
            Debug level which are judgement
        message : str
            Message want to log

        Returns
        -------

        """
        pass

    def can_log(self, debug_level):
        """
        Is debug level match the condition for enable logging

        Parameters
        ----------
        debug_level : int
            Debug level which are judgement

        Returns
        -------
        bool
            Can or can't log

        """
        return self.debug_level >= debug_level


class OfficeFileLogger(OfficeLogger):
    """
    Logger which log to file
    """

    def __init__(self, log_file, debug_level):
        OfficeLogger.__init__(self, debug_level)
        self.log_file = log_file
        self._clear_log_file()

    def log(self, debug_level, message):
        """
        Log message to file

        Parameters
        ----------
        debug_level : int
            Level want to enable log
        message : str
            Message want to log

        Returns
        -------

        """
        if self.can_log(debug_level):
            with open(self.log_file, mode='a') as log_file:
                log_file.write(message)

    def _clear_log_file(self):
        """
        Remove log file if it exists
        """
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
