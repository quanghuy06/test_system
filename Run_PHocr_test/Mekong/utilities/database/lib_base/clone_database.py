# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Luong Van Huan
# Date create:      12/12/2018
# Description:      This python module used to clone database
#                   from database on remote machine.

import logging

import os
import shutil

from baseapi.command_runner import CommandRunner

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, OperationFailure
from configs.database import DbConfig, MongoDbConfig
from configs.credential import Credential
from multiprocessing import Process


def start_server_process(db_path, port):
    """
    Start mongod instance on a subprocess. In the case MekongDB is cloned and
    we want to continue use this db, we can start mongodb by command:
        mongod --auth --port <Port_number_of_mongod> --dbpath <db_on_your_machine_located>

    Parameters
    ----------
    db_path: str
        Where database on your machine located
    port: int
        Port number of mongod

    Returns
    -------
    None

    """
    commands = list()
    commands.append(MongoDbConfig.Mongod.EXECUTABLE)
    commands.append(MongoDbConfig.Mongod.Options.AUTH)
    commands.append(MongoDbConfig.Mongod.Options.PORT)
    commands.append(port)
    commands.append(MongoDbConfig.Mongod.Options.DBPATH)
    commands.append(db_path)

    logging.info(" ".join(commands))
    logging.info("Use port {} to access to database".format(port))

    # Run server ultil the thread was killed
    # or user press Ctrl + C
    CommandRunner.run_with_subprocess(commands)


class CloneDatabase(object):
    """
    Use for clone database from master
    """

    def __init__(self, remote_ip, mongod_port, remote_username,
                 remote_source_path, destination_path):
        """
        Constructor for init CloneDatabase object

        Parameters
        ----------
        remote_ip: str
            Ip of server store origin database
        mongod_port: int
            Port number for mongod
        remote_username: str
            Username to access remote server
        remote_source_path: str
            path to location of origin database on remote server
        destination_path: str
            directory will local clone database on local machine
        """
        self.remote_ip = remote_ip
        self.remote_username = remote_username
        self.remote_source_path = remote_source_path
        self.mekong_dir_name = os.path.basename(self.remote_source_path)
        self.destination_path = destination_path

        # Define a port difference with default port of Mongod
        # to avoid conflict
        self.port = mongod_port

        # Print from INFO level
        logging.basicConfig(level=logging.INFO)

    def go(self):
        """
        Do clone database
        Returns
        -------
        None

        """
        logging.info("Start clone database from {}".format(self.remote_ip))
        try:
            self._init_mekong_dir()
            self._copy_database_from_server()
            self._start_local_mongod_on_separate_process()
        finally:
            self._terminates_local_mongod()

        logging.info("End clone database")

    def _init_mekong_dir(self):
        """
        Ensure mekong database dir is empty and exists.
        Returns
        -------
        None

        """
        logging.info("Init Mekong dir")
        mekong_path = os.path.join(self.destination_path, self.mekong_dir_name)
        if os.path.isdir(mekong_path):
            logging.warning("Delete folder {}".format(mekong_path))
            shutil.rmtree(mekong_path)
        logging.info("Create Mekong path {}".format(mekong_path))
        os.makedirs(mekong_path)

    def _copy_database_from_server(self):
        """
        Use scp to copy database from mongodb server
        Returns
        -------
        None
        """

        remote_path = '{0}@{1}:{2}'.format(self.remote_username,
                                           self.remote_ip,
                                           self.remote_source_path)
        commands = list()
        commands.append("scp")
        commands.append("-r")
        commands.append(remote_path)
        commands.append(self.destination_path)

        logging.info("Copy database from server {}".format(commands))
        logging.info("Copy to: {}".format(self.destination_path))

        CommandRunner.run_with_subprocess(commands)

    def _start_local_mongod_on_separate_process(self):
        """
        Start mongod on new process.

        Returns
        -------
        None

        """
        logging.info("Start Mekong server")

        mekong_path = os.path.join(self.destination_path, self.mekong_dir_name)
        logging.info("Working with mekong on location: {}".format(mekong_path))
        self.process = Process(target=start_server_process,
                               args=(mekong_path, self.port, ))

        self.process.start()

        # Wait until user press Ctrl+C
        # or this process was killed.
        self.process.join()

        logging.info("Mekong server is running")

    def _terminates_local_mongod(self):
        """
        Terminate mongod process on local.

        Returns
        -------
        None
        """

        logging.info("Poweroff server!!!")
        self.process.terminate()
