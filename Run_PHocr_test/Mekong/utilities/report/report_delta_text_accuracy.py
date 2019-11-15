 # TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/08/2017
# Last update:      09/07/2018
# Description:      Script for accuracy reporting of delta versions
import argparse
import sys_path
sys_path.insert_sys_path()
from report.lib_delta_report.phocr_delta_text_accuracy_reporter import \
    PHOcrDeltaTextAccuracyReporter
from configs.common import SupportedPlatform


def main():

    for platform in SupportedPlatform:
        reporter = PHOcrDeltaTextAccuracyReporter(platform=platform)
        reporter.do_work()


if __name__ == "__main__":
    main()
