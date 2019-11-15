# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      October, 7th 2016
# Last update:      06/06/2107
# Description:      This python script is used to distribute test case for machines in test system
import argparse
import sys_path
sys_path.insert_sys_path()
from configs.projects.mekong import TestSystem
from configs.json_key import TestDistributionJson
from handlers.parameters_handler import ParameterHandler
from manager.lib_distribution.distributor import TestDistributor


def parse_arguments():
    # Parse arguments
    parser = argparse.ArgumentParser(description='Distribute test set for test nodes')
    parser.add_argument('-p', '--parameters-file', required=True,
                        help="Path to parameters json file")
    parser.add_argument('-pf', '--profile', default=TestSystem.Paths.PROFILE,
                        help='Profile json, information about test nodes')
    parser.add_argument('-o', '--output-file', default=TestDistributionJson.DEFAULT_NAME,
                        help='Output path file')
    parser.add_argument('-t', '--weight-threshold',
                        help="Weight threshold")
    return parser


def main():
    parser = parse_arguments()
    args = parser.parse_args()

    print "Test distribution is starting..."
    distributor = TestDistributor(args.profile,
                                  ParameterHandler(input_file=args.parameters_file),
                                  args.weight_threshold)
    distributor.export_distribution(args.output_file)
    print "FINISHED: Result is exported to {0}".format(args.output_file)


if __name__ == "__main__":
    main()
