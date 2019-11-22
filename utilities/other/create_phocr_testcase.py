# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      18/07/2017
# Last update:      30/07/2018
# Editor:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Description:      Create PHOcr's test cases
import argparse
import os
import sys
import fnmatch
import sys_path
sys_path.insert_sys_path()

from configs.database import SpecKeys, TestcaseConfig, SpecChecking, SpecCheckKey,\
    FilterInterfaceConfig
from configs.projects.phocr import PhocrProject
from baseapi.file_access import copy_paths, write_json, move_paths
from other.lib_base.specification_exporter import SpecDbExporter
from configs.common import Platform
from other.lib_base.tags_file_parser import TagsTsvParser
from handlers.test_spec_handler import TestSpecHandler

IMAGE_EXTENTIONS = [".tif", ".tiff", ".png", ".jpg", ".bmp"]
SPEC_FILE_DEFAULT = "specification.tsv"
OUTPUT_FOLDER_DEFAULT = "NEW_TESTS"
GT_BB_EXT = ".jpg_0.txt"
GT_TEXT_EXT = ".txt"
GT_TEXT_EXT2 = ".jpg.txt"

# Get tag's value
def get_tag_value(value_str, value_type):
    if value_type == FilterInterfaceConfig.TYPE_BOOL:
        if value_str.lower() == "x":
            return True
        else:
            return False
    if value_type == FilterInterfaceConfig.TYPE_INT:
        try:
            return int(value_str)
        except:
            return 0
    if value_type == FilterInterfaceConfig.TYPE_LIST:
        text_split = value_str.split("|")
        values = list()
        # Prevent append empty string to the list
        for elm in text_split:
            if elm:
                values.append(elm)
        return values
    if value_type == FilterInterfaceConfig.TYPE_FLOAT:
        try:
            return float(value_str)
        except:
            return 0
    if value_type == FilterInterfaceConfig.TYPE_STR:
        return value_str
    return value_str


# Get tag's default value
def get_tag_default_value(tag_type):
    if tag_type == FilterInterfaceConfig.TYPE_BOOL:
        return False
    if tag_type == FilterInterfaceConfig.TYPE_FLOAT \
            or tag_type == FilterInterfaceConfig.TYPE_INT:
        return 0
    if tag_type == FilterInterfaceConfig.TYPE_STR:
        return ""
    if tag_type == FilterInterfaceConfig.TYPE_LIST:
        return []
    return None


# Create default tag
def create_default_tags():
    default_tags = {}
    for value in SpecKeys.Tags.__dict__.itervalues():
        if value and type(value) == str and not "." in value:
            tag_name = value
            tag_type = SpecChecking[SpecKeys.TAGS][tag_name][SpecCheckKey.TYPE]
            default_tags[tag_name] = get_tag_default_value(tag_type)
    default_tags[SpecKeys.Tags.PLATFORMS] = [Platform.LINUX, Platform.WINDOWS]
    return default_tags


# Default specification's content
DEFAULT_SPEC = {
    SpecKeys.PRODUCT: PhocrProject.PRODUCT,
    SpecKeys.COMPONENT: PhocrProject.components.DEFAULT,
    SpecKeys.BINARY_TEST_INFORMATION: {},
    SpecKeys.ENABLE: True,
    SpecKeys.ERROR_FLAGS: {
        Platform.LINUX: False,
        Platform.WINDOWS: False
    },
    SpecKeys.CHANGED_LOG : [],
    SpecKeys.FUNCTIONALITIES: [],
    SpecKeys.HISTORY_DATA: {
        Platform.LINUX: {
            SpecKeys.History.ABBYY: {},
            SpecKeys.History.ESDK: {},
            SpecKeys.History.PHOCR_ON_BOARD: {},
            SpecKeys.History.PHOCR_TEST_MACHINE: {},
            SpecKeys.History.TESSERACT: {}
        },
        Platform.WINDOWS: {
            SpecKeys.History.ABBYY: {},
            SpecKeys.History.ESDK: {},
            SpecKeys.History.PHOCR_ON_BOARD: {},
            SpecKeys.History.PHOCR_TEST_MACHINE: {},
            SpecKeys.History.TESSERACT: {}
        }
    },
    SpecKeys.TAGS: create_default_tags(),
    SpecKeys.WEIGHT: 3,
    SpecKeys.WEIGHTS: {
        Platform.LINUX: 3,
        Platform.WINDOWS: 3
    }
}


