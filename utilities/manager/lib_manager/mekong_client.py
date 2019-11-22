# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      19/06/2018
# Description:      This define base class of a client machine. To execute this code, you need
#                   to stand on master machine. And master machine also need to be Ubuntu machine.

import pexpect
import traceback
import time
# Import base APIs
from baseapi.log_manager import Logger
from configs.timeout import TimeOut
from configs.messages import StandardMessages, ErrorMessages
from utils.paramiko_helper import ParamikoHelper


# Class for client ssh definition. Notice that master need to be authenticated by client.
# This can be done by using "ssh-copy-id -i" command from master to client.
# Example: In the terminal from master, type this
#               ssh-copy-id -i ~/.ssh/id_rsa.pub <client name>@<client IP>
# Without this, code will be failed to execute.
class MekongClient(object):
    def __init__(self, name="", ip="", username="", password="", log_level=-1):
        # This is machine name
        self.name = name
        # Password of username on virtual machine
        self.password = password
        # This is IP address of client
        self.ip = ip
        # This is username will be used to ssh
        self.username = username
        # Logger
        # < 0: No log
        # 0 : reduced log
        # 1 : log execute command
        # > 1: log detail transfer file/folder
        self.log_level = log_level
        self.logger = Logger(name=self.name, log_disable=(self.log_level < 0))
        super(MekongClient, self).__init__()
        self.paramiko_helper = None

    def init_ssh_connection(self):
        if self.ip and self.username:
            self.paramiko_helper = ParamikoHelper(self.ip, self.username, self.password)
        else:
            error_msg = "Can not connect to {0} with {1} and {2}"
            error_msg = error_msg.format(self.name, self.username, self.password)
            raise Exception(error_msg)

    # Node execute a command
    def exec_command(self, cmd, timeout=TimeOut.Default.EXECUTE_COMMAND, cwd=None):

        # Execute over ssh
        if cwd is not None:
            cmd = "cd {0} && {1}".format(cwd, cmd)

        if self.paramiko_helper is None:
            self.init_ssh_connection()

        self.logger.add_line("# EXECUTE COMMAND:  {0}".format(cmd))
        std_in, std_out, std_err = \
            self.paramiko_helper.exec_command(cmd, timeout=timeout)
        if self.log_level > 0:
            self.logger.add_line("\t{0}:".format(StandardMessages.StandartIO.STDOUT))
            for line in std_out:
                self.logger.add_line("\t\t" + line)
            self.logger.add_end_line()
            self.logger.add_line("\t{0}".format(StandardMessages.StandartIO.STDERR))
            for line in std_err:
                self.logger.add_line("\t\t" + line)
        res = std_out.channel.recv_exit_status()
        if res:
            error_msg = "run cmd {0} return exit code: {1}".format(cmd, res)
            raise Exception(error_msg)

    def exec_command_without_err(self, cmd, timeout=TimeOut.Default.EXECUTE_COMMAND, cwd=None):
        # Execute over ssh
        if cwd is not None:
            cmd = "cd {0} && {1}".format(cwd, cmd)

        if self.paramiko_helper is None:
            self.init_ssh_connection()

        self.logger.add_line("# EXECUTE COMMAND:  {0}".format(cmd))
        std_in, std_out, std_err = \
            self.paramiko_helper.exec_command(cmd, timeout=timeout)

    # Node execute a command
    def exec_command_with_channel(self, cmd, timeout=None, cwd=None):

        # Execute over ssh
        if cwd is not None:
            cmd = "cd {0} && {1}".format(cwd, cmd)

        if self.paramiko_helper is None:
            self.init_ssh_connection()

        self.logger.add_line("# EXECUTE COMMAND:  {0}".format(cmd))
        self.paramiko_helper.execute_with_channel(cmd, timeout=timeout)

    # Node execute a command with sudo privileges
    def exec_sudo_command(self, cmd, timeout=TimeOut.Default.EXECUTE_COMMAND, cwd=None):

        # Execute over ssh
        if cwd is not None:
            cmd = "cd {0} && {1}".format(cwd, cmd)

        self.logger.add_line("# EXECUTE COMMAND:  {0}".format(cmd))

        if self.paramiko_helper is None:
            self.init_ssh_connection()

        try:
            std_in, std_out, std_err = \
                self.paramiko_helper.exec_command(cmd, timeout=timeout)
            std_in.write(self.password + "\n")
            if self.log_level == 1:
                self.logger.add_line("\t{0}:".format(StandardMessages.StandartIO.STDOUT))
                for line in std_out:
                    self.logger.add_line("\t\t" + line)
                self.logger.add_end_line()
                self.logger.add_line("\t{0}".format(StandardMessages.StandartIO.STDERR))
                for line in std_err:
                    self.logger.add_line("\t\t" + line)
            return std_out.channel.recv_exit_status()

        except Exception:
            var = traceback.format_exc()
            self.logger.log_and_print(var)
            raise Exception(ErrorMessages.Ssh.EXEC_CMD.format(cmd, self.name))

    # Get file/folder from master
    def get(self, local_path, client_path, timeout=TimeOut.Default.SEND_FILE):

        self.logger.add_line(StandardMessages.Ssh.GET_FILE.format(local_path, self.name,
                                                                  client_path))
        # Basically, we stand on master side and execute scp command. So this code only do on
        # a ubuntu master machine.
        cmd = "scp -r {0} {1}@{2}:{3}".format(local_path, self.username, self.ip, client_path)
        self.logger.add_line(cmd)
        child = pexpect.spawn(cmd)
        no_such_file_mgs = ErrorMessages.FileIO.NO_FILE.format(local_path, client_path)
        opts = [pexpect.EOF, ErrorMessages.Network.NO_ROUTE, no_such_file_mgs ,
                pexpect.TIMEOUT]

        # Check output of pexpect executing command
        while True:
            index = child.expect(opts, timeout)
            if index == 0:
                # End normally -> Success
                if self.log_level > 1:
                    self.logger.add_line(child.before)
                return 0

            elif index == 1:
                # Network error. No route to host, client is disconnected.
                self.logger.add_line(child.before)
                self.logger.log_and_print(ErrorMessages.Network.NO_ROUTE)
                raise Exception(ErrorMessages.Network.NO_ROUTE)

            elif index == 2:
                # File IO error. Can not find file local on master or remote on client
                self.logger.add_line(child.before)
                self.logger.log_and_print(no_such_file_mgs)
                raise Exception(no_such_file_mgs)

            else:
                # Time out
                self.logger.add_line(child.before)
                self.logger.log_and_print(
                    ErrorMessages.Network.TIMEOUT_DETAIL.format(timeout))
                raise Exception(ErrorMessages.Network.TIMEOUT)

    # Copy file/folder from client to master
    def put(self, client_path, local_path,
            timeout=TimeOut.Default.SEND_FILE):

        self.logger.add_line(StandardMessages.Ssh.PUT_FILE.format(client_path, self.name,
                                                                  local_path))

        # Same as get file/folder. Base on scp command of linux
        cmd = "scp -r {1}@{2}:{3} {0}".format(local_path,
                                              self.username,
                                              self.ip, client_path)
        self.logger.add_line(cmd)
        child = pexpect.spawn(cmd)
        no_such_file_mgs = ErrorMessages.FileIO.NO_FILE.format(client_path, local_path)
        opts = [pexpect.EOF, ErrorMessages.Network.NO_ROUTE, no_such_file_mgs,
                pexpect.TIMEOUT]

        # Check output of pexpect execute command
        while True:
            index = child.expect(opts, timeout)
            if index == 0:
                # End normally -> Success
                if self.log_level > 1:
                    self.logger.add_line(child.before)
                return 0

            elif index == 1:
                # Network error, no route to client or client disconnected
                self.logger.add_line(child.before)
                self.logger.log_and_print(ErrorMessages.Network.NO_ROUTE)
                raise Exception(ErrorMessages.Network.NO_ROUTE)

            elif index == 2:
                # File IO error. Can not find file local on master or remote on client
                self.logger.add_line(child.before)
                self.logger.log_and_print(no_such_file_mgs)
                raise Exception(no_such_file_mgs)

            else:
                # Time out
                self.logger.add_line(child.before)
                self.logger.log_and_print(ErrorMessages.Network.TIMEOUT_DETAIL.format(timeout))
                raise Exception(ErrorMessages.Network.TIMEOUT)

    def put_one_test_case(self, client_path, local_path, timeout=TimeOut.Default.SEND_FILE):
        pass

    @staticmethod
    def is_connected():
        return True

    def is_exist(self, client_path):
        """
        Check if file/directory exist on client machine

        Parameters
        ----------
        client_path str

        Returns
        -------
        bool
            True if file/directory exist on client machine. Otherwise, return False.

        """
        if self.paramiko_helper is None:
            self.init_ssh_connection()

        return self.paramiko_helper.is_exist(client_path=client_path)

    def remove_file(self, client_path):
        """
        If file exists on client machine then remove it. Otherwise, nothing to do.

        Parameters
        ----------
        client_path str

        Returns
        -------
        None

        """
        if self.paramiko_helper is None:
            self.init_ssh_connection()

        self.paramiko_helper.remove_file(client_path=client_path)

    def remove_directory(self, client_path):
        """
        If directory exists on client machine then remove it. Otherwise, nothing to do.

        Parameters
        ----------
        client_path str

        Returns
        -------
        None

        """
        if self.paramiko_helper is None:
            self.init_ssh_connection()

        self.paramiko_helper.remove_directory(client_path=client_path)

    def make_directory(self, client_path):
        """
        If directory does not exist on client machine then create it. This function has behavior
        same as mkdir -p on linux system.

        Parameters
        ----------
        client_path str

        Returns
        -------
        None

        """
        if self.paramiko_helper is None:
            self.init_ssh_connection()

        self.paramiko_helper.make_directory(client_path=client_path)
        # Make sure new directory ready
        time.sleep(1)

    def copy(self, client_src, client_des, timeout=TimeOut.Default.SEND_FILE):
        """
        Copy file/folder on a client.

        Parameters
        ----------
        client_src : str
            Source directory on client
        client_des : str
            Destination on client
        timeout : str
            Timeout of transferring data. It will stop when time up.

        Returns
        -------
        None

        """
        cmd = "cp -rn {src} {des}".format(src=client_src, des=client_des)
        self.exec_command(cmd=cmd, timeout=timeout)
