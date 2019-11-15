import sys_path
sys_path.insert_sys_path()

import os
from configs.json_key import ProfileJson
from configs.projects.mekong import TestSystemScripts


jenkins = dict()
jenkins["home"] = "/home/ocr3/.jenkins"
jenkins["artifacts"] = "/media/ocr3/data/Jenkins"


class Jenkins:
    NAME = "Jenkins"
    MASTER = "ocr3"
    ARTIFACT_DIR = "/media/ocr3/data/Jenkins"
    ARCHIVE_FOLDER = "archive"
    HOME_DIR = os.path.expanduser("~/.jenkins")
    JOB_DIR = HOME_DIR + "/jobs"
    SVN_PATH = "/media/ocr3/data/svn/"

    GERRIT_DATA_FOLDER = "gerrit-projects"
    CHANGE_BUILD_MAPPING_FILE = "change_build_mapping.json"
    DELTA_CHANGE_MAPPING_FILE = "delta_change_mapping.json"
    DELTA_VERSION_PROJECTS_FILE = "delta_version_projects.json"

    @staticmethod
    def get_self_clean_ws_cmd(job_name, cwd=None):
        if cwd:
            return 'cd {0} && chmod +x {1} && ./{1} {2}'.format(cwd, TestSystemScripts.CLEAN_WS, job_name)
        else:
            return 'chmod +x {0} && ./{0} {1}'.format(TestSystemScripts.CLEAN_WS, job_name)

    @staticmethod
    def get_clean_ws_node_cmd(job_name):
        return "./prepare_workspace.sh {0}".format(job_name)

    def get_workspace(self, node_name, parameter_handler, profile_handler):
        node_info = profile_handler.get_node_info(node_name)
        if node_name != self.MASTER:
            return "/home/{0}/jenkins/workspace/{1}".format(
                node_info[ProfileJson.info.USER], parameter_handler.get_job())
        else:
            return "/home/{0}/.jenkins/workspace/{1}".format(
                node_info[ProfileJson.info.USER], parameter_handler.get_job())

    def get_archive_path(self, job_name, build_number):
        """
        Get path to archive folder for a build of a job on Jenkins

        Parameters
        ----------
        job_name: str
            Name of jenkins job to extract information
        build_number: str/int
            Build number to extract information

        Returns
        -------
        str
            Path to archive folder for a build on a jenkins job

        """
        return os.path.join(self.ARTIFACT_DIR, job_name, build_number, self.ARCHIVE_FOLDER)

    def get_file_mapping(self, job_name, file_name):
        return os.path.join(self.JOB_DIR, job_name, file_name)

    def get_job_name_folder(self, job_name):
        return os.path.join(self.ARTIFACT_DIR, job_name)

    def get_path_delta_version_projects_file(self):
        """
        Get path to json file which includes information about current delta version of
        gerrit projects

        Returns
        -------
        str
            Path to delta version file

        """
        return os.path.join(self.JOB_DIR, self.GERRIT_DATA_FOLDER, self.DELTA_VERSION_PROJECTS_FILE)

    def get_path_delta_change_mapping_file(self, project):
        """
        Get path to json file which maps between delta version and change number of a gerrit
        project to use in Jenkins processes.

        Parameters
        ----------
        project: str
            Name of project to extract information

        Returns
        -------
        str
            Path to delta-change mapping file of the project

        """
        return os.path.join(self.JOB_DIR, self.GERRIT_DATA_FOLDER,
                            project, self.DELTA_CHANGE_MAPPING_FILE)

    def get_path_change_build_mapping_file(self, job_name):
        """
        Get path to json file which maps between change number and list of build number for it.

        Parameters
        ----------
        job_name: str
            Name of jenkins job want to extract information

        Returns
        -------
        str
            Path to change-build mapping file of the jenkins job

        """
        return os.path.join(self.JOB_DIR, job_name, self.CHANGE_BUILD_MAPPING_FILE)


JenkinsHelper = Jenkins()
