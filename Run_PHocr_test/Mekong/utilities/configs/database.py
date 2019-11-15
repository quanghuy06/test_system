# Toshiba - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date created:     27/06/2017
# Last updated:     28/06/2017
# By:               Phung Dinh Tai
# Description:      This file defines parameters of database server and test case structure

from configs.credential import Credential
from configs.projects.phocr import PhocrProject
from configs.projects.hanoi import HanoiProject
from configs.common import Platform


# Database configuration
class DbConfig:
    HOST = "10.116.41.97"
    PORT = 27018
    DB_NAME = "Mekong"
    FILE_SPEC_DEFAULT = "TestcaseSpecification.tsv"

    class collections:
        TEST_CASE = "test_case"
        TEST_DATA = "test_data"
        REFS_DATA = "refs_data"
        REVIEW_RESULTS = "review_results"
        SCRIPTS = "scripts"
        GROUND_TRUTH_DATA = "ground_truth_data"
        ORIGINAL_DOC = "original_document"

    @staticmethod
    def get_account_base_on_permission(is_readwrite):
        credential = Credential()
        if is_readwrite:
            user, password = credential.get_account_for("MekongDBReadWrite")
        else:
            user, password = credential.get_account_for("MekongDBReadOnly")
        return user, password


class MongoDbConfig(object):
    """
       Mongdb configuration used for execute command related to mongod such as:
       connect, start, stop ...

    """
    class Mongod(object):
        MEKONGDB_PATH = "/media/ocr3/data/MekongDB"
        EXECUTABLE = 'mongod'
        class Options(object):
            AUTH = '--auth'
            PORT = '--port'
            DBPATH = '--dbpath'


# Test case structure
class TestcaseConfig:
    FOLDER_DEFAULT = "TESTS"
    SPEC_FILE = "spec.json"
    FORCE_SPEC_FILE = "force_spec.json"
    SCRIPT_DIR = DbConfig.collections.SCRIPTS
    TEST_DATA_DIR = DbConfig.collections.TEST_DATA
    REF_DATA_DIR = "ref_data"
    GROUND_TRUTH_DATA_DIR = DbConfig.collections.GROUND_TRUTH_DATA
    OUTPUT_FOLDER = "output"

    class Scripts:
        COMPARE = "compare.py"
        TEST = "run.py"

class DbAccountJsonKeys:
    NAME = "name"
    PASSWORD = "password"
    ROLES = "roles"
    DATABASE = "db"
    ROLE = "role"

    class Roles:
        RW = "readWrite"
        R = "read"
        W = "write"

class DbQueryKeys:
    AND = "$and"
    OR = "$or"
    TEXT = "$text"
    SEARCH = "$search"
    ALL = "$all"
    NIN = "$nin"
    IN = "$in"
    SET = "$set"
    PULL = "$pull"
    PUSH = "$push"
    UNSET = "$unset"

# This is some parameter of filter string which is used  by user
class FilterInterfaceConfig:
    PHOCR_HEADER = "[PHOcr]"
    ID = "Testcase ID:"
    PRODUCT = "Products:"
    COMPONENT = "Components:"
    FUNCTIONALITIES = "Functionalities:"
    TAGS = "Tags:"
    ID_CONTAIN = "ID Contains:"
    TEST_ET_DEFAULT = "Test ET Default:"
    CUSTOM_QUERY = "Custom Query:"
    LIST_DELIMITER = ","
    VALUE_DELIMITER = ":"
    OR_DELIMITER = "|"
    AND_DELIMITER = "&"
    AND_COM_DELIMITER = ","
    TYPE_STR = "string"
    TYPE_BOOL = "bool"
    TYPE_LIST = "list"
    TYPE_INT = "int"
    TYPE_FLOAT = "float"
    TYPE_DICT = "dict"


