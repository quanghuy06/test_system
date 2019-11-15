# Toshiba - TSDV
# Team:         PHOcr
# Author:       Le Duc Nam
# Email:        nam.leduc@toshiba-tsdv.com
# Date created: 12/08/2016
# Last updated: 28/06/2017
# Updated by:   Phung Dinh Tai
# Description:  This script define class for run testing test cases of HanoiWorkflow project

import subprocess
from threading import Timer

from configs.test_result import TestResultJsonKeys
from configs.timeout import TimeOut

class HanoiTestExecuter:
    ###########################################################################
    # Execute executable of Hanoi
    def execute_test(self, test_tool, image_path, config_file,
                     timeout=TimeOut.execute.HANOI_DEFAULT_RUN_ONE):

        # Run tesseract executable with image file
        cmds =  [test_tool]
        cmds += [image_path]
        cmds += [config_file]

        # TODO(HuanLV) use BaseTestExecuter class to remove duplication
        import time
        start_time = time.time()
        test_proc = subprocess.Popen(cmds, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, shell = False)

        timer = Timer(timeout, test_proc.terminate)
        timer.start()

        try:
            tess_stdout, tess_stderr = test_proc.communicate()
        finally:
            timer.cancel()

        exe_time = time.time() - start_time
        rc = test_proc.returncode

        is_timeout = exe_time > timeout

        if not is_timeout:
            output_log = str(tess_stdout.decode("utf-8"))
            error_log = str(tess_stderr.decode("utf-8"))
        else:
            output_log = ""
            error_log = "Time out, terminated! Test case run over {0}s\n".format(timeout)

        return {
            TestResultJsonKeys.STDOUT: output_log,
            TestResultJsonKeys.STDERR: error_log,
            TestResultJsonKeys.TIME: exe_time,
            TestResultJsonKeys.CODE: rc
        }
