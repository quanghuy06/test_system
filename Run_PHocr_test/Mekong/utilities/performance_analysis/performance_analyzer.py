# Author: Trong Nguyen Van
# Created: 07/08/2019
# This module mainly do the following jobs:
#   + Download test case, build_package, checkout PHOcr
#   + Copy test case, build_package, trainedata, python3.5, Mekong to Board
#   + Run test on board
#   + Download the test result to local

import os
import sys
import shutil
import traceback
from concurrent.futures import ThreadPoolExecutor
import json
import time
from utility import SSHUtility, FileUtility
from board_tester import BoardTester
from test_distribution import TestDistribution


class PerformanceAnalyser(object):
    """
    Analyze the performance of PHOcr
    """
    TEST_CASE_PATH = "performance_testcases"
    SUCCESS_STATUS = 0
    PHOCR_LOCAL_REPOSITORY = "/tmp/PerformanceTesting"
    PHOCR_DATA = "PHOcr/ocrengine/tessdata/tessdata/phocrdata"
    PHOCR_CLONE_COMMAND = "git clone ssh://trongnv@10.116.41.96:29418/PHOcr.git"
    REMOTE_TESTING_DIR = "/storage/BoardPerformanceTesting"
    MEKONG = "Mekong"
    BOARD_USERNAME = "root"
    BOARD_PASSWORD = "toshibatec1048"
    RESULT = "res"
    TO_NULL = " >/dev/null 2>&1"
    COMMAS_TOKEN = ","
    UNDERLINE_TOKEN = "_"
    SHARE = "share"

    def __init__(self, board_ip, mekong_path, build_package_link, list_tests, gerrit_checkout):
        self.board_ip = board_ip.split(self.COMMAS_TOKEN)    # Board IP address
        self.mekong_path = mekong_path                # Path to Mekong project
        self.build_package_link = build_package_link  # Build package link on Jenkins
        self.list_tests = list_tests                  # List of test case ID
        self.gerrit_checkout_cmd = gerrit_checkout    # Checkout command to the change on Gerrit
        self.current_working = os.getcwd()            # Current working directory
        self.ssh_utilities = dict()                   # Dict of SSHUtility object
        self.build_name = self.detect_build_name()     # Name of build package after decompessing
        # File name of test result, will be add with self.build_name later
        self.test_result_prefix = "test_result_" + self.build_name

    def initialize_ssh_utilities(self, number_ssh_connection):
        """
        Initialize ssh utility based on the board ip
        """
        if len(self.board_ip) < number_ssh_connection:
            raise ValueError("Number of given remote machine is not enough!")
        ssh_connection_count = 0
        for ip in self.board_ip:
            self.ssh_utilities.update({ip: SSHUtility(ip, self.BOARD_USERNAME, self.BOARD_PASSWORD)})
            ssh_connection_count += 1
            if ssh_connection_count == number_ssh_connection:
                break

    def detect_build_name(self):
        """
        Detect the build name from the build package link
        :return:
        """
        package_name = os.path.basename(self.build_package_link)
        return FileUtility.detect_file_stem(package_name)

    def distribute_testcase(self):
        """
        Distribute the test case for each machine based on running time
        """
        worker = TestDistribution(len(self.board_ip), self.TEST_CASE_PATH)
        return worker.distribute_testcase()

    def copy_testcase_to_board(self, testcase_list, ssh_utility):
        """
        Copy test case inside testcase_list to the remote board
        :param testcase_list:
        :param ssh_utility:
        :return:
        """
        testcase_remote = os.path.join(self.REMOTE_TESTING_DIR, self.TEST_CASE_PATH)
        sftp = ssh_utility.ssh_client.open_sftp()
        try:
            sftp.stat(testcase_remote)
        except Exception:
            sftp.mkdir(testcase_remote)
        sftp.close()

        # Clear test case folder to ensure we're working with
        clear_command = "rm -r " + testcase_remote + "/*"
        ssh_utility.ssh_client.exec_command(clear_command)

        start_time = time.time()
        for testcase in testcase_list:
            path = os.path.join(self.TEST_CASE_PATH, testcase)
            # Push test data to board
            ssh_utility.push_to_server_high_performance(path, testcase_remote)
        end_time = time.time()
        print("***** push testcase to machine {} done in {}".format(ssh_utility.server_addr, end_time - start_time))

    def copy_needed_data_to_board(self, ssh_utility):
        """
        Copy need data from local machine to board for testing through SSH protocol
        """
        server_address = ssh_utility.server_addr
        mekong_remote = os.path.join(self.REMOTE_TESTING_DIR, self.MEKONG)
        # Check the existance of on board testing directory
        sftp = ssh_utility.ssh_client.open_sftp()
        try:
            sftp.stat(self.REMOTE_TESTING_DIR)
        except Exception:
            sftp.mkdir(self.REMOTE_TESTING_DIR)
        try:
            sftp.stat(mekong_remote)
        except Exception:
            sftp.mkdir(mekong_remote)

        # Decompress build package and push to board
        start_time = time.time()
        ssh_utility.push_to_server_high_performance(self.build_name, self.REMOTE_TESTING_DIR)
        end_time = time.time()
        print("***** push build package to machine {} done in {} *****".format(server_address, end_time - start_time))

        # Push trained data to board
        start_time = time.time()
        trained_data_path = os.path.join(self.PHOCR_LOCAL_REPOSITORY, self.PHOCR_DATA)
        trained_data_server_path = os.path.join(self.REMOTE_TESTING_DIR, self.build_name, self.SHARE)
        ssh_utility.push_to_server_high_performance(trained_data_path, trained_data_server_path)
        end_time = time.time()
        print("***** push trained data to machine {} done in {} *****".format(server_address, end_time - start_time))

        # Push Mekong to board. Mekong is rarely change that affect to run_all.py feature. So that
        # I only copy it to board when it's not exist only
        start_time = time.time()
        if not sftp.listdir(mekong_remote):
            ssh_utility.push_to_server_high_performance(self.mekong_path, self.REMOTE_TESTING_DIR)
        end_time = time.time()
        print("***** push Mekong to machine {} done in {} *****".format(server_address, end_time - start_time))
        sftp.close()

    def validate_input(self):
        """
        Validate the input data
        """
        # Check Mekong project path
        if not os.path.isdir(self.mekong_path):
            raise ValueError("Absolute path to Mekong project is wrong!")

    def get_test_case(self):
        """
        Get the test case using Mekong script with input test case list.
        Test data will be store inside a folder at current/TEST_CASE_PATH
        """
        if os.path.exists(self.TEST_CASE_PATH):
            shutil.rmtree(self.TEST_CASE_PATH)
        # Get test case
        gettc_script = os.path.join(self.mekong_path, "utilities/tests/get_test_cases.py")
        gettc_command = "python " + gettc_script + " -id " + self.list_tests + " -o " + self.TEST_CASE_PATH + \
                        self.TO_NULL
        status = os.system(gettc_command)
        if status != self.SUCCESS_STATUS:
            raise ValueError("Get test case failed. Please check the test case ID!")
        print("***** download test case done *****")

    def get_phocr_build_package(self):
        """
        Get the build package from jenkins. Always check if build package is
        existed on local already then I will delete it and download new file
        """
        # Check compressed file exist and delete
        package_name = os.path.basename(self.build_package_link)
        if os.path.isfile(package_name):
            os.remove(package_name)

        # Check decompressed folder exist and delete
        if os.path.exists(self.build_name):
            shutil.rmtree(self.build_name)
        status = os.system("cp {build} .".format(build=self.build_package_link))
        if status != self.SUCCESS_STATUS:
            raise ValueError("Download build package from Jenkins is failed. "
                             "Please check internet username or password!")
        decompress_cmd = "tar -xzf " + package_name + self.TO_NULL
        status = os.system(decompress_cmd)
        if status != self.SUCCESS_STATUS:
            raise ValueError("Failed to decompress build package!")
        print("***** download build package done *****")

    def checkout_phocr_repository(self):
        """
        Checkout PHOcr repository to the target revision. The purpose is get the
        exactly trained data, because trainedata is not installed in the build
        package
        """
        if not os.path.exists(self.PHOCR_LOCAL_REPOSITORY):
            # Clone PHOcr to specific folder
            os.makedirs(self.PHOCR_LOCAL_REPOSITORY)
            phocr_clone_cmd = "cd " + self.PHOCR_LOCAL_REPOSITORY + " && " + self.PHOCR_CLONE_COMMAND
            phocr_clone_cmd += self.TO_NULL
            status = os.system(phocr_clone_cmd)
            if status != self.SUCCESS_STATUS:
                raise ValueError("Failed to clone PHOcr to " + self.PHOCR_LOCAL_REPOSITORY)
        phocr_local = os.path.join(self.PHOCR_LOCAL_REPOSITORY, "PHOcr")
        phocr_checkout_cmd = "cd " + phocr_local + " && " + self.gerrit_checkout_cmd + self.TO_NULL
        status = os.system(phocr_checkout_cmd)
        if status != self.SUCCESS_STATUS:
            raise ValueError("Failed to checkout PHOcr to " + self.PHOCR_LOCAL_REPOSITORY)
        print("***** checkout PHOcr repository to {} done *****".format(self.PHOCR_LOCAL_REPOSITORY))

    def download_test_result(self, ssh_utility, result_path):
        """
        Download the test result to local machine
        """
        if not os.path.exists(self.RESULT):
            os.mkdir(self.RESULT)
        ssh_utility.download_to_local(result_path, self.RESULT)
        file_name = os.path.basename(result_path)
        return os.path.join(self.RESULT, file_name)

    def combine_result(self, board_results):
        """
        Combine the result after we have the data inside /res folder
        """
        target_name = self.test_result_prefix + ".json"
        target_path = os.path.join(self.RESULT, target_name)
        output = []
        for result in board_results:
            with open(result, "rb") as input_file:
                output.append(json.load(input_file))

        with open(target_path, "wb+") as target_file:
            json.dump(output, target_file, indent=2)

        # Validate the output
        with open(target_path) as f:
            json.load(f)
        return target_path

    def test_on_remote_machine(self, testcase_list, ssh_utility):
        """
        Test PHOcr with distributed test case on one machine. This method will be called by an multi threading pool
        :return:
        """
        # Copy data include: PHOcr build package, PHOcr trained data, Mekong to remote.
        # This method also create the directory for them if it doesn't present
        print("+++++ Testing on machine: {} +++++".format(ssh_utility.server_addr))
        self.copy_needed_data_to_board(ssh_utility)

        # Copy test case to remote
        self.copy_testcase_to_board(testcase_list, ssh_utility)

        # Run the performance test
        tester = BoardTester(ssh_utility, self.REMOTE_TESTING_DIR,
                             self.MEKONG, self.build_name,
                             self.TEST_CASE_PATH, self.test_result_prefix)
        tester.run_test()

        # Download the test result to local
        local_result = self.download_test_result(ssh_utility, tester.get_test_result())

        # Clear the useless data after testing done
        tester.clear_useless_data()
        return local_result

    def do_job_multithread(self):
        """
        Main API to run the performance analysis
        Do the job with multi thread to optimize the performance
        """
        try:
            # Validate input data
            self.validate_input()

            # Prepare all needed data by using multi threading pool
            download_executor = ThreadPoolExecutor(max_workers=4)
            download_executor.submit(self.get_test_case)
            download_executor.submit(self.get_phocr_build_package)
            download_executor.submit(self.checkout_phocr_repository)
            download_executor.shutdown()

            # Run performance test on multiple machine using multi threading pool
            distributed_testcase = self.distribute_testcase()
            number_ssh_connection = len(distributed_testcase)
            self.initialize_ssh_utilities(number_ssh_connection)
            test_executor = ThreadPoolExecutor(max_workers=number_ssh_connection)
            idx = 0
            futures = []
            for board_ip, ssh_utility in self.ssh_utilities.iteritems():
                testcase_list = distributed_testcase[idx]
                future_obj = test_executor.submit(self.test_on_remote_machine, testcase_list, ssh_utility)
                futures.append(future_obj)
                idx += 1
            test_executor.shutdown()

            # Combine result
            board_results = []
            for future_obj in futures:
                board_results.append(future_obj.result())
            result_file_path = self.combine_result(board_results)
            print("***** DONE, ENJOY RESULT AT {} *****".format(os.path.join(self.current_working, result_file_path)))
            sys.exit(0)
        except Exception as e:
            print("Performance automation test failed with reason: {}".format(e.message))
            traceback.print_exc()
            sys.exit(1)