# Specification of test case
class SpecKeys(object):
    PRODUCT = "product"
    ENABLE = "enable"
    FUNCTIONALITIES = "functionalities"
    WEIGHT = "weight"
    WEIGHTS = "weights"
    ERROR_FLAGS = "error_flags"
    HISTORY_DATA = "history_data"
    TAGS = "tags"
    COMPONENT = "component"
    ID = "_id"
    HISTORY = "history"
    FILE_NAME = "filename"
    ID_CONTAIN = "id_contain"
    CHANGED_LOG = "changed_log"
    BINARY_TEST_INFORMATION = "binary_test_information"
    TEST_ET_DEFAULT = "test_et_default"

    class Tags(object):
        DOC_NAME = "DocumentName"
        DOC_TYPE = "DocumentType"
        DOC_PAGE = "DocumentPage"
        LANGS = "Language"
        PLATFORMS = "Platform"
        ACCURACY = "GetAccuracy"
        IS_INVOICE = "IsInvoice"
        IS_PURCHASE_ORDER = "IsPurchaseOrder"
        IS_FORM = "IsForm"
        IS_MAINLY_TEXT = "IsMainlyText"
        IS_LETTER = "IsLetter"
        BUG_LIST = "BugNumbers"
        IS_PRESENTATION = "IsPresentation"
        IS_LEGAL = "IsLegalDocument"
        IS_COURT = "IsCourtDocument"
        IS_MULTI_COL = "IsMultiColumn"
        IS_MULTI_BYTE_LANG = "IsMultiByteLanguage"
        HAS_TABLE = "HasTable"
        HAS_IMAGE = "HasImage"
        HAS_CHART = "HasChart"
        HAS_CONTRAST = "HasContrast"
        HAS_WATER_MASK = "HasWaterMask"
        HAS_LOGO = "HasLogoCompany"
        IS_ET_DEFAULT = "IsETDefault"
        IS_NON_INTEGRATION = "NonIntegration"
        IS_EXTREME_TEST = "IsExtremeTest"
        IS_UNLV = "IsUNLV"
        IS_EXCEL = "IsExcel"
        IS_FAX_DOCUMENT = "IsFaxDocument"
        HAS_BARCODE = "HasBarcode"
        HAS_TEXTBOX = "HasTextbox"
        IS_MULTI_PAGES = "IsMultiPages"
        IS_MEMCHECK = "IsMemCheckTest"
        IS_MEMCHECK_PEAK = "IsMemCheckPeak"
        CMD_OPTION = "CommandLineOptions"
        IS_PRINT_AS_COLOR = "IsPrintAsColor"
        IS_PRINT_AS_GRAY = "IsPrintAsGray"
        IS_PRINT_AS_MONO = "IsPrintAsMono"
        IS_200_DPI = "Is200dpi"
        IS_300_DPI = "Is300dpi"
        IS_DESKEW = "IsDeskew"
        IS_ROTATE = "IsRotate"
        IS_CLIPPED_IMAGE = "IsClippedImage"

        # List of languages
        class Language(object):
            ENGLISH = 'english'
            FRENCH = 'french'
            ITALIAN = 'italian'
            GERMAN = 'german'
            SPANISH = 'spanish'
            FINNISH = 'finnish'
            DANISH = 'danish'
            DUTCH = 'dutch'
            CHINESE_SIMPLIFIED = 'chinesesimplified'
            CHINESE_TRADITIONAL = 'chinesetraditional'
            GREEK_MODERN = 'greek-modern'
            JAPANESE = 'japanese'
            NORWEGIAN = 'norwegian'
            POLISH = 'polish'
            PORTUGUESE = 'portuguese'
            RUSSIAN = 'russian'
            SWEDISH = 'swedish'
            TURKISH = 'turkish'
            ARABIC = 'arabic'
            HUNGARY = 'hungarian'
            CZECH = 'czech'
            KOREAN = "korean"

    class History_data(object):
        PEAK_INFO = "Memory peak"
        PHOCR_TEST_MACHINE = "phocr_test_machine"
        PHOCR_ON_BOARD = "phocr_on_board"
        ESDK = "esdk"
        ABBYY_CLIENT = "abbyy_client"
        TESSERACT = "tesseract"

    class Functionalities(object):
        OCR = "OCR"
        SEGMENTATION = "Segmentation"

    class History:
        PHOCR_TEST_MACHINE = "phocr_test_machine"
        PHOCR_ON_BOARD = "phocr_on_board"
        ESDK = "esdk"
        TESSERACT = "tesseract"
        ABBYY = "abbyy_client"
        DELTA = "delta"
        TOTAL_CHARACTER = "total_characters"
        ERR_DELETE = "delete_errors"
        ERR_INSERT = "insert_errors"
        ERR_REPLACE = "replace_errors"
        TOTAL_ERRORS = "total_errors"
        PERFORMANCE = "time_execute"

    class ChangedLog:
        USER = "user"
        TIME = "time"
        CHANGED_LOG = "changed_log"
        ADDRESS = "address"

    class BinaryTestInformation(object):
        """
        This class define field name inside "binary_test_infomation" field.
        """
        BINARY_NAME = "binary_name"
        TEST_COMMAND = "test_command"
        OUTPUT = "output"

        class Variable(object):
            """
            This class defines supported variable case use in binaty_test_infomation
            field. Currently support for
                + TEST_DATA: indicate test_data folder in the test case.
                For example we can specify input image as: TEST_DATA/01_0033.jpg
            """
            TEST_DATA = "TEST_DATA"

        class Output(object):
            """
            This class define field name inside "output" field.
            """
            NAME = "name"
            COMPARATOR = "comparator"

            class Comparator(object):
                """
                This class defines supported comparator use in "output.comparator" field
                """
                TEXT = "text"
                BOUNDING_BOX = "bounding_box"
                PDF = "pdf"
                PDFA = "pdfa"
                WORD = "word"
                EXCEL = "excel"
                PPTX = "pptx"
                IGNORE = "ignore"


