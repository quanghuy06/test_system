import sys_path
sys_path.insert_sys_path()

from baseapi.file_access import read_json
from configs.json_key import ProfileJson
import argparse
import os, sys

def parse_argument() :
    parser = argparse.ArgumentParser()
    # General parameters use for both building and testing in parameters.json
    parser.add_argument('-p', '--profile', required=True,
                        help="file profile.json need to check")
    return parser.parse_args()


class ProfileValidator:
    def __init__(self, profile_path):
        self.file_path = profile_path
        profile = read_json(profile_path)
        self.et_info = profile[ProfileJson.ET]
        self.it_info = profile[ProfileJson.IT]
        self.vm_list = profile[ProfileJson.VM_LIST]
        self.node_list = profile[ProfileJson.NODE_LIST]
        self.vm_names = []
        self.node_names = []

    def validate(self):
        # This method relate to structure of profile.json
        # Read profile.json fist
        self.validateVMs()
        self.validateTestNodes()
        self.validateETITConfig(self.et_info)
        self.validateETITConfig(self.it_info)
        print ("Good, file %s has no error!" % self.file_path)

    def validateVMs(self):
        for machine_name, machine_info in self.vm_list.iteritems():
            self.validateAMachine(machine_info)
            self.vm_names.append(machine_name)

    def validateTestNodes(self):
        for machine_name, machine_info in self.node_list.iteritems():
            self.validateAMachine(machine_info)
            self.node_names.append(machine_name)

    def validateETITConfig(self, test_configure):
        build_config = test_configure[ProfileJson.BUILD]
        self.validateBuildConfig(build_config)
        distribution_config = test_configure[ProfileJson.DISTRIBUTION]
        self.validateDistributionConfig(distribution_config)
        test_config = test_configure[ProfileJson.TEST]
        self.validateTestConfig(test_config)
        memory_leak_test_config = test_configure[ProfileJson.MEM_CHECK]
        self.validateMemoryLeakTestConfig(memory_leak_test_config)

    def validateBuildConfig(self, build_config):
        linux_build_config = build_config[ProfileJson.platforms.LINUX]

        linux_node = linux_build_config[ProfileJson.NODE]
        if not self.isNodeExists(linux_node):
            raise ValueError("%s do not correct: node %s does not exits" %
                             (ProfileJson.BUILD, linux_node))

        linux_vm = linux_build_config[ProfileJson.VM]
        if not self.isVMExists(linux_vm):
            raise ValueError("%s do not correct: vm %s does not exits" %
                             (ProfileJson.BUILD, linux_vm))

    def validateDistributionConfig(self, distribution_config):
        if not self.isNodeExists(distribution_config):
            raise ValueError("%s do not correct: node %s does not exits" %
                             (ProfileJson.DISTRIBUTION, distribution_config))

    def validateTestConfig(self, test_config):
        linux_test_config = test_config[ProfileJson.platforms.LINUX]
        for node, vms in linux_test_config.iteritems():
            if not self.isNodeExists(node):
                raise ValueError("%s do not correct: node %s does not exits" %
                                 (ProfileJson.TEST, node))
            for vm in vms:
                if not self.isVMExists(vm):
                    raise ValueError("%s do not correct: vm %s does not exits" %
                                     (ProfileJson.TEST, vm))


    def validateMemoryLeakTestConfig(self, memory_leak_test_config):
        linux_mm_leak_config = memory_leak_test_config[ProfileJson.platforms.LINUX]
        for node, vms in linux_mm_leak_config.iteritems():
            if not self.isNodeExists(node):
                raise ValueError("%s do not correct: node %s does not exits" %
                                 (ProfileJson.TEST, node))
            for vm in vms:
                if not self.isVMExists(vm):
                    raise ValueError("%s do not correct: vm %s does not exits" %
                                     (ProfileJson.TEST, vm))

    # TODO(Huan) write other module for this function
    def getCurrentOs(self):
        return 'linux'

    def isNodeExists(self, node_name):
        return node_name in self.node_names

    def isVMExists(self, vm_name):
        return vm_name in self.vm_names

    def validateAMachine(self, machine_info):
        if ProfileJson.info.IP not in machine_info:
            raise ValueError("Missing ip configure for machine: %s" % machine_info)
        if ProfileJson.info.OS not in machine_info:
            raise ValueError("Missing os configure for machine: %s" % machine_info)
        if ProfileJson.info.USER not in machine_info:
            raise ValueError("Missing username configure for machine: %s" % machine_info)

def main():
    args = parse_argument()
    profile_path = args.profile
    if not os.path.isfile(profile_path):
        print ("Error! File %s does not exists or is not a file!!!" % profile_path)
        sys.exit(1)

    try:
        profileValidator = ProfileValidator(profile_path)
        profileValidator.validate()
    except ValueError as error:
        print (error)


if __name__ == '__main__':
    main()