# Get test name
def get_test_name(image_name, prefix, suffix, order, is_include_test_name):
    # Get base name of image
    testname = ""
    name_split = os.path.splitext(image_name)
    if is_include_test_name:
        testname = name_split[0]
    # Add order
    if order:
        testname = str(order) + "_" + testname
    # Add prefix
    if prefix:
        testname = prefix + testname
    # Add suffix
    if suffix:
        testname = testname + suffix
    return name_split[0].strip(), name_split[1].strip(), testname.strip()


# Parser argument
def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image-folder",
                        help="Folder contains images")
    parser.add_argument('-g', '--ground-truth-folder',
                        help="Folder contain ground truth files. Ground truth file should"
                             "include name of image")
    parser.add_argument('-p', '--prefix',
                        help='Prefix of test name')
    parser.add_argument('-s', '--suffix',
                        help='Suffix of test name')
    parser.add_argument('-n', '--number-start',
                        help="Order of start test case")
    parser.add_argument('--not-include-testname', default=False, action='store_true',
                        help='Do not include image name into test name')
    parser.add_argument('-o', "--output-folder", default=OUTPUT_FOLDER_DEFAULT,
                        help="Output folder. Default is \"{0}\"".format(OUTPUT_FOLDER_DEFAULT))
    parser.add_argument('-f', '--test-folder', default=OUTPUT_FOLDER_DEFAULT,
                        help='Test folder will be updated specification. Default is "{0}"'
                             ''.format(OUTPUT_FOLDER_DEFAULT))
    parser.add_argument('-t', '--spec-file', default=SPEC_FILE_DEFAULT,
                        help='Specification file in tsv format. '
                             'Default is "{0}"'.format(SPEC_FILE_DEFAULT))
    parser.add_argument('--update-specification', default=False, action='store_true')
    parser.add_argument('--export-specification', default=False, action='store_true')
    return parser


