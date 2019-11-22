from performance_for_it.lib_performance_for_it.base_test_cases import BaseTestCases
from performance_for_it.lib_performance_for_it.distribution import Distribution
import subprocess
from datetime import datetime
import shutil
import json
import pexpect
import os


class PerformanceRunner:

    PYTHON = 'python2.7'
    BOARD_IP = '--board-ip'
    BUILD_PACKAGE_LINK = '--build-package-link'
    MEKONG_PATH = '--mekong-path'
    GERRIT_CHECKOUT = '--gerrit-checkout'
    ID = '--id'

    def __init__(self, built_manager_handler, build_package_link, gerrit_checkout, list_test_cases):
        self.built_manager_hander = built_manager_handler
        self.build_package_link = build_package_link
        self.gerrit_checkout = gerrit_checkout
        self.list_test_cases = list_test_cases

    def _combine_result(self):
        """

        Returns
        -------
        dict
            a combine result
        """
        cwd = os.getcwd()
        res = os.path.join(cwd, "res")
        name_build_package = os.path.basename(self.build_package_link)
        name_build_package = os.path.splitext(name_build_package)[0]
        file_test_result = os.path.join(res, 'test_result_{}.json'.format(name_build_package))
        test_result = dict()
        with open(file_test_result, "rb") as fts:
            data = json.load(fts)
            for data_item in data:
                test_result.update(data_item)
        return test_result

    def _run(self, str_id):
        """

        Parameters
        ----------
        str_id str:
            string id of test cases.

        Returns
        -------

        """
        board_ip = ",".join(self.built_manager_hander.get_board_ip())
        script = self.built_manager_hander.get_run_performance_analysis_path()
        mekong = self.built_manager_hander.get_mekong()
        command = [
            PerformanceRunner.PYTHON, script,
            PerformanceRunner.BOARD_IP, board_ip,
            PerformanceRunner.BUILD_PACKAGE_LINK, self.build_package_link,
            PerformanceRunner.MEKONG_PATH, mekong,
            PerformanceRunner.GERRIT_CHECKOUT, "\"" + self.gerrit_checkout + "\"",
            PerformanceRunner.ID, str_id
        ]
        str_command = " ".join(command)
        if len(str_command) > 500:
            print "Command:: ", str_command[:500], "..."
        else:
            print "Command::", str_command
        child = pexpect.spawn(str_command, timeout=36000)
        child.expect(pexpect.EOF)
        exit_code = child.exitstatus
        if exit_code:
            print(child.before)
            assert False, "Can not run performance analysis, exit code {0}".format(exit_code)

    def run_distribute(self, output_test_result):
        """

        Parameters
        ----------
        output_test_result str:
            output test result

        Returns
        -------
        dict:
            a performance data
        """
        start = datetime.now()
        test_result = {}
        distribution_data = Distribution.get('distribution.json', self.list_test_cases)
        for test_set in distribution_data:
            str_id = BaseTestCases.to_str(distribution_data[test_set])
            self._run(str_id)
            cwd = os.getcwd()
            res = os.path.join(cwd, "res")
            if os.path.isdir(res):
                test_result.update(self._combine_result())
                to_res = os.path.join(cwd, "res_{}".format(test_set))
                if os.path.isdir(to_res):
                    shutil.rmtree(to_res)
                shutil.move(res, to_res)

        with open(output_test_result, 'wb+') as f_test_result:
            json.dump(test_result, f_test_result, indent=2)

        perf_data = {}
        for test_result_key in test_result:
            perf_data[test_result_key] = test_result[test_result_key].get('time')
        end = datetime.now()
        test_time = end - start
        print "Performance testing time : {}".format(test_time)
        return perf_data
