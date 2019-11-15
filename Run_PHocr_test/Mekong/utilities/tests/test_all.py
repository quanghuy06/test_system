# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Le Duc Nam
# Email:            nam.leduc@toshiba-tsdv.com
# Date create:      20/11/2017
# Last update:      19/07/2017
# Editor:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Description:      Adhoc testing. Combine run all, compare all and report in only 1 script.
from multiprocessing import Process, Manager
import sys
import datetime
import traceback
import argparse
import os
import shutil
import csv
from operator import itemgetter

import sys_path
sys_path.insert_sys_path()
from baseapi.file_access import move_paths, write_json, remove_paths
from handlers.test_result_handler import TestResultHandler
from handlers.compare_handlers.compare_result_handler import CompareResultHandler
from report.lib_summary_report.overall_information_reporter import OverallInformationReporter
from configs.test_result import TestResultConfig, FinalTestResult
from configs.compare_result import CompareResultConfig
from baseapi.common import padding_time, get_unique_list
from report.lib_summary_report.text_accuracy_reporter import TextAccuracyReporter
from report.lib_summary_report.bounding_box_accuracy_reporter import BbAccuracyReporter
from report.lib_summary_report.barcode_accuracy_reporter import BarcodeAccuracyReporter
from report.lib_delta_report.phocr_delta_memcheck_reporter import PHOcrDeltaMemoryLeakReporter
from report.lib_delta_report.phocr_mem_peak_reporter import PHOcrMemoryPeakReporter
from baseapi.linux_file_access import linux_tar_file_tgz
from configs.database import TestcaseConfig, SpecKeys
from handlers.test_spec_handler import TestSpecHandler
from configs.projects.hanoi import HanoiProject
from configs.timeout import TimeOut
from tests.combine_all_mem_peak import MemPeakCombination
from report.lib_summary_report.memory_peak_reporter import MemPeakReporter, \
    MEM_PEAK_REPORT_DEFAULT_NAME

NUMBER_THREAD_GET_TEST_CASE = 3


def parse_argument():
    parser = argparse.ArgumentParser(
        description='Run and compare all test case on test folder')
    parser.add_argument('-t', '--test-folder',
                        help='folder contain test set',
                        required=True)
    parser.add_argument('-b', '--bin-folder',
                        help='folder contain executable',
                        required=True)
    parser.add_argument('-o', '--output',
                        help='Final package of test result. Should be .tgz '
                             'format and should not contain dot in string.')
    parser.add_argument('--report-bb-accuracy',
                        default=False,
                        action="store_true",
                        help="Export bounding box accuracy report for character and word")
    parser.add_argument('--report-text-accuracy',
                        default=False,
                        action="store_true",
                        help='Report text accuracy')
    parser.add_argument('--report-barcode',
                        default=False,
                        action="store_true",
                        help="Report barcode accuracy")
    parser.add_argument('--get-all-result',
                        default=False,
                        action='store_true',
                        help="Get all compare result.")
    parser.add_argument('--check-memory-leak',
                        default=False,
                        action="store_true",
                        help="Checking memory leak for all test case")
    parser.add_argument('--check-memory-peak',
                        default=False,
                        action="store_true",
                        help="Checking memory peak for all test case")
    parser.add_argument('-p', '--platform',
                        required=True,
                        help="platform need to test on: Windows, Linux")
    return parser.parse_args()


def run_tcs_parallel(test_folder, bin_folder,
                     test_id,
                     run_information,
                     compare_information,
                     tmp_cmp_result_folder,
                     platform):

    from lib_runner.test_runner import TestRunner
    runner = TestRunner()

    from tests.lib_comparison.compare_runner import CompareRunner
    comparator = CompareRunner()

    # Run test cases
    run_info = runner.run(test_folder=test_folder,
                          abs_bin_folders=bin_folder,
                          test_id=test_id,
                          plf=platform)

    compare_info = comparator.run(test_folder=test_folder,
                                  test_id=test_id,
                                  platform=platform,
                                  compare_folder=tmp_cmp_result_folder)

    run_information[test_id] = run_info
    compare_information[test_id] = compare_info


