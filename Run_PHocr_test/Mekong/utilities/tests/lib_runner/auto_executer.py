# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created:     30/06/2017
# Last updated:     30/06/2017
# Update by:        Phung Dinh Tai
# Description:      This script define a class for auto select executer to execute base on
#                   test case specification
import os

from baseapi.common import get_files_in_folder
from configs.auto_command import FunctionMapping, LanguageOption
from configs.common import SupportedImage, Platform
from configs.database import TestcaseConfig, SpecKeys
from configs.json_key import LanguageOptConfig
from configs.projects.hanoi import HanoiProject
from configs.projects.phocr import PhocrProject
from configs.timeout import TimeOut
from handlers.test_spec_handler import TestSpecHandler
from tests.lib_runner.barcode_test_executer import BarcodeTestExecuter
from tests.lib_runner.hanoi_test_executer import HanoiTestExecuter
from tests.lib_runner.memory_check_executer import MemCheckExecutor
from tests.lib_runner.phocr_test_executer import PHOcrTestExecuter
from tests.lib_runner.binary_test_executer import BinaryTestExecuter
from configs.test_result import TestResultJsonKeys

# TODO: Move test configuration to configure file
binaries_platforms = {
    Platform.LINUX: {
        PhocrProject.components.DEFAULT: PhocrProject.components.DEFAULT,
        PhocrProject.components.BARCODE: PhocrProject.components.BARCODE,
        HanoiProject.components.DEFAULT: HanoiProject.components.DEFAULT
    },
    Platform.WINDOWS: {
        PhocrProject.components.DEFAULT: "PHOcrExe.exe",
        PhocrProject.components.BARCODE: "barcode.exe",
        HanoiProject.components.DEFAULT: "HanoiWorkflow.exe"
    }
}


