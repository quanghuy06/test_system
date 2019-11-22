# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      25/06/2018
# Description:      This define abstract class of a worker.
import re
import os
from abc import ABCMeta, abstractmethod
from os.path import expanduser
from manager.lib_manager.mekong_client import MekongClient
import configs.common
from configs.git_resource import GITResource
from configs.svn_resource import SVNResource, DataPathSVN
from manager.lib_vm.defines import VBShareFolder
from baseapi.file_access import remove_paths

PLATFORMS_LABEL = "Platforms:"


class Worker(MekongClient):
    __metaclass__ = ABCMeta

    def __init__(self, platform, info_handler=None, **kwargs):
        """
        Constructor for abstract class for a worker. The worker could be a virtual machine, node
        or master

        Parameters
        ----------
        info_handler : ParametersHandler
            Parameters information for executing work
        platform : str
        """
        super(Worker, self).__init__(**kwargs)
        # In some case we know what should be done and no need information then parameters
        # information is not necessary. Currently, this information is required for build/test
        # and not require for data update on virtual machines
        self.info_handler = info_handler
        if self.info_handler and self.info_handler.is_et():
            self.get_working_platforms()
        self.platform = platform
        self.work_done = True
        self.home_dir = expanduser("~")
        self.svn_resource = SVNResource()
        self.svn_dir = os.path.join(self.home_dir, DataPathSVN.SVN_FOLDER)
        self.git_dir = os.path.join(self.home_dir, GITResource.GIT_FOLDER)

    def get_working_platforms(self):
        regex_str = "^{value}(.+)".format(value=PLATFORMS_LABEL)
        flags = re.M
        commit_message = self.info_handler.get_commit()
        filter_compiled = re.compile(regex_str, flags).search(commit_message)
        filter_value = None
        if filter_compiled:
            filter_value = filter_compiled.group(1)
        if filter_value:
            # Lower the filter
            filter_value = filter_value.lower()
            # Remove all space
            filter_value = filter_value.replace(" ", "")
            platforms = []
            for platform in filter_value.split(","):
                if platform in configs.common.SupportedPlatform:
                    platforms.append(platform)
            if platforms:
                configs.common.SupportedPlatform = platforms

    def init_svn_folder(self):
        if not os.path.isdir(self.svn_dir):
            os.makedirs(self.svn_dir)

    def init_git_folder(self):
        if not os.path.isdir(self.git_dir):
            os.makedirs(self.git_dir)

    @staticmethod
    def init_shared_folder():
        if os.path.isdir(VBShareFolder.NAME):
            remove_paths(VBShareFolder.NAME)
        os.makedirs(VBShareFolder.NAME)

    @abstractmethod
    def do_work(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
