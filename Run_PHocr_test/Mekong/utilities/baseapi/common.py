# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created: 29/06/2017
# Last update:  06/07/2017
# Updated by:   Phung Dinh Tai
# Description:  This script define some usual functions
import os
from configs.common import Delimiter
from baseapi.file_access import write_json
import datetime
import math


def get_time_str(value):
    if value < 60:
        return "{0}s".format(value)
    else:
        return "{0}m {1}s".format(value//60, value % 60)


def get_current_local_time_in_format(format_):
    """
    Get current local time of machine in specific format

    Parameters
    ----------
    format_: str
        the format used to format datetime data output

    Examples
    --------
    get_current_local_time_in_format("%d-%m-%Y %H:%M")
    will have result: 22-11-2018 09:38

    Returns
    -------
    str
        Current local datetime follow format
    """
    current_datetime = datetime.datetime.now()
    return current_datetime.strftime(format_)


def get_files_in_folder(folder, ext_list=None):
    file_list = []
    if not ext_list:
        # If file extension list is not defined -> Get all files in folder
        for f in os.listdir(folder):
            path = os.path.join(folder, f)
            if os.path.isfile(path):
                file_list.append(path)
    else:
        # Only get files have file extension in defined list
        for f in os.listdir(folder):
            path = os.path.join(folder, f)
            for ext in ext_list:
                if f.endswith(ext):
                    file_list.append(path)
    return file_list


def compare_two_list_string(list1, list2):
    same = []
    not_in_1 = []
    not_in_2 = []

    for x in list1:
        x_base_name = os.path.basename(x)
        is_added = False
        for y in list2:
            y_base_name = os.path.basename(y)
            if x_base_name == y_base_name:
                same.append(x_base_name)
                is_added = True
        if not is_added:
            not_in_2.append(x_base_name)

    for y in list2:
        y_base_name = os.path.basename(y)
        is_added = False
        for x in list1:
            x_base_name = os.path.basename(x)
            if y_base_name == x_base_name:
                is_added = True
        if not is_added:
            not_in_1.append(y_base_name)

    return same, not_in_1, not_in_2


def compare_two_list(list1, list2):
    set_list1 = set(list1)
    set_list2 = set(list2)
    same = set_list1 & set_list2
    not_in_list1 = set_list1 - set_list2
    not_in_list2 = set_list2 - set_list1
    return list(same), list(not_in_list1), list(not_in_list2)


def padding_time(time_str):
    if len(time_str) < 2:
        return "0{0}".format(time_str)
    return time_str


class TypeConverter(object):

    @staticmethod
    def convert_str_to_bool(string):
        true_list = ["true", "1"]
        if string.lower() in true_list:
            return True
        else:
            return False


# Get lowercase of a string or list of string input
def get_lower(str_in):
    if type(str_in) == str:
        return str_in.lower()
    elif type(str_in) == list:
        lower_list = []
        for s in str_in:
            lower_list.append(s.lower())
        return lower_list
    else:
        return ""


# Concatenate 2 string list "a,b" and "c,d" to "a,b,c,d"
def concat_2_string_list(str1, str2, delimiter=Delimiter.LIST):
    s_1 = str1.strip("{0} ".format(delimiter))
    s_2 = str2.strip("{0} ".format(delimiter))
    if s_1 and not s_2:
        return s_1
    elif s_2 and not s_1:
        return s_2
    elif s_1 and s_2:
        return s_1 + delimiter + s_2
    else:
        return ""


# Specific a file by a suffix
def specify_file_name(file_name, suffix):
    name_splited = file_name.split(".")
    ext = name_splited[-1]
    base_name = name_splited[0:-1]
    return "".join(base_name) + Delimiter.SPECIFIC + suffix + Delimiter.EXTENSION + ext


# Get glob suffix
def glob_suffix(name):
    return name + "*"


# Add file .empty to empty folder
def add_empty_file_2_dir(directory):
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            d_path = os.path.join(root, d)
            if not os.listdir(d_path):
                f_path = os.path.join(d_path, ".empty")
                json_obj = {}
                write_json(json_obj, f_path)


# Add specific
def append_specific_package(package_name, desc):
    split_name = package_name.split(".")
    suffix = split_name[-1]
    split_name = split_name[0:-1]
    return ".".join(split_name) + "_" + desc + "." + suffix


# Find min value index of array
def find_min_index(value_array):
    min_val = value_array[0]
    min_index = 0
    for i in range(0, len(value_array)):
        if value_array[i] == 0:
            return i
        if min_val > value_array[i]:
            min_val = value_array[i]
            min_index = i
    return min_index


def get_list_defined_string(defined_class):
    """
    Get list of defined strings of a class which define constant values

    Parameters
    ----------
    defined_class : object
        Python class which define constant values

    Returns
    -------
    list
        List of constant string defined in the class

    Examples
    --------
    We have a defined class
    class A:
        VALUE1 = 'Hello'
        VALUE1 = 'Good morning'

        class B:
            VALUE = 'Good afternoon'

    So this function return
        [ 'Hello', 'Good morning' ]

    """
    attributes = list()
    for value in defined_class.__dict__.itervalues():
        # Conditions:
        # Type should be str
        # Ignore default private attribute of a general python object
        if value and (type(value) is str) \
                and (not value.startswith("__")) \
                and ("." not in value):
            attributes.append(value)
    return attributes


def format_string(value):
    if type(value) == bool:
        if value:
            return "x"
        else:
            return ""
    elif type(value) == str:
        return value
    elif type(value) == list:
        return ",".join(value)
    elif value is None:
        return ""
    else:
        return value


def merge_lists(*args):
    list_merged = []
    for arg in args:
        if type(arg) is not list:
            raise Exception("Invalid argument, type need to be a list!")
    for arg in args:
        for elm in arg:
            if elm not in list_merged:
                list_merged.append(elm)
    return list_merged


def get_accuracy_value(errors, total_characters):
    if total_characters == 0:
        if errors == 0:
            return 1
        else:
            return 0
    return float(total_characters - errors)/float(total_characters)


# Get base name of file (without extension)
# Example: a.tgz -> a
def get_base_name_file(file_name):
    split_name = file_name.split(".")
    return ".".join(split_name[0:len(split_name) - 1])


# Get unique list
def get_unique_list(list_elements):
    unique_list = []
    for elem in list_elements:
        if elem not in unique_list:
            unique_list.append(elem)
    return unique_list


def convert_to_unicode(string):
    if not isinstance(string, unicode):
        string = string.decode('utf-8')
    return string


def convert_from_kb_to_mb(value):
    """
    Convert from KB to MB.

    Parameters
    ----------
    value: int
        Input value (unit: kb)

    Returns
    -------

    """
    return float("{0:0.3f}".format(value/(math.pow(2, 10))))


def get_printable_size(byte_size):
    """
    A bit is the smallest unit, it's either 0 or 1
    1 byte = 1 octet = 8 bits
    1 kB = 1 kilobyte = 1000 bytes = 10^3 bytes
    1 KiB = 1 kibibyte = 1024 bytes = 2^10 bytes
    1 KB = 1 kibibyte OR kilobyte ~= 1024 bytes ~= 2^10 bytes (it usually means 1024 bytes but sometimes it's 1000... ask the sysadmin ;) )
    1 kb = 1 kilobits = 1000 bits (this notation should not be used, as it is very confusing)
    1 ko = 1 kilooctet = 1000 octets = 1000 bytes = 1 kB
    Also Kb seems to be a mix of KB and kb, again it depends on context.
    In linux, a byte (B) is composed by a sequence of bits (b). One byte has 256 possible values.
    More info : http://www.linfo.org/byte.html
    """

    BASE_SIZE = 1024.00
    MEASURE = ["B", "KB", "MB", "GB", "TB", "PB"]

    def _fix_size(size, size_index):
        if not size:
            return "0"
        elif size_index == 0:
            return str(size)
        else:
            return "{:.3f}".format(size)

    current_size = byte_size
    size_index = 0

    while current_size >= BASE_SIZE and len(MEASURE) != size_index:
        current_size = current_size / BASE_SIZE
        size_index = size_index + 1

    size = _fix_size(current_size, size_index)
    measure = MEASURE[size_index]
    return size + measure


def takeThird(elem):
    """
    Take third element for sort.
    Parameters
    ----------
    elem: list
       Input list.
    """
    return elem[2]
