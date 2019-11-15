import argparse
import os

import sys_path

sys_path.insert_sys_path()
from baseapi.file_access import copy_paths, remove_paths, move_paths
from configs.database import TestcaseConfig, SpecKeys
from handlers.test_spec_handler import TestSpecHandler

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--test-folder')
    parser.add_argument('-o', '--output-folder', default="MEM_TESTS")
    args = parser.parse_args()

    if os.path.isdir(args.output_folder):
        remove_paths(args.output_folder)
    os.makedirs(args.output_folder)

    test_list = os.listdir(args.test_folder)
    total = len(test_list)
    count = 1

    for test_name in os.listdir(args.test_folder):
        print "[{0}/{1}] {2}".format(count, total, test_name)
        new_test_name = "Memcheck_" + test_name
        src_path = os.path.join(args.test_folder, test_name)
        dest_path = os.path.join(args.output_folder, new_test_name)
        # Copy test case to output folder with new name
        copy_paths(src_path, args.output_folder)
        move_paths(os.path.join(args.output_folder, test_name), dest_path)
        # Remove script folder to use automatic test script
        remove_paths(os.path.join(dest_path, TestcaseConfig.SCRIPT_DIR))
        # Update specification of test case
        spec_file = os.path.join(dest_path, TestcaseConfig.SPEC_FILE)
        spec_handler = TestSpecHandler(input_file=spec_file)
        spec_handler.update_tag(SpecKeys.Tags.ACCURACY, False)
        if spec_handler.has_tag(SpecKeys.Tags.IS_MEMCHECK):
            spec_handler.update_tag(SpecKeys.Tags.IS_MEMCHECK, True)
        else:
            spec_handler.add_tag(SpecKeys.Tags.IS_MEMCHECK, True)
        spec_handler.data[SpecKeys.ID] = new_test_name
        spec_handler.save()
        count += 1

if __name__ == "__main__":
    main()
