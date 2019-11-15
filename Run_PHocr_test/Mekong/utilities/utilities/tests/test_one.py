# Toshiba - TSDV
# Team:         PHOcr
# Author:       Le Duc Nam
# Email:        nam.leduc@toshiba-tsdv.com
# Date created: 29/08/2016
# Last update:  19/07/2017
# Updated by:   Phung Dinh Tai
# Description:  This script is used for testing one test case in a test folder
import sys
import os
import shutil
import datetime
import argparse
import traceback
import sys_path
sys_path.insert_sys_path()
from baseapi.common import padding_time
from lib_runner.test_runner import TestRunner
from tests.lib_comparison.compare_runner import CompareRunner
from configs.compare_result import CompareJsonKeys, CompareResultConfig
from configs.test_result import TestResultConfig, FinalTestResult
from handlers.test_result_handler import TestResultHandler
from handlers.compare_handlers.compare_result_handler import CompareResultHandler
from baseapi.file_access import write_json, move_paths, remove_paths
from report.lib_summary_report.overall_information_reporter import OverallInformationReporter
from report.lib_summary_report.bounding_box_accuracy_reporter import BbAccuracyReporter
from report.lib_summary_report.text_accuracy_reporter import TextAccuracyReporter
from report.lib_summary_report.barcode_accuracy_reporter import BarcodeAccuracyReporter
from baseapi.linux_file_access import linux_tar_file_tgz
from configs.database import TestcaseConfig
from handlers.test_spec_handler import TestSpecHandler
from configs.projects.phocr import PhocrProject


def parse_argument():
    parser = argparse.ArgumentParser(description='Run and compare one test case')
    parser.add_argument('-t', '--test_folder',
                        help='Folder contain test set',
                        required=True)
    parser.add_argument('-b', '--bin_folder',
                        help='Folder contain executable',
                        required=True)
    parser.add_argument('-id', '--test_id', required=True,
                        help='Test case id')
    parser.add_argument('-o', '--output',
                        help='Test output file to export in json formats')
    parser.add_argument('-p', '--platform',
                        help='platform want to compare')

    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_argument()

    platform = args.platform

    # Create a result folder
    if not args.output:
        now = datetime.datetime.now()
        time_stamp = str(now.year) + padding_time(str(now.month)) + padding_time(str(now.day)) + \
            padding_time(str(now.hour)) + padding_time(str(now.minute))
        result_folder = TestResultConfig.PREFIX + "_" + str(time_stamp)
    else:
        result_folder = args.output.split(".")[0]
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    else:
        shutil.rmtree(result_folder)
        os.makedirs(result_folder)

    # Get binary folder
    bin_folders = list()
    if not os.path.isdir(args.bin_folder):
        print ("Has no directory {bin_folder}".format(bin_folder=args.bin_folder))
        sys.exit(1)
    else:
        bin_folders.append(os.path.abspath(args.bin_folder))

    runner = TestRunner()

    comparator = CompareRunner()

    run_info_list = {}
    compare_info_list = {}
    total_errors_change_with_master = 0
    total_errors_change_with_ground_truth = 0
    total_errors_master_with_ground_truth = 0
    print('[' + str(1) + '/' + str(1) + '] Test with test case "' + str(args.test_id) + '"')
    try:
        # Run test cases
        run_info = runner.run(test_folder=args.test_folder, abs_bin_folders=bin_folders,
                              test_id=args.test_id, plf=platform)

        # Compare test cases and out put to json data
        compare_info = comparator.run(args.test_folder, args.test_id, platform)

        if CompareJsonKeys.DIFF in compare_info.keys():
            info = compare_info[CompareJsonKeys.DIFF][CompareJsonKeys.INFO]
            if len(info) > 0:
                for item in info:
                    total_errors_change_with_master += item[CompareJsonKeys.TOTAL_ERROR]
        if CompareJsonKeys.ORIGIN in compare_info.keys():
            info = compare_info[CompareJsonKeys.ORIGIN][CompareJsonKeys.INFO]
            if len(info) > 0:
                for item in info:
                    total_errors_master_with_ground_truth += item[CompareJsonKeys.TOTAL_ERROR]
        if CompareJsonKeys.CHANGE in compare_info.keys():
            info = compare_info[CompareJsonKeys.CHANGE][CompareJsonKeys.INFO]
            if len(info) > 0:
                for item in info:
                    total_errors_change_with_ground_truth += item[CompareJsonKeys.TOTAL_ERROR]

        run_info_list[args.test_id] = run_info
        compare_info_list[args.test_id] = compare_info
    except:
        print('-' * 60)
        traceback.print_exc(file=sys.stdout)
        print('-' * 60)

    # Create handler for run and compare information
    # Test result handler
    test_result_handler = TestResultHandler(None, test_folder=args.test_folder)
    test_result_handler.data = run_info_list
    # Compare result handler
    cmp_result_handler = CompareResultHandler()
    cmp_result_handler.data = compare_info_list

    # Export test result to file
    test_file = os.path.join(result_folder, TestResultConfig.FILE_DEFAULT)
    write_json(run_info_list, test_file)

    # Export compare result to file
    cmp_file = os.path.join(result_folder, CompareResultConfig.FILE_DEFAULT)
    write_json(compare_info_list, cmp_file)

    # Collect compare result of changed test cases
    # Create target folder
    target_folder = os.path.join(result_folder, FinalTestResult.CHANGE)
    if os.path.isdir(target_folder):
        remove_paths(target_folder)
    os.makedirs(target_folder)
    src_folder = os.path.join(CompareResultConfig.FOLDER_DEFAULT, args.test_id)
    move_paths(src_folder, target_folder)
    # Clean compare result folder
    remove_paths(CompareResultConfig.FOLDER_DEFAULT)

    print ("\nMake reports")
    reporters = list()
    # Export overall information
    reporters.append(OverallInformationReporter(test_file=test_file, compare_file=cmp_file,
                                                test_folder=args.test_folder, error_folder=None,
                                                platform=args.platform))

    spec_file = os.path.join(args.test_folder, args.test_id, TestcaseConfig.SPEC_FILE)
    spec_handler = TestSpecHandler(input_file=spec_file)
    # Export bounding box accuracy report
    is_bb_accuracy = PhocrProject.functionalities.TEXT_LAYOUT in spec_handler.get_functions()
    if is_bb_accuracy:
        reporters.append(BbAccuracyReporter(test_file=test_file, compare_file=cmp_file,
                                            test_folder=args.test_folder))

    # Export text accuracy report
    is_text_accuracy = PhocrProject.functionalities.EXPORT_TXT in spec_handler.get_functions()
    if is_text_accuracy:
        reporters.append(TextAccuracyReporter(test_file=test_file, compare_file=cmp_file,
                                              test_folder=args.test_folder))

    # Export barcode accuracy report
    is_barcode_test = spec_handler.get_component() == PhocrProject.components.BARCODE
    if is_barcode_test:
        reporters.append(BarcodeAccuracyReporter(test_file=test_file, compare_file=cmp_file,
                                                 test_folder=args.test_folder))

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
    print ("*** TEST COMPLETED! ***")

###############################################################################
# Check name of module
if __name__ == "__main__":
    main()