class SpecCheckKey:
    TYPE = "type"
    VALUE = "value"

# This structure define type and value of attributes in test case's specification
SpecChecking = {
    SpecKeys.ID: {
        SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_STR,
        SpecCheckKey.VALUE: []
    },
    SpecKeys.PRODUCT: {
        SpecCheckKey.VALUE: ["phocr", "hanoi"],
        SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_STR
    },
    SpecKeys.ENABLE: {
        SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
        SpecCheckKey.VALUE: ["true", "false"]
    },
    SpecKeys.COMPONENT: {
        SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_STR,
        SpecCheckKey.VALUE: {
            PhocrProject.PRODUCT: [PhocrProject.components.DEFAULT,
                                   PhocrProject.components.BARCODE,
                                   PhocrProject.components.OCR_ENGINE,
                                   PhocrProject.components.MACRO_REGION,
                                   PhocrProject.components.PREPROCESS],
            HanoiProject.PRODUCT: [HanoiProject.components.DEFAULT]
        }
    },
    SpecKeys.FUNCTIONALITIES: {
        SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_LIST,
        SpecCheckKey.VALUE: {
            PhocrProject.PRODUCT: {
                PhocrProject.components.DEFAULT: [PhocrProject.functionalities.EXPORT_PDF,
                                                  PhocrProject.functionalities.EXPORT_TXT,
                                                  PhocrProject.functionalities.EXPORT_PDFA,
                                                  PhocrProject.functionalities.EXPORT_PDFA_BIN,
                                                  PhocrProject.functionalities.EXPORT_PDFA_HALFTONE,
                                                  PhocrProject.functionalities.EXPORT_PDFA_PHOTO_HALFTONE,
                                                  PhocrProject.functionalities.NO_OCR_PDF,
                                                  PhocrProject.functionalities.TEXT_LAYOUT,
                                                  PhocrProject.functionalities.EXPORT_DOCX,
                                                  PhocrProject.functionalities.EXPORT_EXCEL,
                                                  PhocrProject.functionalities.EXPORT_PPTX,
                                                  PhocrProject.functionalities.OCR,
                                                  PhocrProject.functionalities.REGION_LAYOUT,
                                                  PhocrProject.functionalities.EXPORT_SINGLE_FILE,
                                                  PhocrProject.functionalities.GET_TEXT_DOCUMENT,
                                                  PhocrProject.functionalities.GET_TEXT_PAGE],
                PhocrProject.components.BARCODE: [PhocrProject.functionalities.BAR_2D,
                                                  PhocrProject.functionalities.BAR_SIMPLE,
                                                  PhocrProject.functionalities.BAR_CSV,
                                                  PhocrProject.functionalities.BAR_MUTIPLE,
                                                  PhocrProject.functionalities.BAR_SINGLE,
                                                  PhocrProject.functionalities.BAR_ALL,
                                                  PhocrProject.functionalities.BAR_DESKEW]
            }
        }
    },
    SpecKeys.TAGS: {
        SpecKeys.Tags.ACCURACY: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.DOC_NAME: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_STR,
            SpecCheckKey.VALUE: []
        },
        SpecKeys.Tags.DOC_PAGE: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_INT,
            SpecCheckKey.VALUE: []
        },
        SpecKeys.Tags.DOC_TYPE: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_STR,
            SpecCheckKey.VALUE: []
        },
        SpecKeys.Tags.BUG_LIST: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_LIST,
            SpecCheckKey.VALUE: []
        },
        SpecKeys.Tags.LANGS: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_LIST,
            SpecCheckKey.VALUE: ["english", "french", "german", "italian",
                                 "spanish", "danish", "dutch", "finnish",
                                 "greek-modern", "norwegian", "polish",
                                 "portuguese", "russian", "swedish",
                                 "turkish", "chinesesimplified",
                                 "chinesetraditional", "japanese"]
        },
        SpecKeys.Tags.PLATFORMS: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_LIST,
            SpecCheckKey.VALUE: ["linux", "windows"]
        },
        SpecKeys.Tags.HAS_CHART: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.HAS_CONTRAST: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.HAS_IMAGE: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.HAS_LOGO: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.HAS_TABLE: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.HAS_WATER_MASK: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_PURCHASE_ORDER: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_COURT: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_ET_DEFAULT: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_FORM: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_INVOICE: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_LEGAL: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_LETTER: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_MAINLY_TEXT: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_MULTI_BYTE_LANG: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_MULTI_COL: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_PRESENTATION: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_NON_INTEGRATION: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_EXTREME_TEST: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_UNLV: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_EXCEL: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.HAS_BARCODE: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.HAS_TEXTBOX: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_MULTI_PAGES: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_MEMCHECK: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_MEMCHECK_PEAK: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.CMD_OPTION: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_STR,
            SpecCheckKey.VALUE: []
        },
        SpecKeys.Tags.IS_PRINT_AS_COLOR: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_PRINT_AS_GRAY: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_PRINT_AS_MONO: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_200_DPI: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_300_DPI: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_DESKEW: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_ROTATE: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_CLIPPED_IMAGE: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        SpecKeys.Tags.IS_FAX_DOCUMENT: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        }
    },
    SpecKeys.ERROR_FLAGS: {
        Platform.LINUX: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        },
        Platform.WINDOWS: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_BOOL,
            SpecCheckKey.VALUE: ["true", "false"]
        }
    },
    SpecKeys.WEIGHTS: {
        Platform.LINUX: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_FLOAT,
            SpecCheckKey.VALUE: []
        },
        Platform.WINDOWS: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_FLOAT,
            SpecCheckKey.VALUE: []
        }
    },
    SpecKeys.HISTORY_DATA: {
        Platform.LINUX: {
            SpecKeys.History.ABBYY: {
                SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_DICT,
                SpecCheckKey.VALUE: {}
            },
            SpecKeys.History.ESDK: {
                SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_DICT,
                SpecCheckKey.VALUE: {}
            },
            SpecKeys.History.PHOCR_ON_BOARD: {
                SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_DICT,
                SpecCheckKey.VALUE: {}
            },
            SpecKeys.History.PHOCR_TEST_MACHINE: {
                SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_DICT,
                SpecCheckKey.VALUE: {}
            },
            SpecKeys.History.TESSERACT: {
                SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_DICT,
                SpecCheckKey.VALUE: {}
            }
        },
        Platform.WINDOWS: {
            SpecKeys.History.ABBYY: {
                SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_DICT,
                SpecCheckKey.VALUE: {}
            },
            SpecKeys.History.ESDK: {
                SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_DICT,
                SpecCheckKey.VALUE: {}
            },
            SpecKeys.History.PHOCR_ON_BOARD: {
                SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_DICT,
                SpecCheckKey.VALUE: {}
            },
            SpecKeys.History.PHOCR_TEST_MACHINE: {
                SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_DICT,
                SpecCheckKey.VALUE: {}
            },
            SpecKeys.History.TESSERACT: {
                SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_DICT,
                SpecCheckKey.VALUE: {}
            }
        }
    },
    SpecKeys.CHANGED_LOG: {
        SpecKeys.ChangedLog.USER: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_STR,
            SpecCheckKey.VALUE: []
        },
        SpecKeys.ChangedLog.TIME: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_STR,
            SpecCheckKey.VALUE: []
        },
        SpecKeys.ChangedLog.CHANGED_LOG: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_STR,
            SpecCheckKey.VALUE: []
        },
        SpecKeys.ChangedLog.ADDRESS: {
            SpecCheckKey.TYPE: FilterInterfaceConfig.TYPE_LIST,
            SpecCheckKey.VALUE: []
        }
    }
}