def main():
    # Parse arguments
    args = parse_argument()

    platform = args.platform
    bin_folders = args.bin_folder.split(",")
    abs_bin_folders = []
    for f in bin_folders:
        if os.path.isdir(f):
            abs_bin_folders.append(os.path.abspath(f))
        else:
            print("Folder {0} does not exist!".format(f))
            sys.exit(1)
    # Create a result folder
    if not args.output:
        now = datetime.datetime.now()
        time_stamp = str(now.year) \
                     + padding_time(str(now.month)) \
                     + padding_time(str(now.day)) \
                     + padding_time(str(now.hour))\
                     + padding_time(str(now.minute))
        result_folder = TestResultConfig.PREFIX + "_" + str(time_stamp)
    else:
        result_folder = args.output.split(".")[0]
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    else:
        shutil.rmtree(result_folder)
        os.makedirs(result_folder)

    # Get test set
    test_set = sorted(os.listdir(args.test_folder))

    # Compare test cases and out put to json data
    tmp_cmp_result_folder = "e7968b1d-19c6-43e4-ed07-d12h32k21e_tmp_cmp_result"
    if os.path.isdir(tmp_cmp_result_folder):
        remove_paths(tmp_cmp_result_folder)
    os.makedirs(tmp_cmp_result_folder)

    manager = Manager()
    run_information_md = manager.dict()
    compare_information_md = manager.dict()
    count = 1
    total = len(test_set)

    while len(test_set) > 0:
        # Check if checking for memory leak:
        if args.check_memory_leak:
            for test_id in os.listdir(args.test_folder):
                spec_file = os.path.join(args.test_folder,
                                         test_id,
                                         TestcaseConfig.SPEC_FILE)
                spec_handler = TestSpecHandler(input_file=spec_file)
                if spec_handler.get_component() != HanoiProject.components.DEFAULT:
                    spec_handler.update_tag(SpecKeys.Tags.IS_MEMCHECK, True)
                    spec_handler.save(spec_file)
                    spec_handler.update_execute_time_for_test_case(
                        platform,
                        TimeOut.execute.RATIO_TIMEOUT_RUN_MEMORY_LEAK)

        if args.check_memory_peak:
            for test_id in os.listdir(args.test_folder):
                spec_file = os.path.join(args.test_folder,
                                         test_id,
                                         TestcaseConfig.SPEC_FILE)
                spec_handler = TestSpecHandler(input_file=spec_file)
                if spec_handler.get_component() != HanoiProject.components.DEFAULT:
                    spec_handler.add_tag(SpecKeys.Tags.IS_MEMCHECK_PEAK, True)
                    spec_handler.save(spec_file)
                    spec_handler.update_execute_time_for_test_case(
                        platform,
                        TimeOut.execute.RATIO_TIMEOUT_RUN_MEMORY_LEAK)
        processes = []
        for index in range(0, NUMBER_THREAD_GET_TEST_CASE):
            if not test_set:
                break
            test_id = test_set.pop()

            print('[{0}/{1}] Test with test case {2}'
                  .format(count, total, str(test_id)))
            count += 1
            try:
                process = Process(target=run_tcs_parallel,
                                  args=(args.test_folder,
                                        abs_bin_folders,
                                        test_id,
                                        run_information_md,
                                        compare_information_md,
                                        tmp_cmp_result_folder,
                                        platform))
                processes.append(process)
                process.start()
            except SystemExit:
                exit(1)
            except:
                print('-'*60)
                traceback.print_exc(file=sys.stdout)
                print('-'*60)

        for p_index in range(0, len(processes)):
            processes[p_index].join()

    run_information = {}
    compare_information = {}

    # Transfer from manager dictionary to natural dictionary
    for key in run_information_md.keys():
        run_information[key] = run_information_md[key]

    for key in compare_information_md.keys():
        compare_information[key] = compare_information_md[key]

    # Export test result to file
    test_file = os.path.join(result_folder, TestResultConfig.FILE_DEFAULT)
    write_json(run_information, test_file)

    # Create memory peak report (xlsx file)
    memory_peak_file = os.path.join(result_folder,
                                    MEM_PEAK_REPORT_DEFAULT_NAME.format(suffix=""))

    # Initial reporter
    mem_peak_reporter = MemPeakReporter(test_file=test_file,
                                        test_folder=args.test_folder,
                                        output_file=memory_peak_file,
                                        platform=platform)
    # Make report
    mem_peak_reporter.do_work()

    # Create handler for run and compare information
    # Test result handler
    test_result_handler = TestResultHandler(input_file=test_file,
                                            test_folder=args.test_folder)
    test_result_handler.data = run_information

    # Export compare result to file
    cmp_file = os.path.join(result_folder, CompareResultConfig.FILE_DEFAULT)
    write_json(compare_information, cmp_file)

    # Create target folder
    target_folder = os.path.join(result_folder, FinalTestResult.CHANGE)
    if os.path.isdir(target_folder):
        remove_paths(target_folder)
    os.makedirs(target_folder)

    # Only copy changes test cases compare result
    compare_result_handler = CompareResultHandler(input_file=cmp_file,
                                                  test_folder=args.test_folder)
    compare_result_handler.data = compare_information

    # Get list of error tests
    error_list = test_result_handler.get_list_error_tests()
    err_output = test_result_handler.get_list_output_0B(None, platform)
    miss_output = test_result_handler.get_list_test_cases_missing_output(None, platform)

    if err_output:
        error_list = error_list + err_output
    if miss_output:
        error_list = error_list + miss_output
    failed_list = compare_result_handler.get_list_failed_tests()
    if failed_list:
        error_list = error_list + failed_list
    error_list = get_unique_list(error_list)
    # Copy changed tests
    test_list = compare_result_handler.get_list_changed_tests()
    for test_id in test_list:
        if test_id not in error_list:
            src_folder = os.path.join(tmp_cmp_result_folder, test_id)
            move_paths(src_folder, target_folder)

    if args.get_all_result:
        # Get not changed test cases result
        target_folder = os.path.join(result_folder, FinalTestResult.NOTCHANGE)
        if os.path.isdir(target_folder):
            remove_paths(target_folder)
        os.makedirs(target_folder)
        test_list = compare_result_handler.get_list_not_changed_tests()
        for test_id in test_list:
            if test_id not in error_list:
                src_folder = os.path.join(tmp_cmp_result_folder, test_id)
                move_paths(src_folder, target_folder)
        # Get error test cases result
        target_folder = os.path.join(result_folder, FinalTestResult.ERROR)
        if os.path.isdir(target_folder):
            remove_paths(target_folder)
        os.makedirs(target_folder)
        for test_id in error_list:
            src_folder = os.path.join(tmp_cmp_result_folder, test_id)
            move_paths(src_folder, target_folder)

    if args.check_memory_peak:
        # Export memory peak information:
        mem_peak_file = os.path.join(result_folder,
                                     TestResultConfig.MEM_PEAK_FILE)
        mem_peak_combination = MemPeakCombination(args.test_folder,
                                                  args.platform,
                                                  test_file,
                                                  mem_peak_file)
        mem_peak_combination.do_work()

    # Clean compare result folder
    remove_paths(tmp_cmp_result_folder)

    ########################################################################
    #                           REPORT

    print "\nMake reports"
    reporters = list()
    # Export overall information
    reporters.append(
        OverallInformationReporter(test_file=test_file,
                                   compare_file=cmp_file,
                                   test_folder=args.test_folder,
                                   error_folder=None,
                                   platform=args.platform))

    # Export bounding box accuracy report
    if args.report_bb_accuracy:
        reporters.append(
            BbAccuracyReporter(test_file=test_file,
                               compare_file=cmp_file,
                               test_folder=args.test_folder))

    # Export text accuracy report
    if args.report_text_accuracy:
        reporters.append(
            TextAccuracyReporter(test_file=test_file,
                                 compare_file=cmp_file,
                                 test_folder=args.test_folder))

    # Export barcode accuracy report
    if args.report_barcode:
        reporters.append(
            BarcodeAccuracyReporter(test_file=test_file,
                                    compare_file=cmp_file,
                                    test_folder=args.test_folder))
    if args.check_memory_leak:
        reporters.append(
            PHOcrDeltaMemoryLeakReporter(test_folder=args.test_folder,
                                         test_file=test_file,
                                         compare_file=cmp_file))

    if args.check_memory_peak:
        mem_peak_file = os.path.join(result_folder,
                                     TestResultConfig.MEM_PEAK_FILE)
        reporters.append(PHOcrMemoryPeakReporter(test_folder=args.test_folder,
                                                 test_file=test_file,
                                                 combine_file=mem_peak_file))

    # Do reports
    for reporter in reporters:
        try:
            reporter.do_work()
            move_paths(reporter.output_file, result_folder)
        except:
            traceback.print_exc()

    # Packaging result folder
    if args.output:
        final_package = args.output
    else:
        final_package = result_folder + ".tgz"
    linux_tar_file_tgz(src_folder=result_folder, des_file=final_package)

    # Remove result folder after compressing
    if os.path.exists(result_folder):
        shutil.rmtree(result_folder)

    # Testing finished!
    print "*** TEST COMPLETED! ***"

###############################################################################


# Check name of module
if __name__ == "__main__":
    main()
