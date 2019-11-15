from abc import ABCMeta
from handlers.lib_base.json_handler import JsonHandler
from configs.json_key import BuiltManagerKey, ChangeDeltaMappingKey
import subprocess
import os


class ChangeDeltaMappingConfigureHandler(JsonHandler):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(ChangeDeltaMappingConfigureHandler, self).__init__(**kwargs)
        self.data = self.data.get(BuiltManagerKey.CHANGE_DELTA)

    def get_path(self):
        """

        Returns
        -------
        str:
            path to change delta mapping
        """
        path = self.data.get(ChangeDeltaMappingKey.PATH)
        return path

    def get_ip(self):
        """

        Returns
        -------
        str:
             a ip address has str type
        """
        ip = self.data.get(ChangeDeltaMappingKey.IP)
        return ip

    def get_username(self):
        """

        Returns
        -------
        str:
             a username has str type
        """
        username = self.data.get(ChangeDeltaMappingKey.USERNAME)
        return username

    def get_password(self):
        """

        Returns
        -------
        str:
            a password has str type
        """
        password = self.data.get(ChangeDeltaMappingKey.PASSWORD)
        return password

    def load(self):
        """
        Load file from user@ip:path to current folder.
        Returns
        -------
        str:
            path to the file in current folder.
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


class ChangeDeltaMappingHandler(JsonHandler):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(ChangeDeltaMappingHandler, self).__init__(**kwargs)

    def get_change(self, delta):
        """

        Parameters
        ----------
        delta str:
            a delta of merged change

        Returns
        -------
        str
            change of the delta.

        """
        for change in self.data.keys():
            if self.data.get(change) == delta:
                return change

    def get_delta(self, change):
        """

        Parameters
        ----------
        change:
            a change of delta merged.

        Returns
        -------
        str
            a delta of the change
        """
        return self.data.get(change)
