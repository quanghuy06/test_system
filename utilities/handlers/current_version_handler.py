from handlers.lib_base.json_handler import JsonHandler
from configs.json_key import CurrentVersionKey
from build_manager_handler import BuiltManagerKey
from abc import ABCMeta
import subprocess
import os


class CurrentVersionConfigureHandler(JsonHandler):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(CurrentVersionConfigureHandler, self).__init__(**kwargs)
        self.data = self.data.get(BuiltManagerKey.CURRENT_VERSION)

    def get_path(self):
        """

        Returns
        -------
        str:
            the path to current version file
        """

        path = self.data.get(CurrentVersionKey.PATH)
        return path

    def get_ip(self):
        """

        Returns
        -------
        str:
            the ip address

        """
        ip = self.data.get(CurrentVersionKey.IP)
        return ip

    def get_username(self):
        """

        Returns
        -------
        str:
            the username
        """
        username = self.data.get(CurrentVersionKey.USERNAME)
        return username

    def get_password(self):
        """

        Returns
        -------
        str:
            the password
        """
        password = self.data.get(CurrentVersionKey.PASSWORD)
        return password

    def load(self):
        """

        Returns
        -------
        str: the file to current folder
        """
        cmd = "scp -r {username}@{ip}:{path} .".format(
            username=self.get_username(),
            ip=self.get_ip(),
            path=self.get_path()
        )
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        assert error is None, error
        return os.path.join(os.getcwd(), os.path.basename(self.get_path()))


class CurrentVersionHandler(JsonHandler):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(CurrentVersionHandler, self).__init__(**kwargs)

    def get_hanoi_change(self):
        """

        Returns
        -------
        str:
            current change of hanoi
        """
        return self.data.get(CurrentVersionKey.HANOI_CHANGE)

    def get_hanoi_delta(self):
        """

        Returns
        -------
        str:
            current hanoi delta
        """
        return self.data.get(CurrentVersionKey.HANOI_DELTA)

    def get_phocr_change(self):
        """

        Returns
        -------
        str:
            current phocr change
        """
        return self.data.get(CurrentVersionKey.PHOCR_CHANGE)

    def get_phocr_delta(self):
        """

        Returns
        -------
        str:
            current phocr delta
        """
        return self.data.get(CurrentVersionKey.PHOCR_DELTA)
