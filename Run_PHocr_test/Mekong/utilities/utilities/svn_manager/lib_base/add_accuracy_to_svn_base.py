# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      08/08/2018
# Description:      This file define base class for function add bounding box accuracy report to svn

import os
import shutil
import sys_path
import subprocess
sys_path.insert_sys_path()

from svn_manager.SVN_common import SVN_manager
from svn_manager.defines import SVN
from svn import remote, local


class AddAccuracyToSVN:
    @staticmethod
    def add_accuracy_report_to_svn(file_name, accuracy_url):
        # Check if file does not exist then return
        if not os.path.exists(file_name):
            print("WARN: No such file {file_name}".format(file_name=file_name))
            return False
        # Create temporary place to contain repository
        current_dir = os.getcwd()
        tmp_path = os.path.join(current_dir, "tmp")
        if os.path.exists(tmp_path):
            shutil.rmtree(tmp_path)
        os.mkdir(tmp_path)

        svn_manager = SVN_manager()
        svn_user = svn_manager.get_user()
        svn_pass = svn_manager.get_pass()
        # Checkout a remote repository
        r = remote.RemoteClient(accuracy_url, svn_user, svn_pass)
        r.checkout(tmp_path)
        l = local.LocalClient(tmp_path, svn_user, svn_pass)

        # Get file accuracy report to add to SVN
        if os.path.exists(file_name):
            shutil.copy(file_name, tmp_path)
            os.chdir(tmp_path)
            cm_add_file = "Add file {0} to SVN.".format(file_name)
            cm_update_file = "Update file {0} to SVN.".format(file_name)
            acc_file_to_add = os.path.join(tmp_path, file_name)
            list_add = list()
            list_add.append(acc_file_to_add)

            # Get status of file will be commited
            cmd = "svn status {0}".format(file_name)
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            stdout = process.communicate()[0]
            status = stdout.split(" ")[0]

            if status == SVN.status.UNVERSIONED:
                l.add(acc_file_to_add)
                l.commit(cm_add_file, list_add)
            if status == SVN.status.ADDED:
                l.commit(cm_add_file, list_add)
            if status == SVN.status.MODIFIED:
                l.commit(cm_update_file, list_add)
            os.chdir(current_dir)
            return True
        else:
            os.chdir(current_dir)
            print("Don't have Bounding box accuracy report file generated!")
            return False


