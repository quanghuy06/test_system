# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      28/12/2016
# Last update:      31/03/2106
# Description:      This configure mekong structure

import sys_path
sys_path.insert_sys_path()

import os
from configs.projects.saigon import SaigonProject

# Configure absolute path to modules or files of mekong utilities
absolute_path = dict()
absolute_path["baseapi"] = os.path.join(sys_path.utilities_dir, "baseapi")
absolute_path["configs"] = os.path.join(sys_path.utilities_dir, "configs")
absolute_path["profile"] = os.path.join(absolute_path["configs"], "profile.json")
absolute_path["manager"] = os.path.join(sys_path.utilities_dir, "manager")
absolute_path["mekong"] = os.path.join(sys_path.utilities_dir, "mekong")
absolute_path["tests"] = os.path.join(sys_path.utilities_dir, "tests")
absolute_path["lib_base"] = os.path.join(absolute_path["tests"], "lib_base")
absolute_path["lib_runner"] = os.path.join(absolute_path["tests"], "lib_runner")
absolute_path["executables"] = os.path.join(absolute_path["tests"], "executables")
absolute_path["compare_sample"] = os.path.join(absolute_path["tests"], "compare_sample")
absolute_path["lib_workspace"] = os.path.join(absolute_path["manager"], "lib_workspace")
absolute_path["lib_manager"] = os.path.join(absolute_path["manager"], "lib_manager")
absolute_path["send_email"] = os.path.join(sys_path.utilities_dir, "send_email")

# Configure relative path to modules or files of mekong utilities
relative_path = dict()
mekong_folder_name = "Mekong"
relative_path["utilities"] = os.path.join(mekong_folder_name, "utilities")
relative_path["configs"] = os.path.join(relative_path["utilities"], "configs")
relative_path["examples"] = os.path.join(relative_path["configs"], "examples")
relative_path["baseapi"] = os.path.join(relative_path["utilities"], "baseapi")
relative_path["manager"] = os.path.join(relative_path["utilities"], "manager")
relative_path["mekong"] = os.path.join(relative_path["utilities"], "mekong")
relative_path["tests"] = os.path.join(relative_path["utilities"], "tests")


class MekongProject(object):
    NAME = "Mekong"
    ROOT = "utilities"
    ROOT_PATH = os.path.join(NAME, ROOT)
    ROOT_PATH_REL = os.path.join(NAME, ROOT)
    ROOT_PATH_ABS = sys_path.utilities_dir
    EXEC_SAIGON_LINUX_ABS = os.path.join(absolute_path["executables"],
                                         SaigonProject.components.DEFAULT)
    EXEC_SAIGON_WINDOWS_ABS = os.path.join(absolute_path["executables"],
                                           SaigonProject.components.WIN_DEFAULT)

    class module(object):
        TEST = "tests"
        MANAGER = "manager"
        CONFIGURATION = "configs"
        CHECKOUT = "mekong"
        BASE = "baseapi"
        REPORT = "report"
        OTHER = "other"
        SCRIPTS = "scripts"
        DEFAULT = "default"
        JENKINS = "jenkins"

    class other:
        BACKUP = "backup"
        JENKINS = "jenkins"

    class libs:
        DB = "lib_base"
        MANAGER = "lib_manager"
        EXECUTABLES = "executables"


# Third party of Mekong configuration
# Configure for valgrind usage. This is third party to run memory leak check test cases
class ValGrind(object):
    # Name of used folder, binary, directory
    BIN_FOLDER = "bin"
    LIB_FOLDER = "lib"
    LIB_ENV = "valgrind"
    VALGRIND_FOLDER = "valgrind-3.13.0"
    VALGRIND_PACKAGE = "valgrind-3.13.0.tgz"
    BINARY = "valgrind"
    # Configuration for options of run command
    OPT_LOG_FILE = "--log-file={log_file}"
    OPT_LEAK_CHECK = "--leak-check={opt}"
    OPT_PEAK_CHECK = "--tool=massif"
    # Some default values
    LOG_FILE_DEFAULT = "memcheck.log"
    LEAK_CHECK_FULL = "full"
    # Environment variable usage
    ENV_LIB = "VALGRIND_LIB"


