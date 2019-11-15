# Author: Trong Nguyen Van
# Created: 07/08/2019
# This module help us work with SSH connection through paramiko library

import paramiko
import os
import pexpect
from scp import SCPClient


class FileUtility(object):
    """
    Just an utility class that help me to hanfle file
    """

    @classmethod
    def detect_file_stem(cls, filename):
        i = 0
        for i in range(len(filename), 0, -1):
            if filename[i - 1] == ".":
                break
        return filename[0: i - 1]

    @classmethod
    def empty_directory(cls, folder_path):
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.unlink(file_path)


class SSHUtility(object):
    """
    A SSH utility that help me to copy files/ directory between local and server.
    As long as execute command over ssh connection
    """

    def __init__(self, server_addr, username, password):
        self.server_addr = server_addr
        self.username = username
        self.password = password
        self.ssh_client = None
        self.connect()
        self.scp_client = SCPClient(self.ssh_client.get_transport())

    def __del__(self):
        # Close connection
        if self.ssh_client is not None:
            self.ssh_client.close()

    def connect(self):
        """
        ssh connect to the server
        """
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.load_system_host_keys()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh_client.connect(self.server_addr, username=self.username, password=self.password)

    def push_to_server(self, local_path, server_path):
        """
        Push directory from local to server
        """
        self.scp_client.put(local_path, server_path, recursive=True)

    def push_to_server_high_performance(self, local_path, server_path):
        """
        This method use the scp command of linux to push data to server. This implementation is much faster than
        the SCP implemented in python
        :param local_path:
        :param server_path:
        :return:
        """
        scp_command = "scp -r " + local_path + " " + self.username + "@" + self.server_addr + ":" + server_path
        try:
            var_child = pexpect.spawn(scp_command, timeout=1000)
            i = var_child.expect([".*:", pexpect.EOF])

            if i == 0:  # send password
                var_child.sendline(self.password)
                var_child.expect(pexpect.EOF)
            elif i == 1:
                print("Got the key or connection timeout")
                pass
        except pexpect.TIMEOUT:
            print("Timeout occur with module pexpect")
        except Exception as e:
            print("Using scp command of linux system failed!")
            print(e)

    def download_to_local(self, server_path, local_path):
        """
        Download directory from server to local
        """
        self.scp_client.get(server_path, local_path, recursive=True)
