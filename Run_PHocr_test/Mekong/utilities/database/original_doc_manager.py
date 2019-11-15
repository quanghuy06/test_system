# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created: 27/06/2017
# Last update:  27/06/2017
# Description:  This script allow user to get, push, delete original document
#               which store on database
import sys_path
sys_path.insert_sys_path()

import argparse
import os
import traceback

from configs.database import DbConfig
from database.lib_base.test_case_manager import TestCaseManager
from configs.database import SpecKeys


def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True,
                        help="username to access Mekong database")
    parser.add_argument('-p', '--password', required=True,
                        help="Password of username to access Mekong database")
    parser.add_argument('--getByName', default=None,
                        help="Get original documents by name."
                             " You can get mutiple files by using comma as delimiter."
                             "\nExample: \"file1,file2,file3\"")
    parser.add_argument('--getByTestCase', default=None,
                        help="Get original documents relate to some test cases."
                             " List of test cases uses comma as "
                             "delimiter."
                             "\nExample: \"testcase1,testcase2,testcase3\"")
    parser.add_argument("--getAll", default=False, action='store_true',
                        help="Get all original documents from Mekong database")
    parser.add_argument('--push', default=None,
                        help="Push original documents to DbConfig."
                             " You should pass file path or folder that"
                             " contains files to push.")
    parser.add_argument('--delete', default=None,
                        help="Delete original documents."
                             " You delete multiple files by using comma as delimiter."
                             "\nExample: \"file1,file2,file3\"")
    parser.add_argument('--deleteAll', default=False, action='store_true',
                        help="Delete all original documents on database")
    return parser


def main():
    # Parse arguments of command
    parser = parse_arguments()
    args = parser.parse_args()

    test_case_manager = TestCaseManager()
    dbFileManager = test_case_manager.fileManager

    # Create folder to store original documents
    if not os.path.isdir(DbConfig.collections.ORIGINAL_DOC):
        os.makedirs(DbConfig.collections.ORIGINAL_DOC)

    # Get all original documents from database
    if args.getAll:
        dbFileManager.get_all_files(DbConfig.collections.ORIGINAL_DOC,
                                    DbConfig.collections.ORIGINAL_DOC)
        return

    # Get original documents by name
    if args.getByName:
        file_list = args.getByName.split(',')
        total = len(file_list)
        count = 1
        for fname in file_list:
            print "[{0}/{1}] Get {2} ...".format(count, total, fname)
            target_file = os.path.join(DbConfig.collections.ORIGINAL_DOC, fname)
            try:
                dbFileManager.get_a_file(DbConfig.collections.ORIGINAL_DOC, fname, target_file)
            except:
                print "\tERROR: Can not get {0} from Mekong database!".format(fname)
                traceback.print_exc()
            count += 1
        return

    if args.getByTestCase:
        test_case_list = args.getByTestCase.split(',')
        file_list = []
        no_doc = []
        # Get list of original documents
        for test_case in test_case_list:
            if not test_case_manager.is_test_case_on_db(test_case):
                print "Test case {0} doesn't exists on database".format(test_case)
            else:
                spec_list = test_case_manager.query_spec_info_by_id(test_case)
                spec_data = spec_list[0]
                doc_name = spec_data[SpecKeys.TAGS][SpecKeys.Tags.DOC_NAME]
                if not doc_name:
                    no_doc.append(test_case)
                    continue
                print "{0}\t:\t{1}".format(test_case, doc_name)
                if doc_name not in file_list:
                    file_list.append(doc_name)
        if no_doc:
            msg = "Test cases that has no specified original document: "
            for test_case in no_doc:
                msg += test_case + ", "
            print msg[0:-2]

        # Get original documents
        total = len(file_list)
        count = 1
        for fname in file_list:
            print "[{0}/{1}] Get {2} ...".format(count, total, fname)
            target_file = os.path.join(DbConfig.collections.ORIGINAL_DOC, fname)
            try:
                dbFileManager.get_a_file(DbConfig.collections.ORIGINAL_DOC, fname, target_file)
            except:
                print "\tERROR: Can not get {0} from Mekong database!".format(fname)
                traceback.print_exc()
            count += 1
        return

    if args.push:
        # Get file list to push
        file_list = []
        source = args.push
        if not os.path.exists(source):
            print "ERROR: No such file or directory {0}".format(source)
        if os.path.isfile(source):
            file_list.append(source)
        if os.path.isdir(source):
            for fname in os.listdir(source):
                fpath = os.path.join(source, fname)
                if os.path.isfile(fpath):
                    file_list.append(fpath)

        # Push files to database
        total = len(file_list)
        count = 1
        for fpath in file_list:
            fname = os.path.basename(fpath)
            print "[{0}/{1}] Push {2} ...".format(count, total, fname)
            try:
                dbFileManager.put_unique_file(DbConfig.collections.ORIGINAL_DOC, fpath, fname)
            except:
                print "ERROR: Can not push {0} to database".format(fpath)
                traceback.print_exc()
            count += 1
        return

    if args.delete:
        file_list = args.delete.split(',')
        total = len(file_list)
        count = 1
        for fname in file_list:
            print "[{0}/{1}] Delete {2} ...".format(count, total, fname)
            try:
                dbFileManager.delete_a_file(DbConfig.collections.ORIGINAL_DOC, fname)
            except:
                print "\tERROR: Can not delete {0} from Mekong database".format(fname)
                traceback.print_exc()
            count += 1
        return

    if args.deleteAll:
        dbFileManager.delete_all_file_bucket(DbConfig.collections.ORIGINAL_DOC)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
