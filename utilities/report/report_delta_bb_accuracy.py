# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/08/2017
# Last update:      29/05/2018
# Description:      Script for accuracy reporting of delta versions
import argparse
import sys_path
sys_path.insert_sys_path()
from report.lib_delta_report.phocr_delta_bb_accuracy_reporter import PHOcrDeltaBbAccuracyReporter
from configs.common import SupportedPlatform


def main():
    for platform in SupportedPlatform:
        reporter = PHOcrDeltaBbAccuracyReporter(platform=platform)

        reporter.do_work()


if __name__ == "__main__":
    main()
