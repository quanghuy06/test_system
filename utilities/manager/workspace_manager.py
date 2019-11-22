# Author : Phung Dinh Tai
# Email: tai.phungdinh@toshiba-tsdv.com
# Date created: 10/11/2016
# Last update: 14/11/2016
# Project: ocrpoc
# Description: This cript can be used to create, delete, mount, unmount workspace.
import sys_path
sys_path.insert_sys_path()

import argparse
import os
import pexpect

from manager.lib_manager.samba_base import SambaManager
from configs.workspace import WorkSpaceConfig
from configs.samba import SmbConfig


def parse_argument() :
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', "--username", required = True,
                        help = "Username to access samba server")
    parser.add_argument('-p', "--password", required = True,
                        help = "Password to access samba server")
    parser.add_argument('-w', "--workspace",
                        help = "Name of workspace")
    parser.add_argument('-m', "--mount-point",
                        help = "Where you want to mount workspace on your machine")
    parser.add_argument("--mount", default = False, action = "store_true",
                        help = "Use this flag to mount an existed workspace")
    parser.add_argument("--unmount", default = False, action = "store_true",
                        help = "Use this flag to unmount a workspace")
    parser.add_argument("--create", default = False, action = "store_true",
                        help = "Use this flag to create a workspace")
    parser.add_argument("--delete", default = False, action = "store_true",
                        help = "Use this flag to delete a workspace")
    parser.add_argument("--list", default = False, action = "store_true",
                        help = "List all workspace on samba share of developer")
    parser.add_argument("--link-mode", default = False, action = "store_true",
                        help = "Use for develop machine Ubuntu 10.04")
    return parser

def mount_workspace(samba_manager, workspace_name, mount_point) :
    # Check workspace exists on samba
    if not samba_manager.check_folder_exists(workspace_name) :
        print "Workspace {0} does not exist on samba share".format(workspace_name)
        exit()
    # Check if workspace is mounted
    smb_dir_bak = samba_manager.cwd
    if smb_dir_bak :
        smb_cwd = os.path.join(smb_dir_bak, workspace_name)
    else :
        smb_cwd = workspace_name
    samba_manager.change_cwd(smb_cwd)
    mount_result = samba_manager.mount(mount_point, True, False, True)
    # Alternatives :
    # "_MOUNTED_" : workspace has already mounted to mount point -> print message then exit
    # True : mount successfully
    samba_manager.change_cwd(smb_dir_bak)
    if mount_result == "_MOUNTED_" :
        print "Workspace {0} has already mounted to {1}".format(workspace_name, mount_point)
        exit()
    print "Workspace {0} has been mounted successfully".format(workspace_name)
    print "Mount point: {0}".format(mount_point)
    return mount_point

# The following function will be used on Ubuntu 10.04, because the release does not support
# directory mounting, you can only mount disk
def mount_workspace_link(samba_manager, workspace_name, link = True, interactive = True) :
    default_mp = os.path.join(WorkSpaceConfig.DEFAULT_MP, samba_manager.disk)
    if not samba_manager.cwd :
        # Samba share path : //server/username/workspace (username is samba disk name)
        ws_mount_path = os.path.join(default_mp, workspace_name)
    else :
        # Samba share path : //server/disk/smb_cwd/username/workspace
        ws_mount_path = os.path.join(default_mp, samba_manager.cwd)
        ws_mount_path = os.path.join(ws_mount_path, workspace_name)
    link_path = os.path.join(WorkSpaceConfig.DEFAULT_WS, workspace_name)
    # Check workspace exists on samba
    if not samba_manager.check_folder_exists(workspace_name) :
        print "Workspace {0} does not exist on samba share".format(workspace_name)
        exit()
    # Check link path
    if link :
        # Check link path
        child = pexpect.spawn("ls -l", cwd = WorkSpaceConfig.DEFAULT_WS)
        for line in child :
            if (line.find("{0} ".format(workspace_name)) >= 0) and\
                    (line.find(" {0}".format(ws_mount_path)) >= 0) :
                print "Workspace {0} has already mounted to {1}".format(workspace_name, link_path)
                exit()
        if os.path.exists(link_path) :
            if interactive :
                print "Path {0} already existed and not mounted right!".format(link_path)
                ans = raw_input("Do you want to delete and continue (Y/N)? ")
                if ((ans == "y") or (ans == "Y")) :
                    pexpect.run("rm -r {0}".format(workspace_name), cwd = WorkSpaceConfig.DEFAULT_WS)
                else :
                    exit()
            else :
                pexpect.run("rm -r {0}".format(workspace_name), cwd = WorkSpaceConfig.DEFAULT_WS)
    mount_check = samba_manager.mount(default_mp, False, False, True)
    if isinstance(mount_check, list) :
        print "Mount workspace {0} fail\n{1}".format(workspace_name, mount_check)
        exit()
    if link :
        # Check link path if mounted
        if not os.path.isdir (link_path) :
            pexpect.run("ln -s {0} {1}".format(ws_mount_path, link_path))
        print "Workspace {0} mounted successfully!".format(workspace_name)
        print "Mount point: {0}".format(link_path)
    return link_path

