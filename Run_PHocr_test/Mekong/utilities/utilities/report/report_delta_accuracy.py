# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      22/05/2019
# Description:      Script for accuracy reporting of delta versions
import sys
import time
import sys_path
sys_path.insert_sys_path()
from report.lib_delta_report.phocr_delta_accuracy_reporter import PHOcrDeltaAccuracyReporter
from configs.common import SupportedPlatform


def main():
    print("<SM> Making report accuracy report for delta versions")

    # Calculate time for processes
    start_time = time.time()

    # Return code when finish
    exit_code = 0

    for platform in SupportedPlatform:
        print("\n+ Report for platform {platform}".format(platform=platform))
        # Initial reporter
        reporter = PHOcrDeltaAccuracyReporter(platform=platform)
        # Execute making report
        try:
            reporter.do_work()
        except:
            print("WARN: Failed to report for platform {platform}".format(platform=platform))
            exit_code = 1

    print("\n<EM> Finish in: {execution_time}s".format(execution_time=time.time()-start_time))
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
