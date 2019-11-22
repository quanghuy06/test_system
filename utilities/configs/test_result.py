# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date created: 28/06/2017
# Last update:  03/07/2017
# By:
# Description:  This script define default file, folder, json key of test result
from configs.compare_result import CompareResultConfig


class TestResultConfig(object):

    FILE_DEFAULT = "test_result.json"
    FOLDER_DEFAULT = "test_result"
    FILE_XML_DEFAULT = "test_result.xml"
    PACK_SUFFIX = ".tgz"
    PREFIX = "test_result"
    MEM_CHECK_LOG = "memcheck.log"
    MEM_PEAK_FILE ="mem_peak.json"
    PHOCR_MEM_PEAK_FILE='phocr_memory_peak.csv'
    PHOCR_MEMORY_LOG = 'phocr_memory.log'


class MemCheckInfo(object):

    # LEAK information
    TAG_DEFINITELY = "definitely lost:"
    TAG_INDERECTLY = "indirectly lost:"
    TAG_POSSIBLY = "possibly lost:"
    TAG_REACHABLE = "still reachable:"
    TAG_SUPPRESSED = "suppressed:"
    LEAK_BYTE = "bytes"
    LEAK_BLOCK = "blocks"
    RE_PATTERN = ".* (.*?) bytes in (.*?) .*"
    PARA_PATTERN = "==.*== \r?\n"
    POSSIBLY_IN_PTHREAD = (
        "==(\d+)== (\d+) bytes in (\d+) blocks are possibly lost.*(\r?\n.*)+"
        "pthread_create@@GLIBC.*"
    )
    # ERROR information
    ERROR_SUMMARY = "ERROR SUMMARY:"
    ERROR = "errors"
    ERROR_CONTEXT = "contexts"
    ERR_PATTERN = ".* (.*?) errors from (.*?) contexts"
    PTHREAD_PATTERN = (
        ".*pthread_create@@GLIBC.*libpthread.*so.*(\r?\n.*)+"
        "GOMP_parallel.*libgomp.*so.*"
    )
    DEFLATE_PATTERN = ".*deflate.*libz.*so.*"
    CRC_PATTERN = ".*crc32.*libz.*so.*"
    IO_IN_FILEOPS_PATTERN = (
        ".*_IO_file_write@@GLIBC.*fileops.*c.*\r?\n.*"
        "new_do_write.*fileops.*c.*\r?\n.*"
        "_IO_do_write@@GLIBC.*fileops.*c.*"
    )
    GET_ENV_PATTERN = ".*getenv.*libc.*.so.*"
    STRXFRM_L_PATTERN = ".*strxfrm_l.*libc.*so.*"
    MKSTEMP_PATTERN = ".*mkstemp.*libc.*so.*"
    LOCAL_TIME_PATTERN = ".*localtime.*libc.*so.*"
    NEW_LOCALE_PATTERN = ".*newlocale.*libc.*so.*"
    IO_IN_LIBC_PATTERN = (
        ".*_IO_do_write.*libc.*so.*\r?\n.*"
        "_IO_file_overflow.*libc.*so.*\r?\n.*"
        "_IO_file_xsputn.*libc.*so.*"
    )
    ICONV_OPEN_PATTERN= ".*iconv_open.*libc.*so.*"

class MemPeakInfo(object):
    """
    All information related to checking for memory peak.
    """
    MEM_PEAK_PATTERN = "time.*\nmem_heap_B.*\nmem_heap_extra_B.*\nmem_stacks_B.*\nheap_tree=peak"
    MEM_HEAP_B = "mem_heap_B"
    MEM_HEAP_EXTRA_B = "mem_heap_extra_B"


# Keys of test result json file
class TestResultJsonKeys(object):

    CODE = "exitcode"
    STDERR = "stderr"
    STDOUT = "stdout"
    TIME = "time"
    DETAIL_INFO = "infors"
    OPTION = "options"
    SYSTEM_ERROR = "system error"
    MEMORY = "memory"

    class MemoryItem(object):
        COMMAND = 'command'
        MEMORY_PEAK = 'memory_peak'


