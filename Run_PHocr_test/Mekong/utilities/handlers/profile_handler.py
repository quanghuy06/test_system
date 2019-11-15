# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      28/12/2016
# Description:      This configure profile of nodes and their virtual machine
from abc import ABCMeta
import configs.common
from configs.common import Platform
from configs.json_key import ProfileJson
from manager.lib_vm.vm_build_phocr_linux_release import VmBuildPHOcrLinuxRelease
from manager.lib_vm.vm_build_phocr_linux_memory import VmBuildPHOcrLinuxMemory
from manager.lib_vm.vm_build_phocr_windows_release import VmBuildPHOcrWindowsRelease
from manager.lib_vm.vm_build_phocr_windows_debug import VmBuildPHOcrWindowsDebug
from manager.lib_vm.vm_update_data_test_linux import VmUpdateDataTestLinux
from manager.lib_vm.vm_test_linux import VmTestLinux
from manager.lib_board.test_on_board_linux import TestOnBoardLinux
from manager.lib_vm.vm_test_windows import VmTestWindows
from manager.lib_node.node_build import NodeBuild
from manager.lib_node.node_test import NodeTest
from manager.lib_node.node_data_updater import NodeDataUpdater
from handlers.lib_base.json_handler import JsonHandler
from collections import defaultdict
from configs.json_key import JobName


class ProfileConfiguration(object):
    FILE_NAME_DEFAULT = "profile.json"

    # Jobs: Profile physical test machines for engineering test and
    # integration test or test time performance on board
    IT = "__IntegrationTest__"
    ET = "__EngineeringTest__"
    TESTING_ON_BOARD = "__TestingOnBoard__"

    # Keys of elements in physical system
    VM_LIST = "__vms__"
    NODE_LIST = "__nodes__"
    NODE = "node"
    VM = "vm"

    # Process
    BUILD = "__build__"
    DISTRIBUTION = "__distribution__"
    TEST = "__test__"  # Normal test

    # Information of a element
    IP = "ip"
    OS = "os"
    USER = "username"
    PWD = "password"
    TEST_MACHINE = "test_machine"


JOB_KEY_MAPPING = {
    "PHOcr-EngineeringTest": "__EngineeringTest__",
    "PHOcr-IntegrationTest": "__IntegrationTest__"
}


