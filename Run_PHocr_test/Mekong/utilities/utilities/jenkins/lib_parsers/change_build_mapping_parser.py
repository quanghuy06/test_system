# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      27/09/2019
# Description:      This script define class to help update data in json mapping file between
#                   gerrit changes with jenkins build and their status.
from abc import ABCMeta
from jenkins.lib_parsers.json_mapping_parser import JsonMappingParser


class ChangeBuildMappingParser(JsonMappingParser):
    __metaclass__ = ABCMeta

    STATUS_SUCCESS = "success"
    STATUS_FAIL = "fail"

    def __init__(self, **kwargs):
        """
        Constructor of class which help extract and update data in json mapping file between
        gerrit changes and jenkins build. Currently, this mapping file has the following structure:
        {
            "<change_number_1>": {
                "<patch_set_1>": {
                    { "<build_1>": "<status>" },
                    { "<build_2": "<status>" }
                },
                "<patch_set_2>": {
                    ...
                }
            },
            "<change_number_2>": {
                ...
            }
        }

        """
        super(ChangeBuildMappingParser, self).__init__(**kwargs)

    def update(self, change_number, patch_set, build_number, status):
        """
        Execute update information of a version of source code change and write data to mapping
        file. If mapping file does not exist then it will be created.

        Parameters
        ----------
        change_number: str/int
            Change number which need to be updated data
        patch_set: str/int
            Patch set number of the change which need to be updated data. This is actually a
            version of source code changes.
        build_number: str/int
            Build number of jenkins job which test for the version of source code changes
        status: str
            Status of jenkins build: success/fail

        Returns
        -------
        None

        """
        change_number_ = str(change_number)
        patch_set_ = str(patch_set)
        build_number_ = str(build_number)
        if not self._data:
            # Data is None
            self._data = {
                change_number_: {
                    patch_set_: {
                        build_number_: status
                    }
                }
            }
        elif change_number_ not in self._data:
            # New change is added
            self._data[change_number_] = {
                patch_set_: {
                    build_number_: status
                }
            }
        elif patch_set_ not in self._data[change_number_]:
            # New patch set is added to existing change
            self._data[change_number_][patch_set_] = {
                build_number_: status
            }
        else:
            # Add new build for a patch set in case old build is re-triggered. Or update status
            # of existing build.
            self._data[change_number_][patch_set_][build_number_] = status

        # Write data to file
        self._write_data()

    def get_latest_success_build(self, change_number):
        """
        Get latest build number which success of a change. This is useful when we need reference
        data to update test cases or when we delete old results and need to keep results of
        latest build.

        Parameters
        ----------
        change_number:  str/int
            Change number to extract information

        Returns
        -------
        str
            Build number of latest success build for the change

        """
        # Initial latest success build at zero
        latest_build = 0

        # Make sure change number is in type str
        change_number_ = str(change_number)

        # No data is specify then return 0
        if not self._data or change_number_ not in self._data:
            return str(latest_build)

        for patch_set in self._data[change_number_]:
            for build_number_ in self._data[change_number_][patch_set]:
                status = self._data[change_number_][patch_set][build_number_]
                build_number = int(build_number_)
                if build_number > latest_build and status == self.STATUS_SUCCESS:
                    latest_build = build_number

        return str(latest_build)

    def get_list_build(self, change_number):
        """
        Get list of all build number relate to the change

        Parameters
        ----------
        change_number: str/int
            Change number to be extracted information

        Returns
        -------
        list
            List of build number of the change. Return empty list in case there is no data
            information.

        """
        build_list = list()
        # Return empty list in case there is no data information
        if not self._data:
            return build_list

        # Make sure change number is in type str
        change_number_ = str(change_number)

        # Collect data
        for patch_set in self._data[change_number_]:
            build_list += self._data[change_number_][patch_set].keys()

        return build_list
