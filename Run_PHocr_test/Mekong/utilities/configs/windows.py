import re
import platform
from configs.common import Platform


class WindowsCmd:
    PYTHON = "C:/Python27/python.exe"
    GIT_PATH = "C:/Program\ Files/Git/bin/git.exe"
    GIT_RESET = "git clean -fdx && git reset --hard"
    VM_LIST_ALL = "vboxmanage list vms"
    VM_LIST_RUNNING = "vboxmanage list runningvms"
    SVN_UPDATE = "svn update"
    MOUNT_SHARE_FOLDER = r"net use {0} \\\\VBOXSVR\\{1}"

    @staticmethod
    def git_merge(project_path):
        return "cd {0} && {1} checkout master && {1} merge FETCH_HEAD".format(project_path, WindowsCmd.GIT_PATH)


class WindowsPath:
    PROGRAMDATA_PATH = "C:/ProgramData"
    USERS_PATH = "C:/Users"
    SHARED_DRIVE = "Z:"

class WindowsUtils:

    @staticmethod
    def is_windows_absolute_path(path):
        # We can determine by check if the first of path contain
        # {Drive}: format, ex: C:, D:, Z:
        drive_pattern = re.compile('^[A-z]:')
        return drive_pattern.search(path) != None

    @staticmethod
    def is_running_on_windows():
        """
        Check is current machine is Windows OS?

        Returns
        -------
        bool
            True if current machine runs Windows OS
            False if current machine not run Windows OS
        """
        return platform.system().lower() == Platform.WINDOWS
