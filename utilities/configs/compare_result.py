# Toshiba - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date created:     28/06/2017
# Last updated:     03/08/2017
# Updated by:       Phung Dinh Tai
# Description:      This script defines parameter for files, folders of compare result;
#                   structure of json compare result file.

# Keys of compare result json file
class CompareJsonKeys:

    CHANGE = "compare_change_vs_ground_truth"
    DIFF = "compare_change_vs_reference"
    ORIGIN = "compare_reference_vs_ground_truth"

    INFO = "detail_information"
    OFFICE_INFO = "detail_office_comparision"
    IS_CHANGE = "is_changed"
    IS_STDOUT_CHANGED = "is_stdout_changed"
    IS_STDERR_CHANGED = "is_stderr_changed"
    IS_FAILED = "is_failed"
    TITLE = "title"
    TOTAL_ERROR = "total_errors"
    TOTAL_CHARACTER = "total_characters"
    SRC = "source"
    TARGET = "target"
    HTML_PATH = "html_path"
    INSERT_ERR = "insert_errors"
    REPLACE_ERR = "replace_errors"
    DELETE_ERR = "delete_errors"
    CONTENT = "content"
    FILE = "file name"
    INFO_OUTPUT = "output data"
    INFO_REF = "reference data"

    REF_ONLY = "reference_only"
    OUTPUT_ONLY = "output_only"
    NOT_IN_OUTPUT_AND_REF = "not_in_output_and_ref"

# Some configuration of file/folder compare output
class CompareResultConfig:
    FILE_DEFAULT = "compare_result.json"
    FILE_ERROR_DEFAULT = "ErrorReport.json"
    FOLDER_DEFAULT = "compare_result"
    SUFFIX_CHANGE = "_change_ground"
    SUFFIX_DIFF = "_change_reference"
    SUFFIX_ORIGIN = "_reference_ground"
    PREFIX = "compare_result"
    HTML_CHANGE_SUFFIX = "newchange"
    HTML_DIFF_SUFFIX = "diff_newchange_original"
    HTML_ORIGIN_SUFFIX = "original"

    TXT_SUFFIX = ".txt"
    LAYOUT_SUFFIX = "_0.txt"
    HTML_SUFFIX = ".html"

    TITLE_CMP_BB = "Compare bounding box"
    TITLE_CMP_TEXT = "Compare text file"
    TITLE_CMP_BARCODE = "Compare barcode"
    TITLE_CMP_FOLDER = "Compare folder"
    TTILE_CMP_FOLDER_BB = "Compare folder contain bounding box files"
    TITLE_CMP_OFFICE = "Compare office "
    TITLE_CMP_DOCX = "Compare docx file"
    TITLE_CMP_EXCEL = "Compare excel file"
    TITLE_CMP_PPTX = "Compare pptx file"
    TITLE_CMP_PDFA = "Compare pdfa file"
    TITLE_CMP_MEMCHECK = "Memory check"
    TITLE_CMP_IMAGE = "Compare image"

    NOT_IN_REFERENCE = "not_in_reference"
    NOT_IN_OUTPUT = "not_in_output"
    DIFF_FILE = "diff_files"

# Errors report
class ErrorReportJsonKeys:
    SUMMARY_INFO = "total_errors_infor"
    TOTAL_ERROR = "total_errors"
    DETAIL_INFO = "detail_information"

class CompareMessage:
    FILE_NOT_IN_OUTPUT = "Files not in output"
    FILE_NOT_IN_REF = "Files not in reference"
    FILE_NOT_IN_GT = "Files not in ground truth"
    FILE_NOT_IN_USER_DEFINED = "Files not in user defined"

class CompareOcrInfo:
    NUM_ERRORS = "total_errors"
    SRC = "src"
    DES = "dest"
    INFO = "infor"

    class info:
        DES = "dest"
        SRC = "src"
        NUM_ERRORS = "errors"
        FILE = "html_path"
        ISCHANGE = "is_changed"
        TITLE = "title"
        NUM_CHARACTERS = "total_characters"

class CompareBarcodeInfo(CompareJsonKeys):
    DETAIL = "detail_information"
    NUM_CORRECT = "number_correct_barcodes"
    NUM_ERROR = "number_error_barcodes"
    TOTAL = "total barcodes"

    class Title:
        SIMPLE = "Barcode simple"
        LOCATION = "Barcode with location"

    class type:
        SIMPLE = "simple"
        LOCATION = "location"

class CompareBarcodeData:
    OUTPUT = "output"
    REF = "reference"
    GROUND = "ground_truth"

class BarcodeCmpType:
    # If overlap percent is over THRESHOLD -> same location
    THRESHOLD = 0.8

    class simple:
        TYPE_1 = "Same format, same content"
        TYPE_2 = "Same format, different content"
        TYPE_3 = "Different format, same content"
        TYPE_4 = "Different format, differnt content"
        TYPE_5 = "In base, not in current"

    class location:
        CORRECT = "Same location, same barcode"
        REPLACE = "Same location, different barcode"
        DIFFER = "Different location"
        INSERT = "Not in current, but in base"
        DELETE = "In current, not in base"
