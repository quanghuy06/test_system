# Toshiba - TSDV
# Team:         PHOcr
# Author:       Le Duc Nam
# Email:        nam.leduc@toshiba-tsdv.com
# Date created:     12/06/2016
# Last updated:     30/06/2017
# Update by:        Phung Dinh Tai
# Description:      This script define a class for execute testing
import subprocess
import re
import csv
import os
from threading import Timer
from configs.test_result import TestResultJsonKeys
from configs.timeout import TimeOut
from configs.test_result import TestResultConfig


class PHOcrTestExecuter:

    def __init__(self):
        pass

    def execute_test(self, test_tool, params, image_path,
                     timeout = TimeOut.execute.PHOCR_DEFAULT_RUN_ONE):

        # Run tesseract executable with image file
        cmds = [test_tool]
        cmds += re.split(' +', params)
        cmds += [image_path]

        # TODO(HuanLV) use BaseTestExecuter class to remove duplication
        import time
        start_time = time.time()
        tess_proc = subprocess.Popen(cmds, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE, shell=False)

        timer = Timer(timeout, tess_proc.terminate)
        timer.start()

        try:
            tess_stdout, tess_stderr = tess_proc.communicate()
        finally:
            timer.cancel()

        exe_time = time.time() - start_time
        rc = tess_proc.returncode

        is_timeout = exe_time > timeout

        if not is_timeout:
            output_log = tess_stdout.decode('utf-8')
            error_log = tess_stderr.decode('utf-8')
        else:
            output_log = ""
            error_log = "Time out, terminated! Test case run over {0}s\n".format(timeout)

        log = {
            TestResultJsonKeys.STDOUT: output_log,
            TestResultJsonKeys.STDERR: error_log,
            TestResultJsonKeys.TIME: exe_time,
            TestResultJsonKeys.CODE: rc,
            TestResultJsonKeys.OPTION: " ".join(re.split(' +', params))
        }

        memory_peaks = []
        memory_path = TestResultConfig.PHOCR_MEMORY_LOG
        if os.path.isfile(memory_path):
            with open(memory_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='\t')
                line_count = 0
                for row in csv_reader:
                    if line_count != 0:
                        item_memory_peak = dict()
                        item_memory_peak [
                            TestResultJsonKeys.MemoryItem.COMMAND
                        ] = '"' + row[0] + '"'
                        item_memory_peak [
                            TestResultJsonKeys.MemoryItem.MEMORY_PEAK
                        ] = row[1]
                        memory_peaks.append(item_memory_peak)
                    line_count += 1
            os.remove(memory_path)
        log[TestResultJsonKeys.MEMORY] = memory_peaks
        return log
