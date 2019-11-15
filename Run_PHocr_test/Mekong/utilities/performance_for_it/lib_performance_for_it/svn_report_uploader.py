from datetime import date
from utils.svn_connector import SvnConnector
import subprocess
import os
from utils.svn_helper import SVNHelper


class SvnReportUploader:
    DIR_URL_FILE_NAME = "svn_report_link.txt"

    def __init__(self, change, delta, report_root_url, report_url):
        self.change = change
        self.report_root_url = report_root_url
        self.delta = delta
        self.report_url = report_url
        self.dir_url = self.create_dir_url()

    def create_dir_url(self):
        """

        Returns
        -------
        str:
            url director
        """
        today = date.today()
        month = today.month
        str_month = '{number_month}.{str_month}'.format(
            number_month=month,
            str_month=today.strftime("%b")
        )
        str_date = today.strftime("%Y%m%d")
        change_delta = 'C{change_number}_D{delta_number}'.format(
            change_number=self.change,
            delta_number=self.delta
        )
        url = os.path.join(
            self.report_root_url,
            str(today.year),
            str_month,
            str(str_date),
            change_delta
        )
        return url

    def write_report_url(self):
        """
        write report url
        Returns
        -------

        """
        with open(SvnReportUploader.DIR_URL_FILE_NAME, "w") as f:
            f.write(self.dir_url)

    def upload(self):
        """
        Upload report to SVN repository

        Returns
        -------
        None/int
            Return None if everything OK, otherwise there are something wrong happened.

        """
        # Url to import report to SVN repository
        svn_url = os.path.join(self.dir_url, os.path.basename(self.report_url))
        commit_message = "Add performance report for C{change} base on D{delta}".format(
            change=self.change, delta=self.delta)
        # Using svn helper object to import report to SVN repository. Old file with the same svn
        # url will be deleted.
        svn_helper = SVNHelper()
        return svn_helper.import_file_to_svn(local_path=self.report_url, svn_url=svn_url,
                                             message=commit_message)
