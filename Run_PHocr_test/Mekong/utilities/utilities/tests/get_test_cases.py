# Toshiba - TSDV
# Team:         PHOcr
# Author:       Luong Van Huan
# Email:        huan.luongvan@toshiba-tsdv.com
# Date created: 27/08/2016
# Last update:  10/10/2019
# Updated by:   Phung Dinh Tai
# Description:  This script allow user to get test case from database
import os
import argparse
import sys
import traceback
from multiprocessing import Process
import sys_path
sys_path.insert_sys_path()
from database.lib_base.test_case_manager import TestCaseManager
from configs.database import SpecKeys
from configs.database import TestcaseConfig, SpecHelper
from manager.lib_distribution.filter_parser import append_tag_filter_string


NUMBER_THREAD_GET_TEST_CASE = 15
LIST_DEFAULT_SPEC_FIELDS = [
    SpecKeys.COMPONENT,
    SpecKeys.PRODUCT,
    SpecKeys.ENABLE,
    SpecKeys.ERROR_FLAGS,
    SpecKeys.FUNCTIONALITIES,
    SpecKeys.TAGS,
    SpecKeys.WEIGHTS,
    SpecKeys.BINARY_TEST_INFORMATION,
    SpecKeys.HISTORY_DATA
]


# TODO : Add option for print debug or not
# TODO : Get each component : test data, spec, reference data, ground truth data,
# TODO : script ~ Update for each one
def main():
    parser = argparse.ArgumentParser(
        description='Get test spec, test data, reference data from data '
                    'base.\nNOTE: By default, test case which has tag '
                    'NonIntegration with True value is ignore to get. To get '
                    'these test cases, please add tag filter '
                    'NonIntegration:True to your filters')
    parser.add_argument('-id', '--test-case-id',
                        help='Query by test case id, support multiple test cases')
    parser.add_argument('-con', '--id-contain',
                        help='Query test cases that contain string')
    parser.add_argument('-q', '--query',
                        help='Query test cases by query json in file')
    parser.add_argument('-l', '--limit',
                        help='Limit returned test cases by query json in file', default=0)
    parser.add_argument('-pro', '--product',
                        help='Query by product')
    parser.add_argument('-c', '--component',
                        help='Query by component')
    parser.add_argument('-f', '--functionalities',
                        help='Query by functionalities')
    parser.add_argument('-t', '--tags',
                        help='Query by tags')
    parser.add_argument('-s', '--spec-filter',
                        help='Query fields in specification as filter, '
                             'Support multiple fields and fields are separated by commas.'
                             'User can use this argument to specified field they want to get.'
                             'If not use this argument, get fields as default')
    parser.add_argument('--get-all-spec-field', default=False, action='store_true',
                        help="Get all fields in specification")
    parser.add_argument('--list-test-name', default=False, action='store_true',
                        help="Do not get test cases, only list up test name of filters")
    parser.add_argument('--get-ground-truth', default=False, action='store_true',
                        help="Get ground truth of test cases by filters into output folder")
    parser.add_argument('--get-image', default=False, action='store_true',
                        help="Get image of test cases by filters into output folder")
    parser.add_argument('--get-test-data', default=False, action='store_true',
                        help="Get test data folder of all selected test cases "
                             "the selected test cases can be choose by "
                             "reference folder.")
    parser.add_argument('--test-reference-folder',
                        help="Using in --get-test-data for list up the test "
                             "cases which need to be append test data")
    parser.add_argument('--get-reference', default=False, action='store_true',
                        help="Get reference data of test cases by filters into output folder")
    parser.add_argument('-o', '--output-folder',
                        help='Ouput folder which will contain test cases/ Output file name when'
                             'export specification of test cases (should be tsv format).')
    parser.add_argument('--force', default=False, action='store_true',
                        help="Force to get if a test case has already existed")
    parser.add_argument('--list-products', default=False, action='store_true',
                        help="List all of available products")
    parser.add_argument('--list-components', default=False, action='store_true',
                        help="List all of available components")
    parser.add_argument('--list-functionalities', default=False, action='store_true',
                        help="List all of available functionalities")
    parser.add_argument('--list-tags', default=False, action='store_true',
                        help="List all of available tags")
    parser.add_argument('--list-spec-field', default=False, action='store_true',
                        help="List all of available of specification")
    parser.add_argument('--case-sensitive', default=False, action='store_true',
                        help="Case sensitive for option query id contain")
    parser.add_argument('--get-test-spec', default=False, action='store_true',
                        help="Get test spec json file for each test case.")
    args = parser.parse_args()

    # Helper
    db_helper = SpecHelper()
    if args.list_products:
        db_helper.list_product()
        return

    if args.list_components:
        db_helper.list_component()
        return

    if args.list_functionalities:
        db_helper.list_functionality()
        return

    if args.list_tags:
        db_helper.list_tags()
        return

    if args.list_spec_field:
        db_helper.list_all_spec_field()
        return

    # create filters from user input
    filters = {}

    if args.test_case_id:
        filters[SpecKeys.ID] = args.test_case_id

    if args.product:
        filters[SpecKeys.PRODUCT] = args.product

    if args.component:
        filters[SpecKeys.COMPONENT] = args.component

    if args.functionalities :
        filters[SpecKeys.FUNCTIONALITIES] = args.functionalities

    # Create tag filters. By default we consider to ignore non-integration
    # test cases by append tag filter for NonIntegration by False value.
    tag_filters_string = ''
    if args.tags:
        tag_filters_string = args.tags
    tag_filters_string = append_tag_filter_string(
        filters_string=tag_filters_string,
        tag_name=SpecKeys.Tags.IS_NON_INTEGRATION,
        tag_value=False)
    filters[SpecKeys.TAGS] = tag_filters_string

    test_case_manager = TestCaseManager()
    if args.id_contain:
        filters[SpecKeys.ID_CONTAIN] = args.id_contain

    if args.query:
        if os.path.exists(args.query):
            import json
            data = json.load(open(args.query))
            test_cases = test_case_manager.query_db(data, int(args.limit))
            ids = []
            for tc_id in test_cases:
                ids.append(tc_id["_id"])
            filters[SpecKeys.ID] = ",".join(ids)
        else:
            print('Not exists file %s' % args.query)

    if args.list_test_name:
        test_case_manager.list_test_names(filters)
        sys.exit(0)

    if args.get_ground_truth:
        print "* GET GROUND TRUTH DATA *"
        if not args.output_folder:
            output_folder = "GroundDBs"
        else:
            output_folder = args.output_folder
        test_case_manager.get_grounds(filters, output_folder)
        sys.exit(0)

    if args.get_image:
        print "* GET TEST DATA *"
        if not args.output_folder:
            output_folder = "ImageDBs"
        else:
            output_folder = args.output_folder
        test_case_manager.get_images(filters, output_folder)
        sys.exit(0)

    if args.get_test_data:
        print("* GET TEST DATA *")
        output_folder = "TestData"
        if args.test_reference_folder and \
                os.path.isdir(args.test_reference_folder):
            test_case_ids = os.listdir(args.test_reference_folder)
            filters = {SpecKeys.ID: ",".join(test_case_ids)}
            if not args.output_folder:
                output_folder = args.test_reference_folder
            else:
                output_folder = args.output_folder
        test_case_manager.get_all_test_data_folders_parallel(filters, output_folder)
        sys.exit(0)

    if args.get_reference:
        print "* GET REFERENCE DATA *"
        if not args.output_folder:
            output_folder = "ReferenceDBs"
        else:
            output_folder = args.output_folder
        test_case_manager.get_refs(filters, output_folder)
        sys.exit(0)

    # Specified filed which will be gotten in specification
    if args.get_all_spec_field:
        # Because of when query specification by id, if find option is None it will get all fields
        # of specification. In there, if input (list_spec_field) is None, find option will be None
        list_spec_fields = None
    elif args.spec_filter:
        list_spec_fields = args.spec_filter.replace(" ", "").split(',')
    else:
        list_spec_fields = LIST_DEFAULT_SPEC_FIELDS

    if args.get_test_spec and SpecKeys.ID in filters:
        if not args.output_folder:
            output_folder = "SpecDBs"
        else:
            output_folder = args.output_folder
        test_case_manager.get_test_spec(
            filters[SpecKeys.ID], output_folder, list_spec_fields)
        sys.exit(0)

    if not args.output_folder:
        output_folder = TestcaseConfig.FOLDER_DEFAULT
    else:
        output_folder = args.output_folder

    get_all_tcs_parallel(args, filters, output_folder, test_case_manager, list_spec_fields,
                         args.get_test_spec)
    sys.exit(0)


