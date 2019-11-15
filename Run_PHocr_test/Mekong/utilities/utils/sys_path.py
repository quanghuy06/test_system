import os, sys

script_dir = os.path.dirname(os.path.abspath(__file__))
deep_path = 2
utilities_dir = script_dir
for round in range(1, deep_path):
    utilities_dir = os.path.dirname(utilities_dir)

Mekong_dir = os.path.dirname(os.path.dirname(utilities_dir))
def insert_sys_path():
    if utilities_dir not in sys.path:
        sys.path.insert(0, utilities_dir)