import os
import shutil
from configs.jenkins import JenkinsHelper
from configs.common import SupportedPlatform
from configs.test_result import FinalTestResult
from configs.json_key import ParametersJson
from handlers.parameters_handler import ParameterHandler
from configs.svn_resource import SVNResource, DataPathSVN
from utils.svn_helper import SVNHelper, SVNStatus


class SVNPostItUpdater:
    def __init__(self, job_name, build_number):
        self.job_name = job_name
        self.build_number = build_number
        self.svn_resource = SVNResource()
        self.archive_folder = JenkinsHelper.get_archive_path(self.job_name,
                                                             self.build_number)
        parameter_file = os.path.join(self.archive_folder,
                                      FinalTestResult.INFO,
                                      ParametersJson.DEFAULT_NAME)
        self.parameter_handler = ParameterHandler(input_file=parameter_file)

    def update(self):
        """
        Update data stored on Jenkins to SVN.

        """
        self.update_hanoi_installer()

    def update_hanoi_installer(self):
        """
        Add or update Hanoi installer to SVN.

        """
        hanoi_data_svn_local = os.path.join(JenkinsHelper.SVN_PATH,
                                            DataPathSVN.HANOI_RELEASE)
        hanoi_data_svn_url = \
            self.svn_resource.get_url(DataPathSVN.HANOI_RELEASE)
        svn_helper = SVNHelper(hanoi_data_svn_url, hanoi_data_svn_local)
        if not svn_helper.is_checkouted():
            svn_helper.checkout()
        svn_helper.update()
        # Copy hanoi installer from Jenkin to SVN path.
        list_files_add = []
        list_files_update = []
        for platform in SupportedPlatform:
            hanoi_installer_name = \
                self.parameter_handler.get_hanoi_package_release(platform)
            hanoi_installer_on_jenkin_path = os.path.join(self.archive_folder,
                                                          platform,
                                                          FinalTestResult.BUILD,
                                                          hanoi_installer_name)
            hanoi_installer_on_local = os.path.join(hanoi_data_svn_local,
                                                    platform,
                                                    hanoi_installer_name)

            # Copy Hanoi installer from Jenkin to local svn path.
            shutil.copyfile(hanoi_installer_on_jenkin_path,
                            hanoi_installer_on_local)

            # Add or update Hanoi installer to SVN
            file_status = \
                svn_helper.get_file_status(
                    os.path.join(hanoi_data_svn_local, platform),
                    hanoi_installer_name
                )
            if file_status:
                if file_status == SVNStatus.UNVERSIONED:
                    list_files_add.append(hanoi_installer_on_local)

                elif file_status == SVNStatus.ADDED \
                        or file_status == SVNStatus.MODIFIED:
                    list_files_update.append(hanoi_installer_on_local)
                else:
                    raise Exception(
                        "Can't update {0}!".format(hanoi_installer_name)
                    )
        change_number = "C{0}".format(self.parameter_handler.get_change_number())
        if list_files_add:
            svn_helper.add_list_file(list_files_add,
                                     JenkinsHelper.NAME,
                                     change_number)

        if list_files_update:
            svn_helper.commit(
                svn_helper.get_update_message(
                    list_files_update,
                    JenkinsHelper.NAME,
                    change_number),
                list_files_update)