def main():
    parser = parse_argument()
    args = parser.parse_args()

    # Export specification for test cases in a folder
    if args.export_specification:
        print ">>> Export specification"
        if not os.path.isdir(args.test_folder):
            print "Folder {0} does not exist!".format(args.test_folder)
            sys.exit(1)
        spec_exporter = SpecDbExporter()
        spec_exporter.export(args.spec_file, args.test_folder)
        print "Created: {0}".format(args.spec_file)
        sys.exit(0)

    # Update specification for test cases in a folder
    if args.update_specification:
        print ">>> Update specification"
        if not os.path.isdir(args.test_folder):
            print "Folder {0} does not exist!".format(args.test_folder)
            sys.exit(1)
        if not os.path.isfile(args.spec_file):
            print "File {0} does not exist!".format(args.spec_file)
            sys.exit(1)
        file_parser = TagsTsvParser(args.spec_file)
        tags_data = file_parser.get_data()
        total = len(tags_data)
        count = 1
        for test_id in tags_data:
            print "[{0}/{1}] {2}".format(count, total, test_id)
            spec_file = os.path.join(args.test_folder, test_id, TestcaseConfig.SPEC_FILE)
            spec_handler = TestSpecHandler(input_file=spec_file)
            tags = tags_data[test_id]
            # Update functionalities
            if SpecKeys.FUNCTIONALITIES in tags:
                spec_handler.set_functions(tags[SpecKeys.FUNCTIONALITIES].split(","))
            # Update component
            if SpecKeys.COMPONENT in tags:
                spec_handler.set_component(tags[SpecKeys.COMPONENT])
            # Update tags
            for tag_name in tags:
                value = tags[tag_name]
                try:
                    tag_type = SpecChecking[SpecKeys.TAGS][tag_name][SpecCheckKey.TYPE]
                    tag_value = get_tag_value(value, tag_type)
                    spec_handler.update_tag(tag_name, tag_value)
                except:
                    if tag_name != SpecKeys.FUNCTIONALITIES and tag_name != SpecKeys.COMPONENT:
                        print "Tag \"{0}\" is not defined!".format(tag_name)
            # Save
            spec_handler.save(spec_file)
            count += 1
        sys.exit(0)

    print ">>> Create PHOcr test cases"
    # Checking folder image and ground
    if not os.path.isdir(args.image_folder):
        print "Folder {0} does not exist!".format(args.image_folder)
        sys.exit(1)
    if args.ground_truth_folder and not os.path.isdir(args.ground_truth_folder):
        print "Folder {0} does not exist!".format(args.ground_truth_folder)
        sys.exit(1)

    has_ground = False
    if args.ground_truth_folder and os.path.isdir(args.ground_truth_folder):
        has_ground = True

    # Get test set
    testset = []
    for fname in os.listdir(args.image_folder):
        fpath = os.path.join(args.image_folder, fname)
        if os.path.isfile(fpath):
            ext = os.path.splitext(fname)[1]
            if ext in IMAGE_EXTENTIONS:
                testset.append(fname)
    total = len(testset)
    count = 1

    # Prepare output folder
    if not os.path.isdir(args.output_folder):
        os.makedirs(args.output_folder)

    if args.number_start:
        start_index = int(args.number_start)
    else:
        start_index = None

    for fname in sorted(testset):
        order = None
        if start_index:
            order = start_index + count - 1
        image_basename, image_ext, test_id = get_test_name(fname, args.prefix, args.suffix, order,
                                                           not args.not_include_testname)
        if test_id:
            print "[{0}/{1}] {2}".format(count, total, test_id)
            # Prepare test data
            test_data_folder = os.path.join(args.output_folder, test_id, TestcaseConfig.TEST_DATA_DIR)
            if not os.path.isdir(test_data_folder):
                os.makedirs(test_data_folder)
            fpath = os.path.join(args.image_folder, fname)
            copy_paths(fpath, test_data_folder)
            # Rename image file name
            if args.prefix or args.suffix or args.number_start:
                curr_path = os.path.join(test_data_folder, fname)
                new_name = test_id + image_ext
                des_path = os.path.join(test_data_folder, new_name)
                move_paths(curr_path, des_path)
            # Copy ground truth
            if has_ground:
                # Prepare ground truth data
                # Copy only ground truth file correspond with image name ignore ground truth files
                # which have the same prefix
                for gfname in os.listdir(args.ground_truth_folder):
                    if fnmatch.fnmatch(gfname, '*{0}'.format(GT_BB_EXT)):
                        image_name = gfname.replace(GT_BB_EXT, "")
                    elif fnmatch.fnmatch(gfname, '*{0}'.format(GT_TEXT_EXT)):
                        image_name = gfname.replace(GT_TEXT_EXT, "")
                    elif fnmatch.fnmatch(gfname, '*{0}'.format(GT_TEXT_EXT2)):
                        image_name = gfname.replace(GT_TEXT_EXT2, "")
                    else:
                        image_name = ""
                    if image_name == image_basename:
                        gfname_ext = gfname.replace(image_basename, "")
                        gfpath = os.path.join(args.ground_truth_folder, gfname)
                        gfolder = os.path.join(args.output_folder, test_id,
                                               TestcaseConfig.GROUND_TRUTH_DATA_DIR, "linux")
                        if not os.path.isdir(gfolder):
                            os.makedirs(gfolder)
                        copy_paths(gfpath, gfolder)
                        # Rename ground file
                        if args.prefix or args.suffix or args.number_start:
                            curr_path = os.path.join(gfolder, gfname)
                            new_name = test_id + gfname_ext
                            des_path = os.path.join(gfolder, new_name)
                            move_paths(curr_path, des_path)
            # Prepare spec file
            DEFAULT_SPEC[SpecKeys.ID] = test_id
            spec_path = os.path.join(args.output_folder, test_id, TestcaseConfig.SPEC_FILE)
            write_json(DEFAULT_SPEC, spec_path)
            count += 1

    if count > 1:
        # Export specification of new test cases
        spec_exporter = SpecDbExporter()
        spec_exporter.export(args.spec_file, args.output_folder)
        print "\nTotal {0} test cases are created!".format(count - 1)
        print "\nNOTICE:"
        print "Specification of test cases are just default value, please update specification " \
              "of test cases such as: component, functionalities and tags to create completely " \
              "test cases! Update tsv file \"{0}\" then use use option --update-specification " \
              "to apply!".format(args.spec_file)
    else:
        print "No test case is created!"


if __name__ == "__main__":
    main()
