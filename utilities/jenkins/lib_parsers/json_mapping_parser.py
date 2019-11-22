# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      27/09/2019
# Description:      This script define class to help update data in json mapping file. This class
#                   can be inherited from other for specific purpose.
import os
from baseapi.file_access import read_json, write_json, make_dir


class JsonMappingParser(object):
    def __init__(self, mapping_file=None):
        """
        Set up path to target json file and load data to json object if available.

        Parameters
        ----------
        mapping_file: str
            Path to json input/output file. When mapping file already exists, then we extract
            data from existing file and update to that file. Otherwise, if mapping file does not
            exist then create them when new data is updated.
        """
        self._data = dict()
        self.mapping_file = mapping_file

    @property
    def mapping_file(self):
        """
        Getter of path to mapping json file

        Returns
        -------
        str
            Path to mapping json file

        """
        return self._mapping_file

    @mapping_file.setter
    def mapping_file(self, file_path):
        """
        Setter for path to mapping json file. Load mapping data from file to json object.

        Parameters
        ----------
        file_path: str
            Path to mapping json file

        Returns
        -------
        None

        """
        # Set up target file path
        self._mapping_file = file_path
        # Extract information
        if os.path.exists(self._mapping_file):
            self._data = read_json(self._mapping_file)

    def _write_data(self):
        """
        Write dat object to target file. If file does not exist then create it.

        Returns
        -------
        None

        """
        # Create parent directory if file does not exist
        if not os.path.exists(self._mapping_file):
            dir_path = os.path.dirname(self._mapping_file)
            if dir_path and not os.path.isdir(dir_path):
                make_dir(dir_path)

        # Write new updated data to the file
        write_json(self._data, self._mapping_file)
