# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      07/10/2016
# Last update:      13/07/2018
# Description:      Define class for manager test cases on MongoDB database
import os
import sys
import datetime
import sys_path

sys_path.insert_sys_path()
from pymongo import MongoClient
from configs.database import DbConfig, TestcaseConfig, SpecKeys, DbQueryKeys
from database.lib_base.file_db_manager import FileManager
from database.lib_base.collection_util import CollectionUtil
from baseapi.file_access import read_json, write_json, move_globs
from configs import database
from baseapi.file_access import remove_paths
from configs.common import Platform, DateTimeFormat
from baseapi.network_base import get_lan_ips
import traceback
from baseapi.common import get_current_local_time_in_format
from baseapi.file_access import make_dir

from multiprocessing import Process


def _get_all_test_data_folders(test_case_id, output_dir):
    manager = TestCaseManager()
    manager.get_a_test_case(test_case_id, output_dir, True,
                            remove_exists=False,
                            get_test_data=True)


def make_query_option(list_fields):
    """
    Returns
    -------
    object
    """
    if not list_fields or list_fields is None:
        return None
    else:
        query_option = {}
        for field in list_fields:
            query_option[field] = 1
        return query_option

# TODO(Huan) Remove all unused methods inside TestCaseManager class
# TODO(Huan) Use prefix _(underscore) for all private functions

