# Author: Trong Nguyen Van
# Created: 09/08/2019
# This module is used to create list of test case for each machine based on the running time of
# test case. Target I need to achive is the running time of each machine with the distributed test
# case is similar.

import json
import os
import sys


class TestDistribution(object):
    """
    Distribute test case based on running time and numbers of machine
    """
    WEIGHTS = "weights"
    LINUX = "linux"
    SPEC_FILE = "spec.json"

    def __init__(self, number_machine, testcase_path):
        self.number_machine = number_machine
        self.testcase_path = testcase_path

    def get_running_time(self, testcase_id):
        """
        Get the running time by read the spec.json file
        """
        spec_file_path = os.path.join(self.testcase_path, testcase_id, self.SPEC_FILE)
        with open(spec_file_path) as f:
            data = json.load(f)
            return float(data[self.WEIGHTS][self.LINUX])

    def get_total_running_time(self):
        """
        Get the total running time by reading the weight field in spec.json file
        """
        total_time = 0.0
        for folder_name in os.listdir(self.testcase_path):
            total_time += self.get_running_time(folder_name)
        return total_time

    def distribute_testcase(self):
        """
        Distribute the test case based on time
        """
        output = []

        # If the number of test case is even smaller than the number of machine, just distribute test case for one
        # machine. Because, it will be the fastest solution
        testcase_list = os.listdir(self.testcase_path)
        if self.number_machine == 1 or len(testcase_list) <= self.number_machine:
            output.append(testcase_list)
            return output
        running_time_per_machine = self.get_total_running_time() / self.number_machine
        tracked_time = 0.0
        testcase_for_machine = []
        for testcase in testcase_list:
            # For the remaining testcase, distribute it for the last machine
            if len(output) == self.number_machine - 1:
                testcase_for_machine.append(testcase)
                continue
            running_time = self.get_running_time(testcase)
            tracked_time += running_time
            if tracked_time >= running_time_per_machine:
                # Add test case for other machine
                if testcase_for_machine:
                    output.append(testcase_for_machine)
                    testcase_for_machine = []
                    tracked_time = 0.0
            testcase_for_machine.append(testcase)
        # Add test case for the last machine
        output.append(testcase_for_machine)
        return output


def unit_test_distribution():
    """
    Unit test distribution
    """
    worker = TestDistribution(3, "performance_testcases")
    testcase_number = len(os.listdir("performance_testcases"))
    output = worker.distribute_testcase()
    idx = 0
    for value in output:
        print("Test case for machine {}: {}".format(idx, value))
        idx += 1

    distributed_total = 0
    for result in output:
        for element in result:
            distributed_total += 1
    if distributed_total == testcase_number:
        print("Distributed successfully!")
        sys.exit(0)
    else:
        print("Distributed failed!")
        sys.exit(1)

# unit_test_distribution()