class UsedScript(object):
    CHECKOUT = "checkout_scm.py"
    PROFILE = "profile.json"
    WORKERS_MANAGER = "workers_manager.py"
    DISTRIBUTE_TESTSET = "distributor_main.py"
    RUN_ALL = "run_all.py"
    JUNIT_EXPORT = "export_junit_result.py"
    NODE_MANAGE = "test_node_manager.py"
    SEND_EMAIL = "send_email.py"
    GET_TEST_CASES = "get_test_cases.py"
    RUN_TEST_BAT = "run_test.bat"
    # Script to update test cases from database to a target test cases folder on local machine
    UPDATE_TEST_CASES_FOLDER = "update_test_cases_folder.py"


class ScriptPath(object):
    # Used scripts
    CHECKOUT_REL = os.path.join(MekongProject.ROOT_PATH_REL,
                                MekongProject.module.CHECKOUT,
                                UsedScript.CHECKOUT)
    PROFILE_ABS = os.path.join(MekongProject.ROOT_PATH_ABS,
                               MekongProject.module.CONFIGURATION,
                               UsedScript.PROFILE)
    PROFILE_REL = os.path.join(MekongProject.ROOT_PATH_REL,
                               MekongProject.module.CONFIGURATION,
                               UsedScript.PROFILE)
    WORKERS_MANAGER = os.path.join(MekongProject.ROOT_PATH_REL,
                                   MekongProject.module.MANAGER,
                                   UsedScript.WORKERS_MANAGER)
    DISTRIBUTE_TESTSET = os.path.join(MekongProject.ROOT_PATH_REL,
                                      MekongProject.module.MANAGER,
                                      UsedScript.DISTRIBUTE_TESTSET)
    RUN_ALL = os.path.join(MekongProject.ROOT_PATH_REL,
                           MekongProject.module.TEST,
                           UsedScript.RUN_ALL)
    GET_TEST_CASES = os.path.join(MekongProject.ROOT_PATH_ABS,
                                  MekongProject.module.TEST,
                                  UsedScript.GET_TEST_CASES)
    JUNIT_EXPORT = os.path.join(MekongProject.ROOT_PATH_ABS,
                                MekongProject.module.TEST,
                                UsedScript.JUNIT_EXPORT)
    NODE_MANAGE = os.path.join(MekongProject.ROOT_PATH_REL,
                               MekongProject.module.MANAGER,
                               UsedScript.NODE_MANAGE)
    RUN_TEST_BAT_PATH = os.path.join(MekongProject.ROOT_PATH_REL,
                                     MekongProject.module.SCRIPTS,
                                     UsedScript.RUN_TEST_BAT)
    UPDATE_TEST_CASE_FOLDER = os.path.join(MekongProject.ROOT_PATH_REL,
                                           MekongProject.module.JENKINS,
                                           UsedScript.UPDATE_TEST_CASES_FOLDER)
    # Default configure files


# These class define some scripts and configurations default in Mekong utilities that
# are used for test system
class TestSystemScripts(object):
    # Checkout source code
    CHECKOUT = "checkout_scm.py"
    RUN_ALL = "run_all.py"
    # Node manager
    NODE_MANAGE = "test_node_manager.py"
    DISTRIBUTE_TESTSET = "distributor_main.py"
    JUNIT_EXPORT = "export_junit_result.py"
    CLEAN_WS = "prepare_workspace.sh"
    # Update data
    POST_INTEGRATION = "update_reference_data_post_integration.py"
    # Report data
    REPORT_DELTA_PERFORMANCE = "report_delta_performance.py"
    REPORT_DELTA_BB_ACCURACY = "report_delta_bb_accuracy.py"
    REPORT_DELTA_TEXT_ACCURACY = "report_delta_text_accuracy.py"


