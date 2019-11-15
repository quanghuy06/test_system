# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Tran Quang Huy
# Email:            huy.tranquang@toshiba-tsdv.com
# Date create:      4/11/2019
# Last update by:
# Date:
# Description:      This script defines class which help us download test cases from database and
#                   update test cases folder on node master
import os
import subprocess
import time
import re
import threading
import pymongo
import sys_path
sys_path.insert_sys_path()
from configs.common import Machines
from configs.linux import LinuxCmd
from configs.command import CommandConfigClass
from configs.database import DbConfig, DbQueryKeys, SpecKeys
from baseapi.log_manager import Logger
from baseapi.common import get_time_str


class TestCasesUpdater(object):
    def __init__(self, test_folder, number_test_set=8, log_file="UpdateTestCasesMaster"):
        """
        Constructor for class which download test cases from database and update test cases
        folder on master machine

        Parameters
        ----------
        test_folder: str
            Path to target test cases folder to be updated
        number_test_set: int
            Number of test set to updated (?)
        log_file: str
            Path to output logging file

        """
        self.test_folder = test_folder
        self.number_test_set = number_test_set

        # Create logging object
        self.logger = Logger(name=log_file)

    @property
    def test_folder(self):
        """
        Getter for path to test cases folder

        Returns
        -------
        str
            Path to test cases folder to update

        """
        return self._test_folder

    @test_folder.setter
    def test_folder(self, test_folder):
        """
        Setter for path to test cases folder which need to be updated

        Parameters
        ----------
        test_folder: str
            Path to target update test cases folder

        Returns
        -------
        None

        """
        self._test_folder = test_folder

    def do_works(self):
        """
        API to executing update test cases folder on master machine.
        Query to get list of test cases which are changed with test cases in local folder then
        update for them

        Returns
        -------
        None

        """
        # Get new test cases from database to test cases folder on master machine
        self._get_new_test_cases_from_database()

        # Update for changed test cases
        self._update_changed_test_cases()

    def _get_new_test_cases_from_database(self):
        """
        Get new test cases from database to test cases folder on master node

        Returns
        -------
        None

        """
        # Calculate time of processing
        start_time = time.time()

        self.logger.log_and_print(">> Get new test cases from database to test cases folder")

        # Command
        query_options = '-o ' + self._test_folder + ' -id {tc_name}'

        # Get new test cases from database to test cases folder
        test_case_counter = 0
        for name in self.get_list_new_test_cases(self):
            self.logger.add_line(
                subprocess.check_output(CommandConfigClass.get_test_cases(
                    query_options.format(tc_name=name)), shell=True)
            )
            self.logger.add_end_line()
            test_case_counter += 1

        self.logger.log_and_print("Get {num} new test cases from database!"
                                  "".format(num=test_case_counter))
        self.logger.log_and_print(">> Finish in: {execution_time}".format(
            execution_time=get_time_str(time.time()-start_time)))

    def _update_changed_test_cases(self):
        """
        Run update data for list changed test cases

        Returns
        -------
        None

        """
        # Calculate execution time of processing
        start_time = time.time()

        self.logger.log_and_print(">> Update for changed test cases")

        # Initial list of test cases which need to be updated
        list_test_cases_updated = dict()

        # Get 2 changed_log of latest and older delta version
        latest_data = self._get_changed_log_test_case(True)
        old_data = self._get_changed_log_test_case(False)

        for name in latest_data.keys():
            try:
                if latest_data[name][SpecKeys.ChangedLog.TIME] != \
                        old_data[name][SpecKeys.ChangedLog.TIME]:
                    list_test_cases_updated.update({name: latest_data[name]})
            except:
                self.logger.add_line(
                    "In old version doesn't have {0}".format(name))

        list_test_set = self.divide_into_chunks(list_test_cases_updated,
                                                self.number_test_set)

        thread_counter = 0
        lock = threading.Lock()
        # Initial list of threads to run updating
        list_thread = list()
        for test_set in list_test_set:
            thread_counter += 1
            thread = threading.Thread(target=self._update_bucket_test_cases,
                                      args=(test_set, thread_counter, lock))
            list_thread.append(thread)

        # Run updating on threads for buckets
        for thread in list_thread:
            thread.start()

        # Wait for all jobs finish
        for thread in list_thread:
            thread.join()

        # Logging for status of work
        self.logger.log_and_print("Updated for {num} test cases!"
                                  "".format(num=len(list_test_cases_updated)))
        self.logger.log_and_print(">> Finish updating for changed test cases in: {execution_time}"
                                  "".format(execution_time=time.time()-start_time))

    def _get_changed_log_test_case(self, latest_change=True):
        """
        (?)

        Parameters
        ----------
        latest_change: (?)
            (?)

        Returns
        -------
        dict()
            (?)

        """
        client = pymongo.MongoClient(host=DbConfig.HOST, port=DbConfig.PORT)
        user, password = DbConfig.get_account_base_on_permission(is_readwrite=False)
        my_db = client[DbConfig.DB_NAME]
        my_collection = my_db[DbConfig.collections.TEST_CASE]
        my_db.authenticate(name=user, password=password)

        my_query = {
            DbQueryKeys.AND: [
                {"{0}.{1}".format(SpecKeys.TAGS,
                                  SpecKeys.Tags.IS_NON_INTEGRATION): False}
            ]
        }

        projection = {
            SpecKeys.ID: 1,
            "{0}.{1}".format(SpecKeys.CHANGED_LOG, SpecKeys.ChangedLog.TIME): 1,
            "{0}.{1}".format(SpecKeys.CHANGED_LOG, SpecKeys.ChangedLog.CHANGED_LOG): 1
        }

        if latest_change:
            index = -1  # latest change
        else:
            index = -2  # older change

        my_doc = my_collection.find(my_query, projection=projection)

        result = dict()
        for content in my_doc:
            try:
                result.update({content[SpecKeys.ID]: content[SpecKeys.CHANGED_LOG][index]})
            except:
                self.logger.log_and_print(
                    "{0} doesn't have changed log.".format(content[SpecKeys.ID]))

        return result

    @staticmethod
    def get_list_new_test_cases(self):
        """
        This function perform get new test case from MongoDB.
        1. List all test case name from DB
        2. List all test case name in local (in MekongTC directory)
        3. Diff 2 list. Then return a list of test cases name

        Returns
        -------
        list
            List of name of new test cases

        """
        # Query all test case which has tag NonIntegration is false
        query_options = "-t NonIntegration:false --list-test-name"

        # Get all test cases of Integration Test
        list_it_test_cases = subprocess.check_output(
            CommandConfigClass.get_test_cases(query_options), shell=True)

        # Remove [****/****] format. For example: [1234/7820] 01_0033
        list_it_test_cases = re.sub("\[\d+\/\d+\] ", '', list_it_test_cases).split()

        # Get path to test cases folder on master machine
        test_cases_folder = Machines.MASTER_MACHINE[Machines.TC_FOLDER]

        # Get all existing test
        list_existing_test_cases = os.listdir(self._test_folder)

        # Check if some test cases which are not in existing list then they are new ones
        list_new_test_cases = \
            (name for name in list_it_test_cases if name not in list_existing_test_cases)

        return list_new_test_cases

    @staticmethod
    def divide_into_chunks(list_changed, number_parts):
        """
        Separate list of changed test cases into a number of sub-set and run concurrently using
        multiple threads

        Parameters
        ----------
        list_changed: dict()
            List of changed test cases
        number_parts: int
            Number of sub-set to be divided

        Returns
        -------
        list
            List of sub-set of changed test cases. From here, each sub-set could be run on a
            different thread to speed up processes.

        """
        tc_in_each_part = len(list_changed) / number_parts
        counter = 0
        result = list()
        temp = dict()
        for k, v in list_changed.items():
            counter += 1
            temp.update({k: v})
            if counter == tc_in_each_part:
                result.append(temp)
                temp = {}
                counter = 0
        result.append(temp)
        return result

    def _update_bucket_test_cases(self, bucket, thread_number, lock):
        """
        Run update for a number of changed test cases (a bucket). By using multi-threading,
        a bucket can run on a thread by call to this method.

        Parameters
        ----------
        bucket: dict
            list of test cases need to be updated data
        thread_number: int
            Index of current working thread
        lock: Lock
            Threading lock to avoid conflict when write to log file

        Returns
        -------
        None

        """
        # Initial counter
        test_case_counter = 0
        ref_data_counter = 0
        gt_counter = 0
        test_data_counter = 0

        # Collect logging message to write to log_message file later
        log_message = ">>> Update test case in thread {0}\n".format(thread_number)

        for tc_name, tc_info in bucket.items():
            what_changed = tc_info[SpecKeys.CHANGED_LOG]

            # Always update specification of test case
            test_spec_query = "--get-test-spec -o {0} -id {1} > {2}".format(
                self._test_folder, tc_name, LinuxCmd.TO_DEV_NULL)

            subprocess.call(CommandConfigClass.get_test_cases(test_spec_query), shell=True)

            log_message += "{0} --> is updated error_flags\n".format(tc_name)
            test_case_counter += 1

            # Update new reference data if it has changed
            if "ref_data" in what_changed:
                ref_data_query = "--get-reference -o {0} -id {1} > {2}".format(
                    os.path.join(self._test_folder,
                                 tc_name, Machines.REF_DATA_PATH), tc_name, LinuxCmd.TO_DEV_NULL)
                subprocess.call(CommandConfigClass.get_test_cases(
                    ref_data_query), shell=True)
                log_message += "{0} --> is updated ref_data\n".format(tc_name)
                ref_data_counter += 1

            # Update new ground truth data if it has changed
            if "ground_truth_data" in what_changed:
                gt_data_query = "--get-ground-truth -o {0} -id {1} > {2}".format(
                    os.path.join(self._test_folder,
                                 tc_name, Machines.GT_DATA_PATH), tc_name, LinuxCmd.TO_DEV_NULL)
                subprocess.call(CommandConfigClass.get_test_cases(
                    gt_data_query), shell=True)
                log_message += "{0} --> is updated ground_truth_data\n".format(tc_name)
                gt_counter += 1

            # Update new test data if it has changed
            if "test_data" in what_changed:
                test_data_query = "--get-image -o {0} -id {1} > {2}".format(
                    os.path.join(self._test_folder,
                                 tc_name, Machines.TEST_DATA), tc_name, LinuxCmd.TO_DEV_NULL)
                subprocess.call(CommandConfigClass.get_test_cases(
                    test_data_query), shell=True)
                log_message += "{0} is updated test_data\n".format(tc_name)
                test_data_counter += 1

        # Lock log_message file to write logging message of processes
        lock.acquire()
        self.logger.add_line(log_message)
        self.logger.log_and_print("Thread {thread_number} status:".format(
            thread_number=thread_number))
        self.logger.log_and_print("+ Specification updated: {counter}".format(
            counter=test_case_counter))
        self.logger.log_and_print("+ Reference data updated: {counter}".format(
            counter=ref_data_counter))
        self.logger.log_and_print("+ Ground truth data update: {counter}".format(
            counter=gt_counter))
        self.logger.log_and_print("+ Test data updated: {counter}".format(
            counter=test_data_counter))
        lock.release()
