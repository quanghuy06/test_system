# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      26/06/2018
# Description:      This python script will be run on master to manage nodes in automation test
#                   system
import argparse
import sys
import sys_path
sys_path.insert_sys_path()
import configs.run_counter
from configs.projects.mekong import TestSystem
from configs.system_data_updater import DataUpdatesAvailable
from manager.lib_manager.nodes_manager_build import NodesManagerBuild
from manager.lib_manager.nodes_manager_test import NodesManagerTest
from manager.lib_manager.nodes_manager_updater import NodesManagerUpdater


MANUAL = \
    """
Manage automation test system to:
1. Build
    Require:
        - Parameters from jenkins in json file
2. Build a release version
    Require:
        - Parameters from jenkins in json file
2. Test
    Require:
        - Parameters from jenkins in json file
    Optional:
        - Test distribution file in json format for a customize usage.

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

4. Reset all test virtual machines to a backup state
    This help us back to a state which test system con run good in case some change of Mekong
    cause issues on automation test system.
    """


def parse_argument():
    parser = argparse.ArgumentParser(MANUAL)
    # General parameters use for both building and testing in
    # parameters.json
    parser.add_argument('-p', '--parameters',
                        default=None,
                        help="Required if build/test flag is ON. All parameter needed for master "
                             "to manage test nodes for build and test.")
    # Build flag
    parser.add_argument('--build',
                        default=False,
                        action="store_true",
                        help="Manage test nodes to execute building")

    # Build a release version
    parser.add_argument('--build-release',
                        default=False,
                        action='store_true',
                        help='Manage test nodes to build a release version')

    # Test flag
    parser.add_argument('--test',
                        default=False,
                        action="store_true",
                        help="Manage test nodes to execute testing")

    parser.add_argument('-d', '--distribution',
                        default=None,
                        help='Optional test distribution for a specific purpose or testing Test'
                             ' system')

    # Static data update
    # Currently, there are some static data which is put directly into Clean-State of test virtual
    # machine to reduce time to transfer data between node and virtual machines. So these options
    # will help us update these data easier. Please make sure data was already updated on SVN.

    # Update python portable
    parser.add_argument('--update-python-portable',
                        default=False,
                        action='store_true',
                        help='Optional: Update python portable package for Virtual machines from'
                             ' SVN')
    # Update phocr trained data
    parser.add_argument('--update-training-data',
                        default=False,
                        action='store_true',
                        help='Optional: Update latest trained data for PHOcr on test virtual '
                             'machines from PHOcr master on GIT')

    # Update valgrind for memory leak checking
    parser.add_argument('--update-valgrind',
                        default=False,
                        action='store_true',
                        help='Optional: Update valgrind package used by Mekong on test virtual '
                             'machines for memory leak checking')

    # Reset all test virtual machines to backup state
    parser.add_argument('--reset-backup',
                        default=False,
                        action='store_true',
                        help='Optional: Reset all test virtual machines to backup state which '
                             'really clean and have no data for testing on them.')

    return parser


def main():
    # Parse argument
    parser = parse_argument()
    args = parser.parse_args()

    manager = None

    # Build flag is on
    if args.build:
        if not args.parameters:
            print("Parameters is missing")
            sys.exit(1)
        manager = NodesManagerBuild(name="master",
                                    parameters_file=args.parameters,
                                    profile_path=TestSystem.Paths.PROFILE)

    # Build a release version
    if args.build_release:
        if not args.parameters:
            print("Parameters is missing")
            sys.exit(1)
        manager = NodesManagerBuild(name="master",
                                    parameters_file=args.parameters,
                                    profile_path=TestSystem.Paths.PROFILE,
                                    is_build_release=True)

    # Manage testing. Run after we already have build packages from run build.
    if args.test:
        if not args.parameters:
            print("Parameters is missing")
            sys.exit(1)
        manager = NodesManagerTest(name="master",
                                   parameters_file=args.parameters,
                                   profile_path=TestSystem.Paths.PROFILE,
                                   distribution_file=args.distribution)

    # Update data on virtual machines
    update_list = list()
    # Check for updating python portable of PHOcr on virtual machines
    if args.update_python_portable:
        update_list.append(DataUpdatesAvailable.PYTHON_PORTABLE)
    # Check for updating trained data of PHOcr on virtual machines
    if args.update_training_data:
        update_list.append(DataUpdatesAvailable.PHOCR_TRAINED_DATA)
    # Check for updating valgrind utility of Mekong for memory leak check on virtual machines
    if args.update_valgrind:
        update_list.append(DataUpdatesAvailable.VALGRIND_MEKONG)
    if args.reset_backup or update_list:
        manager = NodesManagerUpdater(name="master",
                                      update_list=update_list,
                                      reset_backup=args.reset_backup,
                                      profile_path=TestSystem.Paths.PROFILE)

    if manager:
        # Set up number of try to re-run
        if isinstance(manager, NodesManagerTest):
            configs.run_counter.MAX_RUN_TIMES = configs.run_counter.MAX_TEST_TIMES

        # Do work
        while not configs.run_counter.RUN_STOPPED:
            print(" ----- Running time {0} -----".format(configs.run_counter.RUN_COUNT))
            manager.do_work()
    else:
        print("Nothing to be done!")
        parser.print_help()

    sys.exit(0)


if __name__ == "__main__":
    main()
