# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      10/08/2017
# Last update:      29/05/2018
# Description:      Script for accuracy reporting of delta versions
import sys
import time
import sys_path
sys_path.insert_sys_path()
from report.lib_delta_report.phocr_delta_performance_reporter import PHOcrDeltaPerformanceReporter
from configs.common import SupportedPlatform


def main():
    print("<SM> Making performance report for delta versions")

    # Calculate time for processes
    start_time = time.time()

    # Return code when finish
    exit_code = 0

    for platform in SupportedPlatform:
        print("\n+ Report for platform {platform}".format(platform=platform))
        # Initial reporter
        reporter = PHOcrDeltaPerformanceReporter(platform=platform)
        # Execute making report
        try:
            reporter.do_work()
        except:
            print("WARN: Failed to export report for platform {platform}".format(platform=platform))
            exit_code = 1

    print("\n<EM> Finish in: {execution_time}s".format(execution_time=time.time() - start_time))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
