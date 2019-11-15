# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      26/06/2018
# Description:      This script define base class for a node.
import traceback
import time
from abc import ABCMeta, abstractmethod
from manager.lib_manager.worker import Worker
from configs.jenkins import JenkinsHelper
from configs.projects.mekong import MekongProject


class Node(Worker):
    __metaclass__ = ABCMeta

    def __init__(self, profile_handler, **kwargs):
        """
        Constructor for node object which is help us work on a remote node.

        Parameters
        ----------
        profile_handler : ProfileHandler
            Object handler information from system profile configuration
        """
        super(Node, self).__init__(log_level=2, **kwargs)
        self.profile_handler = profile_handler
        self.home_dir = "/home/{username}".format(username=self.username)
        if self.info_handler and self.profile_handler:
            self.working_dir = \
                JenkinsHelper.get_workspace(node_name=self.name,
                                            profile_handler=self.profile_handler,
                                            parameter_handler=self.info_handler)

    def prepare_work(self):
        """
        Prepare some data for executing task on node.

        Returns
        -------
        None

        """
        # Prepare workspace
        self.logger.start_step("Clean workspace")
        self.remove_directory(self.working_dir)
        # Wait for a second for directory really removed
        time.sleep(1)
        self.make_directory(self.working_dir)
        self.logger.end_step(True)
        # Get Mekong utilities
        self.logger.start_step("Get Mekong utilities")
        self.get(local_path=MekongProject.NAME, client_path=self.working_dir)
        self.logger.end_step(True)
        # Prepare some specific data for process
        self.prepare_private_data()

    @abstractmethod
    def prepare_private_data(self):
        """
        This is an abstract method and need to be implemented on derive class. Depend on job in
        charge, some more data should be prepared before running command can be putted here.

        Returns
        -------
        None

        """
        pass

    def do_work(self):
        """
        Execute the manage command on remote node through ssh connection. This is a threading
        process. For each node, a ssh connection is established on a thread.

        Returns
        -------
        None

        """
        try:
            # Prepare for work
            self.prepare_work()

            # Do requested work
            self.logger.start_step("Run workers manager on remote node")
            cmd = self.get_run_command()
            self.logger.log_and_print(cmd)
            self.exec_command(cmd=cmd,
                              timeout=self.timeout(),
                              cwd=self.working_dir)
            self.logger.end_step(True)

        except:
            var = traceback.format_exc()
            if self.log_level >= 0:
                self.logger.log_and_print(var)
            else:
                print(var)
            self.work_done = False
            self.logger.end_step(False)
        finally:
            self.post_process()

    @abstractmethod
    def post_process(self):
        """
        Some work need to be done after do work such as combine results. This method is designed
        as abstract method and depend on which task is processing we have different work to be done.

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def get_run_command(self):
        """
        This class help us control to run work on a remote node. Then this is abstract method and
        depend on which task is processing then we have different command to execute.

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def timeout(self):
        """
        Timeout for processing on a node. This is abstract method and depend on which task is
        processing.

        Returns
        -------

        """
        pass

    def start(self):
        """
        No action on start a node. We assume that nodes are always online.

        Returns
        -------
        None

        """
        pass

    def stop(self):
        """
        No action on stop a node. We assume that nodes are always online.

        Returns
        -------
        None

        """
        pass

    @abstractmethod
    def get_result_from_node(self):
        """
        This is abstract method and will be implemented on derived classes. This is a post
        process step which send result from node to master.

        Returns
        -------
        None

        """
        pass