def delete_workspace(samba_manager, workspace_name, link_mode = False, debug = True, force = False) :
    # samba_manager.cwd need to be parent of workspaces
    if not samba_manager.check_folder_exists(workspace_name) :
        if debug :
            print "Workspace {0} does not exist on samba share".format(workspace_name)
        if force :
            return "_WS_NOT_EXIST_"
        exit()
    if not link_mode :
        # Check if workspace is mounted on client machine -> delete mount points if empty
        smb_dir_bak = samba_manager.cwd
        if smb_dir_bak :
            smb_path = os.path.join(smb_dir_bak, workspace_name)
        else :
            smb_path = workspace_name
        samba_manager.change_cwd(smb_path)
        unmount_result = samba_manager.unmount(None, False, True)
        # Alternatives :
        # "_NOT_MOUNTED_" -> do nothing, continue
        # err_msg: str -> force
        # mount_points: list -> delete if empty
        if isinstance(unmount_result, list) :
            for mp in unmount_result :
                if len(os.listdir(mp)) == 0 :
                    split_path = os.path.split(mp)
                    pexpect.run("rmdir {0}".format(split_path[1]), cwd = split_path[0])
        samba_manager.change_cwd(smb_dir_bak)
        # Delete folder on samba
        samba_manager.delete_folder(workspace_name, False)
    else :
        # Link mode: mount disk and create soft link to workspace
        # Check workspace exists on samba
        default_mp = os.path.join(WorkSpaceConfig.DEFAULT_MP, samba_manager.disk)
        link_path = os.path.join(WorkSpaceConfig.DEFAULT_WS, workspace_name)
        # Check if workspace is linked
        if os.path.isdir(link_path) :
            pexpect.run("rm {0}".format(link_path))
        # Check mount point
        if not samba_manager.check_mount_point(default_mp) :
            samba_manager.mount(default_mp, False, False)
        pexpect.run("rm -r {0}".format(workspace_name), cwd = default_mp)
    if debug :
        print "Delete workspace {0} successfully".format(workspace_name)


def create_workspace(samba_manager, workspace_name, mount_point, link_mode = False) :
    # samba_manager.cwd need to be parent of workspaces
    if not link_mode :
        # Create workspace
        samba_manager.create_folder(workspace_name, True, False)
    else :
        # Check if folder already exists on samba share
        if samba_manager.check_folder_exists(workspace_name) :
            ans = raw_input("Folder {0} has already existed on samba share!"
                            " Do you want to override (Y/N) ? ".format(workspace_name))
            if (ans == "y") or (ans == "Y") :
                delete_workspace(samba_manager, workspace_name, True, False, True)
            else :
                exit()
        samba_manager.create_folder(workspace_name, False, False)
    smb_dir_bak = samba_manager.cwd
    if not smb_dir_bak :
        smb_dir = workspace_name
    else :
        smb_dir = os.path.join( samba_manager.cwd, workspace_name)
    print "Creating..."
    samba_manager.change_cwd(smb_dir)
    samba_manager.create_folder(WorkSpaceConfig.SRC, False, False)
    samba_manager.create_folder(WorkSpaceConfig.UTILITY, False, False)
    samba_manager.create_folder(WorkSpaceConfig.TEST_CASE, False, False)
    samba_manager.create_folder(WorkSpaceConfig.REVIEW, False, False)
    samba_manager.change_cwd(smb_dir_bak)
    print "Create workspace {0} successfully".format(workspace_name)
    print "Mounting..."
    if not link_mode :
        mp = mount_workspace(samba_manager, workspace_name, mount_point)
    else :
        mp = mount_workspace_link(samba_manager, workspace_name, True, True)
    utilities_folder = os.path.join(mp, WorkSpaceConfig.UTILITY)
    pexpect.run(WorkSpaceConfig.CMD_GET_UTILITY, cwd = utilities_folder)

def unmount_workspace(samba_manager, workspace_name, link_mode) :
    # Check workspace exists on samba
    if not samba_manager.check_folder_exists(workspace_name) :
        print "Workspace {0} does not exist on samba share".format(workspace_name)
        exit()
    if not link_mode :
        # Check if workspace is mounted
        smb_dir_bak = samba_manager.cwd
        if smb_dir_bak :
            smb_cwd = os.path.join(smb_dir_bak, workspace_name)
        else :
            smb_cwd = workspace_name
        samba_manager.change_cwd(smb_cwd)
        samba_manager.unmount()
        samba_manager.change_cwd(smb_dir_bak)
    else :
        link_path = os.path.join(WorkSpaceConfig.DEFAULT_WS, workspace_name)
        if os.path.isdir(link_path) :
            pexpect.run("rm {0}".format(link_path), cwd = WorkSpaceConfig.DEFAULT_WS)
            print "Workspace {0} unmounted successfully".format(workspace_name)
        else :
            print "Workspace {0} is not mounted".format(workspace_name)