class AutoTestExecuter():
    def __init__(self, test_folder, bin_folders, test_id, platform):

        self.test_folder = test_folder
        self.test_id = test_id

        # Initial handler for specification
        spec_file = os.path.join(test_folder, test_id, TestcaseConfig.SPEC_FILE)
        self.spec_handler = TestSpecHandler(input_file=spec_file)
        self.bin_folders = bin_folders
        self.platform = platform

    def get_phocr_params(self):
        # Get parameters of command line
        self.params = ""
        product = self.spec_handler.get_product()
        component = self.spec_handler.get_component()
        functionalities = self.spec_handler.get_functions()
        for funct in functionalities:
            try:
                if funct:
                    self.params += FunctionMapping[product][component][funct.lower()] + " "
            except:
                print "\tNo option is defined for functionality \"{0}\"".format(funct)

        # Options follow tags
        self.params += self.spec_handler.get_tag(SpecKeys.Tags.CMD_OPTION)

        # Option for language
        if LanguageOption[product][component] is not None:
            langs = self.spec_handler.get_tag(tag=SpecKeys.Tags.LANGS)
            lang_opt = " "
            # is_cj = False
            for language in langs:
                if (language == "chinesesimplified") \
                        or (language == "chinesetraditional") \
                        or (language == "japanese"):
                    if (PhocrProject.functionalities.EXPORT_DOCX not in functionalities) \
                            and (PhocrProject.functionalities.EXPORT_EXCEL not in functionalities) \
                            and (PhocrProject.functionalities.EXPORT_PPTX not in functionalities):
                        is_cj = True
                    break
            lang_opt += LanguageOption[product][component][LanguageOptConfig.OPTION]
            if lang_opt:
                lang_opt += " "

            for language in langs:
                try:
                    lang_opt += language
                    lang_opt += LanguageOption[product][component][LanguageOptConfig.DELIMITER]
                except:
                    pass

            if lang_opt:
                self.params += lang_opt[:-1]

    def run(self):

        timeout = self.spec_handler.get_weight(platform=self.platform) * \
                  TimeOut.execute.RATIO_TIMEOUT_RUN_ONE
        if timeout < TimeOut.execute.MINIMUM_TIMEOUT_RUN_ONE:
            timeout = TimeOut.execute.MINIMUM_TIMEOUT_RUN_ONE

        # PHOcr project
        if self.spec_handler.get_product() == PhocrProject.PRODUCT:
            # PHOcrExe test runner
            if self.spec_handler.get_component() == PhocrProject.components.DEFAULT:
                self.get_phocr_params()
                auto_executor = PHOcrTestExecuter()
                # Memory check test runner
                is_check_memory_leak = self.spec_handler.get_tag(
                    SpecKeys.Tags.IS_MEMCHECK)
                is_check_memory_peak = False
                if self.spec_handler.has_tag(SpecKeys.Tags.IS_MEMCHECK_PEAK):
                    is_check_memory_peak = self.spec_handler.get_tag(
                        SpecKeys.Tags.IS_MEMCHECK_PEAK)
                if is_check_memory_leak or is_check_memory_peak:
                    print "Memory checking"
                    auto_executor = MemCheckExecutor(is_check_memory_peak)
                binary_name = self.get_binary_name_corresponding_with_component(
                    PhocrProject.components.DEFAULT
                )
                bin_path = self.find_binary_path(binary_name)
                test_data_dir = os.path.join(self.test_folder,
                                             self.test_id,
                                             TestcaseConfig.TEST_DATA_DIR)
                image_files = get_files_in_folder(test_data_dir, SupportedImage)
                if not image_files:
                    return {
                        TestResultJsonKeys.STDOUT: "",
                        TestResultJsonKeys.STDERR: "Missing test data!",
                        TestResultJsonKeys.TIME: 0,
                        TestResultJsonKeys.CODE: 1,
                        TestResultJsonKeys.MEMORY: []
                    }
                return auto_executor.execute_test(test_tool=bin_path,
                                                  params=self.params,
                                                  image_path=image_files[0],
                                                  timeout=timeout)

            # Barcode test runner
            if self.spec_handler.get_component() == PhocrProject.components.BARCODE:
                self.get_phocr_params()
                auto_executor = BarcodeTestExecuter()
                # Memory check test runner
                is_check_memory_leak = self.spec_handler.get_tag(
                    SpecKeys.Tags.IS_MEMCHECK)
                is_check_memory_peak = False
                if self.spec_handler.has_tag(SpecKeys.Tags.IS_MEMCHECK_PEAK):
                    is_check_memory_peak = self.spec_handler.get_tag(
                        SpecKeys.Tags.IS_MEMCHECK_PEAK)
                if is_check_memory_leak or is_check_memory_peak:
                    print "Memory checking"
                    auto_executor = MemCheckExecutor(is_check_memory_peak)
                binary_name = self.get_binary_name_corresponding_with_component(
                    PhocrProject.components.BARCODE
                )
                bin_path = self.find_binary_path(binary_name)
                test_data_dir = os.path.join(self.test_folder,
                                             self.test_id,
                                             TestcaseConfig.TEST_DATA_DIR)
                image_files = get_files_in_folder(test_data_dir)
                if not image_files:
                    return {
                        TestResultJsonKeys.STDOUT: "",
                        TestResultJsonKeys.STDERR: "Missing test data!",
                        TestResultJsonKeys.TIME: 0,
                        TestResultJsonKeys.CODE: 1,
                        TestResultJsonKeys.MEMORY: []
                    }
                return auto_executor.execute_test(test_tool=bin_path,
                                                  params=self.params,
                                                  image_path=image_files,
                                                  timeout=timeout)
            if self.spec_handler.get_component() == PhocrProject.components.BINARY_TEST:
                #  In this case we support for new binaries
                # params will take from tags.CommandLineOptions field
                binary_test_information = self.spec_handler.get_binary_test_information()

                auto_executor = BinaryTestExecuter()
                # Memory check test runner
                is_check_memory_leak = self.spec_handler.get_tag(
                    SpecKeys.Tags.IS_MEMCHECK)
                is_check_memory_peak = False
                if self.spec_handler.has_tag(SpecKeys.Tags.IS_MEMCHECK_PEAK):
                    is_check_memory_peak = self.spec_handler.get_tag(
                        SpecKeys.Tags.IS_MEMCHECK_PEAK)
                if is_check_memory_leak or is_check_memory_peak:
                    print "Memory checking"
                    auto_executor = MemCheckExecutor(is_check_memory_peak)
                binary_name = binary_test_information[
                    SpecKeys.BinaryTestInformation.BINARY_NAME]

                # For linux, binary_executer named is the same with binary_name
                # but on windows, we need to add suffix "*.exe" to binary_name
                if self.platform == Platform.WINDOWS:
                    binary_name = binary_name + ".exe"

                bin_path = self.find_binary_path(binary_name)
                test_data_dir = os.path.join(self.test_folder,
                                             self.test_id,
                                             TestcaseConfig.TEST_DATA_DIR)

                full_command = binary_test_information[
                    SpecKeys.BinaryTestInformation.TEST_COMMAND
                ]

                # Need to make sure use unique format '/'
                full_command = full_command.replace("\\", "/")

                # TODO(Huan) for current design of BinaryTestExecuter class
                # input image must be specify in the last option in "test_command" field
                configure_input_image = full_command.split(" ")[-1:][0]
                params = full_command.replace(configure_input_image, "")

                # Remove defined variable
                real_input_image_path = configure_input_image.replace(
                    SpecKeys.BinaryTestInformation.Variable.TEST_DATA,
                    test_data_dir
                )

                real_input_image_path = real_input_image_path.encode('ascii')

                return auto_executor.execute_test(test_tool=bin_path,
                                                  params=params,
                                                  image_path=real_input_image_path,
                                                  timeout=timeout)

        # Hanoi project
        if self.spec_handler.get_product() == HanoiProject.PRODUCT:
            auto_executor = HanoiTestExecuter()
            test_data_dir = os.path.join(self.test_folder,
                                         self.test_id,
                                         TestcaseConfig.TEST_DATA_DIR)
            config_file = self.find_only_one_hanoiworkflow_config_file(test_data_dir)
            image_files = get_files_in_folder(test_data_dir, SupportedImage)
            if not image_files:
                return {
                    TestResultJsonKeys.STDOUT: "",
                    TestResultJsonKeys.STDERR: "Missing test data!",
                    TestResultJsonKeys.TIME: 0,
                    TestResultJsonKeys.CODE: 1,
                    TestResultJsonKeys.MEMORY: []
                }
            binary_name = self.get_binary_name_corresponding_with_component(
                HanoiProject.components.DEFAULT
            )
            bin_path = self.find_binary_path(binary_name)
            return auto_executor.execute_test(test_tool=bin_path,
                                              image_path=image_files[0],
                                              config_file=config_file,
                                              timeout=timeout)

    def find_binary_path(self, binary_name):

        for bin_folder in self.bin_folders:
            f_path = os.path.join(bin_folder, binary_name)
            if os.path.isfile(f_path):
                return f_path
        error_msg = "Does not find binary named {0}".format(binary_name)
        raise Exception(error_msg)

    def get_binary_name_corresponding_with_component(self, component):
        return binaries_platforms[self.platform][component]

    @staticmethod
    def find_only_one_hanoiworkflow_config_file(test_data_dir):
        found_files = []
        for file in os.listdir(test_data_dir):
            if file.endswith(".wpr"):
                wf_config_file = os.path.join(test_data_dir, file)
                found_files.append(wf_config_file)
        if len(found_files) == 0:
            error_msg = "Does not found Hanoi workflow configure file in {0}". \
                format(test_data_dir)
            raise Exception(error_msg)
        elif len(found_files) > 1:
            error_msg = "There are more than 1 workflow conifgure file in {0}". \
                format(test_data_dir)
            raise Exception(error_msg)

        return found_files[0]
