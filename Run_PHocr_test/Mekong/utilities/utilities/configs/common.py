# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created: 29/06/2017
# Last update:  30/06/2017
# Updated by:   Phung Dinh Tai
# Description:  This script define some common information of Mekong project and Test system


# Platform supported
class Platform(object):
    LINUX = "linux"
    WINDOWS = "windows"


SupportedImage = [".jpg", ".tif", ".tiff", ".bmp", ".png"]
SupportedPlatform = [
    Platform.LINUX,
    # Platform.WINDOWS
    ]


class Delimiter:
    LIST = ","
    SPECIFIC = "_"
    EXTENSION = "."
    PATH = "/\\"
    LINUX_PATH = "/"
    WIN_PATH = "\\"


class file_extension:
    DOCX = ".docx"
    EXCEL = ".xlsx"
    PPTX = ".pptx"
    TXT = ".txt"
    PDF = ".pdf"
    PDFA = ".pdf"
    TEXT_LAYOUT = "*_0.txt"
    GET_TEXT_DOCUMENT = "get_text_in_document.txt"
    GET_TEXT_PAGE = "get_text_in_page_0.txt"

class file_name_pattern:
    TEXT_FILE = ".*\.txt"
    BB_FILE = r'.*_\d+\.txt'
    NOT_BB_FILE = r'^(?!.*_\d+\.txt)'


class DateTimeFormat:
    """
    Store datetime format used in test system
    """
    DATE_IN_DATABASE = "%d-%m-%Y %H:%M"


class Machines:
    """
    This class contain information of all machines of test system
    """
    IP = 'ip'
    TC_FOLDER = 'tc_folder'
    NAME = "name"

    # TODO: Currently, we support only for linux.
    # TODO: So, one day if Windows is also updated, we need to modify below path
    REF_DATA_PATH = "ref_data/linux/"
    GT_DATA_PATH = "ground_truth_data/linux/"
    TEST_DATA = "test_data/"

    MASTER_MACHINE = {
        # NAME: 'ocr3',
        # IP: '10.116.41.96',
        # TC_FOLDER: '/media/ocr3/data/MekongTC/TESTS/'
        NAME: 'ocrdev',
        IP: '10.116.43.104',
        TC_FOLDER: '/home/ocrdev/Mekong_Update_from_database/TESTS'
    }

    NODE_MACHINES = {
        # 'phocrserver1': {
        #     IP: '10.116.42.31',
        #     TC_FOLDER: '/home/phocrserver1/MekongTC/'
        # },
        # 'phocrserver2': {
        #     IP: '10.116.42.42',
        #     TC_FOLDER: '/home/phocrserver2/MekongTC/'
        # },
        # 'phocrserver3': {
        #     IP: '10.116.226.92',
        #     TC_FOLDER: '/home/phocrserver3/MekongTC/'
        # },
        # 'phocrserver4': {
        #     IP: '10.116.226.111',
        #     TC_FOLDER: '/home/phocrserver4/MekongTC/'
        # }
        'huanlvserver': {
            IP: '10.116.41.89',
            TC_FOLDER: '/home/huanlv/MekongTC/'
        },
        'ocr5': {
            IP: '10.116.41.85',
            TC_FOLDER: '/home/ocr5/MekongTC'
        }
    }