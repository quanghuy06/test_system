# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      31/03/2017
# Last update:      26/07/2107
# Updated by:       Phung Dinh Tai
# Description:      This file implements functions for work on file/folder
import os
import shutil
import json
import glob
import traceback
# Input need to be a single
# Silent mode, if do fail only return value. Return 0 if successfully
# Fail -> return trace back information
from threading import Timer
import httplib
from datetime import datetime
from configs.json_key import LoggingServer
import socket
import subprocess


def make_dir(path):
    """
    Make a directory recursively on local. Do nothing in case directory already exists.

    Parameters
    ----------
    path: str
        Directory need to be created.

    Returns
    -------
    None

    """
    # Check if directory exists then do nothing
    if os.path.exists(path):
        return
    # Create directory recursively
    absolute_path = os.path.abspath(path)
    # Create parent directory first
    dir_name = os.path.dirname(absolute_path)
    if not os.path.isdir(dir_name):
        make_dir(dir_name)
    # Create target directory
    os.mkdir(path)


def remove_a_path(path):
    try:
        if os.path.isfile(path):
            os.remove(path)
        if os.path.isdir(path):
            shutil.rmtree(path)
        return 0
    except:
        return traceback.format_exc()


# Input can be a path or a list of paths
# Silent mode, if someone fail, continue to process
# Return list of failure if fail
def remove_paths(paths):
    failure = []
    if type(paths) is list:
        for path in paths:
            if remove_a_path(path) != 0:
                failure.append(path)
    else:
        if remove_a_path(paths) != 0:
            failure.append(paths)
    if len(failure) == 0:
        return 0
    else:
        return failure


# Input can be a glob name or a list of glob names
# Not return a value
def remove_globs(globs):
    if type(globs) is list:
        for glob_path in globs:
            for path in glob.glob(glob_path):
                remove_paths(path)
    else:
        for path in glob.glob(globs):
            remove_paths(path)


# Input need be a single
# Currently, only support linux
# TODO : Make this support for windows
def copy_a_path(path, des, notice=True):
    if not os.path.exists(path):
        if notice:
            error_msg = "No such file or directory: {0}".format(path)
            raise Exception(error_msg)

    # Copy file
    if os.path.isfile(path):
        if os.path.isdir(des):
            file_name = os.path.basename(path)
            des_file = os.path.join(des, file_name)
        else:
            des_file = des
        shutil.copyfile(path, des_file)
    # Copy folder
    if os.path.isdir(path):
        if os.path.isdir(des):
            folder_name = os.path.basename(path)
            des_path = os.path.join(des, folder_name)
            shutil.copytree(path, des_path)
        else:
            shutil.copytree(path, des)
    return 0


def move_path_to_not_empty_directory(src, dst, symlinks=False, ignore=None):
    """
    Move file or directory to a directory which isn't empty.

    :param src: Source file or directory.
    :param dst: Destination directory.
    :param symlinks:
                If the optional symlinks flag is true, symbolic links in the
                source tree result in symbolic links in the destination tree; if
                it is false, the contents of the files pointed to by symbolic
                links are copied.
    :param ignore:
                The optional ignore argument is a callable. If given, it
                is called with the `src` parameter, which is the directory
                being visited by copytree(), and `names` which is the list of
                `src` contents, as returned by os.listdir():

                    callable(src, names) -> ignored_names
    :return:
    """
    if os.path.isfile(src):
        shutil.copy2(src, dst)
    else:
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)
    remove_paths(src)

# Input is a path or a list of paths
# If destination is a file, the file will be replaced
# If destination is a folder, path will be putted in it
def copy_paths(paths, des, notice=True):
    if type(paths) is list:
        for path in paths:
            copy_a_path(path, des, notice)
    else:
        copy_a_path(paths, des, notice)


# Input can be a glob name or a list of glob names
# Return 0 if all successfully
# Return list of failure if have anyone fail
def copy_globs(globs, des, notice=True):
    if not os.path.isdir(des):
        if notice:
            print "No such directory {0}!".format(des)
        return 1
    if type(globs) is list:
        for _glob in globs:
            copy_paths(glob.glob(_glob), des)
    else:
        copy_paths(glob.glob(globs), des)
    return 0


# Input need to be a single
# Real process is using mv command linux
# Support linux only
# TODO : Make this support windows
def move_a_path(path, des):
    copy_a_path(path, des)
    remove_a_path(path)


# Input can be a path or a list of paths
# Real process is copy and after that delete old one
# Return 0 if all successfully
# Return list of failure if have any one fail
def move_paths(paths, des):
    failure = []
    if type(paths) is list:
        for path in paths:
            if move_a_path(path, des) != 0:
                failure.append(path)
    else:
        if move_a_path(paths, des) != 0:
            failure.append(paths)
    return failure


