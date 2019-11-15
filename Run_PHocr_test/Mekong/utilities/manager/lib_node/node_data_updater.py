# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      11/09/2019
# Description:      This script define class for updating data on test virtual machines on a node.
import os
from abc import ABCMeta
from manager.lib_node.node import Node
from configs.command import CommandConfig


class NodeDataUpdater(Node):
    __metaclass__ = ABCMeta

    # Working folder for data updating on Node in Jenkins workspace. So full path of working
    # directory for data updating on a node is: ~/jenkins/workspace/<data working dir>
    WORKING_DIR = "StaticDataUpdate"

    # Time out for updating data on virtual machines of a node
    TIMEOUT_UPDATE_DATA = 3600

    def __init__(self, update_list=None, reset_backup=False, **kwargs):
        """
        Need to define list of data packages which will be updated.

        Parameters
        ----------
        update_list : list
            List of data packages need to be updated
        reset_backup : bool
            Flag to request reset all virtual machines to a backup state which is really clean.
        """
        super(NodeDataUpdater, self).__init__(**kwargs)
        # Working directory on node
        self.working_dir = os.path.join(self.home_dir, "jenkins", "workspace", self.WORKING_DIR)
        # Data update list
        if update_list is not None:
            self.update_list = update_list
        else:
            self.update_list = list()
        # Request to reset virtual machines to backup state
        self.reset_backup = reset_backup

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
        cmd = CommandConfig.node_update_data_command(node_name=self.name,
                                                     update_list=self.update_list,
                                                     reset_backup=self.reset_backup)
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
