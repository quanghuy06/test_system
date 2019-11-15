# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Tran Quang Huy
# Email:            huy.tranquang@toshiba-tsdv.com
# Date create:      4/11/2019
# Description:      This python script will be run on master to update test cases folder on all
# test node of automation test system which are defined in configs.common.Machines
import argparse
import sys
import sys_path
sys_path.insert_sys_path()
from manager.lib_manager.nodes_manager_test_cases_folder_updater import \
    NodesManagerUpdateTestCasesFolder
from configs.projects.mekong import TestSystem


MANUAL = \
    """
Manage automation test system to update test cases folder on all test nodes of automation test 
system.
    """


def parse_argument():
    parser = argparse.ArgumentParser(MANUAL)
    return parser


def main():
    # Parse argument
    parser = parse_argument()
    parser.parse_args()

    manager = NodesManagerUpdateTestCasesFolder(name="Master",
                                                profile_path=TestSystem.Paths.PROFILE)
    manager.do_work()

    sys.exit(0)


if __name__ == "__main__":
    main()
