# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created:     21/04/2017
# Last update:      30/06/2017
# Updated by:       Phung Dinh Tai
# Description:      This script define class to execute barcode testing

import os
import subprocess
import re
from threading import Timer
from configs.projects.phocr import PhocrProject
from configs.test_result import TestResultJsonKeys
from configs.timeout import TimeOut

class BarcodeTestExecuter:
    def execute_one_test(self, testtool, params, image_path,
                         timeout = TimeOut.execute.BARCODE_DEFAULT_RUN_ONE):
        # Run barcode executable with image file
        cmds =  [testtool]
        cmds += re.split(' +', params)
        cmds += [image_path]

        # TODO(HuanLV) use BaseTestExecuter class to remove duplication
        import time
        start_time = time.time()
        test_proc = subprocess.Popen(cmds, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, shell = False)

        timer = Timer(timeout, test_proc.terminate)
        timer.start()

        try:
            test_stdout, test_sterr = test_proc.communicate()
        finally:
            timer.cancel()

        exe_time = time.time() - start_time
        rc = test_proc.returncode

        is_timeout = exe_time > timeout

        if not is_timeout:
            output_log = str(test_stdout.decode("utf-8"))
            error_log = str(test_sterr.decode("utf-8"))
        else:
            output_log = ""
            error_log = "Time out, terminated! Test case run over {0}s\n".format(timeout)

        return {
            TestResultJsonKeys.STDOUT: output_log,
            TestResultJsonKeys.STDERR: error_log,
            TestResultJsonKeys.TIME: exe_time,
            TestResultJsonKeys.CODE: rc
        }

    ###########################################################################
    # Execute executable of Barcode Detection/Detected
    def execute_test(self, test_tool, params, image_path, timeout):

        if not image_path:
            return {
                TestResultJsonKeys.STDOUT : "",
                TestResultJsonKeys.STDERR : "No test data (images) founded!",
                TestResultJsonKeys.TIME : 0,
                TestResultJsonKeys.CODE : 123
            }

        if len(image_path) == 1:
            return self.execute_one_test(testtool=test_tool, params=params, image_path=image_path[0],
                                         timeout=timeout)
        else:
            stdout = ""
            stderr = ""
            time = 0
            exitcode = 0
            detail = {}
            for image_path in image_path:
                stdout += "##### IMAGE: {0}\n".format(os.path.basename(image_path))
                stderr += "##### IMAGE: {0}\n".format(os.path.basename(image_path))
                image_result = self.execute_one_test(testtool=test_tool, params=params,
                                                     image_path=image_path, timeout=timeout)
                detail[image_path] = image_result
                # Append to final result
                stdout += image_result[TestResultJsonKeys.STDOUT]
                stderr += image_result[TestResultJsonKeys.STDERR]
                time += image_result[TestResultJsonKeys.TIME]
                if image_result[TestResultJsonKeys.CODE] != 0:
                    exitcode = image_result[TestResultJsonKeys.CODE]
            return {
                TestResultJsonKeys.STDOUT : stdout,
                TestResultJsonKeys.STDERR : stderr,
                TestResultJsonKeys.TIME : time,
                TestResultJsonKeys.CODE : exitcode
            }
