"""
Toshiba - Toshiba Software Development Vietnam
Team:           PHOcr
Author:         Phung Dinh Tai
Email:          tai.phungdinh@gmail.com
Date created:   23/06/2017
Last updated:   23/06/2017
Description:    This script defines all information for PHOcr project. The
                following configuration will be used in whole project. Please
                give correct information to ensure all work fine.
"""


class PhocrProject(object):
    NAME = "PHOcr"
    PRODUCT = "phocr"
    RELEASE_PREFIX = "PHOcr"
    RELEASE_SUFFIX = "tgz"
    DELTA = "phocr_delta"
    RELEASE_DIRECTORY = "PHOcrReleases"
    THIRD_PARTY_FOLDER = "3rdparty"

    class Products(object):
        PHOCR = 'phocr'
        HANOI = 'hanoi'

    class branches:
        MASTER = "master"
        OMR = "OMR"

    class build:
        FOLDER_DEFAULT = "build"
        PACKAGE_DEFAULT = "build.tar.gz"
        BIN = "bin"
        SHARE = "share"
        LIB = "lib"
        PHOCR_DATA = "phocrdata"
        WORKING_DIR = "PHOcr"
        CMD = "autoreconf -if && ./phobuild.sh release"
        RESULT = "build_release/build"

        class Windows:
            RESULT = "PHOcrSetup.msi"

    class components:
        DEFAULT = "PHOcrExe"
        BARCODE = "barcode"
        OCR_ENGINE = "ocrengine"
        MACRO_REGION = "macroregion"
        PREPROCESS = "preprocess"
        BINARY_TEST = "binary_test"

    class functionalities:
        EXPORT_TXT = "export_txt"
        EXPORT_PDF = "export_pdf"
        EXPORT_PDFA = "export_pdfa"
        EXPORT_PDFA_BIN = "export_pdfa_bin"
        EXPORT_PDFA_HALFTONE = "export_pdfa_halftone"
        EXPORT_PDFA_PHOTO_HALFTONE = "export_pdfa_photo_halftone"
        NO_OCR_PDF = "no_ocr_pdf"
        OCR = "ocr" # Remove all blank lines
        TEXT_LAYOUT = "segmentation"
        REGION_LAYOUT = "region_classification"
        BAR_SIMPLE = "simple"
        BAR_SINGLE = "single"
        BAR_ALL = "all"
        BAR_MUTIPLE = "multiple"
        BAR_CSV = "export_csv"
        BAR_2D = "2d_barcode"
        BAR_DESKEW = "deskew"
        EXPORT_DOCX = "export_word"
        EXPORT_EXCEL = "export_excel"
        EXPORT_PPTX = "export_pptx"
        EXPORT_SINGLE_FILE = "export_single_file"
        GET_TEXT_DOCUMENT = "get-text-document"
        GET_TEXT_PAGE = "get-text-page"

    class HN_functionalities:
        OUTPUT_FORMATS = "output_formats"
        BARCODE = "barcode"
        WORKFOLOW = "workflow"

    class envars:
        PHOCRDATA = "PHOCRDATA_PREFIX"
        LIBPATH = "LD_LIBRARY_PATH"

    class Python(object):
        # This version also is the name of directory store
        # portable python source.
        FOLDER_NAME = "Python-3.5.2"
