# TOSHIBA - TSDV
# Team:             PHOcr
# Author:
# Email:
# Date create:
# Last update by:      Phung Dinh Tai
# Date:             03/10/2019
# Description:      This script is used to synchronize test cases folder on nodes with database
#                   in Post Integration. The script should be called on master machine and after
#                   reference data of test cases were updated to database.
import sys
import time
import traceback
import sys_path
sys_path.insert_sys_path()
from jenkins.lib_synchronization.test_cases_updater import TestCasesUpdater
from jenkins.lib_synchronization.nodes_synchronizer import NodesSynchronizer


def main():

    print("<SM> Synchronize test cases folder on nodes")

    # Calculate execution time for processing
    start_time = time.time()

    # Update test cases folder on master machine includes getting new test cases and updating for
    # changed test cases
    try:
        test_cases_updater = TestCasesUpdater()
        test_cases_updater.do_works()
    except:
        traceback.print_exc()
        print("WARN: Failed to update test cases folder on master machine!")
        print("<EM> Finish in: {execution_time}s".format(execution_time=time.time() - start_time))
        sys.exit(1)

    # Run synchronization between test cases folder on master machine with test cases folder on
    # test
    try:
        test_case_synchronizer = NodesSynchronizer()
        test_case_synchronizer.synchronize_test_cases()
    except:
        traceback.print_exc()
        print("WARN: Failed to synchronize test cases folder on nodes!")
        print("<EM> Finish in: {execution_time}s".format(execution_time=time.time() - start_time))
        sys.exit(2)

    print("<EM> Finish in: {execution_time}s".format(execution_time=time.time()-start_time))
    sys.exit(0)


if __name__ == "__main__":
    main()