def get_all_tcs_parallel(args, filters, output_folder, test_case_manager, list_spec_fields,
                         spec_only=False):
    test_specs = test_case_manager.query_by_filters(filters_str=filters, only_id=True)
    total = len(test_specs)
    count = 1

    while len(test_specs) > 0:
        processes = []
        for index in range(0, NUMBER_THREAD_GET_TEST_CASE):
            if len(test_specs) == 0:
                break

            test_spec = test_specs.pop()

            # Make sure that test_case name does not contain any unexpected spaces.
            test_case_id = test_spec[SpecKeys.ID]
            print "[{0}/{1}] Get test case {2}".format(count, total, test_case_id)
            try:
                process = Process(target=get_tcs_parallel,
                                  args=(test_case_id, output_folder, args.force, list_spec_fields,
                                        spec_only))
                processes.append(process)
                process.start()
                count += 1
            except SystemExit:
                exit(1)
            except:
                print "\tGET FAILED!"
                traceback.print_exc()
        for index in range(0, len(processes)):
            processes[index].join()


def get_tcs_parallel(test_case_id, output_folder, force, list_spec_fields, spec_only=False):
    manager = TestCaseManager()
    if spec_only:
        manager.get_a_test_case(test_case_name=test_case_id,
                                output_dir=output_folder,
                                force=force,
                                list_spec_fields=list_spec_fields,
                                remove_exists=True,
                                get_test_spec=True,
                                get_scripts=False,
                                get_test_data=False,
                                get_ground_truth=False,
                                get_ref_data=False)
    else:
        manager.get_a_test_case(test_case_name=test_case_id,
                                output_dir=output_folder,
                                force=force,
                                list_spec_fields=list_spec_fields,
                                remove_exists=True,
                                get_test_spec=True,
                                get_scripts=True,
                                get_test_data=True,
                                get_ground_truth=True,
                                get_ref_data=True)


if __name__ == "__main__":
    main()
