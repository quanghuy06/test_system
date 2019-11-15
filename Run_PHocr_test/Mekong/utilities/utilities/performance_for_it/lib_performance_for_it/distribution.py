from collections import OrderedDict
import json
import math


class Distribution(object):

    @staticmethod
    def get(file_out, list_test_cases):
        """

        Parameters
        ----------
        file_out str:
            distribution log file
        list_test_cases list:
            list test cases

        Returns
        -------
        OrderedDict
            distribution data

        """
        distribution_data = OrderedDict()
        # size is total test cases is testing in a test set
        size = 352

        # total is to total test sets
        total = int(math.ceil(float(len(list_test_cases)) / size))
        test_set_name = 'test_set_{}'

        for number_test_set in range(total - 1):
            begin = number_test_set * size
            end = begin + size - 1
            distribution_data[test_set_name.format(number_test_set)] = list_test_cases[begin: end]

        distribution_data[test_set_name.format(total - 1)] = list_test_cases[(total - 1) * size:]

        with open(file_out, 'wb+') as f1:
            json.dump(distribution_data, f1, indent=2)

        return distribution_data
