# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      12/12/2016
# Last update:      15/12/2106
# Description:      This configure mekong structure -> Get path to folders in Mekong utilities
#                   base on current machine. If you change location of this script, you need to
#                   fix deep_path variable

import os, sys

script_dir = os.path.dirname(os.path.abspath(__file__))
deep_path = 2
utilities_dir = script_dir
for round in range(1, deep_path):
    utilities_dir = os.path.dirname(utilities_dir)
mekong_dir = os.path.dirname(utilities_dir)
def insert_sys_path():
    if utilities_dir not in sys.path:
        sys.path.insert(0, utilities_dir)
