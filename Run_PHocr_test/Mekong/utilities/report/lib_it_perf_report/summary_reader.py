from openpyxl import load_workbook


class SummaryReportRow:
    def __init__(self, build, version, gerrit_number, performance, improvement, base_version, note):
        self.build = build
        self.version = version
        self.gerrit_number = gerrit_number
        self.performance = performance
        self.improvement = improvement
        self.base_version = base_version
        self.note = note


class SummaryReportReader:

    def __init__(self, summary_report, sheet_name="Summary"):
        self.workbook = load_workbook(summary_report)
        self.sheet_name = sheet_name
        self._performance_data = None

    @property
    def performance_data(self):
        """
        Get performance data
        Returns
        -------
        list
            a list of SummaryReportRow
        """
        if self._performance_data is None:
            sheet_summary = self.workbook.get_sheet_by_name(self.sheet_name)
            self._performance_data = []
            for curr_row, cell in enumerate(sheet_summary.rows):
                if curr_row > 2:
                    self._performance_data.append(
                        SummaryReportRow(
                            build=cell[1].value,
                            version=cell[2].value,
                            gerrit_number=cell[3].value,
                            performance=cell[4].value,
                            improvement=cell[5].value,
                            base_version=cell[6].value,
                            note=cell[7].value
                        )
                    )
        return self._performance_data
