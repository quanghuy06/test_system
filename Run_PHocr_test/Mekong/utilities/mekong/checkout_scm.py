#!/usr/bin/env python

"""Checking out SCM for projects:
    + PHOcr
    + HanoiWorkflow (not yet)

Output folder default is "build" folder

Using "checkout_scm -p PHOcr" for checking out scm for PHOcr project with
default config in PHOcr_scm_config.json

Using "checkout_scm -c phocr_scm_config.json -p PHOcr" for checking out scm for PHOcr project
with config file is phocr_scm_config.json

Using "checkout_scm -p PHOcr -o build/PHOcr" for checking out scm for PHOcr project
to folder build/PHOcr
"""

__author__ = "Le Duc Nam <nam.leduc@toshiba-tsdv.com>"
__date__ = "22 September 2016"

__version__ = "$Revision: 1.00 $"
__credits__ = "Le Duc Nam: create core module for PHOcr"

import os
import argparse
import sys_path
sys_path.insert_sys_path()
from mekong.common.config_checker import ToolChecker
from mekong.common.utilities import load_json
from mekong.common.checkout_repo import CheckoutSCMMain


###############################################################################
# Parsing arguments
def parse_argument(tool_config_file, scm_config_file):
    parser = argparse.ArgumentParser(description='Checkout SCM repository for building')
    parser.add_argument('-c', '--scm_config',
                        default=scm_config_file,
                        help='config file for scm')
    parser.add_argument('-t', '--tool_config',
                        default=tool_config_file,
                        help='tool config file path')
    parser.add_argument('-p', '--project',
                        help='project in list [PHOcr, HanoiWorkflow]',
                        required=True)
    parser.add_argument('-o', '--out',
                        default='build',
                        help='checkout to [out] folder')
    parser.add_argument('--refs',
                        default=None,
                        help='refspecs for checking out (only for git)')

    return parser


###############################################################################
# Main function
def main():
    # Parsing and set default for parameters
    current_folder = os.path.dirname(os.path.abspath(__file__))
    tool_config_file = os.path.join(current_folder, 'config', 'tool_config.json')
    scm_config_file = os.path.join(current_folder, 'config', 'scm_config.json')

    parser = parse_argument(tool_config_file, scm_config_file)
    args = parser.parse_args()

    # Check tool_config
    checker = ToolChecker()
    [err, tool] = checker.is_ok(args.tool_config)
    # if err:
    #     raise err

    # Get scm config

    [err, scm_json] = load_json(scm_config_file)
    if err:
        raise err

    # Project checking out
    scm_getter = CheckoutSCMMain(args.project)
    [err, result] = scm_getter.run(tool, scm_json, args.out, args.refs)
    if err:
        raise err

    print('OK')

###############################################################################
# Check name of module
if __name__ == "__main__":
    main()
