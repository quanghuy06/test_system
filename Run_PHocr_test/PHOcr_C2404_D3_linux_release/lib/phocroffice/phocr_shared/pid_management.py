# -*- encoding: utf-8 -*-
# Copyright (C) 2017 TSDV TTEC.  All rights reserved.

import os


class PIDManagement(object):
    """
    Manage the job create and delete file that contains PID of current python
    process and used by PHOcr to handle cancellation functionality
    """

    def __init__(self, pid_file_name):
        self.pid_file_name = pid_file_name

    def create_pid_file(self):
        """
        Get pid of current running process and save it to file
        """
        current_pid = os.getpid()
        pid_file = open(self.pid_file_name, "w")
        pid_file.write(str(current_pid))
        pid_file.close()

    def remove_pid_file(self):
        """
        Remove pid file after run successfully
        """
        if os.path.isfile(self.pid_file_name):
            os.remove(self.pid_file_name)
