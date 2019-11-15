# This file define key name of configuration in json format.


# Parameters file
class ParametersJson(object):

    DEFAULT_NAME = "parameters.json"
    JENKINS_JOB = "job_name"
    JENKINS_BUILD = "build_number"
    GERRIT_PROJECT = "project"
    GERRIT_REFS = "refspec"
    GERRIT_BRANCH = "branch"
    EMAIL = "email"
    WINDOWS_DISABLE = "is_windows_disable"
    GERRIT = "gerrit"
    MINOR = "minor"
    IS_ET = "is_et"
    IS_EXTREME_TEST = "is_extreme_test"
    DELTA_PHOCR = "phocr_delta"
    DELTA_HANOI = "hanoi_delta"
    IS_RELEASE_DELTA = "release_delta"

    class gerrit(object):
        COMMIT = "commit_message"
        COMMENT = "comment"


# Profile of system configuration
class ProfileJson(object):
    DEFAULT_NAME = "profile.json"
    IT = "__IntegrationTest__"
    ET = "__EngineeringTest__"
    TESTING_ON_BOARD = "__TestingOnBoard__"
    VM_LIST = "__vms__"
    NODE_LIST = "__nodes__"
    BUILD_RELEASE = "__build_release__"
    BUILD_MEMORY = "__build_memory__"
    BUILD_DEBUG = "__build_debug__"
    DISTRIBUTION = "__distribution__"
    TEST = "__test__"
    NODE = "node"
    VM = "vm"
    VIRTUAL_MACHINE = "virtual_machine"
    BOARD = "board"

    class info(object):
        IP = "ip"
        OS = "os"
        USER = "username"
        PWD = "password"
        TEST_MACHINE = "test_machine"

    class platforms(object):
        LINUX = "linux"


# Test distribution
class TestDistributionJson(object):

    PREFIX = "test_distribution"
    DEFAULT_NAME = "test_distribution.json"
    SUMMARY = "__summary__"
    OFF = "__not_available__"

    class location(object):

        DB = "__db__"
        WS = "__ws__"

    class summary(object):

        NUM_VMS = "Total virtual machines available",
        NUM_LINUX_VMS = "Number linux virtual machines available",
        NUM_WINDOWS_VMS = "Number windows virtual machines available"
        NUM_TESTS_DB = "Number test cases from database"
        NUM_TESTS_WS = "Number test cases from work space"
        TESTSET_WS = "Test case from work space"


# TODO: (ThanhLT) This class should be remove because it is unused and
# TODO: duplicate with class in script command.py
# Build configuration
class BuildConfiguration(object):

    PHOCR = "PHOcr"
    HANOI = "Hanoi"

    class info(object):
        WORKINGDIR = "cwd"
        CMD = "command"
        RESULT = "build_result"
        PACKAGING = "packaging"


# Test result
class TestResultJson(object):

    EXITCODE = "exitcode"
    STDERR = "stderr"
    STDOUT = "stdout"
    TIME = "time"


class SpecKeys(object):

    PRODUCT = "product"
    ENABLE = "enable"
    FUNCTIONALITIES = "functionalities"
    WEIGHT = "weight"
    WEIGHTS = "weights"
    TAGS = "tags"
    COMPONENT = "component"
    ID = "_id"
    HISTORY = "history"

    class Tags(object):

        DOC_NAME = "DocumentName"
        DOC_TYPE = "DocumentType"
        DOC_PAGE = "DocumentPage"
        LANGS = "Language"
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

    class Functionalities(object):

        OCR = "OCR"
        SEGMENTATION = "Segmentation"


class LanguageOptConfig(object):

    OPTION = "option"
    DELIMITER = "delimiter"


class TestSystemInfoKeys(object):

    TOTAL = "total_vms"
    FAIL = "fail_vms"
    SUCCESS = "success_vms"


class LoggingServer(object):

    headers = {"Content-type": "application/json", "Accept": "application/json"}
    host = "10.116.41.53"
    port = 8000
    url = "/logs/?format=json"


class JobName:
    ET = "PHOcr-Engineering-Test"
    IT = "PHOcr-Integration-Test"
    TEST_ON_BOARD = "PHOcr-OnBoardTesting"


class ItPerformanceReport(object):
    LINK = "PerformanceReportLink"


class BuildManagerKey(object):
    PATH = "path"
    IP = "ip"
    OS = "os"
    USERNAME = "username"
    PASSWORD = "password"
    BUILD_PATH = "build_path"
    LST_BUILD_NAME = "lst_build_name"


class CurrentVersionKey(object):
    HANOI_CHANGE = "hanoi_change"
    PHOCR_CHANGE = "phocr_change"
    PHOCR_DELTA = "phocr_delta"
    HANOI_DELTA = "hanoi_delta"
    PATH = "path"
    IP = "ip"
    USERNAME = "username"
    PASSWORD = "password"


class BuiltManagerKey(object):
    PREVIOUS_BUILD = "previous_build"
    CURRENT_BUILD = "current_build"
    CHANGE_DELTA = "change_delta"
    CURRENT_VERSION = "current_version"
    CHANGE_BUILD_NUMBER = "change_build_number"
    PYTHON = "python"
    MEKONG = "mekong"
    RUN_PEF_ANALYSIS_PATH = "run_performance_analysis_path"
    BOARD_IP = "board_ip"
    PERF_REPORT_LINK = "performance_report_link"


class PreviousBuiltKey(object):
    BUILD_PATH = "build_path"
    PARAMETERS = "parameters"
    IP = "ip"
    GIT_COMMAND = "git_command"
    USERNAME = "username"
    PASSWORD = "password"


class CurrentBuildKey(object):
    BUILD_PATH = "build_path"
    PARAMETERS = "parameters"
    IP = "ip"
    GIT_COMMAND = "git_command"
    USERNAME = "username"
    PASSWORD = "password"


class ChangeDeltaMappingKey(object):
    PATH = "path"
    IP = "ip"
    USERNAME = "username"
    PASSWORD = "password"


class ChangeBuildMappingKey(object):
    PATH = "path"
    IP = "ip"
    USERNAME = "username"
    PASSWORD = "password"