# Final name of folder and file of test result of automated test system
class FinalTestResult(object):

    BUILD = "build"
    TEST = "test"
    REPORT = "report"
    LOG = "log"
    INFO = "info"
    RAWDATA = "RawResults"
    FILE_INFO_OVERALL = "OverallInformation.txt"
    FILE_REPORT_ACCURACY = "AccuracyReport.xlsx"
    FILE_REPORT_TEXT_ACCURACY = "TextAccuracyReport.xlsx"
    FILE_REPORT_MEMORY_PEAK = "MemoryPeakReport.xlsx"
    FILE_XML = "results.xml"
    FILE_TEST_INFO = "test_info.json"
    FILE_ACCURACY_DETAIL = "ErrorDetail.tsv"
    CHANGE = "changed"
    NOTCHANGE = "notchanged"
    ERROR = "error"
    SPEC = "spec"

    class Test(object):
        PREFIX = "test_results"
        FOLDER = "test_results"
        FILE = "test_result.json"
        CHANGE = "changed"
        TESTSET_PREFIX = "TESTS"
        TRUNK_TEST_OUTPUT = "test_output"
        TRUNK_OUTPUT = "output"
        COMPARE_FILE = "compare_result.json"
        STDERR_FILE_NAME = "stderr.txt"
        STDOUT_FILE_NAME = "stdout.txt"

    class Log(object):
        SYSTEM_PERFORMANCE = "system_performance"
        SYSTEM_PERFORMANCE_BUILD = "build_reports"
        SYSTEM_PERFORMANCE_TEST = "test_reports"
        BUILD = "log_build"
        TEST = "log_test"
        EXTENSION = "log"


class FinalResult(object):
    FINAL_TEST_FILE = "{0}/" + FinalTestResult.TEST + "/" + TestResultConfig.FILE_DEFAULT
    FINAL_COMPARE_FILE = "{0}/" + FinalTestResult.TEST + "/" + CompareResultConfig.FILE_DEFAULT
    FINAL_COMBINE_MEM_PEAK_FILE = "{0}/" + FinalTestResult.TEST + "/" + TestResultConfig.MEM_PEAK_FILE
    FINAL_CHANGED_FOLDER = "{0}/" + FinalTestResult.TEST + "/" + FinalTestResult.CHANGE
    FINAL_ERROR_FOLDER = "{0}/" + FinalTestResult.TEST + "/" + FinalTestResult.ERROR
    FINAL_REPORT_FOLDER = "{0}/" + FinalTestResult.REPORT
    FINAL_SPEC_FOLDER = FinalTestResult.SPEC


