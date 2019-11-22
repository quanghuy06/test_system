# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      19/07/2018
# Description:      This python script will be check commit message before
#                   do anything

import argparse
import sys_path
import sys
sys_path.insert_sys_path()
from validate.commit_message_validator.commit_message_validator import CommitMessageValidator


def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--parameters',
                        help="All parameter needed for master to"
                             " manage test nodes")
    return parser


def main():
    parser = parse_argument()
    args = parser.parse_args()
    if not args.parameters:
        print "\nMissing parameter file! \n"
        sys.exit(1)
    check_mess = CommitMessageValidator(args.parameters)
    check_mess_result = check_mess.check_filter_commit()
    if check_mess_result:
        print "\nCommit message is correct !!!!\n"
    else:
        print "Commit message is not good. Please recheck!"
        sys.exit(1)


if __name__ == "__main__":
    main()