# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      05/09/2019
# Description:      This script used for report memory peak.

from abc import ABCMeta
from report.lib_memory_report.memory_reporter import MemoryReporter, \
    MERConfiguration

MEM_PEAK_TSV_FILE_NAME_DEFAULT = "MemoryPeakInfo{suffix}.tsv"


class MemPeakTsvReporter(MemoryReporter):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(MemPeakTsvReporter, self).__init__(**kwargs)
        if not self.output_file_set:
            suffix = ""
            if self.change_number and self.delta_version:
                suffix = "_C{change_number}_D{delta_version}".format(
                    change_number=self.change_number,
                    delta_version=self.delta_version)

            self.output_file = MEM_PEAK_TSV_FILE_NAME_DEFAULT.format(suffix=suffix)

    def get_list_test_names(self):
        """
        Get list name of test case.

        -------

        """
        self.list_test_names = \
            self.test_result_handler.get_list_not_error_tests()

    def get_header(self):
        """
        Get header of cell

        -------

        """
        self.headers = [MERConfiguration.TEST_NAME,
                        MERConfiguration.PEAK_INFO,
                        MERConfiguration.PEAK_COMMAND]

    def get_line_data(self, test_name):
        """
        Get information of each test name.

        Parameters
        ----------
        test_name: test case name.

        Returns
        -------
        list : data (memory peak information) of test case.

        """
        line_data = list()
        line_data.append(test_name)
        line_data.append(self.test_result_handler.get_mem_peak_info(test_name))
        line_data.append(self.test_result_handler.get_mem_peak_command(test_name))
        return line_data