class SpecHelper:

    def __init__(self):
        pass

    def get_list_product(self):
        return SpecChecking[SpecKeys.PRODUCT][SpecCheckKey.VALUE]

    def list_product(self):
        for product in self.get_list_product():
            print product

    def get_list_component(self):
        return SpecChecking[SpecKeys.COMPONENT][SpecCheckKey.VALUE]

    def list_component(self):
        json_defined = self.get_list_component()
        for product in json_defined:
            print "Components of product \"{0}\":\n".format(product)
            for component in json_defined[product]:
                print "\t{0}".format(component)
            print "\n"

    def get_list_functionality(self):
        return SpecChecking[SpecKeys.FUNCTIONALITIES][SpecCheckKey.VALUE]

    def list_functionality(self):
        json_defined = self.get_list_functionality()
        for product in json_defined:
            print "Product: \"{0}\"\n".format(product)
            for component in json_defined[product]:
                print "\tFunctionalities of component \"{0}\":\n".format(component)
                for funct in json_defined[product][component]:
                    print "\t\t{0}".format(funct)
                print "\n"
            print "\n"

    def get_list_tags(self):
        return SpecChecking[SpecKeys.TAGS]

    def list_tags(self):
        print "{0}\t{1}".format("Tag", "Type")
        json_defined = self.get_list_tags()
        for tag in sorted(json_defined.iterkeys()):
            tag_type = json_defined[tag][SpecCheckKey.TYPE]
            print "{0}\t{1}".format(tag, tag_type.upper())

    # Check tag value:
    def is_valid_tag(self, key, value):
        json_defined = self.get_list_tags()
        for tag in sorted(json_defined.iterkeys()):
            if key == tag.lower():
                if type(value) is list:
                    for elm in value:
                        if str(elm).lower() in [x.lower() for x in
                                                  json_defined[tag][SpecCheckKey.VALUE]]:
                            return True
                        else:
                            return False
                else:
                    if str(value).lower() in [x.lower() for x in
                                              json_defined[tag][SpecCheckKey.VALUE]]:
                        return True
                    else:
                        return False
            else:
                continue
    @staticmethod
    def get_tag_type(tag_name):
        if tag_name in SpecChecking[SpecKeys.TAGS]:
            return SpecChecking[SpecKeys.TAGS][tag_name][SpecCheckKey.TYPE]
        return None

    @staticmethod
    def get_valid_tag_values(tag_name):
        if tag_name in SpecChecking[SpecKeys.TAGS]:
            return SpecChecking[SpecKeys.TAGS][tag_name][SpecCheckKey.VALUE]
        return None

    def list_all_spec_field(self):
        print "\n>>> All available fields in specification: "
        for key in SpecChecking.keys():
            print " "*5 + key