class TestSystemConfigureFiles(object):
    PROFILE = "profile.json"
    BUILD_CONFIGURE = "configure_build.json"
    SEND_EMAIL_CONFIGURE = "send_report_config.json"


class TestSystemPaths(object):
    # Used scripts
    CHECKOUT = os.path.join(MekongProject.ROOT_PATH, MekongProject.module.CHECKOUT,
                            TestSystemScripts.CHECKOUT)
    RUN_ALL = os.path.join(MekongProject.ROOT_PATH,
                           MekongProject.module.TEST,
                           TestSystemScripts.RUN_ALL)
    # Node manager
    NODE_MANAGE = os.path.join(MekongProject.ROOT_PATH,
                               MekongProject.module.MANAGER,
                               TestSystemScripts.NODE_MANAGE)
    DISTRIBUTE_TESTSET = os.path.join(MekongProject.ROOT_PATH,
                                      MekongProject.module.MANAGER,
                                      TestSystemScripts.DISTRIBUTE_TESTSET)
    JUNIT_EXPORT = os.path.join(MekongProject.ROOT_PATH,
                                MekongProject.module.TEST,
                                TestSystemScripts.JUNIT_EXPORT)
    # Default configure files
    PROFILE = os.path.join(MekongProject.ROOT_PATH,
                           MekongProject.module.CONFIGURATION,
                           MekongProject.module.DEFAULT,
                           TestSystemConfigureFiles.PROFILE)
    BUILD_CONFIGURE = os.path.join(MekongProject.ROOT_PATH,
                                   MekongProject.module.CONFIGURATION,
                                   MekongProject.module.DEFAULT,
                                   TestSystemConfigureFiles.BUILD_CONFIGURE)
    SEND_EMAIL_CONFIGURE = os.path.join(MekongProject.ROOT_PATH_ABS,
                                        MekongProject.module.CONFIGURATION,
                                        MekongProject.module.DEFAULT,
                                        TestSystemConfigureFiles.SEND_EMAIL_CONFIGURE)
    # Update data
    POST_INTERGRATION = os.path.join(MekongProject.ROOT_PATH,
                                     MekongProject.module.JENKINS,
                                     TestSystemScripts.POST_INTEGRATION)
    # Report data
    REPORT_DELTA_PERFORMANCE = os.path.join(MekongProject.ROOT_PATH,
                                            MekongProject.module.REPORT,
                                            TestSystemScripts.REPORT_DELTA_PERFORMANCE)
    REPORT_DELTA_ACCURACY = os.path.join(MekongProject.ROOT_PATH,
                                         MekongProject.module.REPORT,
                                         TestSystemScripts.REPORT_DELTA_BB_ACCURACY)

    # Other scripts/files
    CLEAN_WORKSPACE = os.path.join(MekongProject.ROOT_PATH,
                                   MekongProject.module.OTHER,
                                   TestSystemScripts.CLEAN_WS)

    # Executes folder
    EXECUTABLES_DIR = os.path.join(MekongProject.ROOT_PATH,
                                   MekongProject.module.TEST,
                                   MekongProject.libs.EXECUTABLES)

    # Absolutely path of executables
    EXECUTABLES_ABS_DIR = os.path.join(MekongProject.ROOT_PATH_ABS,
                                       MekongProject.module.TEST,
                                       MekongProject.libs.EXECUTABLES)


class TestSystemUtilities:
    def __init__(self):
        self.Scripts = TestSystemScripts()
        self.ConfigureFiles = TestSystemConfigureFiles()
        self.Paths = TestSystemPaths()

# Initial an instance of TestSystemUtilites. To use all above configure, only need
# to import this object.
TestSystem = TestSystemUtilities()


class SystemInfo(object):
    F_SUCCESS = "Success"
    F_FAILED = "Failed"
    SYSTEM_INFO_FILE = "system_info.json"
