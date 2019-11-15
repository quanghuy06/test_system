# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           TaiPD
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      12/09/2016
# Last update:      02/07/2018
# Description:      This python script tend to distribute test cases in test set
#                   to test nodes. Output is a json file
import os
import configs.common
from baseapi.common import find_min_index
from baseapi.file_access import write_json, read_json, write_bson
from configs.json_key import TestDistributionJson
from database.lib_base.test_case_manager import TestCaseManager
from handlers.profile_handler import ProfileHandler
from manager.lib_distribution.filter_parser import *
from configs.projects.hanoi import HanoiProject
from configs.database import TestcaseConfig
from configs.timeout import TimeOut


class TestDistributor:

    def __init__(self, profile_path, parameters, weight_threshold=None):
        # Initial handler for parameters json file
        self.parameters_handler = parameters
        # Initial handler to handle profile json object
        self.profile_handler = ProfileHandler(input_file=profile_path,
                                              parameters_handler=self.parameters_handler)
        # Initial test case manage object to query database
        self.test_case_manager = TestCaseManager()

        # Some variables of self object
        self.distribution = {}
        self.weight_threshold = weight_threshold
        self.test_set_ws = []
        self.filters = None

    # Set custom filters from outside
    def set_filters(self, filters):
        self.filters = filters

    # This function checking if resource is available, make a mask of test distribution,
    # set num_vms, num_linux_vms, and num_windows_vms
    # Change log: If any virtual machine is running, force to poweroff
    def checking_system(self, platform):
        # Check test node
        test_nodes = self.get_test_nodes(platform=platform)
        for node in test_nodes:
            if node.is_connected():
                # Test virtual machines
                workers = self.profile_handler.get_testers_of_node_by_platform(
                    node_name=node.name, platform=platform)
                if workers and (node.name not in self.distribution.keys()):
                    self.distribution[node.name] = {}
                # Force stop running virtual machines
                for worker in workers:
                    # Create a mask for vm distribution
                    self.distribution[node.name][worker.name] = {}
                    self.distribution[node.name][worker.name][TestDistributionJson.location.DB] = []
                    self.distribution[node.name][worker.name][TestDistributionJson.location.WS] = []
            else:
                print ("Node {0} is disconnected!".format(node.name))

    # Get and combine test cases from database base on list of filters.
    def get_test_set_filters(self, filters):
        test_set = []
        for filter_str in filters:
            if filter_str:
                query_data = self.test_case_manager.query_by_filters(filters_str=filter_str,
                                                                     only_id=True)
                for test_id in query_data:
                    if test_id not in test_set:
                        test_set.append(test_id)
        return test_set

    def get_custom_query(self):
        """
        Get custom query under BSON format
        """
        if self.parameters_handler is not None:
            return self.parameters_handler.custom_query()
        return None

    def get_filters_db(self, platform, is_force_user_filter):
        # Get data of filters string from commit message
        commit_message = self.parameters_handler.get_commit()
        filters_commit = parse_filters_message(commit_message)
        filter_list = []
        if self.parameters_handler.is_extreme_test():
            filter_extreme_test = {
                SpecKeys.TAGS: "{0}:true".format(
                    SpecKeys.Tags.IS_EXTREME_TEST)
            }
            filter_list.append(filter_extreme_test)
        elif not self.parameters_handler.is_et():
            # Integration Test get test cases tag Non-Integration = False
            filter_it_default = {
                SpecKeys.TAGS: "{0}:false".format(
                    SpecKeys.Tags.IS_NON_INTEGRATION)
            }
            filter_not_extreme_test = "{extreme_tag}:false" \
                                      "".format(extreme_tag=SpecKeys.Tags.IS_EXTREME_TEST)
            filter_it_default[SpecKeys.TAGS] += "&{0}".format(filter_not_extreme_test)
            if not is_force_user_filter:
                filter_list.append(filter_it_default)
            else:
                if filters_commit:
                    filter_list.append(filters_commit)
                else:
                    filter_list.append(filter_it_default)

        elif not filters_commit:
            # Engineering Test get test cases by default
            # If test set is not defined in commit message and comment of
            # reviewer -> Get test cases that has tag IsEtDefault with true
            # value
            tags_filter_et_default = ''
            tags_filter_et_default = append_tag_filter_string(
                tags_filter_et_default, SpecKeys.Tags.IS_ET_DEFAULT, True
            )
            tags_filter_et_default = append_tag_filter_string(
                tags_filter_et_default, SpecKeys.Tags.IS_NON_INTEGRATION, False
            )
            filter_et_default = {
                SpecKeys.TAGS: tags_filter_et_default
            }
            filter_list.append(filter_et_default)
        else:
            # Filter to ignore test cases which have tag NonIntegration is True.
            # Get exist tag filters string which defined by user
            tag_filters_string = ''
            if SpecKeys.TAGS in filters_commit:
                tag_filters_string = filters_commit[SpecKeys.TAGS]
            # Consider to append filter of tag NonIntegration by False value
            tag_filters_string = append_tag_filter_string(
                filters_string=tag_filters_string,
                tag_name=SpecKeys.Tags.IS_NON_INTEGRATION,
                tag_value=False)
            # Re-assign tag filters to final filters.
            filters_commit[SpecKeys.TAGS] = tag_filters_string
            filter_list.append(filters_commit)
            # Engineering Test get test cases by filters defined in commit
            # message
            if not (SpecKeys.TEST_ET_DEFAULT in filters_commit \
                and filters_commit[SpecKeys.TEST_ET_DEFAULT] == 'false'):
                tags_filter_et_default = ''
                tags_filter_et_default = append_tag_filter_string(
                    tags_filter_et_default, SpecKeys.Tags.IS_ET_DEFAULT, True
                )
                tags_filter_et_default = append_tag_filter_string(
                    tags_filter_et_default, SpecKeys.Tags.IS_NON_INTEGRATION, False
                )
                filter_et_default = {
                    SpecKeys.TAGS: tags_filter_et_default
                }
                filter_list.append(filter_et_default)
        # Append platform for each filter
        platform_filter = "{plf_label}:{plf_value}" \
                            "".format(plf_label=SpecKeys.Tags.PLATFORMS,
                                      plf_value=platform,
                                      mem_label=SpecKeys.Tags.IS_MEMCHECK)
        for i in range(0, len(filter_list)):
            if SpecKeys.TAGS in filter_list[i].keys():
                filter_list[i][SpecKeys.TAGS] += "&{0}".format(platform_filter)
            else:
                filter_list[i][SpecKeys.TAGS] = platform_filter

        return filter_list

    def get_test_set_db_by_platform(self, platform, is_force_user_filter):
        # If have custom query, we only get testcases by custom query
        if self.get_custom_query() is not None:
            custom_query = self.get_custom_query()
            json_temp = os.path.join(os.getcwd(), 'custom_query_bson.json')
            write_bson(custom_query, json_temp)
            import json
            data = json.load(open(json_temp))
            test_cases = self.test_case_manager.query_db(data)
            os.remove(json_temp)
            test_set = []
            for test_id in test_cases:
                if test_id not in test_set:
                    filters = {}
                    filters[SpecKeys.ID] = test_id["_id"]
                    test_set.append(filters)
            return test_set
        else:
            filters = self.filters
            if not filters:
                filters = self.get_filters_db(platform,
                                              is_force_user_filter=is_force_user_filter)
            return self.get_test_set_filters(filters=filters)

    def get_num_workers(self, platform):
        test_nodes = self.get_test_nodes(platform=platform)
        workers = []
        for node in test_nodes:
            node_workers = self.profile_handler.get_testers_of_node_by_platform(
                node_name=node.name, platform=platform)
            workers += node_workers
        return len(workers)

    def get_test_nodes(self, platform):
        return self.profile_handler.get_test_nodes_by_platform(platform=platform)

    def distribute_for_platform(self, platform, test_set=None):
        is_force_user_filter = self.parameters_handler.is_force_specification()
        # Get test list
        if not test_set:
            test_set = \
                self.get_test_set_db_by_platform(platform=platform,
                                                 is_force_user_filter=is_force_user_filter)
        # Get weight of test cases
        test_data = {}
        is_checking_memory = self.parameters_handler.is_checking_for_memory()
        is_test_on_board = self.parameters_handler.is_test_on_board()
        for test_info in test_set:
            test_id = test_info[SpecKeys.ID]
            weight = self.test_case_manager.get_weight(test_id=test_id,
                                                       platform=platform)
            # Current, when testing on board or checking for memory (both
            # checking for memory leak or memory peak) we don't test with
            # Ha Noi test case
            if is_checking_memory or is_test_on_board:
                if self.test_case_manager.get_component(test_id=test_id)\
                        != HanoiProject.components.DEFAULT:
                    if self.parameters_handler.is_check_memory_peak():
                        # If checking for memory peak, we don't test with test
                        # case which are checking for memory leak
                        if not self.test_case_manager.get_tag(test_id=test_id,
                                                              tag_name=SpecKeys.Tags.IS_MEMCHECK):
                            test_data[test_id] = weight
                    elif self.parameters_handler.is_check_memory_leak():
                        # When checking for memory leak, because of weight of
                        # memory leak test case is greater many times with
                        # normal test case so we increase weight of normal test case
                        # by a ratio to balance with memory leak test case to distribute
                        if not self.test_case_manager.get_tag(test_id=test_id,
                                                              tag_name=SpecKeys.Tags.IS_MEMCHECK):
                            test_data[test_id] = weight * TimeOut.execute.RATIO_TIMEOUT_RUN_MEMORY_LEAK
                        else:
                            test_data[test_id] = weight
                    else:
                        test_data[test_id] = weight
            else:
                test_data[test_id] = weight

        # Get number of workers
        num_workers = self.get_num_workers(platform=platform)

        # Distribute to test sets
        test_sets = self.distribute_core(test_data=test_data,
                                         num_workers=num_workers,
                                         weight_threshold=self.weight_threshold)

        # Get test nodes
        test_nodes = self.get_test_nodes(platform=platform)

        # Distribute to workers
        count = 0
        num_set = len(test_sets)
        for node in test_nodes:
            workers = self.profile_handler.get_testers_of_node_by_platform(
                node_name=node.name, platform=platform)
            for worker in workers:
                if count >= num_set:
                    break
                worker_distribution = {
                    TestDistributionJson.location.DB: [],
                    TestDistributionJson.location.WS: []
                }
                current_test_set = test_sets[count]
                for test_name in current_test_set:
                    if test_name in self.test_set_ws:
                        worker_distribution[TestDistributionJson.location.WS].append(test_name)
                    else:
                        worker_distribution[TestDistributionJson.location.DB].append(test_name)
                self.distribution[node.name][worker.name] = worker_distribution
                count += 1

    @staticmethod
    def distribute_core(test_data, num_workers, weight_threshold=None):
        if (num_workers == 0) or (not test_data):
            return []
        # Arrange testSet by weight from less to more (Bubble sort)
        test_set_arrange = []
        for key in test_data:
            tmp = {SpecKeys.ID: key, SpecKeys.WEIGHT: test_data[key]}
            test_set_arrange.append(tmp)
        num_test_cases = len(test_set_arrange)
        for i in range(num_test_cases - 1, 0, -1):
            for j in range(i):
                if test_set_arrange[j][SpecKeys.WEIGHT] > test_set_arrange[j + 1][SpecKeys.WEIGHT]:
                    temp = test_set_arrange[j]
                    test_set_arrange[j] = test_set_arrange[j + 1]
                    test_set_arrange[j + 1] = temp

        # distribute[] store list of test sets that will be distributed to corresponding virtual
        #  machines sum_dis[] store weight summary of vm's test cases, correspond to distribute
        # length of distribute should be equal to number of virtual machines
        distribute = []
        sum_dis = []
        if weight_threshold is None:
            # If weight_threshold is None, we use as much as possible of virtual machines.
            # Distribution is fair for all virtual machines
            # Execute distribution
            # For loop will run one by one test case in test set (which id arranged)
            # and assign test case to virtual machines. Use number of virtual machines as much as
            # possible
            # test_case: {
            #   id: 'tc_001',
            #   weight: 0.29
            # }
            # Init distribute and sum_dis depend on number of test cases in test set
            if num_test_cases < num_workers:
                # If number of test case less than number of virtual machine,
                # so only use num_test_cases virtual machines and each will
                # run a test case
                for i in range(0, num_test_cases):
                    distribute.append([test_set_arrange[i][SpecKeys.ID]])
                return distribute
            else:
                # If number of test cases no less than number of
                # virtual machine, so need to use all virtual machines
                for i in range(0, num_workers):
                    distribute.append([])
                    sum_dis.append(0)
            # Run through all test cases from more to less. Find distribute that
            # has the smallest sum_dis and distribute current test case for
            # this one
            for i in range(num_test_cases, 0, -1):
                test_case = test_set_arrange[i - 1]
                min_index = find_min_index(sum_dis)
                sum_dis[min_index] += test_case[SpecKeys.WEIGHT]
                distribute[min_index].append(test_case[SpecKeys.ID])
        else:
            # If weight_threshold is passed, distribution will distribute
            # test cases until weight summary of virtual machine's test cases is
            # more than weight threshold
            if num_test_cases > 0:
                distributed_count = 0
                count = 0
                sum_dis.append(0)
                distribute.append([])
            else:
                return []
            # Distribute for the first round
            for test_case in test_set_arrange:
                if (sum_dis[count] + test_case[SpecKeys.WEIGHT]) <= weight_threshold:
                    distribute[count].append(test_case[SpecKeys.ID])
                    sum_dis[count] += test_case[SpecKeys.WEIGHT]
                    distributed_count += 1
                else:
                    if (count + 1) < num_workers:
                        count += 1
                        distribute.append([test_case[SpecKeys.ID]])
                        sum_dis.append(test_case[SpecKeys.WEIGHT])
                        distributed_count += 1
                    else:
                        break
            if distributed_count < num_test_cases:
                for i in range(num_test_cases, distributed_count, -1):
                    test_case = test_set_arrange[i - 1]
                    min_index = find_min_index(sum_dis)
                    sum_dis[min_index] += test_case[SpecKeys.WEIGHT]
                    distribute[min_index].append(test_case[SpecKeys.ID])
        return distribute

    # Distribute test set for all test nodes with all virtual machine.
    # Use number of test nodes as much as possible
    # Input: test set
    def export_distribution(self, output_file):
        # Currently, we only need to confirm build when test ET, no need to
        # confirm test results and we also need to confirm checking memory leak
        # on platform linux

        if self.parameters_handler.is_et() \
                or self.parameters_handler.is_checking_for_memory():
            configs.common.SupportedPlatform = [configs.common.Platform.LINUX]
        # Distribute normal test for supported platforms
        for platform in configs.common.SupportedPlatform:
            self.checking_system(platform=platform)
            self.distribute_for_platform(platform=platform)

        # Write distribution to file
        write_json(obj=self.distribution, file_name=output_file)
