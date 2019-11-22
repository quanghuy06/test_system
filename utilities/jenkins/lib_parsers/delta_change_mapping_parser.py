# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      27/09/2019
# Description:      This script define class to help update data in json mapping file between
#                   delta version and change number of gerrit
from abc import ABCMeta
from jenkins.lib_parsers.json_mapping_parser import JsonMappingParser


class DeltaChangeMappingParser(JsonMappingParser):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        """
        Constructor of class which help extract and update data in json mapping file between
        delta version and change number of gerrit. Currently, this mapping file has the following
        structure:
        {
            "<delta_version_1>": "<change_number_2>",
            "<delta_version_2>": "<change_number_5>"
        }

        Currently, a change can be integrated or not into project line. When a change is
        integrated in project line, then it become a delta version. We test for a change,
        and in Post Integration when the change is integrated need to know delta version to
        prepare data for release or make reports.

        """
        super(DeltaChangeMappingParser, self).__init__(**kwargs)

    def change_exists(self, change_number):
        """
        Check if a change number exists or not in data mapping file.

        Parameters
        ----------
        change_number: str/int
            Change number need to be checked.

        Returns
        -------
        bool
            True if change number already exists on the list. Otherwise, False is returned

        """
        # The first time no change were merged and we have no data
        if not self._data:
            return False

        change_number_ = str(change_number)
        for delta_version in self._data:
            if change_number_ == self._data[delta_version]:
                return True
        return False

    def update(self, delta_version, change_number):
        """
        This method allow add a customize data record to mapping data.

        Parameters
        ----------
        delta_version: str/int
            Delta version number need to be updated
        change_number: str/int
            Change number relates to delta version

        Returns
        -------
        tuple
            Value udpated

        """
        # Make sure data is in type str
        delta_version_ = str(delta_version)
        change_number_ = str(change_number)
        # Update data object
        self._data[delta_version_] = change_number_
        # Write update data to json mapping file
        self._write_data()

        return delta_version_, change_number_

    def latest_version(self):
        """
        Get latest delta version in the list

        Returns
        -------
        int
            Latest delta version of project in mapping data

        """
        max_delta = 0
        if self._data:
            for version in self._data:
                version_ = int(version)
                if max_delta < version_:
                    max_delta = version_
        return max_delta

    def change_merge(self, change_number):
        """
        Update mapping file when a change is integrated into project line.
        By normal case, we get the latest delta version in list and increase by 1 for the new
        change merged.
        However, we consider if the change already exists in mapping file, then nothing to do
        => This is case when a Post Integration is re-triggered.
        If there is any data changes then update json mapping file.

        Parameters
        ----------
        change_number: str/int
            Change number of the change which is integrated into project line.

        Returns
        -------
        tuple
            Value updated

        """
        # If the change already exists in mapping data then this is Post Integration
        # re-triggered, then nothing to update.
        if self.change_exists(change_number=change_number):
            print("WARN: Change number is already recorded in delta-change mapping file of "
                  "project, this can be re-trigger of Post Integration then nothing will be "
                  "updated!")
            return

        # Really update when new change is merged into project line
        new_version = self.latest_version() + 1

        # Add new version to data object
        self.update(delta_version=new_version, change_number=change_number)

        return str(new_version), str(change_number)

    def get_change_number(self, delta_version):
        """
        Get change number relates to a delta version

        Parameters
        ----------
        delta_version: str/int
            Delta version of the project want to extract information

        Returns
        -------
        str
            Change number which corresponding to the delta version. If has no delta version in
            data then return zero.

        """
        change_number = "0"

        # Make sure delta version is in type str
        delta_version_ = str(delta_version)

        # If has no data or delta version does not exist then return zeto
        if not self._data or delta_version_ not in self._data:
            return change_number
        else:
            # Extract information
            return self._data[delta_version_]
