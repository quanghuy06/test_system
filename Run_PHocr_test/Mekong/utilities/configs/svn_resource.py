# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:
# Description:
import os
import json


class DataPathSVN(object):
    ROOT = "/home"
    SVN_FOLDER = "SVN"
    TRAINING_DATA_DIR = "TrainingData"
    PHOCRDATA_DIR = "phocrdata"
    MEKONG_3RD_PARTY_DIR = "mekong_3rd"
    PHOCR_LIB = "phocr_lib"
    # This name of HANOI_RELEASE follow svn url.
    # http://vc1.tsdv.com.vn/2018A/phocr/trunk/src/Hanoi-data/
    HANOI_RELEASE = "Hanoi-data"
    PHOCR_HANOI_3RDPARTY = "phocr_hanoi_3rdparty"
    HANOI_WINDOWS_PACKAGE = "windows/packages"
    THIRD_PARTY_PYTHON = "3rdparty_python"
    PYTHON_PORTABLE = "python_portable"
    PYTHON_FOLDER = "Python-3.5.2"
    CHANGE_LOG = "change_log"


class SVNResource:
    def __init__(self):
        script_dir = os.path.dirname(__file__)
        self.config_file = os.path.join(script_dir, "resource/svn_urls.json")

        with open(self.config_file) as f:
            self.data = json.load(f)

    def get_url(self, key):
        return self.data[key]
