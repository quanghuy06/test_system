# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      12/12/2016
# Last update:      15/12/2106
# Description:      This script is used to add utilities folder to sys.path -> This allow us
#                   use scripts directly without set PYTHONPATH environment variable.

import os
import sys

script_dir = os.path.dirname(os.path.abspath(__file__))
deep_path = 2
test_dir = script_dir
for r in range(1, deep_path):
    test_dir = os.path.dirname(test_dir)
mekong_dir = os.path.dirname(test_dir)
utilities_dir = os.path.join(mekong_dir, 'utilities')


def insert_sys_path():
    if utilities_dir not in sys.path:
        sys.path.insert(0, utilities_dir)
