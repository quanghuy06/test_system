# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Tran Quang Huy
# Email:            huy.tranquang@toshiba-tsdv.com
# Date create:      4/11/2019
# Description:      This script define class to help update test cases folder on test nodes in
#                   whole automation test system which are defined in configs.common.Machines
from configs.common import Platform
from configs.common import Machines
from configs.json_key import ProfileJson
from manager.lib_manager.nodes_manager_class import NodesManager
from manager.lib_node.node_test_cases_folder_updater import NodeTestCasesFolderUpdater


class NodesManagerUpdateTestCasesFolder(NodesManager):

    def __init__(self, **kwargs):
        """
        No need information for updating test cases folder. List of nodes and their target test
        cases folder to be updated are defined in configs.common.Machines

        """
        super(NodesManagerUpdateTestCasesFolder, self).__init__(**kwargs)
        self.logger.start_stage("UPDATE TEST CASES FOLDER")

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
        work_nodes = list()

        for node_name in Machines.NODE_MACHINES:
            node_info = Machines.NODE_MACHINES[node_name]
            node_profile = self.profile_handler.get_node_info(node_name=node_name)
            node_object_updater = \
                NodeTestCasesFolderUpdater(name=node_name,
                                           ip=node_info[Machines.IP],
                                           username=node_profile[ProfileJson.info.USER],
                                           platform=Platform.LINUX,
                                           profile_handler=self.profile_handler)
            work_nodes.append(node_object_updater)

        return work_nodes

    def combine_result_when_node_not_done_exception(self):
        """
        No results to combine

        Returns
        -------

        """
        pass