class TestCaseManager(object):
    # --------------------------------- INIT ------------------------------------- #
    def __init__(self, user=None, password=None):
        if user is None and password is None:
            user, password = DbConfig.get_account_base_on_permission(is_readwrite=False)

        self.user = user

        # Connect to data base server
        try:
            client = MongoClient(host=DbConfig.HOST, port=DbConfig.PORT)
            self.db = client[DbConfig.DB_NAME]
            self.db.authenticate(name=user, password=password)
        except Exception as e:
            print(e.args[0])
            sys.exit(2)

        # Create file storage object to get/put a file to data base
        self.fileManager = FileManager(self.db)

        # Create collection utilities for test_case collection to
        # support query test cases.
        self.test_spec_col = self.db[DbConfig.collections.TEST_CASE]
        self.collectionUtil = CollectionUtil(self.test_spec_col)
    # ---------------------------------------------------------------------------- #

    # ----------------------- Query/Filter test case ----------------------------- #
    def is_test_case_on_db(self, test_case):
        # To check test case exists on db or not
        # we query the test case on db.
        # in here, we only get _id field only.
        id_only = {SpecKeys.ID: 1}
        if self.collectionUtil.query_by_id(test_case.strip(), find_option=id_only):
            return True
        else:
            return False

    def get_weight(self, test_id, platform):
        weight_only = {SpecKeys.WEIGHTS: 1}
        spec_info = self.collectionUtil.query_by_id(id=test_id, find_option=weight_only)[0]
        if (SpecKeys.WEIGHTS not in spec_info.keys()) or \
                (platform not in spec_info[SpecKeys.WEIGHTS].keys()):
            return 1
        else:
            return spec_info[SpecKeys.WEIGHTS][platform]

    def is_error(self, test_id, platform):
        spec_list = self.collectionUtil.query_by_id(id=test_id, find_option={
            SpecKeys.ERROR_FLAGS: 1
        })
        error_flags = spec_list[0][SpecKeys.ERROR_FLAGS]
        if platform not in error_flags:
            return None
        else:
            return error_flags[platform]

    def get_functions(self, test_id):
        spec_list = self.collectionUtil.query_by_id(id=test_id, find_option={
            SpecKeys.FUNCTIONALITIES: 1
        })
        return spec_list[0][SpecKeys.FUNCTIONALITIES]

    def get_component(self, test_id):
        spec_list = self.collectionUtil.query_by_id(id=test_id, find_option={
            SpecKeys.COMPONENT: 1
        })
        return spec_list[0][SpecKeys.COMPONENT]

    def get_tag(self, test_id, tag_name):
        spec_list = self.collectionUtil.query_by_id(id=test_id, find_option={
            SpecKeys.TAGS: 1
        })
        spec_info = spec_list[0]
        return spec_info[SpecKeys.TAGS][tag_name]

    def get_history_data(self, test_id, platform):
        spec_list = self.collectionUtil.query_by_id(id=test_id, find_option={
            SpecKeys.HISTORY_DATA: 1
        })
        spec_info = spec_list[0]
        history_data = spec_info[SpecKeys.HISTORY_DATA]
        if platform in history_data.keys():
            return history_data[platform]
        else:
            return None

    # ----------------------------- GET TEST CASES --------------------------------- #
    # Get specification of test case and write to spec.json file
    def get_test_spec(self, test_case_name, test_case_output_dir, list_spec_fields=None):
        """
        Query to data server to get specification of test case then write that dat information to
        spec.json file in test
        case folder structure as follow:
        <test folder>
        |__<test_case_1>
        |  |__spec.json
        |  |__...
        |__<test_case_2>
        |  |...
        |__...

        Parameters
        ----------
        test_case_name: str
            Name of test case to query information
        test_case_output_dir: str
            Path to test folder which can include many test cases
        list_spec_fields: list
            List of fields in specification that will be queried

        Returns
        -------
        None

        """
        test_id = test_case_name.strip()
        find_option = make_query_option(list_spec_fields)
        test_spec = self.collectionUtil.query_by_id(id=test_id,
                                                    find_option=find_option)
        # Checking if test case exist or not
        if not test_spec:
            print("Test case {0} is not exist!".format(test_case_name))
        else:
            test_case_folder = os.path.join(test_case_output_dir, test_id)

            # Check if parten folder of spec file does not exist then create it first
            if not os.path.exists(test_case_folder):
                make_dir(test_case_folder)

            # Write specification of test case to json file
            spec_file_path = os.path.join(test_case_output_dir,
                                          test_id,
                                          TestcaseConfig.SPEC_FILE)
            write_json(test_spec[0], spec_file_path)

    # Get all files that belong to a test case
    def get_all_files_with_the_same_test_case(self, bucket_name, test_case_name, base_output_dir):
        file_specs = self.fileManager.query_all_file_of_a_test_case(bucket_name, test_case_name)
        for file_spec in file_specs:
            file_name_db = file_spec[SpecKeys.FILE_NAME]
            output_file_name = os.path.join(base_output_dir, file_name_db)
            dirname = os.path.dirname(output_file_name)
            if not os.path.isdir(dirname):
                os.makedirs(dirname)
            self.fileManager.get_a_file(bucket_name, file_name_db, output_file_name)

    # Get test data bucket
    def get_test_data(self, test_case_name, base_output_dir):
        bucket_name = DbConfig.collections.TEST_DATA
        self.get_all_files_with_the_same_test_case(bucket_name, test_case_name, base_output_dir)

    # Get reference data bucket
    def get_ref_data(self, test_case_name, base_output_dir):
        bucket_name = DbConfig.collections.REFS_DATA
        self.get_all_files_with_the_same_test_case(bucket_name, test_case_name, base_output_dir)

    # Get scripts bucket
    def get_scripts(self, test_case_name, base_output_dir):
        bucket_name = DbConfig.collections.SCRIPTS
        self.get_all_files_with_the_same_test_case(bucket_name, test_case_name, base_output_dir)

    # Get ground truth bucket
    def get_ground_truth(self, test_case_name, base_output_dir):
        bucket_name = DbConfig.collections.GROUND_TRUTH_DATA
        self.get_all_files_with_the_same_test_case(bucket_name, test_case_name, base_output_dir)

    # Get a test case with specification and files
    def get_a_test_case(self, test_case_name, output_dir,
                        force=False,
                        list_spec_fields=None,
                        remove_exists=True,
                        get_test_spec=False,
                        get_scripts=False,
                        get_test_data=False,
                        get_ground_truth=False,
                        get_ref_data=False):
        """
        Get a test case to output directory
        :param test_case_name:
        :param output_dir:
        :param force:
            if test case exists and not force, write error and return
            if test case exists and force, using remove_exists to decide should
            or should not be delete
        :param list_spec_fields: list fields in specification, which are specified to get
        :param remove_exists: if true and force, remove test case directory
        :param get_test_spec:
        :param get_scripts:
        :param get_test_data:
        :param get_ground_truth:
        :param get_ref_data:
        :return:
        """
        test_case_dir = os.path.join(output_dir, test_case_name)
        if os.path.isdir(test_case_dir):
            if force:
                if remove_exists:
                    remove_paths(test_case_dir)
            else:
                print("\tEXISTED : Test case already existed on your local machine!"
                      " If you still want to get, please use --force option!")
                return 1

        if not os.path.isdir(test_case_dir):
            os.makedirs(test_case_dir)
        if get_test_spec:
            self.get_test_spec(test_case_name, output_dir, list_spec_fields=list_spec_fields)
        if get_scripts:
            self.get_scripts(test_case_name, output_dir)
        if get_test_data:
            self.get_test_data(test_case_name, output_dir)
        if get_ground_truth:
            self.get_ground_truth(test_case_name, output_dir)
        if get_ref_data:
            self.get_ref_data(test_case_name, output_dir)
        return 0

    # Get multiple test cases
    def get_test_cases(self, filters, output_dir=TestcaseConfig.FOLDER_DEFAULT, force=False,
                       list_spec_fields=None):
        # First query test case from db base on filters
        test_specs = self.collectionUtil.query_by_fields(filters)
        total = len(test_specs)
        count = 1
        for test_spec in test_specs:
            # Make sure that test_case name does not contain any unexpected spaces.
            test_case_id = test_spec[SpecKeys.ID]
            print("[{0}/{1}] Get test case {2}".format(count, total, test_case_id))
            self.get_a_test_case(test_case_id, output_dir, force, list_spec_fields)
            count += 1

    # Get only ground truth by filter
    def get_grounds(self, filters, output_dir):
        # First query test case from db base on filters
        test_specs = self.collectionUtil.query_by_fields(filters)
        total = len(test_specs)
        count = 1
        for test_spec in test_specs:
            # Make sure that test_case name does not contain any unexpected spaces.
            test_case_id = test_spec[SpecKeys.ID]
            print("[{0}/{1}] Test case {2}".format(count, total, test_case_id))
            self.get_a_test_case(test_case_id, output_dir, True, get_ground_truth=True)
            ground_glob = os.path.join(output_dir, test_case_id,
                                       TestcaseConfig.GROUND_TRUTH_DATA_DIR, "linux", "*")
            move_globs(ground_glob, output_dir)
            test_path = os.path.join(output_dir, test_case_id)
            remove_paths(test_path)
            count += 1

    # Get only image by filter
    def get_images(self, filters, output_dir):
        # First query test case from db base on filters
        test_specs = self.collectionUtil.query_by_fields(filters)
        total = len(test_specs)
        count = 1
        for test_spec in test_specs:
            # Make sure that test_case name does not contain any unexpected spaces.
            test_case_id = test_spec[SpecKeys.ID]
            print("[{0}/{1}] Test case {2}".format(count, total, test_case_id))
            self.get_a_test_case(test_case_id, output_dir, True, get_test_data=True)
            image_glob = os.path.join(output_dir, test_case_id, TestcaseConfig.TEST_DATA_DIR,
                                      "*")
            move_globs(image_glob, output_dir)
            test_path = os.path.join(output_dir, test_case_id)
            remove_paths(test_path)
            count += 1

    def get_all_test_data_folders_parallel(self, filters, output_dir):
        """
        Get all test data folder for test cases which is chosen using `filters`
        The test data folder will be fill to test case folder inside of
        `output_dir`
        :param filters:
        :param output_dir:
        :return:
        """
        # First query test case from db base on filters
        test_specs = self.collectionUtil.query_by_fields(filters,
                                                         only_id=True)
        total = len(test_specs)
        count = 1

        # The default number of thread for get test data folders
        num_threads = 15
        while len(test_specs) > 0:
            processes = []
            for index in range(0, num_threads):
                if len(test_specs) == 0:
                    break
                test_spec = test_specs.pop()
                test_case_id = test_spec[SpecKeys.ID]
                print("[{0}/{1}] Get test case {2}".format(count, total,
                                                           test_case_id))
                try:
                    process = Process(
                        target=_get_all_test_data_folders,
                        args=(test_case_id,
                              output_dir))
                    processes.append(process)
                    process.start()
                    count += 1
                except SystemExit:
                    exit(1)
                except:
                    traceback.print_exc()
                    print("\tGET FAILED!")
            for index in range(0, len(processes)):
                processes[index].join()

    # Get only image by filter
    def get_refs(self, filters, output_dir):
        # First query test case from db base on filters
        test_specs = self.collectionUtil.query_by_fields(filters)
        total = len(test_specs)
        count = 1
        for test_spec in test_specs:
            # Make sure that test_case name does not contain any unexpected spaces.
            test_case_id = test_spec[SpecKeys.ID]
            print("[{0}/{1}] Test case {2}".format(count, total, test_case_id))
            self.get_a_test_case(test_case_id, output_dir, True, get_ref_data=True)
            ref_glob = os.path.join(output_dir, test_case_id, TestcaseConfig.REF_DATA_DIR, "linux",
                                    "*")
            move_globs(ref_glob, output_dir)
            test_path = os.path.join(output_dir, test_case_id)
            remove_paths(test_path)
            count += 1

    # Do not get test cases, only list up test name of filters
    def list_test_names(self, filters):
        # First query test case from db base on filters
        test_specs = self.collectionUtil.query_by_fields(filters, only_id=True)
        total = len(test_specs)
        count = 1
        for test_spec in test_specs:
            # Make sure that test_case name does not contain any unexpected spaces.
            test_case_id = test_spec[SpecKeys.ID]
            print("[{0}/{1}] {2}".format(count, total, test_case_id))
            count += 1

    # Get list test data name on database
    def get_list_test_data_name(self, test_name):
        file_specs = self.fileManager.query_all_file_of_a_test_case(TestcaseConfig.TEST_DATA_DIR,
                                                                    test_name)
        list_test_case_name = []
        for file_spec in file_specs:
            file_name_db = file_spec[SpecKeys.FILE_NAME]
            file_name = file_name_db.split("/")[-1]
            list_test_case_name.append(file_name)
        return list_test_case_name

    # Get list name test cases which's id contains string
    def get_id_contain_string(self, list_str, case_sensitive):
        # First query test case from db base on filters
        filters = {}
        test_specs = self.collectionUtil.query_by_fields(filters)
        test_case_list = []
        for test_spec in test_specs:
            # Make sure that test_case name does not contain any unexpected spaces.
            test_case_id = test_spec[SpecKeys.ID]
            for s in list_str:
                test_name = test_case_id
                if not case_sensitive:
                    s = s.lower()
                    test_name = test_case_id.lower()
                if s in test_name:
                    test_case_list.append(test_case_id)
        return test_case_list

    # Query directly from DB with filters
    # Input: filters_obj - like parameter of find() in pymongo
    # Input: limit_number - like parameter of limit() in pymongo
    def query_db(self, filters_obj, limit_number=0):
        return self.collectionUtil.query_mongo(filters_obj, limit_number)

    # Query specification's information by test id
    def query_spec_info_by_id(self, id, find_option=None):
        return self.collectionUtil.query_by_id(id.strip(), find_option)

    # Query test cases by filters string
    def query_by_filters(self, filters_str, only_id=False, find_option=None):
        return self.collectionUtil.query_by_fields(filters=filters_str, only_id=only_id,
                                                   find_option=find_option)
    # -------------------------------------------------------------------------------- #

    # ----------------------------------- OTHERS ------------------------------------- #
    # Check if a test case exist in a collection
    def is_test_case_exist_in_collection(self, bucket_name, test_case_name):
        files = self.fileManager.query_all_file_of_a_test_case(bucket_name,
                                                               os.path.basename(test_case_name))
        if files:
            return True
        else:
            return False

    # ------------------------------- PUSH TEST CASES -------------------------------- #
    # Walk through a folder and push files to database
    def push_all_files_in_a_folder(self, folder, bucket_name, test_id):
        for root, dirs, files in os.walk(folder):
            for f in files:
                filename = os.path.join(root, f)
                base_folder = filename.replace(folder, "")
                file_name_in_db = os.path.join(test_id, database.get_folder_bucket(bucket_name),
                                               base_folder.strip("/\\"))
                self.fileManager.put_a_file(bucket_name, filename, file_name_in_db, test_id)

    def _get_changed_log(self, test_id):
        """
        Get changed log of a test case

        Parameters
        ----------
        test_id: str
            Id of test case need to get changed log

        Returns
        -------
        None/dict
            Raise excpetion if test case does not exists
            None if test case does not have changed log
            changed_log dict if test cases does have.
        """
        spec = self.collectionUtil.find_one(test_id)
        if not spec:
            error_msg = "Test case {0} has wrong number of spec collection"
            raise Exception(error_msg.format(test_id))
        if SpecKeys.CHANGED_LOG in spec:
            return spec[SpecKeys.CHANGED_LOG]
        else:
            return None

    def add_new_changed_log(self, test_id, changed_log):
        """
        Add new changed log for a test case in database

        Parameters
        ----------
        test_id: str
            The id of test case need to add changed log
        changed_log: str
            The changed log text need to add

        Returns
        -------
        None
            If failure, raise Exception about error
        """
        if not changed_log:
            raise Exception("changed_log is required to update test case")

        new_change_log_record = self._make_changed_log_record(changed_log)
        current_change_log = self._get_changed_log(test_id)
        if not current_change_log:
            current_change_log = []

        # Append new change log
        current_change_log.append(new_change_log_record)
        change_log_document = {
            SpecKeys.CHANGED_LOG: current_change_log
        }
        self.update_spec_field(test_id, change_log_document)

    def _make_changed_log_record(self, changed_log):
        """
        Utility to create new changed log record base on changed log
        Parameters
        ----------
        changed_log: str
            Changed log need to write to test case's revision

        Examples
        --------
        changed_log = "Test System update for D314"
        _make_change_log_record(changed_log) will return
        {
            "user": "jenkins",
            "date": "22-11-2018 09:38",
            "changed_log": "Test System update for D314",
            "address": [{'ip': u'127.0.0.1', 'mac': u'00:00:00:00:00:00'},
                   {'ip': u'10.116.41.89', 'mac': u'b0:83:fe:aa:d9:1a'}]
        }

        Returns
        -------
        dict
            New changed log record
            Includes: user, date, changed log, ips

        """
        current_datetime = get_current_local_time_in_format(DateTimeFormat.DATE_IN_DATABASE)
        changed_log_record = dict(user=self.user,
                                  time=current_datetime,
                                  changed_log=changed_log,
                                  address=get_lan_ips())

        return changed_log_record

    # Push test case's specification
    def push_test_spec(self, spec_file_path):
        test_case_col = self.db[DbConfig.collections.TEST_CASE]
        data = read_json(spec_file_path)
        test_case_col.insert_one(data)

    # Push test data files
    def push_test_data(self, test_data_folder, test_id):
        self.push_all_files_in_a_folder(test_data_folder,
                                        DbConfig.collections.TEST_DATA, test_id)

    # Push reference data
    def push_ref_data(self, ref_data_folder, test_id):
        self.push_all_files_in_a_folder(ref_data_folder,
                                        DbConfig.collections.REFS_DATA, test_id)

    # Push ground truth data
    def push_ground_truth_data(self, ground_truth_data_folder, test_id):
        self.push_all_files_in_a_folder(ground_truth_data_folder,
                                        DbConfig.collections.GROUND_TRUTH_DATA, test_id)

    # Push ground truth data
    def push_ground_truth_file(self, file_path, test_id, plf=Platform.LINUX):
        bucket_name = DbConfig.collections.GROUND_TRUTH_DATA
        file_name = os.path.basename(file_path)
        file_name_in_db = os.path.join(test_id, TestcaseConfig.GROUND_TRUTH_DATA_DIR, plf,
                                       file_name)
        self.fileManager.delete_a_file(bucket_name, file_name_in_db)
        self.fileManager.put_a_file(bucket_name, file_path, file_name_in_db, test_id)

    # Push scripts
    def push_scripts(self, script_folder, test_id):
        self.push_all_files_in_a_folder(script_folder,
                                        DbConfig.collections.SCRIPTS, test_id)

    # Push a test case
    def push_a_test_case(self, test_case_dir):

        test_id = os.path.basename(test_case_dir)
        # Push test case specification
        spec_file = os.path.join(test_case_dir, TestcaseConfig.SPEC_FILE)
        if os.path.isfile(spec_file):
            self.push_test_spec(spec_file)

        # Push test data
        test_data_folder = os.path.join(test_case_dir, TestcaseConfig.TEST_DATA_DIR)
        if os.path.isdir(test_data_folder):
            self.push_test_data(test_data_folder, test_id)

        # Push reference data
        ref_data_folder = os.path.join(test_case_dir, TestcaseConfig.REF_DATA_DIR)
        if os.path.isdir(ref_data_folder):
            self.push_ref_data(ref_data_folder, test_id)

        # Push ground truth data
        ground_truth_data_folder = os.path.join(test_case_dir,
                                                TestcaseConfig.GROUND_TRUTH_DATA_DIR)
        if os.path.isdir(ground_truth_data_folder):
            self.push_ground_truth_data(ground_truth_data_folder, test_id)

        # Push scripts
        script_folder = os.path.join(test_case_dir, TestcaseConfig.SCRIPT_DIR)
        if os.path.isdir(script_folder):
            self.push_scripts(script_folder, test_id)

    # Push multiple test cases
    def push_test_cases(self, list_test_path, force=False):
        total = len(list_test_path)
        count = 1
        updated_test_cases = []
        for test_path in list_test_path:
            test_id = os.path.basename(test_path)
            label = "Push"
            if self.is_test_case_on_db(test_id):
                if not force:
                    print("[{0}/{1}] {2} {3}".format(count, total, label, test_id))
                    print("\tTest case {0} already existed. If you still want push,"
                          " please use option --force."
                          "".format(test_id))
                    continue
                else:
                    label = "Update"
                    self.delete_a_test_case(test_id)
            print("[{0}/{1}] {2} {3}".format(count, total, label, test_id))
            if test_id not in updated_test_cases:
                updated_test_cases.append(test_id)
            self.push_a_test_case(test_path)
            count += 1
        return updated_test_cases

    # TODO(Huan) remove this unused function
    def push_all_test_cases(self, test_folder, force=False):
        test_set = []
        for f_name in os.listdir(test_folder):
            path = os.path.join(test_folder, f_name)
            if os.path.isdir(path):
                test_set.append(f_name)
        if not test_set:
            print("No test case to push!")
            return
        total = len(test_set)
        count = 1

        for test_id in test_set:
            label = "Push"
            if self.is_test_case_on_db(test_id):
                if not force:
                    print("[{0}/{1}] {2} {3}".format(count, total, label, test_id))
                    print("\tTest case {0} already existed. If you still want push,"
                          " please use option --force."
                          "".format(test_id))
                    continue
                else:
                    label = "Update"
                    self.delete_a_test_case(test_id)
            print("[{0}/{1}] {2} {3}".format(count, total, label, test_id))
            test_case_dir = os.path.join(test_folder, test_id)
            self.push_a_test_case(test_case_dir)
            count += 1
    # ---------------------------------------------------------------------------------- #

    # ------------------------------ DELETE TEST CASES --------------------------------- #
    # Delete test data
    def delete_test_data(self, test_id):
        self.fileManager.delete_all_file_bucket_test_case(DbConfig.collections.TEST_DATA,
                                                          test_id)

    # Delete reference data
    def delete_ref_data(self, test_id):
        self.fileManager.delete_all_file_bucket_test_case(DbConfig.collections.REFS_DATA,
                                                          test_id)

    # Delete ground truth data
    def delete_ground_truth_data(self, test_id):
        self.fileManager.delete_all_file_bucket_test_case(DbConfig.collections.GROUND_TRUTH_DATA,
                                                          test_id)

    # Delete scripts
    def delete_scripts(self, test_id):
        self.fileManager.delete_all_file_bucket_test_case(DbConfig.collections.SCRIPTS,
                                                          test_id)

    # Delete a test case
    def delete_a_test_case(self, test_id):
        if self.is_test_case_on_db(test_id):
            # Delete test case specification
            self.test_spec_col.delete_many({
                SpecKeys.ID: test_id
            })
            # Delete files in collections
            self.delete_test_data(test_id)
            self.delete_ref_data(test_id)
            self.delete_ground_truth_data(test_id)
            self.delete_scripts(test_id)
        else:
            print("Test case {0} does not exist on MekongDB!".format(test_id))

    # Delete a list of test cases
    def delete_test_cases(self, list_test_id):
        total = len(list_test_id)
        count = 1
        for test_id in list_test_id:
            print("[{0}/{1}] Delete {2}".format(count, total, test_id))
            self.delete_a_test_case(test_id)

    # Delete all database
    def delete_all(self):
        test_case_col = self.db[DbConfig.collections.TEST_CASE]
        test_case_col.delete_many({})
        self.fileManager.delete_all_file_bucket(DbConfig.collections.TEST_DATA)
        self.fileManager.delete_all_file_bucket(DbConfig.collections.SCRIPTS)
        self.fileManager.delete_all_file_bucket(DbConfig.collections.REFS_DATA)
    # ------------------------------------------------------------------------------------- #

    # ----------------------------------- UPDATE DATA ------------------------------------- #
    # 1. Update specification
    # Update fields of a test case
    def update_spec_field(self, test_case_name, json_post):
        from configs.database import DbQueryKeys
        self.test_spec_col.update_many(
            {SpecKeys.ID: test_case_name},
            {DbQueryKeys.SET: json_post})

    # Update fields by new value
    def update_spec_by_field(self, test_id, field_name, new_value):
        post = {
            field_name: new_value
        }
        self.update_spec_field(test_case_name=test_id, json_post=post)

    # Test directory is path to test case
    def update_spec(self, test_case_name, spec_file):
        try:
            post = read_json(spec_file)
            self.update_spec_field(test_case_name, post)
        except:
            print ("Not have file spec.json")

    # Update weight
    def update_weight(self, test_case_name, new_value):
        post = {
            SpecKeys.WEIGHT: new_value
        }
        self.update_spec_field(test_case_name, post)

    # Update product value
    def update_product_value(self, test_id, new_value):
        post = {
            SpecKeys.PRODUCT: new_value
        }
        self.update_spec_field(test_case_name=test_id, json_post=post)

    # Update component value
    def update_component_value(self, test_id, new_value):
        post = {
            SpecKeys.COMPONENT: new_value
        }
        self.update_spec_field(test_case_name=test_id, json_post=post)

    # Update functions value
    def update_functions_value(self, test_id, new_value):
        post = {
            SpecKeys.FUNCTIONALITIES: new_value
        }
        self.update_spec_field(test_case_name=test_id, json_post=post)

    # Update weight for platform
    def update_weight_platform(self, test_id, new_value, platform):
        spec_infos = self.collectionUtil.query_by_id(id=test_id, find_option={
            SpecKeys.WEIGHTS: 1
        })
        if not spec_infos:
            print("WARN: Weight update - No test case name {test_name} found!".format(
                test_name=test_id))
            return
        spec_info = spec_infos[0]
        if SpecKeys.WEIGHTS in spec_info:
            post = {
                SpecKeys.WEIGHTS: spec_info[SpecKeys.WEIGHTS]
            }
        else:
            post = {
                SpecKeys.WEIGHTS: {}
            }
        post[SpecKeys.WEIGHTS][platform] = new_value
        self.update_spec_field(test_case_name=test_id, json_post=post)

    # Update error flag for platform
    def update_error_flag_platform(self, test_id, new_value, platform):
        spec_infos = self.collectionUtil.query_by_id(id=test_id, find_option={
            SpecKeys.ERROR_FLAGS: 1
        })
        if not spec_infos:
            print("WARN: Error flag update - No test case name {test_name} found!".format(
                test_name=test_id))
            return
        spec_info = spec_infos[0]
        if SpecKeys.ERROR_FLAGS in spec_info:
            post = {
                SpecKeys.ERROR_FLAGS: spec_info[SpecKeys.ERROR_FLAGS]
            }
        else:
            post = {
                SpecKeys.ERROR_FLAGS: {}
            }
        post[SpecKeys.ERROR_FLAGS][platform] = new_value
        self.update_spec_field(test_case_name=test_id, json_post=post)

    # Update tag
    def update_tag(self, test_id, tag_name, value):
        key = "{0}.{1}".format(SpecKeys.TAGS, tag_name)
        self.test_spec_col.update_many({
            SpecKeys.ID: test_id
        }, {
            DbQueryKeys.SET: {
                key: value
            }
        })

    # Update history data for a platform
    def update_history_data(self, test_id, platform, product, version, info):
        spec_infos = self.collectionUtil.query_by_id(id=test_id, find_option={
            SpecKeys.HISTORY_DATA: 1
        })
        spec_info = spec_infos[0]
        history_info = spec_info[SpecKeys.HISTORY_DATA]
        if platform not in history_info:
            history_info[platform] = {}
        if product not in history_info[platform]:
            history_info[platform][product] = {}
        history_info[platform][product][version] = info
        self.update_spec_field(test_case_name=test_id, json_post={
            SpecKeys.HISTORY_DATA: history_info
        })

    # Update history data for a platform by a new value
    def update_history_data_by_value(self, test_id, platform, product, version, label, new_value):
        spec_infos = self.collectionUtil.query_by_id(id=test_id, find_option={
            SpecKeys.HISTORY_DATA: 1
        })
        if not spec_infos:
            print("WARN: History update - No test case name {test_name} found!".format(
                test_name=test_id))
            return
        spec_info = spec_infos[0]
        if SpecKeys.HISTORY_DATA in spec_info:
            history_info = spec_info[SpecKeys.HISTORY_DATA]
            if platform not in history_info:
                history_info[platform] = {}
            if product not in history_info[platform]:
                history_info[platform][product] = {}
            if version not in history_info[platform][product]:
                history_info[platform][product][version] = {}
            history_info[platform][product][version][label] = new_value
            self.update_spec_field(test_case_name=test_id, json_post={
                SpecKeys.HISTORY_DATA: history_info
            })

    # Update history
    def update_history(self, test_id, product, version, info):
        spec_infos = self.query_by_filters({
            SpecKeys.ID: test_id
        })
        spec_info = spec_infos[0]
        history_info = spec_info[SpecKeys.HISTORY]
        if product in history_info:
            history_pro = history_info[product]
        else:
            history_pro = []

        if SpecKeys.History.DELTA not in info:
            info[SpecKeys.History.DELTA] = version

        is_exist = False
        for element in history_pro:
            if element[SpecKeys.History.DELTA] == version:
                is_exist = True
                for key in info:
                    element[key] = info[key]
                break
        if not is_exist:
            history_pro.append(info)

        key = "{0}.{1}".format(SpecKeys.HISTORY, product)
        # Set history information of product
        self.test_spec_col.update_many({
            SpecKeys.ID: test_id
        }, {
            DbQueryKeys.SET: {
                key: history_pro
            }
        })

    # 2. Update reference data
    # Update all file and folder in reference folder to REF bucket on database
    def update_reference_data(self, ref_folder, test_id):
        self.delete_ref_data(test_id)
        self.push_ref_data(ref_folder, test_id)

    # Update test data
    def update_test_data(self, test_data_folder, test_id):
        self.delete_test_data(test_id)
        self.push_test_data(test_data_folder, test_id)

    # Update ground truth data
    def update_ground_truth_data(self, ground_truth_data_folder, test_id):
        self.delete_ground_truth_data(test_id)
        self.push_ground_truth_data(ground_truth_data_folder, test_id)

    # Update scripts
    def update_scripts(self, scripts_folder, test_id):
        self.delete_scripts(test_id)
        self.push_scripts(scripts_folder, test_id)
