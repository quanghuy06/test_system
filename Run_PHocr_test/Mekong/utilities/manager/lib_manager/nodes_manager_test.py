# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      26/06/2018
# Description:      This script define base class for a build node.
import os
import csv
import traceback
import configs.common
import configs.run_counter
from baseapi.file_access import remove_paths, copy_paths, read_json
from baseapi.file_access import write_json
from configs.compare_result import CompareResultConfig
from configs.projects.mekong import SystemInfo
from configs.database import SpecKeys, TestcaseConfig
from configs.json_key import ProfileJson
from configs.test_result import FinalTestResult, TestResultConfig, FinalResult
from handlers.compare_handlers.compare_result_handler import CompareResultHandler
from handlers.distribution_handler import DistributionHandler
from handlers.test_result_handler import TestResultHandler
from handlers.profile_handler import ProfileHandler
from manager.lib_distribution.distributor \
    import TestDistributor, TestDistributionJson
from manager.lib_manager.nodes_manager_class import NodesManager
from report.lib_summary_report.junit_xml_reporter \
    import JunitXmlReporter, JXRConfiguration
from report.lib_summary_report.barcode_accuracy_reporter \
    import BarcodeAccuracyReporter, BCARConfiguration
from report.lib_errors_report.bb_error_types_reporter \
    import BbErrorTypesReporter, BB_ERROR_TYPES_REPORT_NAME_DEFAULT
from report.lib_errors_report.text_error_types_reporter \
    import TextErrorTypesReporter, TEXT_ERROR_TYPES_REPORT_NAME_DEFAULT
from report.lib_summary_report.bounding_box_accuracy_reporter \
    import BbAccuracyReporter, BB_ACCURACY_REPORT_DEFAULT_NAME
from report.lib_summary_report.overall_information_reporter import OIRConfiguration
from report.lib_summary_report.overall_information_reporter \
    import OverallInformationReporter
from report.lib_summary_report.text_accuracy_reporter \
    import TextAccuracyReporter, TEXT_ACCURACY_REPORT_DEFAULT_NAME
from report.lib_summary_report.memory_peak_reporter import MemPeakReporter, \
    MEM_PEAK_REPORT_DEFAULT_NAME
from report.lib_delta_report.phocr_delta_memcheck_reporter \
    import DATConfiguration, PHOcrDeltaMemoryLeakReporter
from report.lib_delta_report.phocr_mem_peak_reporter\
    import MemPeakReportConfiguration, PHOcrMemoryPeakReporter
from report.lib_system_performance.system_performance_reports_generator \
    import SystemPerformanceReportsGenerator
from report.lib_memory_report.mem_peak_tsv_reporter import MemPeakTsvReporter, \
    MEM_PEAK_TSV_FILE_NAME_DEFAULT


