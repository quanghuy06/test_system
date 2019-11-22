# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      26/06/2018
# Description:      This script define base class for a build node.
import os
from manager.lib_node.node import Node
from configs.command import CommandConfig


class NodeBuild(Node):

    def __init__(self, is_build_release=False, **kwargs):
        """
        Constructor for class which help to manage remote node over ssh connection from master

        Parameters
        ----------
        is_build_release: bool
            Flag to request build a release version of latest delta on master branch of the project

        """
        self.is_build_release = is_build_release
        super(NodeBuild, self).__init__(**kwargs)
        self.result_folder = "build_results_" + self.name
        self.build_result_path = os.path.join(self.working_dir, self.result_folder)

    def prepare_private_data(self):
        """
        There are some more data need to be prepared for build job rather than data which already
        be prepared in prepare_work() method of Node class (super class)

        Returns
        -------
        None

        """
        # Get parameters json file
        self.logger.start_step("Get parameters file")
        self.get(local_path=self.info_handler.input_file,
                 client_path=self.working_dir)
        self.logger.end_step(True)

    def post_process(self):
        """
        Copy build results from node to master

        Returns
        -------
        None

        """
        self.logger.start_step("Copy results from node to master")
        self.get_result_from_node()
        self.logger.end_step(True)

        # End of logging on node thread
        self.logger.end(write_to_file=False)

    def get_run_command(self):
        """
        Get command which used workers_manager.py to manage build virtual machines to run and
        generate build packages.

        Returns
        -------
        None

        """
        if self.is_build_release:
            # Command to manage virtual machines on a node to build release packages
            return CommandConfig.node_build_release_command(self.name)
        else:
            # Command to manage virtual machines on a node to build packages for normal testing
            return CommandConfig.node_build_command(self.name)

    def timeout(self):
        """
        Define time out of build processes. If execution time over this value then all processes
        will be interrupted

        Returns
        -------
        None

        """
        return 3600

    def get_result_from_node(self):
        """
        This method will get all result from build node include: build result if build
        successfully and log files

        Returns
        -------
        None
        """
        self.put(client_path=self.build_result_path, local_path=os.getcwd())
