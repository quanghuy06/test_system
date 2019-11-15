# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:
# Last update:      Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/09/2019
# Description:      This script define class which help us work with remote machine.

import os
import paramiko
import time
import stat
from configs.timeout import TimeOut


class ParamikoHelper:

    def __init__(self, ip, user, pwd):
        self.ip = ip
        self.user = user
        self.pwd = pwd
        self.client = None
        self.create_ssh_connection()

    def create_ssh_connection(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy())
            self.client.connect(self.ip, username=self.user, timeout=TimeOut.ssh.CONNECT,
                                password=self.pwd)
        except paramiko.AuthenticationException:
            error_msg = "Authentication failed, please verify your credentials"
            raise Exception(error_msg)
        except paramiko.SSHException as sshException:
            error_msg = "Unable to establish SSH connection: {0}".format(sshException)
            raise sshException

    def check_ssh_connection(self, interval=0.1, retries=100):
        for x in range(retries):
            try:
                self.client.exec_command("ls", timeout=3)
                return True
            except Exception as exception:
                print (exception)
                time.sleep(interval)
        return False

    def exec_command(self, cmd, timeout, inputs=None):
        std_in, std_out, std_err = \
            self.client.exec_command(cmd, timeout=timeout)
        if inputs is not None:
            for input_var in inputs:
                std_in.write(input_var)
        return std_in, std_out, std_err

    def execute_with_channel(self, cmd, timeout):
        """

        :param cmd: the command to be executed on the remote computer
        :examples:  execute('ls')
                    execute('finger')
                    execute('cd folder_name')
        """
        channel = self.client.invoke_shell()
        channel.settimeout(timeout)
        self.stdin = channel.makefile('wb')
        self.stdout = channel.makefile('r')

        cmd = cmd.strip('\n')
        self.stdin.write(cmd + '\n')
        finish = 'end of stdOUT buffer. finished with exit status:'
        echo_cmd = 'echo {} $?'.format(finish)
        self.stdin.write(echo_cmd + '\n')
        shin = self.stdin
        self.stdin.flush()
        shout = []
        sherr = []
        for line in self.stdout:
            str_line = str(line)
            if str_line.startswith(cmd) or str_line.startswith(echo_cmd):
                shout = []
            elif str_line.startswith(finish):
                exit_status = (str_line.split(":"))[1]
                exit_status = exit_status.strip()
                exit_status = int(exit_status)
                if exit_status:
                    error_msg = "Run cmd {0} with channel failure!!!"
                    error_msg = error_msg.format(cmd)
                    raise Exception(error_msg)
                break
            else:
                shout.append(str_line)
        return shin, shout, sherr

    def exec_command_with_password(self, cmd, timeout, password):
        std_in, std_out, std_err = \
            self.client.exec_command(cmd, timeout=timeout)
        std_in.write(password + "\n")
        return std_in, std_out, std_err

    def is_exist(self, client_path):
        """
        Check if file/directory exists on a remote machine

        Parameters
        ----------
        client_path str

        Returns
        -------
        bool
            True if file/directory exists. Otherwise, return False

        """
        sftp = self.client.open_sftp()
        try:
            sftp.stat(client_path)
            return True
        except IOError:
            return False
        finally:
            sftp.close()

    def is_file(self, client_path):
        """
        Check if file exists on a remote machine

        Parameters
        ----------
        client_path str

        Returns
        -------
        bool
            True if file exists on remote. Otherwise, return False

        """
        sftp = self.client.open_sftp()
        try:
            return stat.S_ISREG(sftp.stat(client_path).st_mode)
        except IOError:
            return False
        finally:
            sftp.close()

    def is_dir(self, client_path):
        """
        Check if folder exist on a remote machine

        Parameters
        ----------
        client_path str

        Returns
        -------
        bool
            True if directory exists on remote. Otherwise, return False

        """
        sftp = self.client.open_sftp()
        try:
            return stat.S_ISDIR(sftp.stat(client_path).st_mode)
        except IOError:
            return False
        finally:
            sftp.close()

    def remove_file(self, client_path):
        """
        If client path is a file and exists on remote machine, then file will be deleted. Otherwise,
        nothing to do.

        Parameters
        ----------
        client_path str

        Returns
        -------
        None

        """
        if self.is_file(client_path=client_path):
            sftp = self.client.open_sftp()
            sftp.remove(client_path)
            sftp.close()

    def remove_directory(self, client_path, timeout=360):
        """
        If client path is a directory and exists on remote machine, then delete it. Otherwise,
        nothing to do.

        Parameters
        ----------
        client_path str

        Returns
        -------
        None

        """
        start_time = time.time()
        if self.is_exist(client_path=client_path):
            cmd = "rm -rf {path}".format(path=client_path)
            self.exec_command(cmd=cmd, timeout=timeout)

        # Make sure directory is removed before leave
        execution_time = time.time() - start_time
        while self.is_exist(client_path=client_path) and execution_time < timeout:
            time.sleep(0.1)
            execution_time = time.time() - start_time

        # If directory still exit then something happen
        if self.is_exist(client_path=client_path):
            raise IOError("Can not remove directory {dir}".format(dir=client_path))

    def make_directory(self, client_path):
        """
        If client path does not exist on remote machine then create it. Otherwise, nothing to do.
        Behavior same as mkdir -p on linux system.

        Parameters
        ----------
        client_path str

        Returns
        -------
        None

        """
        # If directory is already existed then nothing to do
        if self.is_exist(client_path=client_path):
            return
        start_time = time.time()
        # Create directory recursively
        # Create parent directory first
        dir_name = os.path.dirname(client_path)
        if not self.is_exist(client_path=dir_name):
            self.make_directory(client_path=dir_name)
        # Create target directory
        sftp = self.client.open_sftp()
        sftp.mkdir(client_path)
        sftp.close()

        # Make sure directory is ready
        timeout = 300
        execution_time = time.time() - start_time
        while not self.is_exist(client_path=client_path) and execution_time < timeout:
            time.sleep(0.1)
            execution_time = time.time() - start_time

        # If directory is still not ready, then somthing happen
        if not self.is_dir(client_path=client_path):
            raise IOError("Can not create directory {dir}".format(dir=client_path))
