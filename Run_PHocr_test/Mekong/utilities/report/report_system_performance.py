# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      17/09/2019
# Description:      This is run script to generate performance report of automation test system.
#                   This report will be useful to analyze system and have some improvements for
#                   bottle necks.
import argparse
import os
import sys
import sys_path
sys_path.insert_sys_path()
from baseapi.file_access import remove_paths, make_dir
from report.lib_system_performance.system_performance_reports_generator \
    import SystemPerformanceReportsGenerator


MANUAL = \
    """
    This script is used to generate excel report for performance of automation test system. You
    need provide path to log folder of system which is generated after calling to nodes_manager.py
    Default path will be: info/log.
    This report will help you see the order of processes on master/node/virtual machine and
    execution time of each processes. From this data, we can see which is bottle neck and how can
    we improve performance of automation test system.
    """


def parse_arguments():
    # Parsing arguments
    parser = argparse.ArgumentParser(MANUAL)
    parser.add_argument("-l", "--log-folder", required=True,
                        help="Log folder which is generate from automation test system after run "
                             "nodes_manager.py scripts")
    parser.add_argument('-o', '--output-folder',
                        default="system_performance_reports",
                        help='All reports for automation test system will be generated in this '
                             'directory')
    return parser


def main():
    # Parse arguments for run scripts
    parser = parse_arguments()
    args = parser.parse_args()

    # Check if log folder exists or not
    if not os.path.isdir(args.log_folder):
        print("No such directory: {path}".format(path=args.log_folder))
        sys.exit(1)

    # Prepare output folder to storage reports
    output_folder = args.output_folder
    if os.path.exists(output_folder):
        remove_paths(output_folder)
    make_dir(output_folder)

    # Initial reports generator
    reports_generator = SystemPerformanceReportsGenerator(log_folder=args.log_folder,
                                                          output_folder=output_folder)
    # Generate reports
    reports_generator.generate_reports()


if __name__ == "__main__":
    main()
