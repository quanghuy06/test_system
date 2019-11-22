import os
import sys
import shutil
import argparse
from datetime import datetime

import sys_path
sys_path.insert_sys_path()
from performance_for_it.lib_performance_for_it.base_test_cases import BaseTestCases
from performance_for_it.lib_performance_for_it.performance_runner import PerformanceRunner
from handlers.build_manager_handler import BuildManagerHandler
from handlers.previous_build_handler import PreviousBuildHandler
from handlers.current_build_handler import CurrentBuildHandler
from performance_for_it.lib_performance_for_it.performance_report_finder import PerformanceReportFinder
from report.lib_it_perf_report.performance_reporter import PerformanceReport
from performance_for_it.lib_performance_for_it.svn_report_uploader import SvnReportUploader


def main():
    parser = argparse.ArgumentParser(description='Performance testing on board')

    parser.add_argument(
        '-b',
        '--base-test-cases',
        required=True,
        help='Setting path to test cases file'
    )

    parser.add_argument(
        '-c',
        '--config-path',
        required=True,
        help='Setting path to config path folder'
    )

    args = parser.parse_args()
    config_path = args.config_path

    # To load current build package into current_built folder
    current_built = CurrentBuildHandler(input_file=config_path)
    if os.path.isdir("current_built"):
        shutil.rmtree("current_built")
    current_built_package = current_built.load_build_package("current_built")

    # To get pattern gerrit path to make gerrit path string for get trainning data.
    current_built_gerrit_path = current_built.get_gerrit_path("current_built")

    # To load previous build package into previous_built folder
    previous_built = PreviousBuildHandler(input_file=config_path)
    if os.path.isdir("previous_built"):
        shutil.rmtree("previous_built")

    # To get pattern gerrit path to make gerrit path string for get trainning data.
    previous_built_package = previous_built.load_built_package("previous_built")

    previous_built_gerrit_path = previous_built.get_gerrit_path("previous_built")

    build_handler = BuildManagerHandler(input_file=config_path)

    base_test_cases = BaseTestCases.get_from_svn(args.base_test_cases)

    # To run performance testing for current change
    performance_runner = PerformanceRunner(
        build_handler,
        current_built_package,
        current_built_gerrit_path,
        base_test_cases
    )
    current_perf_data = performance_runner.run_distribute("it_perf_test_result")

    # To run performance testing for previous change
    performance_runner = PerformanceRunner(
        build_handler,
        previous_built_package,
        previous_built_gerrit_path,
        base_test_cases
    )
    previous_perf_data = performance_runner.run_distribute("it_perf_test_result")

    # Find delta of current change
    current_parameter = current_built.get_parameter_handler("current_built")
    current_change = current_parameter.get_change_number()
    current_delta = int(current_parameter.get_delta_version())

    # Find previous report of current change
    report_finder = PerformanceReportFinder(build_handler)
    perf_report = report_finder.find(current_delta)
    assert perf_report is not None, "Not found previous performance report"

    # Create report performance.
    performance_report = PerformanceReport(
        perf_report,
        previous_perf_data,
        current_perf_data,
        current_change,
        current_delta
    )
    report = performance_report.write_report()
    perf_report_link = build_handler.get_perf_report_link()

    # Upload svn
    uploader = SvnReportUploader(current_change, current_delta, perf_report_link, report)
    upload_exit = uploader.upload()
    if upload_exit is not None:
        sys.exit(1)
    # To groovy reader and notice to gerrit.
    uploader.write_report_url()


if __name__ == "__main__":
    start = datetime.now()
    main()
    end = datetime.now()
    test_time = end - start
    print("Total performance running time : {}".format(test_time))