def check_workspace_structure(samba_manager, workspace_name, debug = True) :
    if not samba_manager.check_folder_exists(workspace_name) :
        if debug :
            print "Workspace {0} does not exist".format(workspace_name)
        return "_NOT_EXIST_"
    else :
        result = True
        smb_dir_bak = samba_manager.cwd
        if smb_dir_bak :
            smb_cwd = os.path.join(smb_dir_bak, samba_manager.username)
            smb_cwd = os.path.join(smb_cwd, workspace_name)
        else :
            if SmbConfig.DISK:
                smb_cwd = os.path.join(samba_manager.username, workspace_name)
            else :
                smb_cwd = workspace_name
        samba_manager.change_cwd(smb_cwd)
        if not samba_manager.check_folder_exists(WorkSpaceConfig.SRC) :
            result = False
        if not samba_manager.check_folder_exists(WorkSpaceConfig.TEST_CASE) :
            result = False
        if not samba_manager.check_folder_exists(WorkSpaceConfig.REVIEW) :
            result = False
        if not samba_manager.check_folder_exists(WorkSpaceConfig.UTILITY) :
            result = False
        samba_manager.change_cwd(smb_dir_bak)
        return result

def list_workspace(samba_manager, username) :
    smb_dir_bak = samba_manager.cwd
    path = ""
    if smb_dir_bak :
        # Path to user folder on samba: //server/disk/cwd/username
        path = os.path.join(smb_dir_bak, samba_manager.username)
    else :
        # Path to user folder on samba: //server/disk/username
        if SmbConfig.DISK :
            path = username
    default_mp = os.path.join(WorkSpaceConfig.DEFAULT_MP, username)
    samba_manager.mount(default_mp, False, False, True)
    if not path :
        path = default_mp
    else :
        path = os.path.join(default_mp, path)
    list_dirs = os.listdir(path)
    no_ws = True
    for directory in list_dirs :
        abs_dir = os.path.join(path, directory)
        if (os.path.isdir(abs_dir) and check_workspace_structure(samba_manager, directory, True)):
            print directory
            no_ws = False
    if no_ws :
        print "User {0} has no workspace on samba share".format(samba_manager.username)

def main() :
    # Check input of main
    parser = parse_argument()
    args = parser.parse_args()
    flag_count = 0 
    if args.mount :
        flag_count += 1
    if args.unmount :
        flag_count += 1
    if args.create :
        flag_count += 1
    if args.delete :
        flag_count += 1
    if args.list :
        flag_count += 1
    if flag_count >=2 :
        print "You can not combine multiple flag in a command"
        print parser.print_help()
        exit()
    # Get samba manager parameter
    if SmbConfig.DISK :
        disk = SmbConfig.DISK
        username = SmbConfig.USERNAME
        password = SmbConfig.PASSWORD
        samba_manager_check = SambaManager(SmbConfig.SERVER, username, password,
                                           disk, SmbConfig.DIRECTORY)
        if not samba_manager_check.check_folder_exists(args.username) :
            samba_manager_check.create_folder(args.username)
        if SmbConfig.DIRECTORY :
            # samba working path: //server/disk/directory/username
            smb_cwd = os.path.join(SmbConfig.DIRECTORY, args.username)
        else :
            # samba working path: //server/disk/username
            smb_cwd = args.username
    else :
        # Name of disk as username
        disk = args.username
        username = args.username
        password = args.password
        # samba working directory: //server/username
        smb_cwd = ""
    samba_manager = SambaManager(SmbConfig.SERVER, username, password, disk, smb_cwd)
    if args.list :
        list_workspace(samba_manager, args.username)
        exit()
    link_mode = args.link_mode
    import platform
    release = platform.release()
    if release.find("2.6") >= 0:
        link_mode = True
    # Mount workspace to client machine
    if not args.mount_point:
        mount_point = os.path.join( WorkSpaceConfig.DEFAULT_WS, args.workspace)
    else :
        mount_point = args.mount_point
    # Create workspace
    if args.create :
        create_workspace(samba_manager, args.workspace, mount_point, link_mode)
        exit()
    if args.mount :
        if not link_mode :
            mount_workspace(samba_manager, args.workspace, mount_point)
        else :
            mount_workspace_link(samba_manager, args.workspace)
        exit()
    if args.unmount :
        unmount_workspace(samba_manager, args.workspace, link_mode)
        exit()
    if args.delete :
        delete_workspace(samba_manager, args.workspace, link_mode)
        exit()
    print "You don't pass any flag!"
    parser.print_help()

if __name__ == "__main__":
    main()
