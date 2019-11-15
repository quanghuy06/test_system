import subprocess
import re
from threading import Timer
from configs.test_result import TestResultJsonKeys
from configs.timeout import TimeOut
from tests.lib_runner.test_result import TestResult


class BaseTestExecuter(object):
    def __init__(self):
        pass

    def run_test_in_subprocess(self, cmds,
                     timeout = TimeOut.execute.PHOCR_DEFAULT_RUN_ONE):

        # Run tesseract executable with image file
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

        # Get command args to report
        args = " ".join(cmds[1:])

        # Remove all duplicate spaces, trailing spaces
        args = args.replace(' +', ' ')
        args = args.strip()
        test_result = TestResult(rc,
                                 output_log,
                                 error_log,
                                 exe_time,
                                 args)
        return test_result.__dict__
