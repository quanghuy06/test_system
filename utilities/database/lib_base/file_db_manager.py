# Toshiba - TSDV
# Team:         PHOcr
# Author:       Luong Van Huan
# Email:        huan.luongvan@toshiba-tsdv.com
# Date created: 20/08/2017
# Last update:  27/06/2017
# By:
# Description:  This define a class to manage file store on dabase
import os
import json
from bson.json_util import dumps
from gridfs import GridFS
from gridfs import GridFSBucket
from pymongo.errors import OperationFailure


class FileManager(object):

    def __init__(self, db):
        self.db = db

    def put_a_file(self, bucket_name, file_name, file_name_in_db, test_case_name):
        fs = GridFS(self.db, collection=bucket_name)
        os.path.isfile(file_name)
        f = open(file_name, 'rb')
        fs.put(f.read(), filename=file_name_in_db, test_case=test_case_name)
        f.close()

    def put_unique_file(self, bucket_name, local_file, file_name_in_db):
        fs = GridFS(self.db, collection=bucket_name)
        f = open(local_file, 'rb')
        fs.put(f.read(), filename=file_name_in_db)
        f.close()

    def get_a_file(self, bucket_name, file_name_in_db, file_name_output):
        files = self.db[bucket_name].files.find({"filename": file_name_in_db})
        if not files.count():
            raise Exception("Cannot find the file in database")
        fs_ = GridFSBucket(self.db, bucket_name=bucket_name)

        # Get file to write to
        f = open(file_name_output, 'wb')
        fs_.download_to_stream_by_name(file_name_in_db, destination=f)
        f.close()

    # Get all files in a collection
    def get_all_files(self, bucket_name, out_folder):
        # Query all files in collection
        cursor = self.db[bucket_name].files.find({})
        file_list = []
        for f_info in cursor:
            file_list.append(f_info['filename'].encode('utf-8'))
        if len(file_list) == 0:
            print "Collection {0} has no files".format(bucket_name)
            return []

        # Create output folder if not exist
        if not os.path.isdir(out_folder):
            os.makedirs(out_folder)

        fs_ = GridFSBucket(self.db, bucket_name=bucket_name)
        total = len(file_list)
        count = 1

        for fname in file_list:
            print "[{0}/{1}] Get {2} ...".format(count, total, fname)
            target_file = os.path.join(out_folder, fname)
            f = open(target_file, 'wb')
            fs_.download_to_stream_by_name(fname, destination=f)
            f.close()
            count += 1

        return file_list

    def delete_a_file(self, bucket_name, file_name_in_db):
        cursor = self.db[bucket_name].files.find({"filename": file_name_in_db})
        fs = GridFS(self.db, collection=bucket_name)
        for f_info in cursor:
            fs.delete(f_info['_id'])

    def delete_all_file_bucket_test_case(self, bucket_name, test_case_name):
        cursor = self.db[bucket_name].files.find({"test_case": test_case_name})
        fs = GridFS(self.db, collection=bucket_name)
        for f_info in cursor:
            fs.delete(f_info['_id'])

    def delete_all_file_bucket(self, bucket_name):
        cursor = self.db[bucket_name].files.find({})
        fs = GridFS(self.db, collection=bucket_name)
        for f_info in cursor:
            fs.delete(f_info['_id'])

    def query_all_file_of_a_test_case(self, bucket_name, test_case_name):
        try:
            result = self.db[bucket_name].files.find({"test_case": test_case_name})
        except OperationFailure:
            print("DatabaseFileManager: This bucket does not have text index")
            raise
        # Convert Bson object to Json object
        json_format = dumps(result)
        data = json.loads(json_format)
        if len(data):
            return data
        else:
            return {}
