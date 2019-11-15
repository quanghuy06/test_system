# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.
"""
This module will contain the process for adding PHOcr submodule path into
system path
"""
import os
import sys

SUB_MODULES = [
    '3rdparty'
]


def load_path():
    """
    Load configured paths into system path
    :return:
    """
    root_folder = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    root_folder = os.path.abspath(root_folder)
    for sub_module in SUB_MODULES:
        module_path = os.path.join(root_folder, sub_module)
        if os.path.exists(module_path):
            sys.path.insert(0, module_path)
        else:
            print('Please add PYTHONPATH to folder which contains 3rdparty')