# Some functions useful for handler database access

def get_folder_bucket(bucket_name):
    if bucket_name == DbConfig.collections.TEST_DATA:
        return TestcaseConfig.TEST_DATA_DIR
    if bucket_name == DbConfig.collections.REFS_DATA:
        return TestcaseConfig.REF_DATA_DIR
    if bucket_name == DbConfig.collections.GROUND_TRUTH_DATA:
        return TestcaseConfig.GROUND_TRUTH_DATA_DIR
    if bucket_name == DbConfig.collections.SCRIPTS:
        return TestcaseConfig.SCRIPT_DIR
    return ""

def get_list_filter_interfaces():
    return [FilterInterfaceConfig.ID, FilterInterfaceConfig.PRODUCT,
            FilterInterfaceConfig.COMPONENT, FilterInterfaceConfig.FUNCTIONALITIES,
            FilterInterfaceConfig.TAGS, FilterInterfaceConfig.ID_CONTAIN,
            FilterInterfaceConfig.TEST_ET_DEFAULT]

def get_spec_key_from_label(label):
    if label == FilterInterfaceConfig.ID:
        return SpecKeys.ID
    if label == FilterInterfaceConfig.PRODUCT:
        return SpecKeys.PRODUCT
    if label == FilterInterfaceConfig.COMPONENT:
        return SpecKeys.COMPONENT
    if label == FilterInterfaceConfig.FUNCTIONALITIES:
        return SpecKeys.FUNCTIONALITIES
    if label == FilterInterfaceConfig.TAGS:
        return SpecKeys.TAGS
    if label == FilterInterfaceConfig.ID_CONTAIN:
        return SpecKeys.ID_CONTAIN
    if label == FilterInterfaceConfig.TEST_ET_DEFAULT:
        return SpecKeys.TEST_ET_DEFAULT
    return ""

def get_label_of_spec_key(spec_key):
    if spec_key == SpecKeys.ID:
        return FilterInterfaceConfig.ID
    if spec_key == SpecKeys.PRODUCT:
        return FilterInterfaceConfig.PRODUCT
    if spec_key == SpecKeys.COMPONENT:
        return FilterInterfaceConfig.COMPONENT
    if spec_key == SpecKeys.FUNCTIONALITIES:
        return FilterInterfaceConfig.FUNCTIONALITIES
    if spec_key == SpecKeys.TAGS:
        return FilterInterfaceConfig.TAGS
    return ""
