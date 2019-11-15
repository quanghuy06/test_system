# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Tran Quang Huy
# Email:            huy.tranquang@toshiba-tsdv.com
# Date create:      4/11/2019
# Description:      This script define class for updating data on test virtual machines on a node.
import os
from abc import ABCMeta
from manager.lib_node.node import Node
from configs.command import CommandConfig


class NodeTestCasesFolderUpdater(Node):
    __metaclass__ = ABCMeta

    # Working folder for data updating on Node in Jenkins workspace. So full path of working
    # directory for data updating on a node is: ~/jenkins/workspace/<data working dir>
    WORKING_DIR = "TestCasesFolderUpdate"

    # Time out for updating test cases folder on node
    TIMEOUT_UPDATE_DATA = 10800

    def __init__(self, **kwargs):
        """
        Constructor for class which help manage processes on a thread which manage ssh
        connection to a node for updating test cases folder on that node.

        """
        super(NodeTestCasesFolderUpdater, self).__init__(**kwargs)
        # Working directory on node
        self.working_dir = os.path.join(self.home_dir, "jenkins", "workspace", self.WORKING_DIR)

    def prepare_private_data(self):
        """
        No data need to be prepared.

        Returns
        -------
        None

        """
        pass

    def post_process(self):
        """
        Nothing to be done in post process.

        Returns
        -------
        None

        """
        pass

    def get_result_from_node(self):
        """
        No results from node.

        Returns
        -------

        """
        pass

    def get_run_command(self):
        """
        Implement abstract method which generate command line to run updating data on node.

        Returns
        -------
        str
            Command line which will be run on node to update data for it's test virtual machines

        """
        cmd = CommandConfig.node_update_test_cases_folder(node_name=self.name)
        return cmd

    def timeout(self):
        """
        Time out for processing updating data on node

        Returns
        -------
        int
            Time out for updating data on node

        """
        return self.TIMEOUT_UPDATE_DATA
