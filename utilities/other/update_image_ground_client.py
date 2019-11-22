import sys_path
sys_path.insert_sys_path()

import argparse
import os
import sys
from baseapi.file_access import copy_paths, remove_paths
from configs.database import TestcaseConfig

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test-folder', required=True,
                        help="Path to test folder")
    parser.add_argument('-i', '--image-folder',
                        help='Path to image folder - this script only support for .jpg images! ')
    parser.add_argument('-g', '--ground-folder',
                        help='Path to ground truth folder')
    return parser

def main():
    parser = parse_argument()
    args = parser.parse_args()
    if not os.path.isdir(args.test_folder):
        print "No such file or directory {0}".format(args.test_folder)
        sys.exit(1)
    print "Please wait..."

    if not (args.image_folder or args.ground_folder):
        print "Choose image or ground truth folder to update!!!"
        sys.exit(1)
    else:
        # Replace image
        if args.image_folder:
            if not os.path.isdir(args.image_folder):
                print "No such file or directory {0}".format(args.image_folder)
            else:
                for test_name in os.listdir(args.test_folder):
                    image_name = test_name + ".jpg"
                    image_path = os.path.join(args.image_folder, image_name)
                    test_data = os.path.join(args.test_folder, test_name,
                                             TestcaseConfig.TEST_DATA_DIR,
                                             image_name)
                    if os.path.exists(image_path):
                        remove_paths(test_data)
                        copy_paths(image_path, test_data)
                print "\nImage are updated!"

        # Replace ground truth
        if args.ground_folder:
            if not os.path.isdir(args.ground_folder):
                print "No such file or directory {0}".format(args.ground_folder)
            else:
                for file in os.listdir(args.test_folder):
                    gt_text_name = file + ".jpg.txt"
                    gt_bb_name = file + ".jpg_0.txt"
                    gt_text_file_path = os.path.abspath(os.path.join(args.ground_folder, gt_text_name))
                    gt_bb_file_path = os.path.abspath(os.path.join(args.ground_folder, gt_bb_name))
                    gt_text_file = os.path.abspath(os.path.join(args.test_folder, file,
                                                                TestcaseConfig.GROUND_TRUTH_DATA_DIR,
                                                                "linux", gt_text_name))
                    gt_bb_file = os.path.abspath(os.path.join(args.test_folder, file,
                                                              TestcaseConfig.GROUND_TRUTH_DATA_DIR,
                                                              "linux", gt_bb_name))
                    if os.path.isfile(gt_text_file_path):
                        if os.path.exists(gt_text_file):
                            remove_paths(gt_text_file)
                        copy_paths(gt_text_file_path, gt_text_file)
                    if os.path.isfile(gt_bb_file_path):
                        if os.path.exists(gt_bb_file):
                            remove_paths(gt_bb_file)
                        copy_paths(gt_bb_file_path, gt_bb_file)

                print "\nGround truth are updated!"
        print "\n-----Done!------"

if __name__ == "__main__":
    main()