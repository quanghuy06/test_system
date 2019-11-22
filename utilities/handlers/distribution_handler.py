# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           TaiPD
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      06/07/2017
# Description:      This python script can be used to get information from test distribution result.
from abc import ABCMeta

from configs.json_key import TestDistributionJson
from handlers.lib_base.json_handler import JsonHandler


class DistributionHandler(JsonHandler):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(DistributionHandler, self).__init__(**kwargs)

    def get_node_distribution(self, node_name):
        if node_name in self.data.keys():
            return self.data[node_name]
        else:
            return {}

    def get_worker_distribution(self, node_name, worker_name):
        node_distribution = self.get_node_distribution(node_name=node_name)
        if node_distribution and (worker_name in node_distribution.keys()):
            return node_distribution[worker_name]
        else:
            return {}

    def get_worker_distribution_by_location(self, node_name, worker_name, location):
        worker_distribution = self.get_worker_distribution(node_name=node_name,
                                                           worker_name=worker_name)
        if worker_distribution and (location in worker_distribution.keys()):
            return worker_distribution[location]
        else:
            return []

    def is_worker_distributed(self, node_name, worker_name):
        locations = [TestDistributionJson.location.DB, TestDistributionJson.location.WS]
        for loc in locations:
            if self.get_worker_distribution_by_location(node_name=node_name,
                                                        worker_name=worker_name, location=loc):
                return True
        return False

    def get_test_set_worker_db(self, node_name, worker_name):
        return self.get_worker_distribution_by_location(node_name=node_name,
                                                        worker_name=worker_name,
                                                        location=TestDistributionJson.location.DB)

    def get_test_set_node_db(self, node_name):
        node_distribution = self.get_node_distribution(node_name)
        test_set = []
        for worker_name in node_distribution:
            worker_distribution_db = self.get_test_set_worker_db(node_name=node_name,
                                                                 worker_name=worker_name)
            for test_name in worker_distribution_db:
                if test_name not in test_set:
                    test_set.append(test_name)
        return test_set

    def get_testers_of_node(self, node_name, profile_handler):
        testers = []
        if node_name in self.data:
            for worker_name in self.get_node_distribution(node_name=node_name):
                if self.is_worker_distributed(node_name=node_name, worker_name=worker_name):
                    tester = profile_handler.get_vm_test(worker_name)
                    if tester:
                        testers.append(tester)
        return testers

    def get_test_nodes(self, profile_handler):
        nodes = []
        for node_name in self.data:
            testers = self.get_testers_of_node(node_name=node_name,
                                               profile_handler=profile_handler)
            if testers:
                node = profile_handler.get_node_test(node_name=node_name,
                                                     distribution_path=self.input_file)
                nodes.append(node)
        return nodes
