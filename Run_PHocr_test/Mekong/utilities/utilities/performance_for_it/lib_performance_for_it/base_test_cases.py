import pexpect
import os


class BaseTestCases(object):
    @staticmethod
    def get_from_svn(svn_path):
        """

        Parameters
        ----------
        svn_path str:
            path to svn

        Returns
        -------
        str
            a list test cases
        """
        command = "svn export --force {0}".format(svn_path)

        child = pexpect.spawn(command, timeout=36000)
        child.expect(pexpect.EOF)
        exit_code = child.exitstatus
        if exit_code:
            print(child.before)
            assert False, "Can not run performance analysis, exit code {0}".format(exit_code)

        base_name = os.path.basename(svn_path)
        local_path = os.path.join(os.getcwd(), base_name)
        with open(local_path, 'r') as f:
            test_cases = f.read().splitlines()
        return test_cases

    @staticmethod
    def to_str(base_test_cases):
        """

        Parameters
        ----------
        base_test_cases list:
            list of test cases

        Returns
        -------
        str:
            string id of list test cases

        """
        return ",".join(base_test_cases)