# Input can be a glob name or a list of glob names
# Return 0 if all successfully
# Return list of failure if have anyone fail
def move_globs(globs, des):
    failure = []
    if type(globs) is list:
        for _glob in globs:
            failure += move_paths(glob.glob(_glob), des)
    else:
        failure = move_paths(glob.glob(globs), des)
    return failure


# Read a json file
# Return json object
def read_json(path):
    with open(path) as data:
        config = json.load(data)
        return config


# Write/Override json object to file
def write_json(obj, file_name):
    with open(file_name, "w") as my_file:
        my_file.write(json.dumps(obj, indent=4, sort_keys=True))


def write_bson(obj, file_name):
    """
    Write bson data to a json file.

    Parameters
    ----------
    obj : object
        Bson data
    file_name : str
        Output file name.

    """
    with open(file_name, "w") as my_file:
        my_file.write(obj)


def write_data_to_json_file(json_data, file_name):
    """
    Write json data to a json file.

    Parameters
    ----------
    json_data : object
        Json data
    file_name : str
        Output file name.

    """
    if json_data:
        write_json(json_data, file_name)
    else:
        write_json({}, file_name)


# Suffix file name
def suffix_file(file_name, suffix):
    split_name = file_name.split('.')
    split_name[0] = "{0}_{1}".format(split_name[0], suffix)
    return '.'.join(split_name)


# Write a line to file
def write_line(message, file_path, is_first_line=False):
    # [TODO] NamLD: disable for future
    # try:
    #     write_to_server(message)
    # except:
    #     pass

    try:
        if not os.path.isfile(file_path):
            mode = 'w'
        else:
            mode = 'a'
        with open(file_path, mode=mode) as my_file:
            if not is_first_line:
                my_file.write("\n")
            if type(message) is unicode:
                message = message.encode('utf-8')
            my_file.write(message)
            my_file.close()
        return 0
    except:
        return traceback.print_exc()


def _write_to_server(params, tag):
    conn = httplib.HTTPConnection(LoggingServer.host, LoggingServer.port)
    conn.request("POST", LoggingServer.url, json.dumps(params), LoggingServer.headers)
    response = conn.getresponse()
    del params[:]


def get_host_identify():
    hostname = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    address = s.getsockname()[0]
    s.close()
    return address, hostname


message_queue = []
MAX_QUEUE = 15


def write_to_server(message, tag="Mekong"):
    address, hostname = get_host_identify()
    params = {
        "log_tag": tag,
        "log_type": "DEBUG",
        "at_time": str(datetime.now()),
        "client_name": hostname,
        "client_address": address,
        "message": message
    }
    message_queue.append(params)

    if len(message_queue) > MAX_QUEUE:
        t = Timer(1, _write_to_server, [message_queue, tag])
        t.start()


# Overwrite a file if it exists
def write_text(content, file_path):
    try:
        with open(file_path, "w") as my_file:
            msg = content.encode("utf-8")
            my_file.write(msg)
            my_file.close()
        return 0
    except:
        return traceback.print_exc()


# Write log and also print to standard output
# Write and print
def write_log_and_print(message, file_path):
    print message
    msg = message.encode("utf-8")
    return write_line(msg, file_path)


def find_file_in_folders(file_name, folders):
    for folder in folders:
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path):
            return file_path

    error_msg = "File {0} does not found in {1}".format(file_name, folders)
    raise Exception(error_msg)


def remove_files_with_ext(folder, ext):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(ext):
                file_path = os.path.join(root, file)
                os.remove(file_path)


def copy_ignore_exists(src, dest):
    if not os.path.isdir(src):
        error_msg = "Source does not exists: {0}".format(src)
        raise Exception(error_msg)
    if not os.path.isdir(dest):
        error_msg = " Destination does not exists {0}".format(dest)
        raise Exception(error_msg)

    subprocess.call(['cp', '-rn', src, dest])


def list_all_file_in_folder_recusively(directory):
    """
    Query and return all files exists in the directory
    Parameters
    ----------
    directory: basestring
        path to directory need to get list of all file inside.

    Returns
    -------
    list
        list all files

    """
    file_list = list()
    for dirpath, dirnames, filenames in os.walk(directory):
        for file_name in filenames:
            abs_file_path = os.path.join(dirpath, file_name)
            rel_file_path = os.path.relpath(abs_file_path, directory)
            file_list.append(rel_file_path)

    return file_list

def get_test_set(test_folder):
    test_set = []
    for x in os.listdir(test_folder):
        test_set.append(x)
    return test_set
