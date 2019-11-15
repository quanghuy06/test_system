import os
from svn import remote
from svn.local import LocalClient
from configs.credential import Credential


class SvnConnector:
    def __init__(self):
        self.credential = Credential()
        self.user, self.password = self.credential.get_account_for("svn")

    def connect_remote_client(self, url):
        """

        Parameters
        ----------
        url str:
            url

        Returns
        -------
        RemoteClient
            remote client
        """
        return remote.RemoteClient(
            url,
            username=self.user,
            password=self.password
        )

    def connect_local_client(self, path):
        """

        Parameters
        ----------
        path str:
            path

        Returns
        -------
        LocalClient
            local client
        """
        if not os.path.isdir(path):
            os.makedirs(path)
        return LocalClient(
            path,
            username=self.user,
            password=self.password
        )
