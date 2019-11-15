from abc import ABCMeta
from handlers.lib_base.json_handler import JsonHandler
from configs.json_key import BuiltManagerKey


class BuildManagerHandler(JsonHandler):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(BuildManagerHandler, self).__init__(**kwargs)

    def get_previous_built(self):
        """
        Returns
        -------
        str:
            path to previous built
        """

        return self.data.get(BuiltManagerKey.PREVIOUS_BUILD)

    def get_current_built(self):
        """

        Returns
        -------
        str:
            path to current built
        """
        return self.data.get(BuiltManagerKey.CURRENT_BUILD)

    def get_mekong(self):
        """

        Returns
        -------
        str:
            path to mekong
        """
        return self.data.get(BuiltManagerKey.MEKONG)

    def get_python(self):
        """

        Returns
        -------
        str:
            python
        """
        return self.data.get(BuiltManagerKey.PYTHON)

    def get_run_performance_analysis_path(self):
        """

        Returns
        -------
        str:
            path to performance analysis
        """
        return self.data.get(BuiltManagerKey.RUN_PEF_ANALYSIS_PATH)

    def get_board_ip(self):
        """
        Returns
        -------
        str:
            list of board ip
        """
        return self.data.get(BuiltManagerKey.BOARD_IP)

    def get_perf_report_link(self):
        """

        Returns
        -------
        str:
            link performance report
        """
        return self.data.get(BuiltManagerKey.PERF_REPORT_LINK)
