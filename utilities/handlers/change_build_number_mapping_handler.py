from handlers.lib_base.json_handler import JsonHandler
from abc import ABCMeta
from configs.json_key import BuiltManagerKey, ChangeBuildMappingKey
import subprocess
import os


class ChangeBuildNumberMappingConfigureHandler(JsonHandler):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(ChangeBuildNumberMappingConfigureHandler, self).__init__(**kwargs)
        self.data = self.data.get(BuiltManagerKey.CHANGE_BUILD_NUMBER)

    def get_path(self):
        """

        Returns
        -------
        str:
            path to change build mapping

        """
        path = self.data.get(ChangeBuildMappingKey.PATH)
        return path

    def get_ip(self):
        """

        Returns
        -------
        str:
            a str class of ip address

        """
        ip = self.data.get(ChangeBuildMappingKey.IP)
        return ip

    def get_username(self):
        """

        Returns
        -------
        str:
             a string class of username

        """
        username = self.data.get(ChangeBuildMappingKey.USERNAME)
        return username

    def get_password(self):
        """

        Returns
        -------
        str:
            a string class of password

        """
        password = self.data.get(ChangeBuildMappingKey.PASSWORD)
        return password

    def load(self):
        """
        Copy file from username@ip:path to current folder.
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


class ChangeBuildNumberMappingHandler(JsonHandler):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(ChangeBuildNumberMappingHandler, self).__init__(**kwargs)

    def build_number(self, change):
        """

        Parameters
        ----------
        change str:
            the change is merged.

        Returns
        -------
        str:
            a build number has int type

        """
        return self.data.get(change)