class NodesManagerTest(NodesManager):

    def __init__(self, distribution_file=None, **kwargs):
        super(NodesManagerTest, self).__init__(**kwargs)
        self.logger.start_stage(
            "TEST  {project}  FOR  {job}  ON  {platforms}".format(
                project=self.info_handler.get_project(),
                job=self.info_handler.get_job(),
                platforms=", ".join(configs.common.SupportedPlatform)))
        self.is_force_spec = self.info_handler.is_force_specification()
        self.distribution_file = distribution_file
        if self.distribution_file:
            self.distribution_handler = \
                DistributionHandler(input_file=self.distribution_file)
            self.work_nodes = self.get_work_nodes()
        else:
            self.distribution_handler = None
        self.log_folder = os.path.join(FinalTestResult.INFO,
                                       FinalTestResult.LOG,
                                       FinalTestResult.Log.TEST)
        self.test_result = {}
        self.compare_result = {}
        # Set up files and folders
        self.final_test_file = None
        self.is_check_memory_peak = False
        if self.info_handler.is_check_memory_peak():
            self.final_mem_peak_info_file = None
            self.is_check_memory_peak = True
            self.mem_peak_info = {}
        self.final_compare_file = None
        self.final_report_folder = None
        self.final_changed_folder = None
        self.final_error_folder = None
        self.final_spec_folder = None
        self.change_number = self.info_handler.get_change_number()
        self.delta_version = self.info_handler.get_phocr_version()
        self.suffix_report = None
        self.get_suffix_report()
        self.list_reporters = []

    # Pre-process of testing
    def pre_process(self):
        if self.is_force_spec:
            self.logger.log_and_print(" Create force spec file")
            self.create_force_spec_file()
        # Distribute test cases. We do not execute distribution if this is the
        #  first time and distribution file is already provided
        is_first_time = configs.run_counter.RUN_COUNT == configs.run_counter.START_COUNT
        if self.distribution_file and is_first_time:
            # No need execute for the first time run with distribution file provided
            pass
        elif is_first_time:
            self.distribute_tests()
        else:
            self.distribute_for_retry()

    # Prepare for build
    def prepare_work(self):
        # Clean old results
        is_first_time = configs.run_counter.RUN_COUNT == configs.run_counter.START_COUNT
        if is_first_time:
            self.clean_old_results()

    def clean_old_results(self):
        self.logger.start_step("Clean old results")
        clean_list = list()
        clean_list.append(self.log_folder)
        clean_list.append(os.path.join(FinalTestResult.INFO,
                                       TestDistributionJson.DEFAULT_NAME))
        clean_list.append(FinalTestResult.SPEC)
        for platform in configs.common.SupportedPlatform:
            clean_list.append(os.path.join(platform, FinalTestResult.TEST))
            clean_list.append(os.path.join(platform, FinalTestResult.REPORT))

        # Clean all old results
        for f in clean_list:
            if os.path.exists(f):
                remove_paths(f)
        self.logger.end_step(True)

    # Get system information of last run
    def get_system_info_last_run(self):
        log_folder_by_latest_run = \
            configs.run_counter.RUN_FOLDER_TEMPLATE.format(count=configs.run_counter.RUN_COUNT - 1)
        system_info_file = os.path.join(self.log_folder, log_folder_by_latest_run,
                                        SystemInfo.SYSTEM_INFO_FILE)
        if not os.path.isfile(system_info_file):
            raise Exception("System falls down, no system information file found!")
        return read_json(system_info_file)

    # Get profile information of last run
    def get_profile_info_last_run(self):
        # Get old profile system of last run
        log_folder_by_run_time = \
            configs.run_counter.RUN_FOLDER_TEMPLATE.format(count=configs.run_counter.RUN_COUNT - 1)
        profile_file_name = os.path.basename(self.profile_handler.input_file)
        old_profile_path = os.path.join(self.log_folder,
                                        log_folder_by_run_time,
                                        profile_file_name)
        return ProfileHandler(input_file=old_profile_path,
                              parameters_handler=self.info_handler)

    # Edit profile to ignore failed workers base on system information of latest run
    def remove_failed_workers_from_profile(self):
        system_info = self.get_system_info_last_run()
        for node in system_info:
            node_info = system_info[node]
            if not node_info:
                # Node failed test
                self.profile_handler.remove_test_node(node_name=node)
            else:
                for worker in node_info:
                    if node_info[worker] == SystemInfo.F_FAILED:
                        # Worker of node failed test
                        self.profile_handler.remove_test_worker(node_name=node,
                                                                worker_name=worker)
        # Save the edit
        self.profile_handler.dump()

    # Get filters to get list test case for trying run again. This is list of
    # test cases of failed workers
    def get_retry_test_set(self, platform):
        profile_old_handler = self.get_profile_info_last_run()
        # Filter profile by memory check tag
        profile = profile_old_handler.test_config
        distribution_handler = \
            DistributionHandler(input_file=self.distribution_file)
        tests_list = []
        system_info = self.get_system_info_last_run()
        for node in system_info:
            if node not in profile:
                continue
            # Get list of workers
            workers_list = []
            # Filter profile by platform tag
            for worker in profile[node]:
                worker_profile = \
                    self.profile_handler.get_worker_info(worker_name=worker)
                if worker_profile[ProfileJson.info.OS] == platform:
                    workers_list.append(worker)

            node_info = system_info[node]
            if not node_info:
                # Re-test for test cases on failed node
                node_distribution = \
                    distribution_handler.get_node_distribution(node_name=node)
                for worker in node_distribution:
                    if worker in workers_list:
                        tests_list += node_distribution[worker][
                            TestDistributionJson.location.DB]
            else:
                for worker in node_info:
                    if node_info[worker] == SystemInfo.F_FAILED and worker in workers_list:
                        # Re-test for test cases on failed worker
                        worker_distribution = distribution_handler.get_worker_distribution(
                            node_name=node, worker_name=worker)
                        tests_list += worker_distribution[TestDistributionJson.location.DB]
        filter_str = {
            SpecKeys.ID: ",".join(tests_list)
        }
        distributor = TestDistributor(profile_path=self.profile_handler.input_file,
                                      parameters=self.info_handler)
        distributor.set_filters(filters=[filter_str])
        return distributor.get_test_set_db_by_platform(platform=platform,
                                                       is_force_user_filter=self.is_force_spec)

    # Distribute test set for retry
    def distribute_for_retry(self):
        self.logger.start_step("Distribute test cases for retry")
        self.remove_failed_workers_from_profile()
        distributor = TestDistributor(profile_path=self.profile_handler.input_file,
                                      parameters=self.info_handler)
        for platform in configs.common.SupportedPlatform:
            # Get test set for platform
            test_set = self.get_retry_test_set(platform=platform)
            # Get distribution
            if test_set:
                distributor.checking_system(platform=platform)
                distributor.distribute_for_platform(platform=platform, test_set=test_set)

        # Write distribution for retry
        write_json(obj=distributor.distribution, file_name=self.distribution_file)

        self.distribution_handler = DistributionHandler(input_file=self.distribution_file)
        self.work_nodes = self.get_work_nodes()
        self.logger.end_step(True)

    # Distribute test set base on profile
    def distribute_tests(self):
        self.logger.start_step("Distribute test cases")
        distributor = TestDistributor(profile_path=self.profile_handler.input_file,
                                      parameters=self.info_handler)
        distributor.export_distribution(TestDistributionJson.DEFAULT_NAME)
        self.distribution_file = TestDistributionJson.DEFAULT_NAME
        self.distribution_handler = DistributionHandler(input_file=self.distribution_file)
        self.work_nodes = self.get_work_nodes()
        self.logger.end_step(True)

    # Combine all result from build nodes
    def post_process(self):
        # Combine test result
        self.combine_test_results()

        # Create report
        self.create_report()

        # End of test stage
        self.logger.end_stage(True)

        # Generate profiling data of execution time of test system
        self.generate_execution_time_data()

    def combine_test_results(self):
        self.logger.start_step("Combine test results from nodes")
        total = len(self.work_nodes)
        count = 1
        for node in self.work_nodes:
            self.logger.log_and_print("[{0}/{1}] Extract result from {2}"
                                      "".format(count, total, node.name))
            self.combine_node_test_result(node=node)
            self.logger.log_and_print("End combine test results from {0}"
                                      "".format(node.name))
            count += 1
            # Write test result to file
            for platform in self.test_result:
                final_test_folder = os.path.join(platform, FinalTestResult.TEST)
                if not os.path.isdir(final_test_folder):
                    os.makedirs(final_test_folder)
                final_test_file = os.path.join(final_test_folder,
                                               TestResultConfig.FILE_DEFAULT)
                write_json(self.test_result[platform], final_test_file)
            # Write compare result to file
            for platform in self.compare_result:
                final_test_folder = os.path.join(platform, FinalTestResult.TEST)
                if not os.path.isdir(final_test_folder):
                    os.makedirs(final_test_folder)
                final_compare_file = os.path.join(final_test_folder,
                                                  CompareResultConfig.FILE_DEFAULT)
                write_json(self.compare_result[platform], final_compare_file)

            if self.is_check_memory_peak:
                for platform in self.mem_peak_info:
                    final_test_folder = os.path.join(platform,
                                                     FinalTestResult.TEST)
                    if not os.path.isdir(final_test_folder):
                        os.makedirs(final_test_folder)
                    final_mem_peak_file = os.path.join(final_test_folder,
                                                       TestResultConfig.MEM_PEAK_FILE)
                    write_json(self.mem_peak_info[platform], final_mem_peak_file)
        self.logger.end_step(True)

    def set_final_paths(self, platform):
        self.final_test_file = FinalResult.FINAL_TEST_FILE.format(platform)
        if os.path.isfile(self.final_test_file):
            # Load test result from last run
            self.test_result[platform] = read_json(self.final_test_file)
        self.final_compare_file = FinalResult.FINAL_COMPARE_FILE.format(platform)
        if os.path.isfile(self.final_compare_file):
            # Load compare result from last run
            self.compare_result[platform] = read_json(self.final_compare_file)
        if self.is_check_memory_peak:
            self.final_mem_peak_info_file = FinalResult.FINAL_COMBINE_MEM_PEAK_FILE.format(platform)
            if os.path.isfile(self.final_mem_peak_info_file):
                self.mem_peak_info[platform] = read_json(self.final_mem_peak_info_file)

        self.final_changed_folder = FinalResult.FINAL_CHANGED_FOLDER.format(platform)
        self.final_report_folder = FinalResult.FINAL_REPORT_FOLDER.format(platform)
        self.final_error_folder = FinalResult.FINAL_ERROR_FOLDER.format(platform)
        self.final_spec_folder = FinalResult.FINAL_SPEC_FOLDER

    def combine_node_test_result(self, node):
        node_result_folder = node.result_folder
        if os.path.isdir(node_result_folder):
            for platform in configs.common.SupportedPlatform:
                platform_test_result = os.path.join(node_result_folder, platform)
                if os.path.isdir(platform_test_result):
                    self.set_final_paths(platform)
                    # Combine test result
                    test_file = os.path.join(platform_test_result,
                                             TestResultConfig.FILE_DEFAULT)
                    if os.path.isfile(test_file):
                        if platform not in self.test_result:
                            self.test_result[platform] = {}
                        test_result_handler = TestResultHandler(input_file=test_file)
                        for test_name in test_result_handler.data:
                            self.test_result[platform][test_name] = \
                                test_result_handler.data[test_name]
                    elif self.log_level >= 0:
                        self.logger.log_and_print("Has no test result file from node {0}".format(
                            node.name))
                    # Combine compare result
                    compare_file = os.path.join(platform_test_result,
                                                CompareResultConfig.FILE_DEFAULT)
                    if os.path.isfile(compare_file):
                        if platform not in self.compare_result:
                            self.compare_result[platform] = {}
                        compare_result_handler = CompareResultHandler(
                            input_file=compare_file)
                        for test_name in compare_result_handler.data:
                            self.compare_result[platform][test_name] = \
                                compare_result_handler.data[test_name]
                    elif self.log_level >= 0:
                        self.logger.log_and_print("Has no compare result file from node {0}"
                                                  "".format(node.name))

                    if self.is_check_memory_peak:
                        # Combine memory peak result
                        mem_peak_file = os.path.join(platform_test_result,
                                                     TestResultConfig.MEM_PEAK_FILE)
                        if os.path.isfile(mem_peak_file):
                            if platform not in self.mem_peak_info:
                                self.mem_peak_info[platform] = {}
                            mem_peak = read_json(mem_peak_file)
                            for test_name in mem_peak:
                                self.mem_peak_info[platform][test_name] = \
                                    mem_peak[test_name]
                        elif self.log_level >= 0:
                            self.logger.log_and_print(
                                "Has no combine result file from node {0}"
                                "".format(node.name))

    def create_report(self):
        self.logger.start_step("Make reports")
        for platform in configs.common.SupportedPlatform:
            self.logger.log_and_print("\tReport for {0}".format(platform))
            # Make report folder
            platform_test_result_folder = os.path.join(platform,
                                                       FinalTestResult.TEST)
            if not os.path.isdir(platform_test_result_folder):
                continue
            self.set_final_paths(platform)
            if not os.path.exists(self.final_report_folder):
                os.makedirs(self.final_report_folder)
            # Make overall information report
            self.make_overall_report(platform=platform)

            # Make bounding box accuracy report
            self.make_bb_accuracy_report()

            # Make text accuracy report
            self.make_text_accuracy_report()

            # Make barcode accuracy report
            self.make_barcode_accuracy_report()

            # Make bounding box error types report
            self.make_bb_error_types_report()

            # Make text error types report
            self.make_text_error_types_report()

            # Make memory peak report (tsv file)
            self.make_memory_peak_tsv_report()

            # Make memory peak report (xlsx file)
            self.make_memory_peak_report(platform=platform)

            # Make junit xml report
            self.make_junit_xml_report()

            if self.info_handler.is_check_memory_leak():
                # Make report for checking memory leak
                self.make_memory_leak_report()

            if self.is_check_memory_peak:
                # Make report for checking memory peak
                self.make_mem_peak_report()

        # Do make report
        for reporter in self.list_reporters:
            try:
                reporter.do_work()
            except:
                var = traceback.format_exc()
                self.logger.log_and_print(var)
        # End of processes
        self.logger.end_step(True)

    def make_overall_report(self, platform):
        # Get report file name and specific by change number and
        # delta version
        suffix = "_" + self.suffix_report
        file_name = OIRConfiguration.FILE_NAME_DEFAULT.format(suffix=suffix)
        final_text_accuracy_report = os.path.join(self.final_report_folder,
                                                  file_name)
        # Initial reporter and add to reporters list
        self.list_reporters.append(
            OverallInformationReporter(test_file=self.final_test_file,
                                       compare_file=self.final_compare_file,
                                       test_folder=self.final_spec_folder,
                                       error_folder=self.final_error_folder,
                                       change_number=self.change_number,
                                       delta_version=self.delta_version,
                                       output_file=final_text_accuracy_report,
                                       platform=platform)
        )

    def make_bb_accuracy_report(self):
        # Get report file name and specific by change number and
        # delta version
        suffix = "_" + self.suffix_report
        file_name = BB_ACCURACY_REPORT_DEFAULT_NAME.format(suffix=suffix)
        final_bb_accuracy_report = os.path.join(self.final_report_folder,
                                                file_name)
        # Initial reporter and add to reporters list
        self.list_reporters.append(
            BbAccuracyReporter(test_file=self.final_test_file,
                               compare_file=self.final_compare_file,
                               test_folder=self.final_spec_folder,
                               change_number=self.change_number.replace("C", ""),
                               delta=self.delta_version.replace("D", ""),
                               output_file=final_bb_accuracy_report)
        )

    def make_text_accuracy_report(self):
        # Get report file name and specific by change number and
        # delta version
        suffix = "_" + self.suffix_report
        file_name = TEXT_ACCURACY_REPORT_DEFAULT_NAME.format(suffix=suffix)
        final_text_accuracy_report = os.path.join(self.final_report_folder, file_name)
        # Initial reporter and add to reporters list
        self.list_reporters.append(
            TextAccuracyReporter(test_file=self.final_test_file,
                                 compare_file=self.final_compare_file,
                                 test_folder=self.final_spec_folder,
                                 change_number=self.change_number.replace("C", ""),
                                 delta=self.delta_version.replace("D", ""),
                                 output_file=final_text_accuracy_report)
        )

    def make_barcode_accuracy_report(self):
        # Get report file name and specific by change number and
        # delta version
        suffix = "_" + self.suffix_report
        file_name = BCARConfiguration.FILE_NAME_DEFAULT.format(suffix=suffix)
        final_barcode_accuracy_report = os.path.join(self.final_report_folder,
                                                     file_name)
        # Initial reporter and add to reporters list
        self.list_reporters.append(
            BarcodeAccuracyReporter(test_file=self.final_test_file,
                                    compare_file=self.final_compare_file,
                                    test_folder=self.final_spec_folder,
                                    output_file=final_barcode_accuracy_report)
        )

    def make_bb_error_types_report(self):
        # Get report file name and specific by change number and
        # delta version
        suffix = "_" + self.suffix_report
        file_name = BB_ERROR_TYPES_REPORT_NAME_DEFAULT.format(suffix=suffix)
        final_bb_error_types_report = os.path.join(self.final_report_folder,
                                                   file_name)
        # Initial reporter
        self.list_reporters.append(
            BbErrorTypesReporter(test_file=self.final_test_file,
                                 compare_file=self.final_compare_file,
                                 test_folder=self.final_spec_folder,
                                 output_file=final_bb_error_types_report)
        )

    def make_text_error_types_report(self):
        # Get report file name and specific by change number and
        # delta version
        suffix = "_" + self.suffix_report
        file_name = TEXT_ERROR_TYPES_REPORT_NAME_DEFAULT.format(suffix=suffix)
        final_text_error_types_report = os.path.join(self.final_report_folder,
                                                     file_name)
        # Initial reporter
        self.list_reporters.append(
            TextErrorTypesReporter(test_file=self.final_test_file,
                                   compare_file=self.final_compare_file,
                                   test_folder=self.final_spec_folder,
                                   output_file=final_text_error_types_report)
        )

    def make_memory_peak_tsv_report(self):
        """
        Get memory peak information to report to tsv file

        -------

        """
        suffix = "_" + self.suffix_report
        file_name = MEM_PEAK_TSV_FILE_NAME_DEFAULT.format(suffix=suffix)
        final_memory_peak_tsv_report = os.path.join(self.final_report_folder,
                                                    file_name)
        # Initial reporter
        self.list_reporters.append(MemPeakTsvReporter(
            test_file=self.final_test_file,
            test_folder=self.final_spec_folder,
            output_file=final_memory_peak_tsv_report))

    def make_memory_peak_report(self, platform):
        """
        Report memory peak information to xlsx file

        Returns
        -------

        """
        suffix = "_" + self.suffix_report
        file_name = MEM_PEAK_REPORT_DEFAULT_NAME.format(suffix=suffix)
        final_memory_peak_report = os.path.join(self.final_report_folder,
                                                file_name)
        # Initial reporter
        self.list_reporters.append(MemPeakReporter(
            test_file=self.final_test_file,
            test_folder=self.final_spec_folder,
            output_file=final_memory_peak_report,
            platform=platform,
            change_number=self.change_number,
            delta=self.delta_version))

    def make_junit_xml_report(self):
        # Get report file name and specific by change number and
        # delta version
        suffix = "_" + self.suffix_report
        file_name = JXRConfiguration.FILE_NAME_DEFAULT.format(suffix=suffix)
        final_junit_xml_report = os.path.join(self.final_report_folder,
                                              file_name)
        # Initial reporter
        self.list_reporters.append(
            JunitXmlReporter(test_file=self.final_test_file,
                             compare_file=self.final_compare_file,
                             output_file=final_junit_xml_report)
        )

    def make_memory_leak_report(self):
        # Get report file name and specific by change number and
        # delta version
        suffix = "_" + self.suffix_report
        file_name = DATConfiguration.FILE_NAME.format(suffix=suffix)
        final_file_report = os.path.join(self.final_report_folder, file_name)
        # Initial reporter and add to reporters list
        self.list_reporters.append(
            PHOcrDeltaMemoryLeakReporter(test_folder=self.final_spec_folder,
                                         test_file=self.final_test_file,
                                         compare_file=self.final_compare_file,
                                         error_folder=self.final_error_folder,
                                         change_number=self.change_number,
                                         delta_version=self.delta_version,
                                         output_file=final_file_report))

    def make_mem_peak_report(self):
        # Get report file name and specific by change number and
        # delta version
        suffix = "_" + self.suffix_report
        file_name = MemPeakReportConfiguration.FILE_NAME.format(suffix=suffix)
        final_file_report = os.path.join(self.final_report_folder,
                                         file_name)
        # Initial reporter and add to reporters list
        self.list_reporters.append(
            PHOcrMemoryPeakReporter(test_folder=self.final_spec_folder,
                                    test_file=self.final_test_file,
                                    combine_file=self.final_mem_peak_info_file,
                                    error_folder=self.final_error_folder,
                                    change_number=self.change_number,
                                    delta_version=self.delta_version,
                                    output_file=final_file_report))

    def get_suffix_report(self):
        self.suffix_report = ""
        if self.change_number:
            self.suffix_report += "C{0}_".format(self.change_number)
        self.suffix_report += "D{0}".format(self.delta_version)

    def get_more_log(self):
        """
        There are something to archive for test job on master:
        - Collect test distribution file into system information folder
        - Make reports for performance of automation test system on test job

        Returns
        -------
        None

        """
        log_folder_by_run_time = \
            configs.run_counter.RUN_FOLDER_TEMPLATE.format(count=configs.run_counter.RUN_COUNT)
        final_log_folder = os.path.join(self.log_folder, log_folder_by_run_time)
        # Arrange distribution file
        copy_paths(self.distribution_file, final_log_folder)

        # Path to log folder of test system for both of build and test. This will be used to
        # generate report for performance of automation test system
        system_log_folder = os.path.join(FinalTestResult.INFO, FinalTestResult.LOG)
        # Path to directory which will be used to storage system performance reports
        target_directory = os.path.join(FinalTestResult.INFO,
                                        FinalTestResult.Log.SYSTEM_PERFORMANCE,
                                        FinalTestResult.Log.SYSTEM_PERFORMANCE_TEST)
        # Initial reports generator
        reports_generator = SystemPerformanceReportsGenerator(log_folder=system_log_folder,
                                                              output_folder=target_directory)
        # Generate reports for performance of system on test job
        reports_generator.generate_test_performance_reports()

    def get_work_nodes(self):
        return self.distribution_handler.get_test_nodes(self.profile_handler)

    # Combine test results of success workers
    def combine_result_when_node_not_done_exception(self):
        self.combine_test_results()

    def create_force_spec_file(self):
        force_spec_info = self.info_handler.get_spec_updated_from_commit_message()
        if force_spec_info:
            write_json(force_spec_info, TestcaseConfig.FORCE_SPEC_FILE)
