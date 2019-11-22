import re
import os
import sys
import fnmatch
import traceback
import argparse
import sys_path
sys_path.insert_sys_path()

from baseapi.file_access import write_data_to_json_file, remove_paths
from configs.test_result import TestResultConfig, MemPeakInfo
from handlers.test_result_handler import TestResultHandler
from configs.database import TestcaseConfig


class MemPeakCombination(object):
    def __init__(self, test_folder, platform, test_result, output_file=None):
        self.test_folder = test_folder
        self.platform = platform
        self.test_result = test_result
        if output_file:
            self.output_file = output_file
        else:
            self.output_file = TestResultConfig.MEM_PEAK_FILE

    def do_work(self):
        combine_results = self.combine_mem_peak_info()
        # Check and remove old file
        if os.path.isfile(self.output_file):
            remove_paths(self.output_file)
        write_data_to_json_file(combine_results, self.output_file)

    def get_mem_peak_info(self, output_path):
        """
        Parse memory peak information to get memory heap.
        Parameters
        ----------
        output_path: output folder of test case

        Returns
        -------
            tuple: memory peak information: mem_heap_B, mem_heap_extra_B

        """
        mem_heap_B = 0
        mem_heap_extra_B = 0

        for item in os.listdir(output_path):
            if fnmatch.fnmatch(item, 'massif.out.*'):
                mem_peak_file = os.path.join(output_path, item)
                with open(mem_peak_file, 'r') as data:
                    file_contents = data.read()
                    flags = re.M
                    re_compile = re.compile(MemPeakInfo.MEM_PEAK_PATTERN,
                                            flags)
                    search_result = re_compile.search(file_contents)

                    if search_result:
                        peak_info = search_result.group(0)
                        lines = re.split("\n", peak_info)
                        for line in lines:
                            if re.compile(MemPeakInfo.MEM_HEAP_B,
                                          flags).search(line):
                                mem_heap_B = line.split("=")[1]
                            if re.compile(MemPeakInfo.MEM_HEAP_EXTRA_B,
                                          flags).search(line):
                                mem_heap_extra_B = line.split("=")[1]
                return {
                    MemPeakInfo.MEM_HEAP_B: mem_heap_B,
                    MemPeakInfo.MEM_HEAP_EXTRA_B: mem_heap_extra_B
                }

    def combine_mem_peak_info(self):
        # Get test set
        test_result_handler = TestResultHandler(input_file=self.test_result,
                                                test_folder=self.test_folder)
        # Only combine test case which is not error
        # Inform error tests
        error_list = test_result_handler.get_list_error_tests()
        if error_list:
            msg = "INFORM: There are {0} error test cases that will not be " \
                  "combined: \n\t".format(len(error_list))
            for test_name in error_list:
                msg += test_name + ", "
            print msg[:-2] + "\n"

        # Get list of test cases that are not error. These also will be combined.
        test_set = sorted(test_result_handler.get_list_not_error_tests())

        # Check if test case directory exists
        not_founds = []
        real_test_set = []
        for test_id in test_set:
            test_path = os.path.join(self.test_folder, test_id)
            if not os.path.isdir(test_path):
                not_founds.append(test_id)
            else:
                real_test_set.append(test_id)
        # Notice test cases that can not found in test folder
        if not_founds:
            msg = "INFORM: Can not find {0} test cases in test folder {1}: \n\t".format(
                len(not_founds), self.test_folder)
            for test_id in not_founds:
                msg += test_id + ", "
            print msg[:-2] + "\n"

        print "\n>>> Start combine memory peak information."

        if real_test_set:
            results = {}
            for test_id in real_test_set:
                try:
                    output_path = os.path.join(self.test_folder,
                                               test_id,
                                               TestcaseConfig.OUTPUT_FOLDER,
                                               self.platform)
                    mem_peak_info = self.get_mem_peak_info(output_path)
                    results[test_id] = mem_peak_info
                except Exception as e:
                    print('-' * 60)
                    traceback.print_exc(file=sys.stdout)
                    print('-' * 60)
            print ">>> Combine memory peak information end!"
            return results
        else:
            print "All test cases are error!"


def parse_argument():
    parser = argparse.ArgumentParser(
        description='Combine all memory peak information.')
    parser.add_argument('-t', '--test_folder', required=True,
                        help='Folder contain test set')
    parser.add_argument('-r', '--result-json', required=True,
                        help='Path to test result json file')
    parser.add_argument('-o', '--output-file',
                        default=TestResultConfig.MEM_PEAK_FILE,
                        help='Combine output file to export in json format')
    parser.add_argument('-p', '--platform',
                        help='Platform want to combine')
    return parser.parse_args()


def main():
    # Parse arguments
    args = parse_argument()
    combine_executor = MemPeakCombination(args.test_folder,
                                          args.platform,
                                          args.result_json)
    combine_executor.do_work()


if __name__ == "__main__":
    main()

