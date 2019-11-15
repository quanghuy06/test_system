import argparse
import sys_path
sys_path.insert_sys_path()
from report.lib_delta_report.phocr_delta_memcheck_reporter import PHOcrDeltaMemoryLeakReporter


def parse_argument():
    parser = argparse.ArgumentParser(description='Run test to checking memory for all nominated '
                                                 'test case.')
    parser.add_argument('-t', '--test-folder', required=True,
                        help='folder contain test set')
    parser.add_argument('-r', '--test-file', required=True,
                        help="Test result file which is generated from run_all.py")
    parser.add_argument('-c', '--compare-file', required=True,
                        help="Compare result file which is generated from compare_all.py")

    return parser.parse_args()


def main():
    args = parse_argument()

    memory_leak_reporter = PHOcrDeltaMemoryLeakReporter(test_folder=args.test_folder,
                                                        test_file=args.test_file,
                                                        compare_file=args.compare_file)
    memory_leak_reporter.do_work()


if __name__ == '__main__':
    main()
