# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      26/06/2018
# Description:      This script define base class for a build node.
import os
import re
from manager.lib_manager.nodes_manager_class import NodesManager
from configs.test_result import FinalTestResult
from baseapi.file_access import move_paths, remove_paths, remove_globs, \
    move_path_to_not_empty_directory
from configs.common import SupportedPlatform, Platform
from configs.projects.hanoi import HanoiProject
from report.lib_system_performance.system_performance_reports_generator \
    import SystemPerformanceReportsGenerator


class NodesManagerBuild(NodesManager):

    def __init__(self, is_build_release=False, **kwargs):
        """
        Constructor for class to support user on master to manage automation test system build
        and test then get build packages and results of testing.

        Parameters
        ----------
        is_build_release: bool
            Flag to request build a release package for a delta version. By this request,
            head of original master will be checked out and build. Then build package will named
            by prefix of delta version only.
        """
        self.is_build_release = is_build_release
        super(NodesManagerBuild, self).__init__(**kwargs)
        self.log_folder = os.path.join(FinalTestResult.INFO, FinalTestResult.LOG,
                                       FinalTestResult.Log.BUILD)
        self.logger.start_stage("BUILD  {project}  FOR  {job}  ON  {platforms}".format(
            project=self.info_handler.get_project(), job=self.info_handler.get_job(),
            platforms=", ".join(SupportedPlatform)))

    def pre_process(self):
        """
        Nothing for pre-process on build job. By test job, this step will execute distributing
        test cases for virtual machines on whole systems.

        Returns
        -------
        None

        """
        pass

    # Prepare for build
    def prepare_work(self):
        """
        Some work to do before execute build job such as clean old results of last build on
        current working directory of master.

        Returns
        -------
        None

        """
        self.logger.start_step("Clean old build results on master")
        # Clean old results
        if os.path.isdir(self.log_folder):
            remove_paths(self.log_folder)
        # Remove all of old build results
        for platform in SupportedPlatform:
            build_folder = os.path.join(platform, FinalTestResult.BUILD)
            if os.path.isdir(build_folder):
                remove_globs(os.path.join(build_folder, "*"))
        self.logger.end_step(True)

    # Combine all result from build nodes
    def post_process(self):
        self.logger.start_step("Combine build results from nodes")
        total = len(self.work_nodes)
        count = 1
        for node in self.work_nodes:
            self.logger.log_and_print("[{0}/{1}] Extract result from {2}"
                                      "".format(count, total, node.name))
            node_result_folder = node.result_folder
            if os.path.isdir(node_result_folder):
                # Currently, data in node_result_folder include
                # + Hanoi package (Hanoi installer)
                # + PHOcr build package
                # + "log" folder
                # But log is gotten in finally (after post process).
                # So this code blocks only combine Hanoi and PHOcr build package
                for f_name in os.listdir(node_result_folder):
                    if HanoiProject.is_hanoi_installer(f_name):
                        self.move_hanoi_installer_to_build_folder(
                            node_result_folder,
                            f_name)
                    elif f_name != FinalTestResult.LOG:
                        build_folder = os.path.join(node_result_folder, f_name)
                        if Platform.LINUX in f_name:
                            des_path = os.path.join(Platform.LINUX,
                                                    FinalTestResult.BUILD)
                        else:
                            des_path = os.path.join(Platform.WINDOWS,
                                                    FinalTestResult.BUILD)
                        if not os.path.isdir(des_path):
                            os.makedirs(des_path)
                        move_path_to_not_empty_directory(build_folder, des_path)
                    else:
                        pass

            else:
                self.logger.log_and_print("Has no build results from {0}"
                                          "".format(node.name))
            count += 1
        # End of step for combining build results from nodes on master
        self.logger.end_step(True)
        # End of build stage
        self.logger.end_stage(True)

        # All works done, then generate execution data collection of system
        self.generate_execution_time_data()

    def get_more_log(self):
        """
        Make reports for performance of automation test system on build job

        Returns
        -------
        None

        """
        # Path to log folder of test system for both of build and test. This will be used to
        # generate report for performance of automation test system
        system_log_folder = os.path.join(FinalTestResult.INFO, FinalTestResult.LOG)
        # Path to directory which will be used to storage system performance reports
        target_directory = os.path.join(FinalTestResult.INFO,
                                        FinalTestResult.Log.SYSTEM_PERFORMANCE,
                                        FinalTestResult.Log.SYSTEM_PERFORMANCE_BUILD)
        # Initial reports generator
        reports_generator = SystemPerformanceReportsGenerator(log_folder=system_log_folder,
                                                              output_folder=target_directory)
        # Generate reports for performance of system on build job
        reports_generator.generate_build_performance_reports()

    def get_work_nodes(self):
        """
        Initial node object which help control work on remote node over ssh connection base on
        system configuration in profile.json

        Returns
        -------
        list
            List of node object which help control work on remote node over ssh connection by run
            workers_manager.py on remote node

        """
        # Get node objects base on system configuration
        nodes = self.profile_handler.get_build_nodes()
        # Request to build a release version (latest on original master of project)
        if self.is_build_release:
            for node in nodes:
                node.is_build_release = True
        return nodes

    def combine_result_when_node_not_done_exception(self):
        """
        Currently, nothing to be done when any build node fail. If have any, just leave system
        failed.

        Returns
        -------
        None

        """
        pass

    @staticmethod
    def move_hanoi_installer_to_build_folder(node_result, file_name):
        """
        Move Hanoi Installer to build folder corresponding with platform.

        Parameters
        ----------
        node_result: str
           Node result folder name.
        file_name: str
           Hanoi installer name:
           Platform linux: Hanoi_installer.run
           Platform windows: HanoiInstaller.exe

        """

        hanoi_installer_path = os.path.join(node_result,
                                            file_name)
        if re.search(HanoiProject.RELEASE_PREFIX, file_name, re.I):
            build_folder_path = \
                os.path.join(Platform.LINUX, FinalTestResult.BUILD)
        else:
            build_folder_path = \
                os.path.join(Platform.WINDOWS, FinalTestResult.BUILD)
        if not os.path.isdir(build_folder_path):
            os.makedirs(build_folder_path)
        move_paths(hanoi_installer_path,
                   os.path.join(build_folder_path, file_name))
