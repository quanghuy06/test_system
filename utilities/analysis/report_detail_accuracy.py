# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      17/05/2017
# Last update:      17/05/2107
# Description:      Compare bounding box file and report to xls file

import report.sys_path
report.sys_path.insert_sys_path()

import argparse
import os
from analysis.detail_report import DetailInformationReporter, BookInfo

def print_help():
    help = """
Usage:  -f <test_folder> [--change --diff --origin] [-o OUTFILE]
        -s <source_folder> -d <destination_folder> [-o OUTFILE]

Note:
    --change    Compare your change with reference data
    --diff      Compare your change with ground truth data
    --origin    Compare reference data with ground truth data
    [DEFAULT] --change

- File in source folder and destination folder need to be same name
- Currently, only support compare bounding box (text layout)
- File name should be suffixed by _0.txt
- Output file should in xls format
"""
    print help

def main():
    # Parse options
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--test-folder",
                        help = "Test folder after testing by using run_all.py or test_all.py")
    parser.add_argument("-s", "--source-folder",
                        help = "Folder contains all source files")
    parser.add_argument("-d", "--dest-folder",
                        help = "Folder contains all destination files")
    parser.add_argument("-o", "--output-file", default = None,
                        help = "Name of output xls file should be exported")
    parser.add_argument("--change", default = False, action = "store_true",
                        help = "Compare your change with reference data")
    parser.add_argument("--diff", default=False, action="store_true",
                        help="Compare your change with ground truth data")
    parser.add_argument("--origin", default=False, action="store_true",
                        help="Compare reference data with ground truth data")
    args = parser.parse_args()

    if args.source_folder and args.dest_folder:
        print "Processing..."
        diff_reporter = DetailInformationReporter(args.source_folder, args.dest_folder)
        diff_reporter.Report(args.output_file)
        print "-- Done --"
        return

    if args.test_folder:
        print "Processing..."
        file_list = []
        # Compare change with ground truth data
        if args.diff:
            # Collect file list
            for test_name in os.listdir(args.test_folder):
                test_path = os.path.join(args.test_folder, test_name)
                out_folder = os.path.join(test_path, "output", "linux")
                if not os.path.isdir(out_folder):
                    print "Test case {0}: No output folder found".format(test_name)
                    continue
                ground_folder = os.path.join(test_path, "ground_truth_data", "linux")
                if not os.path.isdir(ground_folder):
                    print "Test case {0}: No ground truth folder found".format(test_name)
                    continue
                for fname in os.listdir(out_folder):
                    out_file = os.path.join(out_folder, fname)
                    if os.path.isfile(out_file) and fname.endswith(BookInfo.LAYOUT_SUFFIX):
                        ground_file = os.path.join(ground_folder, fname)
                        if not os.path.isfile(ground_file):
                            print "Test case {0}: No such file {1}".format(test_name, ground_file)
                        else:
                            file_list.append([out_file, ground_file])
            diff_reporter = DetailInformationReporter()
            diff_reporter.SetFileList(file_list)
            diff_reporter.Report(args.output_file)
            print "-- Done --"
            return

        # Compare reference data with ground truth data
        if args.origin and (not file_list):
            # Collect file list
            for test_name in os.listdir(args.test_folder):
                test_path = os.path.join(args.test_folder, test_name)
                ref_folder = os.path.join(test_path, "ref_data", "linux")
                if not os.path.isdir(ref_folder):
                    print "Test case {0}: No reference data folder found".format(test_name)
                    continue
                ground_folder = os.path.join(test_path, "ground_truth_data", "linux")
                if not os.path.isdir(ground_folder):
                    print "Test case {0}: No ground truth folder found".format(test_name)
                    continue
                for fname in os.listdir(ref_folder):
                    ref_file = os.path.join(ref_folder, fname)
                    if os.path.isfile(ref_file) and fname.endswith(BookInfo.LAYOUT_SUFFIX):
                        ground_file = os.path.join(ground_folder, fname)
                        if not os.path.isfile(ground_file):
                            print "Test case {0}: No such file {1}".format(test_name, ground_file)
                        else:
                            file_list.append([ref_file, ground_file])
            diff_reporter = DetailInformationReporter()
            diff_reporter.SetFileList(file_list)
            diff_reporter.Report(args.output_file)
            print "-- Done --"
            return

        # Default is compare change with reference data
        # Collect file list
        for test_name in os.listdir(args.test_folder):
            test_path = os.path.join(args.test_folder, test_name)
            out_folder = os.path.join(test_path, "output", "linux")
            if not os.path.isdir(out_folder):
                print "Test case {0}: No output folder found".format(test_name)
                continue
            ref_folder = os.path.join(test_path, "ref_data", "linux")
            if not os.path.isdir(ref_folder):
                print "Test case {0}: No reference data folder found".format(test_name)
                continue
            for fname in os.listdir(out_folder):
                out_file = os.path.join(out_folder, fname)
                if os.path.isfile(out_file) and fname.endswith(BookInfo.LAYOUT_SUFFIX):
                    ref_file = os.path.join(ref_folder, fname)
                    if not os.path.isfile(ref_file):
                        print "Test case {0}: No such file {1}".format(test_name, ref_file)
                    else:
                        file_list.append([out_file, ref_file])
            diff_reporter = DetailInformationReporter()
            diff_reporter.SetFileList(file_list)
            diff_reporter.Report(args.output_file)
            print "-- Done --"
            return

    print_help()

    # word_count_info = {}
    # character_count_info = {}
    # word_classify_error_frequency = {}
    # character_classify_error_frequency = {}
    # character_frequency = {}
    # word_frequency = {}
    # character_replace_error_frequency = {}
    # word_replace_error_frequency = {}
    # replace_error_detail_frequency = {}
    # replace_classify_error_detail_frequency = {}
    # if args.folder:
    #     ocr_result_folder = os.path.join(args.folder, "BBox-result")
    #     ground_truth_folder = os.path.join(args.folder, "Ground-withoutimage")
    #     compare_folder = os.path.join(args.folder, "Ground-withoutimage-html")
    #     for filename in os.listdir(ocr_result_folder):
    #         if filename.endswith(".txt"):
    #             fbname = filename[:-4]
    #             test_name = fbname[:-2]
    #             print test_name
    #             ocr_result_file = os.path.join(ocr_result_folder, filename)
    #             ground_truth_file = os.path.join(ground_truth_folder, filename)
    #             html_file = os.path.join(compare_folder, "{0}.html".format(fbname))
    #             compare_result = parse_compare_html(html_file)
    #             counter_word = Counter("word", compare_result)
    #             word_count_info = counter_word.CountError(ocr_result_file, ground_truth_file, word_count_info)
    #             word_classify_error_frequency = count_classify_error_frequency("word", counter_word.data, word_classify_error_frequency)
    #             word_frequency = count_word_frequency(ground_truth_file, word_frequency)
    #             counter_character = Counter("character", compare_result)
    #             character_count_info = counter_character.CountError(ocr_result_file, ground_truth_file, character_count_info)
    #             character_classify_error_frequency = count_classify_error_frequency("character", counter_character.data, character_classify_error_frequency)
    #             character_frequency = count_character_frequency(ground_truth_file, character_frequency)
    #             word_replace_error_frequency = count_replace_error_frequency("word", counter_word.data, word_replace_error_frequency)
    #             character_replace_error_frequency = count_replace_error_frequency("character", counter_character.data, character_replace_error_frequency)
    #             replace_error_detail_frequency = get_replace_error_detail_frequency(counter_character.replace_list, replace_error_detail_frequency)
    #             replace_classify_error_detail_frequency = get_replace_error_detail_frequency(counter_character.replace_classify_list, replace_classify_error_detail_frequency)
    # else:
    #     compare_result = parse_compare_html(args.compare_result)
    #     counter_word = Counter("word", compare_result)
    #     word_count_info = counter_word.CountError(args.ocr_result, args.ground_truth)
    #     counter_character = Counter("character", compare_result)
    #     character_count_info = counter_character.CountError(args.ocr_result, args.ground_truth)
    #     word_classify_error_frequency = count_classify_error_frequency("word", counter_word.data, {})
    #     character_classify_error_frequency = count_classify_error_frequency("character", counter_character.data, {})
    #     word_replace_error_frequency = count_replace_error_frequency("word", counter_word.data, {})
    #     character_replace_error_frequency = count_replace_error_frequency("character", counter_character.data, {})
    #     word_frequency = count_word_frequency(args.ground_truth, {})
    #     character_frequency = count_character_frequency(args.ground_truth, {})
    #     replace_error_detail_frequency = get_replace_error_detail_frequency(counter_character.replace_list, {})
    #     replace_classify_error_detail_frequency = get_replace_error_detail_frequency(counter_character.replace_classify_list, {})
    # # Clean current csv file in current folder
    # remove_globs(["*.xlsx"])
    # # Export summary report
    # summary = get_summary_info(character_count_info, word_count_info)
    # export_summary_report(summary)
    # # Export accuracy vs frequency report
    # accuracy_by_character = get_accuracy_by_frequency(character_replace_error_frequency, character_frequency)
    # accuracy_by_word = get_accuracy_by_frequency(word_replace_error_frequency, word_frequency)
    # stop_word_info = get_stop_word_info(accuracy_by_word, word_frequency)
    # export_frequency_report(character_frequency, accuracy_by_character, word_frequency, accuracy_by_word, stop_word_info)
    # # Export replace error in detail
    # export_detail_error(replace_error_detail_frequency, replace_classify_error_detail_frequency)
    # # Export character accuracy by class
    # export_character_accuracy_by_class(character_frequency, accuracy_by_character)
    # # Move all reports to "AccuracyReport" folder
    # report_folder = "AccuracyReport"
    # if args.folder:
    #     base_name = os.path.basename(args.folder)
    #     report_folder += "_{0}".format(args.folder)
    # if os.path.isdir(report_folder):
    #     remove_paths(report_folder)
    # os.makedirs(report_folder)
    # move_globs("*.xlsx", report_folder)

if __name__ == "__main__":
    main()