class ProfileHandler(JsonHandler):
    __metaclass__ = ABCMeta

    def __init__(self, parameters_handler=None, **kwargs):
        """
        Constructor for handler of system profile configuration. In case build and test process,
        parameters input and we extract some data specific for task.

        Parameters
        ----------
        parameters_handler : ParametersHandler
            Handler for parameters information which is necessary for executing task. This is
            required in case execute Build/Test and no need in case updating data for virtual
            machines
        """
        super(ProfileHandler, self).__init__(**kwargs)
        self.parameters_handler = parameters_handler
        if self.parameters_handler:
            # Configuration for job. From parameters information, we know that which job should be
            # done. The system profile for a job should include configuration for build/test.
            self.profile = self.data[self.get_job_key(self.parameters_handler)]
            # Configuration for build release
            self.build_release_config = self.profile[ProfileJson.BUILD_RELEASE]
            # Configuration for build memory
            self.build_memory_config = self.profile[ProfileJson.BUILD_MEMORY]
            # Configuration for build debug
            self.build_debug_config = self.profile[ProfileJson.BUILD_DEBUG]
            # Configuration of testing
            self.test_config = self.profile[ProfileJson.TEST]

    def refresh_data(self):
        self.profile = self.data[self.get_job_key(self.parameters_handler)]
        self.build_release_config = self.profile[ProfileJson.BUILD_RELEASE]
        self.build_memory_config = self.profile[ProfileJson.BUILD_MEMORY]
        self.build_debug_config = self.profile[ProfileJson.BUILD_DEBUG]
        self.test_config = self.profile[ProfileJson.TEST]

    @staticmethod
    def get_job_key(parameters_handler):
        """
        Currently, we have 3 different jobs:
        - Engineering Test
        - Integration Test
        - Testing on board

        Parameters
        ----------
        parameters_handler : ParametersHandler

        Returns
        -------
        None

        """
        if parameters_handler.get_job() == JobName.TEST_ON_BOARD:
            # Test on board
            return ProfileConfiguration.TESTING_ON_BOARD
        elif parameters_handler.is_et():
            # Test for Engineering Test
            return ProfileConfiguration.ET
        else:
            # Test for Integration Test
            return ProfileConfiguration.IT

    def get_node_info(self, node_name):
        return self.data[ProfileJson.NODE_LIST][node_name]

    def get_worker_info(self, worker_name):
        return self.data[ProfileJson.VM_LIST][worker_name]

    def get_nodes_available(self):
        nodes_info = self.data[ProfileJson.NODE_LIST]
        nodes_available = []
        for node in nodes_info:
            nodes_available.append(node)
        return nodes_available

    def get_vm_build(self, vm_name, is_release):
        vm_info = self.data[ProfileJson.VM_LIST][vm_name]
        vm_ip = vm_info[ProfileJson.info.IP]
        vm_platform = vm_info[ProfileJson.info.OS]
        vm_user = vm_info[ProfileJson.info.USER]
        vm_pwd = vm_info[ProfileJson.info.PWD]
        if vm_platform not in configs.common.SupportedPlatform:
            return None
        if vm_platform == Platform.LINUX:
            if is_release:
                return VmBuildPHOcrLinuxRelease(name=vm_name,
                                                ip=vm_ip,
                                                username=vm_user,
                                                password=vm_pwd,
                                                platform=vm_platform,
                                                log_level=1,
                                                info_handler=self.parameters_handler)
            else:
                return VmBuildPHOcrLinuxMemory(name=vm_name,
                                               ip=vm_ip,
                                               username=vm_user,
                                               password=vm_pwd,
                                               platform=vm_platform,
                                               log_level=1,
                                               info_handler=self.parameters_handler)
        elif vm_platform == Platform.WINDOWS:
            if is_release:
                return VmBuildPHOcrWindowsRelease(name=vm_name,
                                                  ip=vm_ip,
                                                  username=vm_user,
                                                  platform=vm_platform,
                                                  password=vm_pwd,
                                                  log_level=1,
                                                  info_handler=self.parameters_handler)
            else:
                return VmBuildPHOcrWindowsDebug(name=vm_name,
                                                ip=vm_ip,
                                                username=vm_user,
                                                platform=vm_platform,
                                                password=vm_pwd,
                                                log_level=1,
                                                info_handler=self.parameters_handler)
        else:
            return None

    def get_vm_test(self, vm_name):
        vm_info = self.data[ProfileJson.VM_LIST][vm_name]
        platform = vm_info[ProfileJson.info.OS]
        if platform not in configs.common.SupportedPlatform:
            return None
        if platform == Platform.LINUX:
            if vm_info[ProfileJson.info.TEST_MACHINE] == ProfileJson.BOARD:
                return TestOnBoardLinux(name=vm_name,
                                        ip=vm_info[ProfileJson.info.IP],
                                        username=vm_info[ProfileJson.info.USER],
                                        password=vm_info[ProfileJson.info.PWD],
                                        platform=platform, log_level=1,
                                        info_handler=self.parameters_handler)
            else:
                return VmTestLinux(name=vm_name, ip=vm_info[ProfileJson.info.IP],
                                   username=vm_info[ProfileJson.info.USER],
                                   password=vm_info[ProfileJson.info.PWD],
                                   platform=platform, log_level=1,
                                   info_handler=self.parameters_handler)
        elif platform == Platform.WINDOWS:
            return VmTestWindows(name=vm_name, ip=vm_info[ProfileJson.info.IP],
                                 username=vm_info[ProfileJson.info.USER],
                                 password=vm_info[ProfileJson.info.PWD], platform=platform,
                                 info_handler=self.parameters_handler, log_level=1)
        return None

    def get_vm_data_update(self, vm_name):
        """
        Get instance of a virtual machine which will be updated static data base on information in
        profile.

        Parameters
        ----------
        vm_name str

        Returns
        -------
        VmUpdateDataTestLinux

        """
        vm_info = self.data[ProfileJson.VM_LIST][vm_name]
        platform = vm_info[ProfileJson.info.OS]
        return VmUpdateDataTestLinux(
            name=vm_name, ip=vm_info[ProfileJson.info.IP],
            username=vm_info[ProfileJson.info.USER],
            password=vm_info[ProfileJson.info.PWD],
            platform=platform, log_level=1,
            info_handler=self.parameters_handler
        )

    def get_workers_update_data_of_node(self, node_name):
        """
        Get list of instances for virtual machines which will be updated static data. All test
        virtual machines on node will be updated (both of ET and IT).

        Parameters
        ----------
        node_name str
        profile_handler ProfileHandler

        Returns
        -------
        list
            List of VmUpdateDataTestLinux

        """
        # Get all configs for testing (ET and IT)
        test_configs = list()
        test_configs.append(self.data[ProfileConfiguration.ET][ProfileConfiguration.TEST])
        test_configs.append(self.data[ProfileConfiguration.IT][ProfileConfiguration.TEST])

        workers = []
        for test_config in test_configs:
            if node_name in test_config:
                worker_names = test_config[node_name]
                for name in worker_names:
                    worker = self.get_vm_data_update(name)
                    if worker is not None:
                        workers.append(worker)
        return workers

    def get_node_data_updater(self, node_name):
        """
        Create instance for node data updater.

        Parameters
        ----------
        node_name : str

        Returns
        -------
        NodeDataUpdater
            Object to handle data updating for virtual machines on node

        """
        node_info = self.data[ProfileJson.NODE_LIST][node_name]
        return NodeDataUpdater(name=node_name,
                               ip=node_info[ProfileJson.info.IP],
                               username=node_info[ProfileJson.info.USER],
                               platform=node_info[ProfileJson.info.OS],
                               profile_handler=self)

    def get_nodes_data_updater(self):
        """
        Get list of all nodes which are distributed for testing in both Engineering Test and
        Integration Test for updating data.

        Returns
        -------
        list
            List of NodeDataUpdater

        """
        # Get all configs for testing (ET and IT)
        test_configs = list()
        test_configs.append(self.data[ProfileConfiguration.ET][ProfileConfiguration.TEST])
        test_configs.append(self.data[ProfileConfiguration.IT][ProfileConfiguration.TEST])
        # Create list of node data update objects
        nodes = list()
        for test_config in test_configs:
            for node_name in test_config:
                nodes.append(self.get_node_data_updater(node_name=node_name))
        return nodes

    def get_vm_build_of_node(self, node_name):
        builders = []
        if node_name in self.build_debug_config:
            worker_names = self.build_debug_config[node_name]
            for vm_name in worker_names:
                vm_build = self.get_vm_build(vm_name, is_release=False)
                if vm_build is not None:
                    builders.append(vm_build)
        if node_name in self.build_release_config:
            worker_names = self.build_release_config[node_name]
            for vm_name in worker_names:
                vm_build = self.get_vm_build(vm_name, is_release=True)
                if vm_build is not None:
                    builders.append(vm_build)
        if node_name in self.build_memory_config:
            worker_names = self.build_memory_config[node_name]
            for vm_name in worker_names:
                vm_build = self.get_vm_build(vm_name, is_release=False)
                if vm_build is not None:
                    builders.append(vm_build)
        return builders

    def get_testers_of_node(self, node_name):
        testers = []
        if node_name in self.test_config:
            worker_names = self.test_config[node_name]
            for name in worker_names:
                vm_test = self.get_vm_test(name)
                if vm_test is not None:
                    testers.append(vm_test)
        return testers

    def get_testers_of_node_by_platform(self, node_name, platform):
        all_testers = self.get_testers_of_node(node_name)
        testers = []
        for tester in all_testers:
            if tester.platform == platform:
                testers.append(tester)
        return testers

    def get_node_build(self, node_name):
        node_info = self.data[ProfileJson.NODE_LIST][node_name]
        return NodeBuild(name=node_name, ip=node_info[ProfileJson.info.IP],
                         username=node_info[ProfileJson.info.USER],
                         platform=node_info[ProfileJson.info.OS],
                         profile_handler=self,
                         info_handler=self.parameters_handler)

    def get_node_test(self, node_name, distribution_path):
        node_info = self.data[ProfileJson.NODE_LIST][node_name]
        return NodeTest(name=node_name,
                        ip=node_info[ProfileJson.info.IP],
                        username=node_info[ProfileJson.info.USER],
                        platform=node_info[ProfileJson.info.OS],
                        profile_handler=self,
                        info_handler=self.parameters_handler,
                        distribution_file=distribution_path)

    def get_build_nodes(self):
        nodes = []
        build_config = self.get_build_config()
        for node_name in build_config:
            builders = self.get_vm_build_of_node(node_name=node_name)
            if builders:
                nodes.append(self.get_node_build(node_name=node_name))
        return nodes

    def get_build_config(self):
        """
        Combine config of build release and build debug.

        Returns
        -------
        dict
            Build configuration for corresponding with node.
        """
        build_config = defaultdict(list)
        for node_name in (self.build_release_config,
                          self.build_memory_config,
                          self.build_debug_config):
            for key, value in node_name.iteritems():
                for item in value:
                    build_config[key].append(item)
        return build_config

    def get_test_nodes(self, distribution_path):
        nodes = []
        for node_name in self.test_config:
            testers = self.get_testers_of_node(node_name)
            if testers:
                nodes.append(self.get_node_test(node_name=node_name,
                                                distribution_path=distribution_path))
        return nodes

    def get_test_nodes_by_platform(self, platform):
        nodes = []
        for node_name in self.test_config:
            workers = self.test_config[node_name]
            for worker_name in workers:
                worker_info = self.get_worker_info(worker_name=worker_name)
                if worker_info[ProfileJson.info.OS] == platform:
                    nodes.append(self.get_node_test(node_name=node_name,
                                                    distribution_path=None))
                    break
        return nodes

    # Remove a test node from profile data
    def remove_test_node(self, node_name):
        if node_name in self.test_config:
            self.test_config[node_name] = []
        self.data[self.get_job_key(self.parameters_handler)][
            ProfileJson.TEST] = self.test_config

    # Remove a test worker from profile data of node
    def remove_test_worker(self, node_name, worker_name):
        if node_name in self.test_config:
            node_old_config = self.test_config[node_name]
            self.test_config[node_name] = []
            for name in node_old_config:
                if name != worker_name:
                    self.test_config[node_name].append(name)
            self.data[self.get_job_key(self.parameters_handler)][
                ProfileJson.TEST] = self.test_config
        self.refresh_data()
