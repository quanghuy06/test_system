# Author: Trong Nguyen Van
# Created: 07/08/2019
# This module is used to help PHOcr developers to run the performance analysis
# of theirs change and hep the manager track the performance of PHOcr for each
# delta release in an automatically way.

import argparse
from performance_analyzer import PerformanceAnalyser


def parse_argument():
    """
    Parse the arguments from command line
    """
    parser = argparse.ArgumentParser(description="Run performance analysis with PHOcr on board")
    parser.add_argument("--board-ip", dest="board_ip", type=str, required=True,
                        help="IP address of target MFP board, separated by , token")
    parser.add_argument("--build-package-link", dest="build_package_link", type=str, required=True,
                        help="Link to build package on Jenkins")
    parser.add_argument("--mekong-path", dest="mekong_path", type=str, required=True,
                        help="Absolute path to Mekong project")
    parser.add_argument("--gerrit-checkout", dest="gerrit_checkout", type=str, required=True,
                        help="Git command to checkout the change")
    parser.add_argument("--id", dest="test_case_id", type=str, required=True, help="List of test case ID")
    return parser.parse_args()


def main():
    print("\n\t\t+------------------------------------------------+")
    print("\t\t+         PERFORMANCE AUTOMATION TEST            +")
    print("\t\t+                                                +")
    print("\t\t+------------------------------------------------+")
    show_info()
    args = parse_argument()
    analyser = PerformanceAnalyser(
        args.board_ip,
        args.mekong_path,
        args.build_package_link,
        args.test_case_id,
        args.gerrit_checkout)
    analyser.do_job_multithread()


def show_info():
    print("PERFORMANCE AUTOMATION TEST is a tool designed and implemented by Trong Nguyen Van")
    print("Copyright by Trong Nguyen Van\n")


if __name__ == "__main__":
    main()
