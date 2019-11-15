# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Luong Van Huan
# Date create:      12/12/2018
# Description:      This script used for provide several ways to run a
#                   terminal command by python.

import pexpect
import subprocess
from threading import Timer

from configs.messages import ErrorMessages


class CommandRunner(object):
    """
    This class provide several ways to run a command:
    pexpect, os.sys

    """

    @staticmethod
    def run_with_subprocess(commands, timeout=None):
        """
        Run system command with subprocess
        Parameters
        ----------
        commands: list
            list to make a command
        timeout: int
            timeout to terminate command


        Returns
        -------
        tuple
            stdout, stderr of the command

        """
        sub_proc = subprocess.Popen(commands,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,
                                    shell=False)
        timer = None
        if timeout:
            timer = Timer(timeout, sub_proc.terminate)
            timer.start()

        try:
            stdout, stderr = sub_proc.communicate()
        finally:
            if timer:
                timer.cancel()

        return_code = sub_proc.returncode
        if return_code != 0:
            error_msg = "Run command: {0} error with error code: {1}," \
                        " message: {2}"
            error_msg = error_msg.format(commands, return_code, stderr)
            raise Exception(error_msg)
        return stdout, stderr
