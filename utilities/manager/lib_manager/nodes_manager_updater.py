# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/09/2019
# Description:      This script define class to help update static data on all virtual machines in
#                   system.
from manager.lib_manager.nodes_manager_class import NodesManager


class NodesManagerUpdater(NodesManager):

    def __init__(self, update_list=None, reset_backup=False, **kwargs):
        """
        Constructor for updater manager class

        Parameters
        ----------
        update_list : list
           List packages need to update on virtual machines. These packages will be updated from
           SVN repository and are defined in svn_resource.py
        reset_backup : bool
            Flag to request reset all test virtual machines on test system to backup state which
            really clean and have no testing data on them.

        """
        super(NodesManagerUpdater, self).__init__(**kwargs)
        self.logger.start_stage("UPDATE STATIC DATA FOR VIRTUAL MACHINES")
        # List of data package which need to be updated
        if update_list:
            self.update_list = update_list
        else:
            self.update_list = list()
        # Request to reset all test virtual machines to backup state
        self.reset_backup = reset_backup

    def pre_process(self):
        """
        Nothing to do in pre-process

        Returns
        -------
        None

        """
        pass

    def prepare_work(self):
        """
        Nothing need to be prepared

        Returns
        -------
        None

        """
        pass

    def post_process(self):
        """
        Nothing to do, just end stage and log time.

        Returns
        -------
        None

        """
        self.logger.end_stage(True)

    def get_more_log(self):
        """
        Currently, do not get log of processing

        Returns
        -------
        None

        """
        pass

    def get_work_nodes(self):
        """
        Get all nodes which are distributed for testing in both Engineering Test and Integration
        Test to update data.

        Returns
        -------
        None

        """
        work_nodes = self.profile_handler.get_nodes_data_updater()

        # Set up data update list for data update nodes
        for node in work_nodes:
            node.update_list = self.update_list
            node.reset_backup = self.reset_backup

        return work_nodes

    def combine_result_when_node_not_done_exception(self):
        """
        No results to combine

        Returns
        -------

        """
        pass