class FinalResultsHelper(object):

    # Suffix for a build release version: Build in release mode with ICC
    RELEASE_BUILD = "release"

    # Suffix for a build version which is used for memory checking. As you know, currently,
    # we can not use a build package of ICC to profiling memory leak check using valgrind. Then
    # we need to build another version in release mode with GCC to run memory leak check test
    # cases.
    MEMORY_BUILD = "memory"

    """
    This class will help us construct name or path of directory/file result on master
    """
    def __init__(self, project=None, baseline_version=None, change_number=None, patch_set=None,
                 platform=None, build_mode=None):
        """
        Constructor of final result helper

        Parameters
        ----------
        project: str
            Name of project to be tested
        baseline_version: str/int
            Current delta version of project which is base of testing for the change at testing time
        change_number: str/int
            Gerrit number to be tested
        patch_set: str/int
            Patch set number on the change to be tested
        platform: str
            Platform to be tested
        build_mode: str
            Build mode to specify purpose of build package. Currently, there are two build mode
            one is 'release' which built with ICC for normal testing and one is 'memory' which
            built with GCC for memory leak checking. These build mode are defined in current
            class in RELEASE_BUILD and MEMORY_BUILD.

        """
        self.project = project
        self.baseline = baseline_version
        self.change_number = change_number
        self.patch_set = patch_set
        self.platform = platform
        self.build_mode = build_mode

    def get_name_build_package_change(self):
        """
        Get name of release build package on the platform for tested patch set, change and
        project. Currently, package has name as follow:
            <project>_C<change_number>_D<baseline>_<platform>_<build_mode>.tgz

        Examples
        --------
        PHOcr_C2981_D467_linux_release.tgz

        Returns
        -------
        str
            Name of release build package in a testing process

        """
        return "{project}_C{change}_D{baseline}_{platform}_{mode}.tgz".format(
            project=self._project,
            change=self._change_number,
            baseline=self._baseline,
            platform=self._platform,
            mode=self.build_mode
        )

    def get_name_build_package_delta(self, delta_version):
        """
        Get name of release build package which is used to release for a delta version in Post
        Integration, not for testing. Structure:
            <project>_D<delta>_<platform>_release.tgz

        Returns
        -------
        str
            Name of release build package for a delta version in Post Integration

        """
        return "{project}_D{delta}_{platform}_{mode}.tgz".format(
            project=self._project,
            delta=delta_version,
            platform=self._platform,
            mode=self.build_mode
        )

    def get_name_build_folder_change(self):
        """
        Get name of release build folder on the platform for tested patch set, change and
        project. Currently, package has name as follow:
            <project>_C<change_number>_D<baseline>_<platform>_<build_mode>

        Examples
        --------
        PHOcr_C2981_D467_linux_release

        Returns
        -------
        str
            Name of release build folder in a testing process

        """
        return "{project}_C{change}_D{baseline}_{platform}_{mode}".format(
            project=self._project,
            change=self._change_number,
            baseline=self._baseline,
            platform=self._platform,
            mode=self.build_mode
        )

    def get_name_build_folder_delta(self, delta_version):
        """
        Get name of release build folder which is used to release for a delta version in Post
        Integration, not for testing. Structure:
            <project>_D<delta>_<platform>_release

        Returns
        -------
        str
            Name of release build folder for a delta version in Post Integration

        """
        return "{project}_D{delta}_{platform}_{mode}".format(
            project=self._project,
            delta=delta_version,
            platform=self._platform,
            mode=self.build_mode
        )

    @property
    def project(self):
        """
        Getter for name of project

        Returns
        -------
        str
            Name of project to be tested

        """
        return self._project

    @project.setter
    def project(self, project):
        """
        Setter for name of project

        Parameters
        ----------
        project: str
            Name of project to be tested

        Returns
        -------
        None

        """
        self._project = project

    @property
    def baseline(self):
        """
        Getter for baseline - current delta version of the project at the testing time

        Returns
        -------
        str
            Current delta version of project at the testing time

        """
        return self._baseline

    @baseline.setter
    def baseline(self, baseline_version):
        """
        Setter for baseline version of testing

        Parameters
        ----------
        baseline_version: str/int

        Returns
        -------
        None

        """
        self._baseline = str(baseline_version)

    @property
    def change_number(self):
        """
        Getter for gerrit change number

        Returns
        -------
        str
            Gerrit change number to be tested

        """
        return self._change_number

    @change_number.setter
    def change_number(self, change_number):
        """
        Setter for gerrit change number

        Parameters
        ----------
        change_number: str/int

        Returns
        -------
        None

        """
        self._change_number = str(change_number)

    @property
    def patch_set(self):
        """
        Getter for patch set number on the change

        Returns
        -------
        str
            Patch set number on the change to be tested

        """
        return self._patch_set

    @patch_set.setter
    def patch_set(self, patch_set):
        """
        Setter for patch set number

        Parameters
        ----------
        patch_set: str/int
            Patch set number on the change to be tested

        Returns
        -------
        None

        """
        self._patch_set = str(patch_set)

    @property
    def platform(self):
        """
        Getter for test platform

        Returns
        -------
        str
            Platform to be tested

        """
        return self._platform

    @platform.setter
    def platform(self, platform):
        """
        Setter for tested platform

        Parameters
        ----------
        platform: str
            Platform to be tested

        Returns
        -------
        None

        """
        self._platform = platform

    @property
    def build_mode(self):
        """
        Getter for build mode of build package

        Returns
        -------
        str
            Build mode to specify purpose of build package

        """
        return self._build_mode

    @build_mode.setter
    def build_mode(self, build_mode):
        """
        Setter for build mode of build package

        Parameters
        ----------
        build_mode: str
            Build mode to specify purpose of build package

        Returns
        -------
        None

        """
        self._build_mode = build_mode
