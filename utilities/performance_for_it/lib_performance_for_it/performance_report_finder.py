from utils.svn_connector import SvnConnector
from handlers.change_delta_mapping_handler import ChangeDeltaMappingConfigureHandler
from jenkins.lib_parsers.delta_change_mapping_parser import DeltaChangeMappingParser
import os
import re


class PerformanceReportFinder:
    def __init__(self, build_manager_handler):
        self.build_manager_handler = build_manager_handler

    def find(self, delta):
        """

        Parameters
        ----------
        delta int:
            delta of change is merged

        Returns
        -------
        str:
            link to report of delta
        """
        delta_change_mapping_path_handler = ChangeDeltaMappingConfigureHandler(
            input_file=self.build_manager_handler.input_file)
        delta_change_mapping_file_path = delta_change_mapping_path_handler.load()
        delta_change_mapping_parser = \
            DeltaChangeMappingParser(mapping_file=delta_change_mapping_file_path)

        for version in range(delta, delta - 10, -1):
            change = delta_change_mapping_parser.get_change_number(delta_version=version)
            link = self.build_manager_handler.get_perf_report_link()
            svn_connector = SvnConnector()
            connector = svn_connector.connect_remote_client(link)

            change_delta = 'C{change}_D{delta}'.format(
                change=change,
                delta=version - 1
            )
            print("Search for performance for delta {delta}: *{report_name}.xlsx"
                  "".format(delta=version, report_name=change_delta))
            report_pat = os.path.join('(.*)', '(.*)', '(.*)', change_delta, '(.*).xlsx')
            report_pat = re.compile(report_pat)

            for rel_path, e in connector.list_recursive():
                report = os.path.join(rel_path, e.get("name"))
                report_mat = report_pat.match(report)
                if report_mat is not None:
                    report_url = os.path.join(link, report)
                    conn = svn_connector.connect_remote_client(report_url)
                    conn.export('.', force=True)
                    return os.path.join(os.getcwd(), os.path.basename(report_url))
            print("NOT FOUND!")
