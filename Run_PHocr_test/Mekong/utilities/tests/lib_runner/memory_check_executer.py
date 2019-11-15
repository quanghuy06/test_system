# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created:     29/08/2017
# Last updated:     29/08/2017
# Update by:        Phung Dinh Tai
# Description:      This script define a class for execute memory checking

import subprocess
import re
import os
import csv
from threading import Timer
from configs.test_result import TestResultJsonKeys
from configs.timeout import TimeOut
from configs.projects.mekong import TestSystem
from configs.projects.mekong import ValGrind
from configs.test_result import TestResultConfig


class MemCheckExecutor(object):
    def __init__(self, is_check_memory_peak):
        self.is_check_memory_peak = is_check_memory_peak

    # Execute executable of PHOcr
    def execute_test(self, test_tool, params, image_path,
                     timeout=TimeOut.execute.MEMCHECK_DEFAULT_RUN_ONE):
        # Run phocr executable with image file
        valgrind_abs_path = os.path.join(TestSystem.Paths.EXECUTABLES_ABS_DIR,
                                         ValGrind.VALGRIND_FOLDER,
                                         ValGrind.BIN_FOLDER,
                                         ValGrind.BINARY)
        print"path of valgrind: {0}".format(valgrind_abs_path)
        cmds = [valgrind_abs_path]
        cmds += [ValGrind.OPT_LOG_FILE.format(log_file=ValGrind.LOG_FILE_DEFAULT)]
        cmds += self.get_valgrind_option()
        cmds += [test_tool]
        cmds += re.split(' +', params)

        if type(image_path) == list:
            cmds += image_path
        elif type(image_path) == str:
            cmds += [image_path]

        my_env = os.environ.copy()
        my_env[ValGrind.ENV_LIB] = os.path.join(
            TestSystem.Paths.EXECUTABLES_ABS_DIR,
            ValGrind.VALGRIND_FOLDER,
            ValGrind.LIB_FOLDER,
            ValGrind.LIB_ENV)

        # TODO(HuanLV) use BaseTestExecuter class to remove duplication
        import time
        start_time = time.time()
        tess_proc = subprocess.Popen(cmds, stdout=subprocess.PIPE, env=my_env,
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
            output_log = str(tess_stdout.decode("utf-8"))
            error_log = str(tess_stderr.decode("utf-8"))
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
        memory_path = os.path.join(os.getcwd(), TestResultConfig.PHOCR_MEMORY_LOG)
        memory_peaks = []
        if os.path.isfile(memory_path):
            print("is file")
            with open(memory_path) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='\t')
                line_count = 0
                for row in csv_reader:
                    if line_count != 0:
                        item_memory_peak = dict()
                        item_memory_peak[
                            TestResultJsonKeys.MemoryItem.COMMAND
                        ] = '"' + row[0] + '"'
                        item_memory_peak[
                            TestResultJsonKeys.MemoryItem.MEMORY_PEAK
                        ] = row[1]
                        memory_peaks.append(item_memory_peak)
                    line_count += 1
            os.remove(memory_path)
        log[TestResultJsonKeys.MEMORY] = memory_peaks
        return log

    def get_valgrind_option(self):
        """
        Get valgrind command line, it may be check memory leak or memory peak


        Returns
        -------
        str:
            Command for checking memory leak and in the other case, checking for
             memory peak

        """

        if self.is_check_memory_peak:
            return [ValGrind.OPT_PEAK_CHECK]
        else:
            return [ValGrind.OPT_LEAK_CHECK.format(opt=ValGrind.LEAK_CHECK_FULL)]
