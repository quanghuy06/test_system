# Author: Trong Nguyen Van
# Created: D08/M08/2019
# This module run the testing job on Board

import os


class BoardTester(object):
    """
    A tester that run test on board
    """
    PYTHON_EXECUTABLE_PATH = "/home/SYSROM_SRC/build/release/bin/python3.5"

    def __init__(self, ssh_utility, testing_dir, mekong, build_package, testcases, result_name_prefix):
        self.ssh_utility = ssh_utility
        self.testing_dir = testing_dir
        self.mekong = mekong
        self.build_package = build_package
        self.testcases = testcases
        self.testcases_path = os.path.join(self.testing_dir, testcases)
        self.build_path = os.path.join(self.testing_dir, build_package)
        self.mekong_path = os.path.join(self.testing_dir, mekong)
        self.environments = {}
        self.result_name = result_name_prefix

    def prepare_environment(self):
        """
        Prepare the test environment
        """
        phocr_data_path = os.path.join(self.build_path, "share")
        phocr_lib_path = os.path.join(self.build_path, "lib")
        self.environments = {
            "PHOCRDATA_PREFIX": phocr_data_path,
            "LD_LIBRARY_PATH": phocr_lib_path,
            "PHOCR_PYTHON_EXECUTABLE_PATH": self.PYTHON_EXECUTABLE_PATH
        }

    def create_export_command(self):
        """
        Create export command from the environments
        """
        command = ""
        for variable, value in self.environments.iteritems():
            command += "export " + variable + "=" + value + ";"
        return command

    def run_test(self):
        """
        Run the test
        """
        server_address = self.ssh_utility.server_addr
        print("***** Running test on machine {} *****".format(server_address))
        self.prepare_environment()
        export_environment_cmd = self.create_export_command()
        run_all_path = os.path.join(self.mekong_path, "utilities/tests/run_all.py")
        bin_folder_path = os.path.join(self.build_path, "bin")
        self.result_name += "_" + self.ssh_utility.server_addr + ".json"
        run_all_cmd = "python " + run_all_path + " -p linux -b " + bin_folder_path + \
                      " -t " + self.testcases_path + " -o " + self.result_name
        cd_command = "cd " + self.testing_dir

        # Create final command to run performance test
        final_command = cd_command + ";" + export_environment_cmd + run_all_cmd
        stdin, stdout, stderr = self.ssh_utility.ssh_client.exec_command(final_command)
        print(stdout.read())
        print("++++++ Test done on machine: {} +++++".format(server_address))

    def get_test_result(self):
        """
        Return the absolute path to test result json file
        """
        return os.path.join(self.testing_dir, self.result_name)

    def clear_useless_data(self):
        """
        Clear useless data after the testing is done. This method save the memory on disk
        """
        remove_testcase_cmd = "rm -r " + self.testcases_path
        result_path = os.path.join(self.testing_dir, self.result_name)
        remove_result_cmd = "rm " + result_path
        remove_build_package_cmd = "rm -r " + self.build_path
        self.ssh_utility.ssh_client.exec_command(remove_testcase_cmd)
        self.ssh_utility.ssh_client.exec_command(remove_result_cmd)
        self.ssh_utility.ssh_client.exec_command(remove_build_package_cmd)
