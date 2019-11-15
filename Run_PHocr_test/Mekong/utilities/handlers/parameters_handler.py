# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      06/07/2017
# Last update:      06/07/2107
# Updated by:
# Description:      This python script define a class to handle json object of
#                   parameters which is used in automated test system
import re
from abc import ABCMeta
from configs.json_key import ParametersJson
from configs.projects.phocr import PhocrProject
from configs.projects.hanoi import HanoiProject
from handlers.lib_base.json_handler import JsonHandler
from configs.commit_message import CommitMessage
from configs.database import SpecKeys
from configs.common import Platform
from configs.json_key import JobName


class ParameterHandler(JsonHandler):

    __metaclass__ = ABCMeta

    # Init object with path to parameters file
    def __init__(self, **kwargs):
        super(ParameterHandler, self).__init__(**kwargs)

    # Check if Engineering Test or not
    def is_et(self):
        return self.data[ParametersJson.IS_ET]

    def is_extreme_test(self):
        return self.data[ParametersJson.IS_EXTREME_TEST]

    # Get jenkins job
    def get_job(self):
        return self.data[ParametersJson.JENKINS_JOB]

    def is_test_on_board(self):
        return self.get_job() == JobName.TEST_ON_BOARD

    # Get commit message
    def get_commit(self):
        return self.data[ParametersJson.GERRIT][ParametersJson.gerrit.COMMIT]

    # Get comment message
    def get_review_comment(self):
        return self.data[ParametersJson.GERRIT][ParametersJson.gerrit.COMMENT]

    # Get patch set of commit
    def get_ref_spec(self):
        return self.data[ParametersJson.GERRIT_REFS]

    # Get PHOcr delta version
    def get_phocr_version(self):
        return str(self.data[ParametersJson.DELTA_PHOCR])

    # Get HanoiWorkflow delta version
    def get_hanoi_version(self):
        # At commit message, user can specify a version of Hanoi
        # If user does not specify, use the latest one.
        user_specify_version = self.get_version_of_hanoi_user_specify()
        if user_specify_version:
            return user_specify_version
        else:
            return self.get_latest_version_of_hanoi()

    # Get gerrit project name
    def get_project(self):
        return self.data[ParametersJson.GERRIT_PROJECT]

    # Save information to file
    def save(self, output_file=None):
        if not output_file:
            output_file = self.input_file
        self.dump(output_file=output_file)

    # SOME ADDITIONAL FUNCTIONS THAT WILL BE USEFUL
    # Get change number from ref spec
    def get_change_number(self):
        ref_spec = self.get_ref_spec()
        return ref_spec.split("/")[3]

    # Get delta version
    def get_delta_version(self):
        if self.get_project() == PhocrProject.NAME:
            return self.get_phocr_version()
        elif self.get_project() == HanoiProject.NAME:
            return self.get_hanoi_version()
        else:
            return None

    # Get folder specific specific by change number and delta version
    def get_folder_specific(self):
        return "{project}_C{change_number}_D{delta}"\
            .format(project=self.get_project(),
                    change_number=self.get_change_number(),
                    delta=self.get_delta_version())

    # Get release build folder name
    def get_build_folder_release(self):
        return "{project}_D{delta}".format(project=self.get_project(),
                                           delta=self.get_delta_version())

    def get_hanoi_package_release(self, platform):
        """
        Get Hanoi package name corresponding with platform.

        Parameters
        ----------
        platform: str
             Platform supported.

        Returns
        -------
        str
           Hanoi package name

        """
        if platform == Platform.LINUX:
            return "{prefix}_D{delta}.{suffix}"\
                .format(prefix=HanoiProject.RELEASE_PREFIX,
                        delta=self.get_hanoi_version(),
                        suffix=HanoiProject.RELEASE_SUFFIX)
        else:
            return "{prefix}_D{delta}.{suffix}" \
                .format(prefix=HanoiProject.Windows.RELEASE_PREFIX,
                        delta=self.get_hanoi_version(),
                        suffix=HanoiProject.Windows.RELEASE_SUFFIX)

    def get_latest_version_of_hanoi(self):
        return str(self.data[ParametersJson.DELTA_HANOI])

    def get_version_of_hanoi_user_specify(self):
        commit_message = self.get_commit()
        hanoi_version_key = CommitMessage.AutomationTestInformation.HANOI_VERSION
        hanoi_version_pattern = "^{value}(.+)".format(value=hanoi_version_key)
        flags = re.M
        re_compile = re.compile(hanoi_version_pattern, flags)
        search_result = re_compile.search(commit_message)
        if search_result:
            return search_result.group(1)
        else:
            return None

    def get_custom_query(self, key):
        """
        Parse custom query by regular expression

        Parameters
        ----------
        key : str
            Key to parse.

        """
        commit_message = self.get_commit()
        regex = r'{key}(.|\n)*\n{bracket}\n'.format(key=key, bracket='}')
        result = re.search(regex, commit_message)
        if result is None:
            return None
        return result.group().strip()

    def get_value_by_key(self, key):
        commit_message = self.get_commit()
        key_pattern = "^{value}(.+)".format(value=key)
        flags = re.M
        re_compile = re.compile(key_pattern, flags)
        search_result = re_compile.search(commit_message)

        if search_result:
            return search_result.group(1).strip()
        else:
            return ""

    def is_check_memory_leak(self):
        """
        Check if commit message has requirement for checking memory leak.

        Returns
            bool : True if key exist in commit message
                   False in the other case.

        """
        return self.is_key_exists_in_commit_message(
            CommitMessage.AutomationTestInformation.IS_CHECK_MEMORY_LEAK)

    def is_check_memory_peak(self):
        """
        Check if commit message has requirement for checking memory peak

        Returns
            bool : True if key exist in commit message
                   False in the other case.
        """
        return self.is_key_exists_in_commit_message(
            CommitMessage.AutomationTestInformation.IS_CHECK_MEMORY_PEAK)

    def is_key_exists_in_commit_message(self, key):
        """
        Check if specific key exist in commit message.

        Parameters
        ----------
        key: str

        Returns
        -------
        bool: True if key exists in commit message
              False if key doesn't exist in commit message

        """
        checking_value = \
            self.get_value_by_key(key)
        return checking_value.lower() == "true"

    def is_checking_for_memory(self):
        """
        Check that commit message checking for memory leak, memory peak or not.

        Returns
        -------
        bool: True if commit message has requirement checking for memory leak
              or memory peak
              False in the other case.

        """
        return self.is_check_memory_leak() or self.is_check_memory_peak()

    def is_force_specification(self):
        """
        Check if have any require in testing such as: check memory leak,
        check memory peak ..., we will force specification.

        Returns
        -------
        bool: True if commit message has any requirement to force specification.
              False if doesn't have any requirement to force specification.
        """

        return self.is_check_memory_leak() or self.is_check_memory_peak()

    def get_spec_updated_from_commit_message(self):
        force_spec_info = dict()
        force_spec_info[SpecKeys.TAGS] = {}
        if self.is_check_memory_leak():
            force_spec_info[SpecKeys.TAGS][SpecKeys.Tags.IS_MEMCHECK] = "true"

        if self.is_check_memory_peak():
            force_spec_info[SpecKeys.TAGS][
                SpecKeys.Tags.IS_MEMCHECK_PEAK] = "true"

        return force_spec_info

    def is_build_hanoi(self):
        """
        Check commit message if developer require build Hanoi,
        IF not require build Hanoi, using Hanoi_Installer on SVN.

        Returns
        -------
        bool
            True if commit message has string "Is build Hanoi" and value is True
            False in other case

        """
        # 30-01-2019 (HuanLV) Now we enable build Hanoi on both ET and IT
        # so this function always return True
        return True

        # checking_value = \
        #     self.get_value_by_key(
        #         CommitMessage.AutomationTestInformation.IS_BUILD_HANOI)
        # return checking_value.lower() == "true"

    def hanoi_checkout_command(self):
        """
        Get Hanoi check out command on commit message of change
        The checkout command will be command on git repository of Hanoi to
        checkout to change of Hanoi which Mekong want to build and test along
        with PHOcr.

        For setting checkout command on commit message:
            Hanoi Checkout Command: <command>

        Examples
        -------
            Hanoi Checkout Command: git fetch ssh://namld@10.116.41.96:29418/HanoiWorkflow refs/changes/25/1825/1 && git checkout FETCH_HEAD

        Returns
        -------
        str
            empty if not defined on commit message
            else return the checkout command

        """
        hanoi_checkout_command = \
            self.get_value_by_key(
                CommitMessage.AutomationTestInformation.HANOI_CHECKOUT_COMMAND)

        # Because username in checkout command can be variable. Therefore need
        # to fix username to be authorized user (namld) which used for checkout
        # PHOcr. Additional, change method to ssh checkout
        import re
        hanoi_checkout_command = \
            re.sub(r'(http|ssh)://[^@]+@', 'ssh://namld@',
                   hanoi_checkout_command)
        hanoi_checkout_command = \
            re.sub(r':9090/a/', ':29418/',
                   hanoi_checkout_command)

        return hanoi_checkout_command.strip()

    def custom_query(self):
        """
        Get custom query from commit message of change.
        From that, get testcases by query
        """
        custom_query = \
            self.get_custom_query(
                CommitMessage.AutomationTestInformation.CUSTOM_QUERY)
        if custom_query is None:
            return None
        custom_query = custom_query.replace(CommitMessage.AutomationTestInformation.CUSTOM_QUERY, '')
        custom_query = custom_query.replace('\\', '')
        if len(custom_query) == 0:
            return None
        return custom_query
