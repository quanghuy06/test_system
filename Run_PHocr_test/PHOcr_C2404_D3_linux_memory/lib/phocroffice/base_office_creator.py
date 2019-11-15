# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

from datetime import datetime
from abc import abstractmethod, ABCMeta

from phocr_shared.logger import OCRFileLogger, OCRLogLevel


class BaseOfficeCreator(object):
    """
    This class is parent class of other output formattings as:
    PHOcrWordCreator, PHOcrExcelCreator or PHOcrPowerPointCreator
    It stores common attributes which are used in children classes
    """
    __metaclass__ = ABCMeta

    def __init__(self, language, working_directory, debug=0):
        self.language = str(language)
        self.debug = int(debug)
        self.working_directory = working_directory
        # Settings for logger
        self.log_level = OCRLogLevel.LOG_LEVEL_OFF
        if debug != 0:
            self.log_level = OCRLogLevel.LOG_LEVEL_DEBUG
        current_timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        logfile_name = 'BaseOfficeCreator-{0}.log'.format(current_timestamp)
        error_logfile_name = 'BaseOfficeCreator-error-{0}.log'.format(
            current_timestamp
        )
        self.file_logger = OCRFileLogger(logfile_name, self.log_level, self.working_directory)
        self.error_logger = OCRFileLogger(
            error_logfile_name,
            OCRLogLevel.LOG_LEVEL_ERROR,
            self.working_directory
        )

    @abstractmethod
    def generate_document(self, xml_obj):
        """
        Interface for generating document
        Children classes must implement this method for exporting to
        specific format: .docx, .xlsx, .pptx

        Parameters
        ----------
        xml_obj : Object
            XML object information which is parsed from .xml file
        Returns
        -------

        """
        pass
