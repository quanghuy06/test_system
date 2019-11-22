# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Luong Van Huan
# Date create:      12/12/2018
# Description:      This script used to call lib_base/clone_database.py module
#                   to execute clone database

import argparse
import sys_path
sys_path.insert_sys_path()

from database.lib_base.clone_database import CloneDatabase
from configs.database import MongoDbConfig


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--ip", default="10.116.41.96",
                        help="IP of remote machine store database."
                             " Default IP is 10.116.41.96")
    parser.add_argument("-port", "--port", default="27018",
                        help="Port number for mongod."
                             " Default port is 27018")
    parser.add_argument("-u", "--username", default="ocr3",
                        help="Username to access to remote machine."
                             " Default username is 'ocr3'.")
    parser.add_argument("-sp", "--source-path",
                        default=MongoDbConfig.Mongod.MEKONGDB_PATH,
                        help="The directory on remote machine where locates "
                             "database. Default path is "
                             "'/media/ocr3/data/MekongDB'.")
    parser.add_argument("-dp", "--destination-path", required=True,
                        help="The directory to store database cloned on local "
                             "machine. This is require parameters.")

    return parser.parse_args()

def main():

    args = parse_args()

    ip = args.ip
    port = args.port
    username = args.username
    source_path=args.source_path
    destination_path = args.destination_path

    clone_database = CloneDatabase(ip,
                                   port,
                                   username,
                                   source_path,
                                   destination_path)
    clone_database.go()


if __name__ == '__main__':
    main()