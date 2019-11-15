# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Luong Van Huan
# Email:            huan.luongvan@toshiba-tsdv.com
# Date create:      20/08/2016
# Last update:      13/07/2018
# Editor:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Description:      This script define users and roles to access Mekong database

from pymongo import MongoClient
from configs.database import DbConfig, DbAccountJsonKeys
from pymongo.errors import DuplicateKeyError

# Define accounts will add into data base:
# admin of any database: Name: siteUserAdmin, pass: password
# admin of Mekong database: Name: "admin", pass: "1"

# Only gerrit account has read, write permission. Because only gerrit can update database
# other members has own account to read database data.

# To add new user account: insert to "users" dictionary, then call this script

# Required: mongodb server start with authentication enabled


class AccountManager(object):
    def __init__(self, admin, password):
        # Connect to data base server
        client = MongoClient(host=DbConfig.HOST, port=DbConfig.PORT)
        self.db = client[DbConfig.DB_NAME]
        self.db.authenticate(name=admin, password=password)

    users = \
        [
            {
                DbAccountJsonKeys.NAME: 'jenkins',
                DbAccountJsonKeys.PASSWORD: 'jenkins',
                DbAccountJsonKeys.ROLES: [
                    {
                        DbAccountJsonKeys.ROLE: DbAccountJsonKeys.Roles.RW,
                        DbAccountJsonKeys.DATABASE: DbConfig.DB_NAME
                    }
                ]
            },
            {
                DbAccountJsonKeys.NAME: 'huanlv',
                DbAccountJsonKeys.PASSWORD: '1',
                DbAccountJsonKeys.ROLES: [
                    {
                        DbAccountJsonKeys.ROLE: DbAccountJsonKeys.Roles.R,
                        DbAccountJsonKeys.DATABASE: DbConfig.DB_NAME
                    }
                ]
            },
            {
                DbAccountJsonKeys.NAME: 'namld',
                DbAccountJsonKeys.PASSWORD: '1',
                DbAccountJsonKeys.ROLES: [
                    {
                        DbAccountJsonKeys.ROLE: DbAccountJsonKeys.Roles.R,
                        DbAccountJsonKeys.DATABASE: DbConfig.DB_NAME
                    }
                ]
            },
            {
                DbAccountJsonKeys.NAME: 'phuchm',
                DbAccountJsonKeys.PASSWORD: '1',
                DbAccountJsonKeys.ROLES: [
                    {
                        DbAccountJsonKeys.ROLE: DbAccountJsonKeys.Roles.R,
                        DbAccountJsonKeys.DATABASE: DbConfig.DB_NAME
                    }
                ]
            }
        ]

    def update_user(self):
        for user in self.users:
            try:
                self.db.add_user(name=user[DbAccountJsonKeys.NAME],
                                 password=user[DbAccountJsonKeys.PASSWORD],
                                 roles=user[DbAccountJsonKeys.ROLES])
            except DuplicateKeyError as err:
                print(err)

    @staticmethod
    def add_user(is_read_write):
        if is_read_write:
            role = [
                {
                    DbAccountJsonKeys.ROLE: DbAccountJsonKeys.Roles.RW,
                    DbAccountJsonKeys.DATABASE: DbConfig.DB_NAME
                }
            ]
        else:
            role = [
                {
                    DbAccountJsonKeys.ROLE: DbAccountJsonKeys.Roles.R,
                    DbAccountJsonKeys.DATABASE: DbConfig.DB_NAME
                }
            ]
        return role
