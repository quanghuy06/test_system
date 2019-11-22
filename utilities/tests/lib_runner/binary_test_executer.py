from configs.timeout import TimeOut
from tests.lib_runner.base_test_executer import BaseTestExecuter
import re

class BinaryTestExecuter(BaseTestExecuter):
    """
    This class aims to run user specific binary and command to run test case
    This class will use "binary_test_information" field to get information
    To make code use this class, define "component" field to "binary_test"
    """

    def __init__(self):
        # type: () -> object
        super(BinaryTestExecuter, self).__init__()

    def execute_test(self, test_tool, params, image_path,
                     timeout = TimeOut.execute.BINARY_TEST_DEFAULT_RUN_ONE):
        cmds = [test_tool]
        cmds += re.split(' +', params.strip())
        cmds += [image_path]

        return self.run_test_in_subprocess(cmds, timeout)
