# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      25/06/2018
# Description:      This script define class for a virtual machine that build
#                   PHOcr on linux platform.
import os
import sys
from abc import ABCMeta
from manager.lib_manager.workers_manager_class import WorkersManager
from baseapi.file_access import remove_paths
from baseapi.linux_file_access import linux_move
from configs.svn_resource import DataPathSVN
from utils.svn_helper import SVNHelper


class WorkersBuildManager(WorkersManager):
    __metaclass__ = ABCMeta

    def __init__(self, is_build_release=False, **kwargs):
        """
        Constructor for virtual machine management of build. This class is used for all build tasks:
        build a release package for normal testing using ICC, build a release package for memory
        leak checking using GCC, build a debug package for make sure debug work.

        Parameters
        ----------
        is_build_release : bool
            Build a release package of latest version on original master for release
        """
        self.is_build_release = is_build_release
        super(WorkersBuildManager, self).__init__(**kwargs)
        # Parameters information is required for build process
        if not self.info_handler:
            print("Missing parameters information for executing build")
            sys.exit(self.ERR_NO_MISSING_PARAMETERS)
        self.result_node_folder = os.path.join(os.getcwd(), "build_results_" + self.name)

    def prepare_work(self):
        """
        Prepare some data before managing work processes such as clean old data, update new data
        which required for build.

        Returns
        -------

        """
        self.logger.start_step("Prepare for build")
        if os.path.isdir(self.result_node_folder):
            remove_paths(self.result_node_folder)

        # Update package for build Hanoi
        self.update_phocr_hanoi_3rdparty()

        self.logger.end_step(True)

    def update_phocr_hanoi_3rdparty(self):
        """
        Update svn to get the newest package which is used for build Hanoi.

        """

        self.logger.start_step("Update 3rd party of PHOcr and Hanoi.")
        phocr_hanoi_3rdparty_url = \
            self.svn_resource.get_url(DataPathSVN.PHOCR_HANOI_3RDPARTY)
        phocr_hanoi_3rdparty_svn = \
            os.path.join(self.svn_dir,
                         DataPathSVN.PHOCR_HANOI_3RDPARTY)
        svn_helper = SVNHelper(phocr_hanoi_3rdparty_url,
                               phocr_hanoi_3rdparty_svn)

        if not svn_helper.is_checkouted():
            svn_helper.checkout()
        else:
            svn_helper.update()
        self.logger.end_step(True)

    def post_process(self):
        """
        Get log and arrange final results folder. Also generate profiling data for execution time
        of automation test system.

        Returns
        -------
        None

        """
        self.logger.start_step("Arrange build results from build virtual machines")
        # Create final build result folder
        if not os.path.isdir(self.result_node_folder):
            os.makedirs(self.result_node_folder)
        # Arrange build folder
        for worker in self.workers:
            phocr_build_package = worker.get_final_phocr_build_package_name()
            self.get_build_package(worker, phocr_build_package)
            hanoi_build_package = worker.get_final_hanoi_installer_name()
            if os.path.exists(hanoi_build_package):
                self.get_build_package(worker, hanoi_build_package)
        self.logger.end_step(True)

        # All processes done. Generate execution time data of system to json file. This data can
        # be used to analyze performance of test system.
        self.generate_execution_time_data()

    def get_workers(self):
        """
        Create objects which help run work on workers. List of workers base on system
        configuration in profile config.

        Returns
        -------
        None

        """
        # Create worker objects base on system configuration
        workers = self.profile_handler.get_vm_build_of_node(self.name)

        # Set up build a release version
        if self.is_build_release:
            for worker in workers:
                worker.is_release_build = True
        return workers

    def combine_results_when_worker_not_done_exception(self):
        """
        When any build node fails, just leave it as system failed.
        No try to be done.

        Returns
        -------
        None

        """
        pass

    def get_build_package(self, worker, build_package):
        """
        Get build package (It may be Hanoi package or PHOcr package)

        Parameters
        ----------
        worker:
             Each worker is a virtual machine.
        build_package: str
             Build package name

        """
        if os.path.exists(build_package):
            linux_move(build_package, self.result_node_folder)
        else:
            self.logger.log_and_print("Can't find {0} build package of {1}"
                                      .format(worker.platform,
                                              worker.name))
