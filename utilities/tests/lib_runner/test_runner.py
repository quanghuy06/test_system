# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Le Duc Nam
# Email:            nam.leduc@toshiba-tsdv.com
# Date create:      20/11/2017
# Last update:      30/06/2107
# Editor:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Description:      Class for running test

import imp
import os
import csv
import platform
import shutil
import sys
import traceback
import time

from baseapi.file_access import remove_paths, find_file_in_folders
from configs.common import Platform
from configs.database import TestcaseConfig, SpecKeys
from configs.projects.phocr import PhocrProject
from configs.test_result import TestResultJsonKeys
from handlers.test_spec_handler import TestSpecHandler
from tests.lib_runner.auto_executer import AutoTestExecuter, binaries_platforms
from baseapi.file_access import write_text
from configs.json_key import TestResultJson
from configs.test_result import FinalTestResult
from configs.test_result import TestResultConfig

###########################################################################
class TestRunner:
    # Get test case folder depend on test folder and test case ID
    def get_test_case_data(self, working_dir, test_folder, test_id):
        test_case_folder = os.path.join(working_dir, test_folder, test_id)

        if not os.path.exists(test_case_folder):
            raise Exception("Path \"" + test_case_folder + "\" not exists")

        test_runner_path = os.path.join(test_case_folder, TestcaseConfig.SCRIPT_DIR,
                                        TestcaseConfig.Scripts.TEST)

        return [test_case_folder, test_runner_path]

    ###########################################################################
    def change_to_output_dir(self, output_folder):
        # Change current directory before run real test
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        os.chdir(output_folder)

    ###########################################################################
    def comeback_workingdir(self, working_dir):
        os.chdir(working_dir)

    ###########################################################################
    def move_output_to_test_case_folder(self, test_case_folder, output_folder):

        # Check platform before moving
        sys_str = platform.system()
        if sys_str.lower() == Platform.LINUX:  # If platform is Linux
            test_case_folder_output = os.path.join(test_case_folder,
                                                   TestcaseConfig.OUTPUT_FOLDER,
                                                   Platform.LINUX)
        elif sys_str.lower() == Platform.WINDOWS:  # If platform is Windows
            test_case_folder_output = os.path.join(test_case_folder,
                                                   TestcaseConfig.OUTPUT_FOLDER,
                                                   Platform.WINDOWS)
        else: # If other platforms
            raise Exception(sys_str + " is not tested")

        if os.path.isdir(test_case_folder_output):
            shutil.rmtree(test_case_folder_output, ignore_errors = False)

        shutil.copytree(output_folder, test_case_folder_output)

    ###########################################################################
    # Run one test case and move output to test case folder
    def run(self, test_folder, abs_bin_folders, test_id, plf):
        abs_test_folder = os.path.abspath(test_folder)
        curr_dir = os.getcwd() # Directory run this scripts
        tmp_folder = 'e7968b1d-19c6-43e4-bc07-d203d893a4be_test_{0}_{1}'
        tmp_folder = tmp_folder.format(test_id, plf)
        tmp_folder_path = os.path.join(curr_dir, tmp_folder)

        # Name of test case runner
        test_case_folder = os.path.join(abs_test_folder, test_id)
        test_runner_path = os.path.join(abs_test_folder, test_id, TestcaseConfig.SCRIPT_DIR,
                                        TestcaseConfig.Scripts.TEST)

        self.change_to_output_dir(tmp_folder_path)

        start_time = time.time()
        # Load runner of test cases
        try:
            mod_name, file_ext = os.path.splitext(os.path.split(test_runner_path)[-1])

            # Add path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            sys.path.append(current_dir)

            # Load user defined script
            if os.path.isfile(test_runner_path):
                # Test with user defined script
                spec_file = os.path.join(abs_test_folder, test_id, TestcaseConfig.SPEC_FILE)
                spec_handler = TestSpecHandler(input_file=spec_file)
                if spec_handler.get_component() == PhocrProject.components.BINARY_TEST:
                    binary_test_information = spec_handler.get_binary_test_information()

                    # Memory check test runner
                    binary_name = binary_test_information[SpecKeys.BinaryTestInformation.BINARY_NAME]
                else:
                    binary_name = binaries_platforms[plf][spec_handler.get_component()]
                bin_path = find_file_in_folders(binary_name, abs_bin_folders)
                test_runner = imp.load_source(mod_name, test_runner_path)
                test = test_runner.Test()
                log = test.run(bin_path)
                memory_path = os.path.join(tmp_folder_path, TestResultConfig.PHOCR_MEMORY_LOG)
                memory_peaks = []
                if os.path.isfile(memory_path):
                    with open(memory_path) as csv_file:
                        csv_reader = csv.reader(csv_file, delimiter='\t')
                        line_count = 0
                        for row in csv_reader:
                            if line_count != 0:
                                item_memory_peak = dict()
                                item_memory_peak[
                                    TestResultJsonKeys.MemoryItem.COMMAND
                                ] = '"' + row[0] + '"'
                                item_memory_peak[
                                    TestResultJsonKeys.MemoryItem.MEMORY_PEAK
                                ] = row[1]
                                memory_peaks.append(item_memory_peak)
                            line_count += 1
                    os.remove(memory_path)
                log[TestResultJsonKeys.MEMORY] = memory_peaks
            else:
                # Test with functionality from spec.json
                test_executor = AutoTestExecuter(test_folder=abs_test_folder,
                                                 bin_folders=abs_bin_folders,
                                                 test_id=test_id,
                                                 platform=plf)
                log = test_executor.run()

            # Run test
            if log == None:
                raise Exception('Test run script should return result of execute_test()')

            # Write stderr to file
            write_text(log[TestResultJson.STDERR], FinalTestResult.Test.STDERR_FILE_NAME)
            # Write stdout to file
            write_text(log[TestResultJson.STDOUT], FinalTestResult.Test.STDOUT_FILE_NAME)

            # On Windows env, we need to change working dir before we move and delete test result
            # in temp folder. Windows will report error
            # "The process cannot access the file because it is being used by another process"
            self.comeback_workingdir(curr_dir)

            # Move output directory to test cases folder
            self.move_output_to_test_case_folder(test_case_folder, tmp_folder_path)
            return log
        except Exception as e:
            # Unit test code throw exception
            print "System error on test case: {0}".format(test_id)
            traceback.print_exc()
            var = traceback.format_exc()

            end_time = time.time()
            running_time = float(end_time - start_time)
            return {
                TestResultJsonKeys.CODE: -1000,
                TestResultJsonKeys.SYSTEM_ERROR: var,
                TestResultJsonKeys.TIME: running_time,
                TestResultJsonKeys.MEMORY: []
            }
        finally:
            # Comback working directory and clean temporary directory
            self.comeback_workingdir(curr_dir)
            remove_paths(tmp_folder)
