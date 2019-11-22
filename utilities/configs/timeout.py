# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           TaiPD
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      01/06/2017
# Description:      This python script defines timeout of processes


class TimeOut(object):

    class Default(object):
        SEND_FILE = 3600
        EXECUTE_COMMAND = 3600
        BUILD_TOTAL = 3600
        TEST_TOTAL = 7200
        EXTRACT_FILE = 300

    class VirtualMachine(object):
        DEFAULT = 120
        START = 120
        STOP = 120
        RESTORE = 120
        CHECK_RUNNING = 120
        ADD_SHARED_FOLDER = 300
        SNAPSHOT_DELETE = 360
        SNAPSHOT_TAKE = 600

    class samba(object):
        GET_TRAINED_DATA = 1800
        GET_PHOCR_LIBS = 600

    class vms(object):
        START = 120
        STOP = 120
        RESTORE = 120
        CHECK_VM_RUNNING = 120
        GET_PHOCR_BUILD = 1800
        GET_HANOI_BUILD = 1800
        TURNOFF_VM = 120

    class execute(object):
        DEFAULT_CLIENT = 1200
        DEFAULT_NODE = 300
        DEFAULT_VM = 300
        TEST = 18000
        REMOVE_TEST_REDUNDANT = 1000
        COMPARE = 3600
        CHECKOUT_PHOCR = 1200
        CHECKOUT_HANOI = 1200
        GIT_MERGE = 300
        EXTRACT_PHOCR_PACKAGE = 180
        NODE_BUILD = 1800
        NODE_TEST = 3600
        NODE_TEST_MEMORY_LEAK = 36000
        NODE_TEST_MEMORY_PEAK = 18000
        NODE_TEST_ON_BOARD = 18000
        NODE_TEST_MEMORY_LEAK_ONBOARD = 120000
        NODE_TEST_MEMORY_PEAK_ONBOARD = 180000
        MINIMUM_TIMEOUT_RUN_ONE = 120
        RATIO_TIMEOUT_RUN_ONE = 5
        RATIO_TIMEOUT_RUN_MEMORY_LEAK = 50
        RATIO_TIMEOUT_RUN_MEMORY_PEAK = 20
        PHOCR_DEFAULT_RUN_ONE = 120
        BINARY_TEST_DEFAULT_RUN_ONE = 120
        MEMCHECK_DEFAULT_RUN_ONE = 900
        HANOI_DEFAULT_RUN_ONE = 300
        BARCODE_DEFAULT_RUN_ONE = 60
        BUILD_PHOCR_LINUX = 3600
        BUILD_PHOCR_WINDOWS = 3600
        BUILD_HANOI_LINUX = 3600
        BUILD_HANOI_WINDOWS = 3600

    class install(object):
        HANOI_WINDOWS = 1800
        PHOCR_WINDOWS = 1800

    class ssh(object):
        CONNECT = 120
        COPY_FILE = 1800
        GET_PHOCR_BUILD_LINUX = 900
        GET_HANOI_BUILD_LINUX = 900
        GET_PHOCR_BUILD_WINDOWS = 1200
        GET_HANOI_BUILD_WINDOWS = 1200
        WORKER_GET_TEST_SET = 1800
        DELETE_DATA_ON_BOARD = 60

    class file(object):
        class node(object):
            GET_FILE_FROM_MASTER = 600
            COPY_FILE_TO_MASTER = 600
        class vms(object):
            GET_FILE_FROM_NODE = 1800
            COPY_FILE_TO_NODE = 1800

    class node(object):
        GET_TEST_CASES = 3600


class TimeWait(object):
    VM_LINUX_START = 20
    VM_WINDOWS_START = 25
