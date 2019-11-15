from report.lib_it_perf_report.performance_reader import PerformanceReportReader
from report.lib_it_perf_report.performance_writer import PerformanceReportWriter
from report.lib_it_perf_report.summary_reader import SummaryReportReader, SummaryReportRow
from report.lib_it_perf_report.summary_writer import SummaryReportWriter
from openpyxl import Workbook
import re


class PerformanceReport(object):

    def __init__(
            self,
            previous_report_performance,
            previous_performance_data,
            current_performance_data,
            current_change,
            current_delta
    ):
        self.previous_report_performance = previous_report_performance
        self.previous_performance_data = previous_performance_data
        self.current_performance_data = current_performance_data
        self.performance_data = self.get_performance_data()
        self.current_change = current_change
        self.current_delta = current_delta

    def get_performance_data(self):
        """
        Get performance data
        Returns
        -------
        list
            a list with each a element in list is a tuple has 3 elements.
            It is (test case, test time, report time)

        """
        test_cases = list(dict.fromkeys(
            self.current_performance_data.keys()
            + self.previous_performance_data.keys()
        ))
        test_cases.sort()
        performance_data = []
        for test_case in test_cases:
            testing_time = self.current_performance_data.get(test_case)
            if testing_time is None:
                testing_time = -1
            report_time = self.previous_performance_data.get(test_case)
            if report_time is None:
                report_time = -1
            performance_data.append((test_case, testing_time, report_time))
        return performance_data

    def make_summary_data(self):
        """
        Make summary data

        1. Reading summary report of previous merged change, gets summary data of previous merged
            change
        2. Update version for last data of the summary data.
        3. Insert new data of current change.
        Returns
        -------
        list:
            A list with each a element in list is a object(SummaryReportRow).
        """
        # Read summary report
        summary_reader = SummaryReportReader(self.previous_report_performance)
        summary_data = summary_reader.performance_data

        # Add version for last data
        if len(summary_data) > 0:
            base_version = summary_data[-1].base_version
            match = re.compile(r'D(\d+)').match(base_version)
            if match is not None:
                last_report_base_delta = int(match.group(1))
                last_report_delta = last_report_base_delta + 1
                last_report_gerrit_number = summary_data[-1].gerrit_number
                summary_data[-1].version = 'D{}'.format(last_report_delta)

        # Read performance report
        perf_reader = PerformanceReportReader(self.previous_report_performance)
        perf_data = perf_reader.perf_report_data

        # Insert data into summary report
        inner_data = set(self.current_performance_data.keys()) & set(perf_data.keys())

        remove_test_cases = set(perf_data.keys()) - inner_data

        if len(inner_data) < len(perf_data.keys()):
            total_perf_report_time = 0
            for key in inner_data:
                total_perf_report_time += perf_data[key]

            summary_data.append(
                SummaryReportRow(
                    build='',
                    version='D{}'.format(last_report_delta),
                    gerrit_number=int(last_report_gerrit_number),
                    performance=total_perf_report_time,
                    base_version='D{}'.format(last_report_base_delta),
                    improvement='',
                    note='Delete {} test cases.'.format(len(remove_test_cases))
                )
            )

        total_current_time = 0
        total_previous_time = 0
        for key in inner_data:
            total_current_time += self.current_performance_data[key]
            total_previous_time += self.previous_performance_data[key]

        improvement = '-'
        if total_previous_time > 0:
            improvement = (total_current_time - total_previous_time) / total_previous_time

        summary_data.append(
            SummaryReportRow(
                build='',
                version='',
                gerrit_number=int(self.current_change),
                performance=total_current_time,
                base_version='D{}'.format(self.current_delta),
                improvement=improvement,
                note=''
            )
        )

        add_test_cases = set(self.current_performance_data.keys()) - inner_data
        # If adding test case
        if len(inner_data) < len(self.current_performance_data.keys()):
            total_current_time = 0
            for key in self.current_performance_data:
                total_current_time += self.current_performance_data[key]

            summary_data.append(
                SummaryReportRow(
                    build='',
                    version='',
                    gerrit_number=int(self.current_change),
                    performance=total_current_time,
                    base_version='D{}'.format(self.current_delta),
                    improvement='',
                    note='Add {} test cases.'.format(len(add_test_cases))
                )
            )
        return summary_data

    def write_report(self):
        """
        Write report
        :return: a file
        """
        workbook = Workbook()
        workbook.remove(workbook['Sheet'])

        # make summary data
        summary_data = self.make_summary_data()

        # Writing summary report
        summary_writer = SummaryReportWriter(workbook, summary_data)
        summary_writer.write_sheet()

        # Writing performance sheet
        perf_writer = PerformanceReportWriter(
            workbook,
            self.current_change,
            self.current_delta,
            self.performance_data
        )
        perf_writer.write_sheet()

        # Saving file
        file_out = 'PHOcr_C{change}_D{delta}_Performance-Multi-JPG.xlsx'.format(
            change=self.current_change,
            delta=self.current_delta
        )
        workbook.save(file_out)
        return file_out
