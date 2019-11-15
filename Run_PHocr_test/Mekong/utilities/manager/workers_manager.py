# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      25/06/2018
# Description:      This python script is used to manage worker machines on a test machine
import argparse
import sys
import sys_path
sys_path.insert_sys_path()

from manager.lib_manager.workers_manager_build import WorkersBuildManager
from manager.lib_manager.workers_manager_test import WorkersTestManager
from manager.lib_manager.workers_manager_updater import WorkersManagerUpdater
from configs.projects.mekong import TestSystem
from configs.system_data_updater import DataUpdatesAvailable


MANUAL = \
    """
Manage virtual machines on a node to:
1. Build
    Require:
        - Parameters from jenkins in json file
    Optional:
        - A custom profile configuration in json file. Currently, default configuration is inside
        Mekong
2. Build a release version
    Require:
        - Parameters from jenkins in json file
    Optional:
        - A custom profile configuration in json file. Currently, default configuration is inside
        Mekong
2. Test
    Require:
        - Parameters from jenkins in json file
        - Test distribution file in json format
    Optional:
        - A custom profile configuration in json file. Currently, default configuration is inside
        Mekong

3. Update static data for virtual machines
    Currently, there are some data which rarely changes. Therefore, we put them directly into
    test virtual machines to reduce TAT of system. Whenever these data change, then we run script
    to update them on Virtual machines.
    There are 3 types of data can be support updating:
        - PHOcr trained data
        - Python portable for PHOcr office
        - Valgrind used by Mekong for memory leak checking
    You can run updating a single type of data or combine them in a run time. Data will be updated
    for all virtual machines which is distributed (in system profile configuration) for testing
    in both Engineering Test an Integration Test.
    Parameters file is not require in this situation.
    Optional:
        - A custom profile configuration in json file. Currently, default configuration is inside
        Mekong

4. Reset all test virtual machines to a backup snapshot
    This help us can return to a state which system can run good in case new change of Mekong
    make automation test system not reliable.
    """


def parse_argument():
    """
    Parse argument for run script.

    Returns
    -------
    ArgumentParser
        Arguments parser object

    """
    parser = argparse.ArgumentParser(MANUAL)
    # Required arguments for both functionality
    # Name of current node that run script
    parser.add_argument('-n', '--name',
                        required=True,
                        help="Name of test machine")
    # Path to json parameters file
    parser.add_argument('-p', '--parameters',
                        help="Configuration file for run build and test.")
    # Build functionality
    parser.add_argument('--build',
                        default=False,
                        action="store_true",
                        help="Manage virtual machine for building project")

    # Build a release version
    parser.add_argument('--build-release',
                        default=False,
                        action='store_true',
                        help='Manage virtual machine to build a release version')

    # Test functionality
    parser.add_argument("--test",
                        default=False,
                        action="store_true",
                        help="Execute testing")
    parser.add_argument('-d', '--distribution',
                        help="Path to json file that contains test cases distribution")

    # Update static data for test virtual machines on Node
    # Update python portable package for PHOcr
    parser.add_argument('--update-python-portable',
                        default=False,
                        action='store_true',
                        help='Update newest python portable package for test virtual machines from'
                             ' SVN')
    # Update training data
    parser.add_argument('--update-training-data',
                        default=False,
                        action='store_true',
                        help='Update newest training data for test virtual machines from SVN')

    # Update valgrind for memory checking of Mekong utilities
    parser.add_argument('--update-valgrind',
                        default=False,
                        action='store_true',
                        help='Update newest valgrind utility for memory testing on test virtual'
                             ' machines from SVN')

    # Reset all test virtual machines to backup snapshot
    parser.add_argument('--reset-backup',
                        default=False,
                        action='store_true',
                        help='Reset all virtual machines on node to backup snapshot')

    # Optional arguments that have default value if it's not pass
    # through (can be use for both)
    parser.add_argument('-pf', '--profile',
                        default=None,
                        help="Path to profile of test machines")
    return parser


def main():
    # Parse argument
    parser = parse_argument()
    args = parser.parse_args()
    if args.profile:
        # Use custom system configuration
        profile_path = args.profile
    else:
        # Use default system configuration inside Mekong
        profile_path = TestSystem.Paths.PROFILE

    manager = None
    log_level = 2

    # Build
    if args.build:
        if not args.parameters:
            print("Missing parameters file which required for executing build")
            sys.exit(1)
        manager = WorkersBuildManager(name=args.name,
                                      parameters_file=args.parameters,
                                      profile_path=profile_path,
                                      log_level=log_level)

    # Build release
    if args.build_release:
        if not args.parameters:
            print("Missing parameters file which required for executing build")
            sys.exit(1)
        manager = WorkersBuildManager(name=args.name,
                                      parameters_file=args.parameters,
                                      profile_path=profile_path,
                                      is_build_release=True,
                                      log_level=log_level)

    # Manage test virtual machines for testing. Make sure we already have build packages in the
    # right location.
    if args.test:
        if not args.parameters:
            print("Missing parameters file which required for executing test")
            sys.exit(1)
        manager = WorkersTestManager(name=args.name,
                                     parameters_file=args.parameters,
                                     profile_path=profile_path,
                                     distribution_file=args.distribution,
                                     log_level=log_level)

    # Checking for updating static data
    update_list = list()

    # Check if updating python portable
    if args.update_python_portable:
        update_list.append(DataUpdatesAvailable.PYTHON_PORTABLE)

    # Check if updating training data
    if args.update_training_data:
        update_list.append(DataUpdatesAvailable.PHOCR_TRAINED_DATA)

    # Check if updating valgrind utility for Mekong
    if args.update_valgrind:
        update_list.append(DataUpdatesAvailable.VALGRIND_MEKONG)

    if args.reset_backup or update_list:
        manager = WorkersManagerUpdater(update_list=update_list,
                                        reset_backup=args.reset_backup,
                                        profile_path=profile_path,
                                        name=args.name)

    if not manager:
        print("No work to be done!")
        parser.print_help()
    else:
        manager.do_work()

    sys.exit(0)


if __name__ == "__main__":
    main()
