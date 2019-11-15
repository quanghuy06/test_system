# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/09/2019
# Description:      This script define class which manage updating static data of all testing
#                   virtual machines on a node
import os
from manager.lib_manager.workers_manager_class import WorkersManager
from utils.svn_helper import SVNHelper
from configs.system_data_updater import DataUpdatesAvailable
from configs.svn_resource import DataPathSVN
from configs.git_resource import GITResource
from mekong.common.config_checker import ToolChecker
from mekong.common.checkout_repo import CheckoutSCMMain
from mekong.common.utilities import load_json


class WorkersManagerUpdater(WorkersManager):

    def __init__(self, update_list=None, reset_backup=False, **kwargs):
        """
        Constructor for updater manager class. This class will manage updating static data on
        testing virtual machines on node and create new snapshot of Clean-State.

        Parameters
        ----------
        update_list: list
           List packages need to update on virtual machines. These packages will be updated from SVN
           repository and are
           defined in svn_resource.py

        """
        super(WorkersManagerUpdater, self).__init__(**kwargs)
        if update_list is not None:
            self.update_list = update_list
        else:
            self.update_list = list()
        # Flag to reset all virtual machines to backup snapshot of testing
        self.reset_backup = reset_backup

    def get_log(self):
        """
        Get log for processes

        Returns
        -------
        None

        """
        pass

    def prepare_work(self):
        """
        Get updated data on Node from SVN and prepare to copy these new data to testing virtual
        machines. Only update data packages which is defined in requested update list.

        Returns
        -------
        None

        """
        # If this is a request to reset all virtual machines to backup snapshot, then nothing to do
        if self.reset_backup:
            return

        self.init_svn_folder()
        self.init_git_folder()

        # Check to update phocr trained data
        if DataUpdatesAvailable.PHOCR_TRAINED_DATA in self.update_list:
            self.update_phocr_trained_data_on_node()

        # Check to update python portable package
        if DataUpdatesAvailable.PYTHON_PORTABLE in self.update_list:
            self.update_python_portable_on_node()

        # Check to update valgrind utility for memory checking
        if DataUpdatesAvailable.VALGRIND_MEKONG in self.update_list:
            self.update_valgrind_mekong_on_node()

    def post_process(self):
        """
        Currently, nothing to do after updating data on virtual machines.

        Returns
        -------
        None

        """
        pass

    def get_workers(self):
        """
        Get list of instances of virtual machine data updater to update static data

        Returns
        -------
        list
            List of VmUpdateDataTestLinux

        """
        workers = self.profile_handler.get_workers_update_data_of_node(node_name=self.name)
        # Setup request list of data packages which need to be updated
        for worker in workers:
            worker.update_list = self.update_list
            worker.reset_backup = self.reset_backup
        return workers

    def combine_results_when_worker_not_done_exception(self):
        """
        No results to combine in this case.

        Returns
        -------
        None

        """
        pass

    def update_phocr_trained_data_on_node(self):
        """
        Update phocr trained data from git

        Returns
        -------
        None

        """
        project = "PHOcrOnNode"
        output_directory = GITResource.PHOcr.PHOCR_FOLDER

        # TODO: this code is duplicated with file checkout_scm.py
        utilities_folder = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))))
        tool_config_file = os.path.join(utilities_folder, 'mekong', 'config', 'tool_config.json')
        scm_config_file = os.path.join(utilities_folder, 'mekong', 'config', 'scm_config.json')

        [err, scm_json] = load_json(scm_config_file)
        if err:
            raise err

        # Check tool_config
        checker = ToolChecker()
        [err, tool] = checker.is_ok(tool_config_file)
        if err:
            raise err

        # change working dir to directory where we want to checkout source code
        current_dir = os.getcwd()
        if not os.path.isdir(self.git_dir):
            os.mkdir(self.git_dir)
        os.chdir(self.git_dir)
        # Project checking out
        scm_getter = CheckoutSCMMain(project)
        # Check out latest version of PHOcr
        [err, result] = scm_getter.run(tool, scm_json, output_directory, None)
        if err:
            os.chdir(current_dir)
            raise err
        os.chdir(current_dir)

    def update_python_portable_on_node(self):
        """
        Update python portable package from SVN

        Returns
        -------
        None

        """
        python_portable_dir = os.path.join(self.svn_dir, DataPathSVN.PYTHON_PORTABLE)
        python_portable_url = self.svn_resource.get_url(DataPathSVN.PYTHON_PORTABLE)
        svn_helper = SVNHelper(python_portable_url, python_portable_dir)
        if not svn_helper.is_checkouted():
            svn_helper.checkout()
        svn_helper.update()

    def update_valgrind_mekong_on_node(self):
        """
        Update valgrind utility for memory checking from SVN

        Returns
        -------
        None

        """
        mekong_3rd_party_dir = os.path.join(self.svn_dir, DataPathSVN.MEKONG_3RD_PARTY_DIR)
        mekong_3rd_party_url = self.svn_resource.get_url(DataPathSVN.MEKONG_3RD_PARTY_DIR)
        svn_helper = SVNHelper(mekong_3rd_party_url, mekong_3rd_party_dir)
        if not svn_helper.is_checkouted():
            svn_helper.checkout()
        svn_helper.update()
