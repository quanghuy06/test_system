# Author : Phung Dinh Tai
# Email: tai.phungdinh@toshiba-tsdv.com
# Date created: 09/11/2016
# Last update: 10/11/2016
# Project: ocrpoc
# Description: This cript defines SambaManager class that can be used to do
#              some activities when you work with samba share on Linux.
#              Such as: create folder, delete folder, mount, unmount, check mounted,
#              check if file or folder exist.

import argparse
import pexpect
import getpass
import os

#Check input
def check_input(name, var) :
    if not var :
        print "Missing {0}".format(name)
        exit()

class SambaManager:
    def __init__(self, server, username, password, disk, smb_directory = None):
        self.server = server
        self.disk = disk
        self.smb_disk_path = "//{0}/{1}".format(self.server, self.disk)
        self.smb_directory = smb_directory
        self.username = username
        self.password = password
        self.curr_user = getpass.getuser()
        self.sudo_pwd = ""
        if not self.smb_directory :
            self.smb_path = "//{0}/{1}".format(self.server, self.disk)
            self.smbdir_opt = ""
        else :
            self.smb_path = "//{0}/{1}/{2}".format(self.server, self.disk, self.smb_directory)
            self.smbdir_opt = "--directory " + self.smb_directory
        # Check input
        check_input("server name or ip", self.server)
        check_input("username", self.username)
        check_input("password", self.password)
        check_input("disk", self.disk)
        child = pexpect.spawn("smbclient {0} {1} -U {2}%{3} -c \"ls\"".format(self.smb_disk_path, self.smbdir_opt, self.username, self.password))
        for line in child :
            if line.find("NT_STATUS_BAD_NETWORK_NAME") >= 0 :
                child.close()
                print "Bad network name! Disk name incorrect!"
                print "Please use this command to see which disk available\n\"smbclient -L [server]\" "
                exit()
            if line.find("NT_STATUS_ACCESS_DENIED") >= 0 :
                child.close()
                print "Access denied! Username incorrect!"
                exit()
            if line.find("NT_STATUS_LOGON_FAILURE") >= 0 :
                child.close()
                print "Authencation fail! Password incorrect!"
                exit()
            if line.find("NT_STATUS_OBJECT_NAME_NOT_FOUND") >= 0 :
                child.close()
                print "Directory {0} does not exist!".format(self.smb_directory)
                exit()
            if line.find("NT_STATUS_IO_TIMEOUT") >= 0 :
                child.close()
                print "Connection to server {0} failed!".format(self.server)
                exit()
        child.close()

    # Mount disk to client machine
    def mount(self, mount_point, mount_directory = False, debug = True) :
        if not self.sudo_pwd :
            if debug :
                print "Mount disk..."
            sudo_pwd = raw_input("[sudo] password for {0}: ".format(self.curr_user))
            self.sudo_pwd = sudo_pwd
        if mount_directory :
            smb_path = self.smb_path
        else :
            smb_path = self.smb_disk_path
        child = pexpect.spawn("sudo mount -t cifs {0} {1} -o \"username={2},password={3},uid={4},gid=sudo\"".format(smb_path, mount_point, self.username, self.password, self.curr_user))
        child.expect("password")
        child.sendline(self.sudo_pwd)
        err_msg = ""
        for line in child :
            if line.find("mount:") >= 0 :
                err_msg += "{0}".format(line)
        if err_msg :
            print err_msg
            if debug :
                print "Can not mount samba share path to your machine!"
            exit()
        child.close()
        if debug :
            print "Mount {0} successfully!".format(self.smb_path)
            print "Mount point: {0}".format(mount_point)

    # Unmount
    def unmount(self, mount_point = None, debug = True) :
        if not mount_point :
            mount_point = self.check_mounted()
            if not mount_point :
                print "Directory {0} is not mounted".format(self.smb_path)
                exit()
        if not self.sudo_pwd :
            if debug :
                print "Unmount {0}...".format(mount_point)
            sudo_pwd = raw_input("[sudo] password for {0}: ".format(self.curr_user))
            self.sudo_pwd = sudo_pwd
        child = pexpect.spawn("sudo umount {0}".format(mount_point))
        child.expect("password")
        child.sendline(self.sudo_pwd)
        err_msg = ""
        for line in child :
            if line.find("umount:") >= 0 :
                err_msg += "{0}\n".format(line)
        if err_msg :
            print err_msg
            if debug :
                print "Can not unmount {0}".format(mount_point)
            exit()
        child.close()
        if debug :
            print "{0} unmounted successfully!".format(mount_point)

    # Check if a file exists on samba share
    def check_file_exists(self, file_name) :
        child = pexpect.spawn("smbclient //{0}/{1} {2} -U {3}%{4} -c \"ls\"".format(self.server, self.disk, self.smbdir_opt, self.username, self.password))
        for line in child :
            if (line.find("{0} ".format(file_name)) >= 0) and ((line.find(" A ") >= 0) or (line.find(" N ") >= 0)):
                child.close()
                return True
        child.close()
        return False

    # Check if a folder exists on samba share
    def check_folder_exists(self, folder_name) :
        child = pexpect.spawn("smbclient //{0}/{1} {2} -U {3}%{4} -c \"ls\"".format(self.server, self.disk, self.smbdir_opt, self.username, self.password))
        for line in child :
            if (line.find("{0} ".format(folder_name)) >= 0) and (line.find(" D ") >= 0) :
                child.close()
                return True
        child.close()
        return False

    # Check if samba path is mounted
    def check_mounted(self) :
        with open("/proc/mounts","r") as myfile :
                for line in myfile.readlines():
                    if line.find(self.smb_path) >= 0 :
                        be = line.find(" /") + 1
                        en = line.find(" cifs")
                        mount_point = line[be:en]
                        return mount_point
        return ""

    # Check if a folder on local is mounted
    def check_mount_point(self, folder_name, debug = True) :
        # Check if folder exists
        if not os.path.exists(folder_name) :
            if debug :
                print "Folder {0} does not exist!".format(folder_name)
            exit()
        abs_path = os.path.abspath(folder_name)
        with open("/proc/mounts","r") as myfile :
                for line in myfile.readlines():
                    if line.find(abs_path) >= 0 :
                        sp = line.find(" /")
                        smb_path = line[:sp]
                        return smb_path
        return ""

    # Delete a folder on samba share
    def delete_folder(self, folder_name, debug = True) :
        # Check if folder exists on samba share
        if not self.check_folder_exists(folder_name) :
            if debug :
                print "Folder {0} does not exist on samba share!".format(folder_name)
            exit()
        # Use temporary folder to mount disk
        temp_folder = "delete_samba_folder_temp~"
        # Check if temporary folder exists. If existed -> delete
        if os.path.exists(temp_folder) :
            # Check if temporary folder is mounted
            if self.check_mount_point(temp_folder) :
                self.unmount(temp_folder, False)
            os.rmdir(temp_folder)
        os.makedirs(temp_folder)
        self.mount(temp_folder, False, False)
        if self.smb_directory :
            local_cwd = os.path.join(temp_folder, self.smb_directory)
        else :
            local_cwd = temp_folder
        child = pexpect.spawn("rm -r {0}".format(folder_name), cwd = local_cwd)
        for line in child :
            print line
        self.unmount(temp_folder, False)
        os.rmdir(temp_folder)
        if debug :
            print "Delete folder {0} successfully!".format(folder_name)

    # Create a folder on samba share
    def create_folder(self, folder_name, interactive = True, debug = True) :
        # Check if folder already exists on samba share
        if self.check_folder_exists(folder_name) :
            if interactive :
                ans = raw_input("Folder {0} has already existed on samba share! Do you want to override (Y/N) ? ".format(folder_name))
                if (ans == "y") or (ans == "Y") :
                    self.delete_folder(folder_name, False)
                else :
                    exit()
            else :
                print "Folder {0} has already existed and will be overrided!".format(folder_name)
                self.delete_folder(folder_name)
        pexpect.run("smbclient {0} {1} -U {2}%{3} -c \"mkdir {4}\"".format(self.smb_disk_path, self.smbdir_opt, self.username, self.password, folder_name))
        if debug :
            print "Create folder {0}/{1} successfully!".format(self.smb_path, folder_name)

    # Get folder from samba share
    def get_folder(self, folder_name, output, interactive = True, debug = True) :
        # Check if folder exists on samba share
        if not self.check_folder_exists(folder_name) :
            if debug :
                print "Folder {0} does not exists on samba share!".format(folder_name)
            exit()
        # Check if output folder exists on client machine
        local_path = ""
        if not output :
            local_path = folder_name
        else :
            if not os.path.exists(output) :
                if debug :
                    print "Directory {0} does not exist!".format(output)
                exit()
            else :
                local_path = os.path.join(output, folder_name)
        if os.path.exists(local_path) :
            if interactive :
                ans = raw_input("Folder {0} has already existed! Do you want to override (Y/N) ? ".format(local_path))
                if (ans == "y") or (ans == "Y") :
                    abs_path = os.path.abspath(local_path)
                    path_split = os.path.split(abs_path)
                    pexpect.run("rm -r {0}".format(path_split[1]), cwd = path_split[0])
                else :
                    exit()
            else :
                if debug :
                    print "Folder {0} has already existed and will be overrided!".format(local_path)
                path_split = os.path.split(output)
                pexpect.run("rm -r {0}".format(path_split[1]), cwd = path_split[0])
        os.makedirs(local_path)
        # Get folder from samba share
        if debug :
            print "Getting folder {0} ...".format(folder_name)
        if not self.smbdir_opt :
            smbdir_opt = "--directory {0}".format(folder_name)
        else :
            smbdir_opt = "{0}/{1}".format(self.smbdir_opt, folder_name)
        pexpect.run("smbclient {0} {1} -U {2}%{3} -c \"prompt OFF; recurse ON; mget *\"".format(self.smb_disk_path, smbdir_opt, self.username, self.password), cwd = local_path)
        if debug :
            print "Get folder {0} successfully!".format(folder_name)

    # Get file from samba share
    def get_file(self, file_name, output, interactive = True) :
        # Check if file exists on samba share
        if not self.check_file_exists(file_name) :
            print "File {0} does not exist on samba share!".format(file_name)
            exit()
        # Check if output folder exists on client machine
        if output :
            if not os.path.exists(output) :
                print "Directory {0} does not exist!".format(output)
                exit()
            else :
                local_file_path = os.path.join(output, file_name)
        else :
            local_file_path = file_name
        # Check if file already 
        if os.path.exists(local_file_path) :
            if interactive :
                ans = raw_input("File {0} has already existed! Do you want to override (Y/N) ? ".format(local_file_path))
                if not ((ans == "y") or (ans == "Y")) :
                    exit()
            else :
                print "File {0} has already existed and will be overrided!".format(local_file_path)
        # Get file from samba share
        print "Getting file {0} ...".format(file_name)
        if not output :
            pexpect.run("smbclient {0} {1} -U {2}%{3} -c \"prompt OFF; get {4}\"".format(self.smb_disk_path, self.smbdir_opt, self.username, self.password, file_name))
        else :
            pexpect.run("smbclient {0} {1} -U {2}%{3} -c \"prompt OFF; get {4}\"".format(self.smb_disk_path, self.smbdir_opt, self.username, self.password, file_name), cwd = output)
        print "Get file {0} successfully!".format(file_name)

    # Put folder to samba share
    def put_folder(self, local_folder_path, interactive = True, debug = True) :
        # Check if folder exists on local
        if not os.path.isdir(local_folder_path) :
            if debug :
                print "Folder {0} does not exist!".format(local_folder_path)
            exit()
        # Split folder name and local_cwd
        abs_path = os.path.abspath(local_folder_path)
        split_path = os.path.split(abs_path)
        folder_name = split_path[1]
        # Create folder name on samba share
        self.create_folder(folder_name, interactive, False)
        # Put local to samba share
        if not self.smbdir_opt :
            smbdir_opt = "--directory {0}".format(folder_name)
        else :
            smbdir_opt = "{0}/{1}".format(self.smbdir_opt, folder_name)
        pexpect.run("smbclient {0} {1} -U {2}%{3} -c \"prompt OFF; recurse ON; mput *\"".format(self.smb_disk_path, smbdir_opt, self.username, self.password), cwd = local_folder_path)
        if debug :
            print "Put folder {0} successfully!".format(folder_name)

    # Put a file to samba share
    def put_file(self, local_file_path, interactive = True, debug = True) :
        # Check if file exists on local
        if not os.path.isfile(local_file_path) :
            if debug :
                print "File {0} does not exist!".format(local_file_path)
            exit()
        # Split file name and cwd
        abs_path = os.path.abspath(local_file_path)
        split_path = os.path.split(abs_path)
        local_cwd = split_path[0]
        file_name = split_path[1]
        # Check if file exists on samba share
        if self.check_file_exists(file_name) :
            if interactive :
                ans = raw_input("File {0} has already existed! Do you want to override (Y/N) ? ".format(file_name))
                if not ((ans == "y") or (ans == "Y")) :
                    exit()
            else :
                if debug :
                    print "File {0} has already existed on samba share and will be overrided".format(file_name)
        pexpect.run("smbclient {0} {1} -U {2}%{3} -c \"prompt OFF; put {4}\"".format(self.smb_disk_path, self.smbdir_opt, self.username, self.password, file_name), cwd = local_cwd)
        if debug :
            print "Put file {0} successfully!".format(file_name)

    # Change working directory on samba
    def change_working_directory(self, directory) :
        self.smb_directory = directory
        if not self.smb_directory :
            self.smb_path = "//{0}/{1}".format(self.server, self.disk)
            self.smbdir_opt = ""
        else :
            self.smb_path = "//{0}/{1}/{2}".format(self.server, self.disk, self.smb_directory)
            self.smbdir_opt = "--directory " + self.smb_directory

    # Change working directory to disk on samba
    def change_cwd_disk(self) :
        self.smb_directory = ""
        self.smb_path = "//{0}/{1}".format(self.server, self.disk)
        self.smbdir_opt = ""
