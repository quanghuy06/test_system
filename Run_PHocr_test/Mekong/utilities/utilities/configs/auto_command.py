# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created:     30/06/2017
# Last updated:     30/06/2017
# Update by:        Phung Dinh Tai
# Description:      This script define parameters for auto generating command line in case of
#                   custom run.py script not found
from configs.projects.phocr import PhocrProject
from configs.json_key import LanguageOptConfig
from configs.projects.saigon import SaigonProject
from configs.database import SpecKeys

FunctionMapping = {
    PhocrProject.PRODUCT: {
        PhocrProject.components.DEFAULT: {
            PhocrProject.functionalities.EXPORT_TXT: "",
            PhocrProject.functionalities.EXPORT_PDF: "-pdf",
            PhocrProject.functionalities.EXPORT_PDFA: "-pdfa",
            PhocrProject.functionalities.EXPORT_PDFA_BIN: "-pdfa-bin",
            PhocrProject.functionalities.EXPORT_PDFA_HALFTONE: "-pdfa-halftone",
            PhocrProject.functionalities.EXPORT_PDFA_PHOTO_HALFTONE: "-pdfa-photo-halftone",
            PhocrProject.functionalities.NO_OCR_PDF: "-no-ocr-pdf",
            PhocrProject.functionalities.TEXT_LAYOUT: "-layout",
            PhocrProject.functionalities.REGION_LAYOUT: "-reg_data",
            PhocrProject.functionalities.OCR: "-ocr",
            PhocrProject.functionalities.EXPORT_DOCX: "-word",
            PhocrProject.functionalities.EXPORT_EXCEL: "-excel",
            PhocrProject.functionalities.EXPORT_PPTX: "-pptx",
            PhocrProject.functionalities.EXPORT_SINGLE_FILE: "--export-single-file",
            PhocrProject.functionalities.GET_TEXT_PAGE: "-get-text-page",
            PhocrProject.functionalities.GET_TEXT_DOCUMENT: "-get-text-document"
        },
        PhocrProject.components.BARCODE: {
            PhocrProject.functionalities.BAR_SINGLE: "-single",
            PhocrProject.functionalities.BAR_ALL: "-all",
            PhocrProject.functionalities.BAR_SIMPLE: "-simple",
            PhocrProject.functionalities.BAR_MUTIPLE: "-multiple",
            PhocrProject.functionalities.BAR_2D: "-two_d",
            PhocrProject.functionalities.BAR_CSV: "-csv",
            PhocrProject.functionalities.BAR_DESKEW: "-deskew"
        }
    },
    SaigonProject.PRODUCT: {
        SaigonProject.components.DEFAULT: {
            SaigonProject.functionalities.CMP_TEXT: "",
            SaigonProject.functionalities.CMP_BB: "-bbcompare",
            SaigonProject.functionalities.TOTAL_CHARACTER: "-tc",
            "output": "-o"
        }
    }
}

TagMapping = {
    PhocrProject.PRODUCT: {
        SpecKeys.Tags.IS_PRESENTATION: "-idoctype pptx"
    }
}

LanguageOption = {
    PhocrProject.PRODUCT: {
        PhocrProject.components.DEFAULT: {
            LanguageOptConfig.OPTION: "",
            LanguageOptConfig.DELIMITER: ","
        },
        PhocrProject.components.OCR_ENGINE: {
            LanguageOptConfig.OPTION: "-l",
            LanguageOptConfig.DELIMITER: "+"
        },
        PhocrProject.components.BARCODE: None,
        PhocrProject.components.PREPROCESS: None,
        PhocrProject.components.MACRO_REGION: None
    }
}

