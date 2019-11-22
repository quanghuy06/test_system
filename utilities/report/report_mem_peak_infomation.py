import argparse
import sys_path
sys_path.insert_sys_path()
from report.lib_delta_report.phocr_mem_peak_reporter import PHOcrMemoryPeakReporter


def parse_argument():
    parser = argparse.ArgumentParser(
        description='Run test to check memory peak for all nominated test case.')
    parser.add_argument('-t', '--test-folder', required=True,
                        help='Folder contain test set')
    parser.add_argument('-r', '--test-file', required=True,
                        help="Test result file which is generated from run_all.py")
    parser.add_argument('-c', '--combined-file', required=True,
                        help="Combine result file which is generated from "
                             "combine_all_mem_peak.py")

    return parser.parse_args()


def main():
    args = parse_argument()

    memory_peak_reporter = PHOcrMemoryPeakReporter(test_folder=args.test_folder,
                                                   test_file=args.test_file,
                                                   combine_file=args.combined_file)
    memory_peak_reporter.do_work()


if __name__ == '__main__':
    main()
