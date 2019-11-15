# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      30/08/2018
# Description:      This python script define global variables which are use for re-testing test
#                   cases which are distributed on failed workers.


# Default number of run to try
MAX_RUN_TIMES = 1
# Default start of run counter
START_COUNT = 1
# Current count
RUN_COUNT = START_COUNT
# Check to stop run
RUN_STOPPED = False
# Number of re-try for test
MAX_TEST_TIMES = 3
# Template for result folder of run time x
RUN_FOLDER_TEMPLATE = "run_{count}"
