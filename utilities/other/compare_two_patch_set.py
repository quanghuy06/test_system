# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      13/08/2018
# Last update:
# Description:      Script is used for comparing between two patch set's results

import sys
import sys_path
import argparse
sys_path.insert_sys_path()
from configs.common import SupportedPlatform
from other.lib_base.two_path_set_comparing import TwoPatchSetComparing



def parse_argument():
    parser = argparse.ArgumentParser(
                description='Compare output and reference of all test cases on test folder')
    parser.add_argument('-j', "--job-name", required=True,
                        help="Jenkins job name")
    parser.add_argument('-b', "--last-build-number", required=True,
                        help="Jenkins last build number will contain reference data")
    parser.add_argument('-p', "--platform",
                        help="Platform to compare. If not platform , it will execute compare all "
                             "platform in list SupportedPlatform. If platform is specified, it will"
                             "compare only this platform! ")
    return parser.parse_args()


def main():
    # Parse argument
    args = parse_argument()
    job_name = args.job_name
    last_build_number = args.last_build_number
    if last_build_number:
        if args.platform:
            if args.platform in SupportedPlatform:
                compare_obj = TwoPatchSetComparing(job_name, last_build_number, args.platform)
                compare_obj.do_work()
            else:
                print "Please recheck platform, it must be \"linux\" or \"windows\"! "
                sys.exit(0)
        else:
            for platform in SupportedPlatform:
                compare_obj = TwoPatchSetComparing(job_name, last_build_number, platform)
                compare_obj.do_work()
    else:
        print "Don't have last build number! No comparison executed! "
        sys.exit(0)


if __name__ == '__main__':
    main()
