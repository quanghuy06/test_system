# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      27/09/2019
# Description:      This script defines class to help extracting and updating information in
#                   version file which store current delta version on base line of projects
from abc import ABCMeta
from configs.jenkins import JenkinsHelper
from jenkins.lib_parsers.json_mapping_parser import JsonMappingParser
from jenkins.lib_parsers.delta_change_mapping_parser import DeltaChangeMappingParser


class DeltaVersionProjectsParser(JsonMappingParser):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        """
        Constructor of class which help extract and update data in json file which store current
        delta version on base line of projects. The following is data structure:
        {
            "<project 1>": "<delta version>",
            "<project 2>": "<delta version>"
        }
        When we build and test for a change of a project, first we need to merge the change into
        base line so we need to know the current version base line for testing. We can find this
        information from delta version mapping json file of the project by searching the latest
        delta version in the list. However, by separating these information into individual file,
        we can access these information faster.
        This file need to be updated when a change of project is integrated into base line.

        """
        super(DeltaVersionProjectsParser, self).__init__(**kwargs)

    def update(self, project, version):
        """
        This method allow updating current delta version of a project in delta version of
        projects file.

        Parameters
        ----------
        project: str
            Name of project to be updated
        version: str/int
            Current delta version of project

        Returns
        -------
        None

        """
        # Make sure data is in type str
        version_ = str(version)
        # Update data object
        self._data[project] = version_
        # Write update data to json mapping file
        self._write_data()

    def get_delta_version(self, project):
        """
        Get current delta version on base line of a project

        Returns
        -------
        str
            Current delta version of the project. If project is not define in data file then
            return 0.

        """
        version = 0
        if project in self._data:
            version = self._data[project]
        return str(version)

    def change_merge(self, project, change_number=None):
        """
        A change was integrated into base line of a project then automatically increase current
        delta version of the project by 1. If the project currently is not defined in json file
        then set delta version equal 1.
        Then write updated data to json file output.

        Parameters
        ----------
        project: str
            Name of project to be updated
        change_number: str/int
            Change number which to be merged. When this parameter is None then just increase
            current delta version by 1. When the change number is passed, then it'll check
            delta-change mapping of project first to make sure that this is not a re-trigger build.

        Returns
        -------
        None

        """
        if change_number:
            # Get path to delta-change mapping file of the project
            delta_change_mapping_file = JenkinsHelper.get_path_delta_change_mapping_file(
                project=project)

            # Create data parser for delta-change mapping
            delta_change_mapping_parser = \
                DeltaChangeMappingParser(mapping_file=delta_change_mapping_file)

            # Check if change number already exists in delta-change mapping then this actually
            # re-trigger of Post Integration. So we no need to increase current delta version of
            # the project in this case.
            if delta_change_mapping_parser.change_exists(change_number=change_number):
                print("WARN: Change number already recorded in delta-change mapping, so this may "
                      "be re-trigger of Post Integration and nothing to be updated!")
                return

        # Get current delta version of project. If project is not defined then 0 is returned
        current_version = int(self.get_delta_version(project=project))
        # Increment current version by 1
        current_version += 1
        # Update data object
        self._data[project] = str(current_version)
        # Write updated data to file
        self._write_data()
