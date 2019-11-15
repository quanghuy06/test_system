# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      31/03/2017
# Last update:      26/07/2107
# Updated by:       Phung Dinh Tai
# Description:      This file implements functions for work on file/folder
import os
import pexpect
from baseapi.file_access import remove_paths
# Input need to be a single
# Silent mode, if do fail only return value. Return 0 if successfully
# Fail -> return trace back information


def linux_move(src_path, des_path, timeout=300):
    cmd = "mv {src} {des}".format(src=src_path, des=des_path)
    pexpect.run(command=cmd, timeout=timeout)


def linux_tar_file_tgz(src_folder, des_file, timeout=300):
    cmd = "tar czf {des} {src}".format(des=des_file, src=src_folder)
    pexpect.run(command=cmd, timeout=timeout)


def linux_rename_dir(src_path, new_name, timeout=300):
    dir_name = os.path.dirname(src_path)
    des_path = os.path.join(dir_name, new_name)
    if os.path.exists(des_path):
        remove_paths(des_path)
    cmd = "mv {src} {des}".format(src=src_path, des=des_path)
    pexpect.run(command=cmd, timeout=timeout)


def linux_extract_tgz_file(src_file, des_path=None, timeout=300):
    cmd = "tar xzf {src}".format(src=src_file)
    if des_path:
        cmd += " -C {des}".format(des=des_path)
    pexpect.run(command=cmd, timeout=timeout)


def linux_copy_ignore_exist(src, des, timeout=300):
    cmd = "cp -rn {0} {1}".format(src, des)
    child = pexpect.spawn(command=cmd, timeout=timeout)
    child.expect(pexpect.EOF)
    if child.exitstatus:
        raise Exception("Failed to run command: {cmd}\n{msg}".format(cmd=cmd, msg=child.before))
