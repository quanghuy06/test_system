import sys
import json
import os

def load_json(json_file_path):
    """Get config file
    :param definition_file: file path relative to working directory
    :return
        array
            [0]: error
            [1]: config dictionary
    """
    try:
        with open(json_file_path) as data_file:
            config = json.load(data_file)
    except Exception as e:
        return [e, None]

    return [None, config]

def print_c(str, color=None):
    from colorama import init
    from colorama import Fore, Back, Style
    init(autoreset=True)

    if color == 'red':
        sys.stderr.write(Fore.RED + str)
    elif color == 'green':
        print(Fore.GREEN + str)
    else:
        print(str)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        pass
