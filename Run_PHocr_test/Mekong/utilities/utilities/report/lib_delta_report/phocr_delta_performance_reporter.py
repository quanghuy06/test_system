# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/07/2018
# Updated by:       Phung Dinh Tai
# Description:
import sys
from abc import ABCMeta
from report.lib_delta_report.delta_reporter import DeltaReporter
from report.lib_base.history_data_informer\
    import HistoryDataInformer, HistoryDataConfiguration
from configs.database import SpecKeys
from configs.projects.phocr import PhocrProject
from baseapi.common import merge_lists
from report.lib_base.cell_format import Color, Align
from report.lib_base.defines import ReportNames, ReportTitles
from baseapi.common import get_list_defined_string


class PDPConfiguration(object):

    # Define sheets name
    SHEET_PROGRESS = "Progress"
    SHEET_BY_GROUPS = "Progress By Language Groups"
    SHEET_BY_LANGUAGE = "Progress By Language"

    LANGUAGES = sorted(get_list_defined_string(SpecKeys.Tags.Language))

    GROUPS = {
        "EFIGS": ["english", "french", "italian", "german", "spanish"],
        "+10": ["danish", "dutch", "finnish", "greek-modern", "norwegian",
                "polish", "portuguese", "russian", "swedish", "turkish"],
        "ASIAN": ["chinesesimplified", "chinesetraditional", "japanese"]
    }

    GROUPS_BY_ORDERS = ["EFIGS", "+10", "ASIAN"]

    # Headers
    TEST_NAME = "Test case"
    ESDK = "e-SDK"
    ON_BOARD = "PHOcr on board"
    K_TEST_MACHINE = "PHOcr K reference"
    PHOCR_TEST_MACHINE = "Time execute"

    # Progress sheet
    ESDK_TOTAL_TIME = "e-SDK total time"
    PHOCR_TOTAL_TIME = "PHOcr total time"
    RATIO = "Ratio PHOcr vs e-SDK"
    NUM_PAGES = "Number of pages"

    # List delta to report
    NUM_LAST_DELTA = 5
    RANGE_LAST_DELTA = 300
    DELTA_STEP = 25


class PHOcrDeltaPerformanceReporter(DeltaReporter):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        self.phocr_test_machine_deltas = []
        self.phocr_on_board_deltas = []
        self.esdk_newest_version = 1
        self.phocr_on_board_informer = None
        super(PHOcrDeltaPerformanceReporter, self).__init__(**kwargs)
        self.esdk_time_range = {}
        self.phocr_on_board_time_range = {}
        self.phocr_for_k_time_range = {}
        self.phocr_time_range = {}

    def add_sheets(self):
        # Add progress sheet
        self.add_progress_sheet()

        # Add progress by groups of languages sheet
        self.add_progress_by_groups_sheet()

        # Add progress by languages sheet
        self.add_progress_by_languages_sheet()

        # Add raw data sheets of delta versions
        self.add_raw_data_sheets()

    def add_progress_sheet(self):
        self.logger.start_step("Make {0} sheet".format(PDPConfiguration.SHEET_PROGRESS))
        sheet = self.book.add_worksheet(name=PDPConfiguration.SHEET_PROGRESS)
        self.write_block_performance_progress(sheet=sheet, block_name="", start_line=2,
                                              start_column=1, conditions_template="",
                                              list_delta=self.deltas)

        # Column width
        col = 0
        sheet.set_column(col, col, 5)
        col += 1
        sheet.set_column(col, col, 25)
        col += 1
        sheet.set_column(col, col + 2, 25)
        col += 1
        sheet.set_column(col, col + 3, 25)
        self.logger.end_step(True)

    def add_progress_by_groups_sheet(self):
        self.logger.start_step("Make {0} sheet".format(PDPConfiguration.SHEET_BY_GROUPS))
        sheet = self.book.add_worksheet(name=PDPConfiguration.SHEET_BY_GROUPS)
        start_line = 1
        for lang_group in PDPConfiguration.GROUPS_BY_ORDERS:
            list_langs = list()
            list_delta = list()
            for language in PDPConfiguration.GROUPS[lang_group]:
                list_langs.append("\"{lang}\"".format(lang=language))
                list_delta = self.get_list_delta_performance_by_language(list_delta, language)
            lang_group_filter_string = "{{{list_langs}}}" \
                                       "".format(list_langs=",".join(list_langs))
            conditions_template = self.get_condition_template(header=SpecKeys.Tags.LANGS,
                                                              value=lang_group_filter_string)
            written_lines = \
                self.write_block_performance_progress(sheet=sheet, block_name=lang_group,
                                                      conditions_template=conditions_template,
                                                      start_line=start_line, start_column=1,
                                                      list_delta=list_delta)
            start_line += written_lines + 2
        # Column width
        col = 0
        sheet.set_column(col, col, 5)
        col += 1
        sheet.set_column(col, col, 25)
        col += 1
        sheet.set_column(col, col + 2, 25)
        col += 1
        sheet.set_column(col, col + 3, 25)
        self.logger.end_step(True)

    def add_progress_by_languages_sheet(self):
        self.logger.start_step("Make {0} sheet".format(PDPConfiguration.SHEET_BY_LANGUAGE))
        sheet = self.book.add_worksheet(name=PDPConfiguration.SHEET_BY_LANGUAGE)
        start_line = 1
        for language in PDPConfiguration.LANGUAGES:
            list_delta = []
            language_condition_tpl = self.get_condition_template(header=SpecKeys.Tags.LANGS,
                                                                 value="\"{0}\"".format(language))
            list_delta = self.get_list_delta_performance_by_language(list_delta, language)
            written_lines = \
                self.write_block_performance_progress(sheet=sheet, block_name=language,
                                                      start_line=start_line, start_column=1,
                                                      conditions_template=language_condition_tpl,
                                                      list_delta=list_delta)
            start_line += written_lines + 2
        # Column width
        col = 0
        sheet.set_column(col, col, 5)
        col += 1
        sheet.set_column(col, col, 25)
        col += 1
        sheet.set_column(col, col + 2, 25)
        col += 1
        sheet.set_column(col, col + 3, 25)
        self.logger.end_step(True)

    def add_raw_data_sheets(self):
        self.logger.start_step("Make delta version sheets")
        for delta in self.deltas:
            self.add_delta_sheet(delta=delta)
        self.logger.end_step(True)

    def add_delta_sheet(self, delta):
        on_board_delta = self.get_on_board_delta(delta=delta)
        on_board_sheet_reference = self.get_delta_sheet_name(on_board_delta)
        sheet_name = self.get_delta_sheet_name(delta=delta)
        sheet = self.book.add_worksheet(name=sheet_name)
        # Write header line
        line = 0
        header_format = self.get_cell_format(set_border=True, set_bold=True, align=Align.CENTER,
                                             bg_color=Color.GREY)
        self.headers[2] = PDPConfiguration.ON_BOARD
        self.headers[3] = PDPConfiguration.K_TEST_MACHINE
        self.write_line(sheet=sheet, value_array=self.headers, cell_format=header_format, line=line)
        # Write data
        # Format for line data
        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        float_number_format = self.get_cell_format(set_border=True, align=Align.RIGHT,
                                                   num_format='#,##0.00')
        tag_value_format = self.get_cell_format(set_border=True, align=Align.CENTER)
        # Test name format
        line_formats = [text_format]
        # Time execute format
        for i in range(0, 4):
            line_formats.append(float_number_format)
        # Tag values format
        for i in range(0, len(self.tag_headers)):
            line_formats.append(tag_value_format)
        # Get line data
        for test_name in self.list_test_names:
            line += 1
            # Test name
            line_data = [test_name]
            # e-SDK execute time
            esdk_time = self.esdk_informer.get_time(test_id=test_name,
                                                    delta=self.esdk_newest_version)
            line_data.append(esdk_time)
            if delta in self.phocr_on_board_deltas:
                on_board_delta_of_test = self.get_on_board_delta_of_test(test_id=test_name,
                                                                         delta=delta)
                # PHOcr on board execute time
                phocr_on_board_time = self.phocr_on_board_informer.get_time(
                    test_id=test_name, delta=on_board_delta_of_test)
                line_data.append(phocr_on_board_time)
                # PHOCr on test machine for K-factor calculation
                phocr_for_k_calculation_time = self.phocr_test_machine_informer.get_time(
                    test_id=test_name, delta=on_board_delta_of_test)
                line_data.append(phocr_for_k_calculation_time)
            else:
                on_board_delta_of_test = self.get_on_board_delta_of_test(test_id=test_name,
                                                                         delta=delta)
                # PHOcr on board execute time
                phocr_on_board_time = self.phocr_on_board_informer.get_time(
                    test_id=test_name, delta=on_board_delta_of_test)
                if phocr_on_board_time:
                    # PHOcr on board execute time
                    phocr_on_board_time = self.get_cell_reference(
                        sheet_name=on_board_sheet_reference, test_name=test_name,
                        header=PDPConfiguration.ON_BOARD)
                line_data.append(phocr_on_board_time)
                # PHOCr on test machine for K-factor calculation
                phocr_for_k_calculation_time = self.phocr_test_machine_informer.get_time(
                    test_id=test_name, delta=on_board_delta_of_test)
                if phocr_for_k_calculation_time:
                    phocr_for_k_calculation_time = self.get_cell_reference(
                        sheet_name=on_board_sheet_reference, test_name=test_name, 
                        header=PDPConfiguration.K_TEST_MACHINE)
                line_data.append(phocr_for_k_calculation_time)
            # PHOcr execute time on test machine of current delta
            phocr_execute_time = self.phocr_test_machine_informer.get_time(test_id=test_name,
                                                                           delta=delta)
            line_data.append(phocr_execute_time)
            # Tags value
            line_data += self.tags_informer.get_tags_value(test_id=test_name,
                                                           list_tags=self.tag_headers)
            # Write line data
            self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                         formats=line_formats)
        # Specific column width
        # Test name column
        col = 0
        sheet.set_column(col, col, 40)
        col += 1
        sheet.set_column(col, col + 4, 25)
        col += 4
        sheet.set_column(col, col + 3, 20)
        col += 3
        sheet.set_column(col, col + 23, 20)

    def get_delta_sheet_name(self, delta):
        sheet_name = "D{0}".format(delta)
        if delta in self.phocr_on_board_deltas:
            return sheet_name + " - MFP"
        else:
            return sheet_name

    def get_on_board_delta(self, delta):
        for i in range(0, len(self.phocr_on_board_deltas)):
            on_board_delta = self.phocr_on_board_deltas[i]
            if on_board_delta <= delta:
                return on_board_delta
        return None

    def get_on_board_delta_of_test(self, test_id, delta):
        on_board_deltas = self.phocr_on_board_informer.get_list_deltas_of_test(test_id=test_id)
        for i in range(0, len(on_board_deltas)):
            on_board_delta = on_board_deltas[i]
            if on_board_delta <= delta:
                return on_board_delta

    def get_primary_conditions_string_for_all_delta(self):
        filters = {}
        for delta in self.deltas:
            filters[delta] = self.get_primary_conditions_string(delta)
        return filters

    def get_primary_conditions_string(self, delta):
        conditions = list()
        # e-SDK time not empty
        conditions.append(self.get_condition_template(header=PDPConfiguration.ESDK, value="\"<>\""))
        # PHOcr on board time not empty
        conditions.append(self.get_condition_template(header=PDPConfiguration.ON_BOARD,
                                                      value="\"<>\""))
        # PHOcr time for K-factor calculation not empty
        conditions.append(self.get_condition_template(header=PDPConfiguration.K_TEST_MACHINE,
                                                      value="\"<>\""))
        # PHOcr execute time not empty
        conditions.append(self.get_condition_template(header=PDPConfiguration.PHOCR_TEST_MACHINE,
                                                      value="\"<>\""))
        res = ",".join(conditions)
        sheet_name = self.get_delta_sheet_name(delta=delta)
        return res.replace("SHEET_NAME", "{0}".format(sheet_name))

    def write_block_performance_progress(self, sheet, block_name, conditions_template, start_line,
                                         start_column=0, list_delta=None):
        # Header line
        line = start_line
        line_data = [block_name, PDPConfiguration.PHOCR_TOTAL_TIME,
                     PDPConfiguration.ESDK_TOTAL_TIME, PDPConfiguration.RATIO,
                     PDPConfiguration.NUM_PAGES]
        label_format = self.get_cell_format(set_border=True, align=Align.CENTER, set_bold=True,
                                            bg_color=Color.BLUE)
        header_format = self.get_cell_format(set_border=True, align=Align.CENTER, set_bold=True,
                                             bg_color=Color.HEAVY_RED)
        headers_format = [label_format, header_format, header_format, header_format, header_format]
        self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                     formats=headers_format, start_position=start_column)

        primary_conditions_string = self.get_primary_conditions_string_for_all_delta()


        # PHOcr time lines
        for delta in sorted(list_delta):
            line += 1
            if conditions_template:
                sheet_name = self.get_delta_sheet_name(delta=delta)
                final_conditions_string = primary_conditions_string[delta] + "," + \
                    conditions_template.replace("SHEET_NAME", "{0}".format(sheet_name))
            else:
                final_conditions_string = primary_conditions_string[delta]
            # Line header - delta version
            line_header = self.get_delta_sheet_name(delta=delta)
            line_data = [line_header]
            # Total time
            if delta in self.phocr_on_board_deltas:
                bg_color = Color.BROWN
                time_formula = \
                    self.get_sum_formula(range_string=self.phocr_on_board_time_range[delta],
                                         conditions_string=final_conditions_string)
            else:
                bg_color = Color.SLIGHT_BROWN
                phocr_time_formula = self.get_sum_formula(range_string=self.phocr_time_range[delta],
                                                          conditions_string=final_conditions_string)
                phocr_time_formula = phocr_time_formula.replace("=", "")
                phocr_on_board_time_formula = self.get_sum_formula(
                    range_string=self.phocr_on_board_time_range[delta],
                    conditions_string=final_conditions_string)
                phocr_on_board_time_formula = phocr_on_board_time_formula.replace("=", "")
                phocr_for_k_time_formula = self.get_sum_formula(
                    range_string=self.phocr_for_k_time_range[delta],
                    conditions_string=final_conditions_string)
                phocr_for_k_time_formula = phocr_for_k_time_formula.replace("=", "")
                time_formula = "={phocr_time}*{phocr_on_board}/{phocr_for_k}".format(
                    phocr_time=phocr_time_formula, phocr_on_board=phocr_on_board_time_formula,
                    phocr_for_k=phocr_for_k_time_formula)

            # Write PHOcr data
            phocr_text_format = self.get_cell_format(set_border=True, align=Align.LEFT,
                                                     bg_color=bg_color)
            phocr_float_format = self.get_cell_format(set_border=True, align=Align.RIGHT,
                                                      num_format='#,##0.00',
                                                      bg_color=bg_color)
            phocr_number_format = self.get_cell_format(set_border=True, align=Align.RIGHT,
                                                       num_format='#,##0',
                                                       bg_color=bg_color)
            phocr_line_formats = [phocr_text_format, phocr_float_format, phocr_float_format,
                                  phocr_float_format, phocr_number_format]
            phocr_time_cell = self.get_cell_str(line_idx=line,
                                                col_idx=start_column + len(line_data))
            line_data.append(time_formula)
            esdk_time_cell = self.get_cell_str(line_idx=line, col_idx=start_column + len(line_data))
            esdk_time_formula = \
                self.get_sum_formula(range_string=self.esdk_time_range[self.current_delta],
                                     conditions_string=final_conditions_string)
            line_data.append(esdk_time_formula)
            # Ratio vs e-SDK
            ratio_formula = "={phocr_time}/{esdk_time}".format(phocr_time=phocr_time_cell,
                                                               esdk_time=esdk_time_cell)
            line_data.append(ratio_formula)
            # Number of pages
            num_pages_formula = self.get_count_formula(conditions_string=final_conditions_string)
            line_data.append(num_pages_formula)
            # Write line data
            self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                         formats=phocr_line_formats, start_position=start_column)
        return line - start_line + 1

    def prepare_private_data(self):
        # Get some information range: e-SDK time, PHOcr on board time, PHOcr time for K-factor,
        # PHOcr execute time
        for delta in self.deltas:
            self.esdk_time_range[delta] = self.get_range_string(delta=delta,
                                                         header=PDPConfiguration.ESDK)
            self.phocr_on_board_time_range[delta] = self.get_range_string(delta=delta,
                                                                   header=PDPConfiguration.ON_BOARD)
            self.phocr_for_k_time_range[delta] = self.get_range_string(delta=delta,
                                                                header=PDPConfiguration.K_TEST_MACHINE)
            self.phocr_time_range[delta] = self.get_range_string(delta=delta,
                                                          header=PDPConfiguration.PHOCR_TEST_MACHINE)
        self.output_file = ReportNames.DELTA_PERFORMANCE.format(self.current_delta,
                                                                self.platform)
        self.title = ReportTitles.DELTA_BB_ACCURACY

    def get_some_history_informers(self):
        self.phocr_on_board_informer = \
            HistoryDataInformer(product=HistoryDataConfiguration.Product.PHOCR_ON_BOARD,
                                platform=self.platform, data=self.data)

    def get_filters(self):
        tags_filter = "{accuracy}:true&{non_integration}:false&{platform_tag}:{platform_value}" \
                      "".format(accuracy=SpecKeys.Tags.ACCURACY,
                                non_integration=SpecKeys.Tags.IS_NON_INTEGRATION,
                                platform_tag=SpecKeys.Tags.PLATFORMS,
                                platform_value=self.platform)
        return {
            SpecKeys.PRODUCT: PhocrProject.PRODUCT,
            SpecKeys.TAGS: tags_filter
        }

    def get_private_headers(self):
        return [PDPConfiguration.TEST_NAME, PDPConfiguration.ESDK, PDPConfiguration.ON_BOARD,
                PDPConfiguration.K_TEST_MACHINE, PDPConfiguration.PHOCR_TEST_MACHINE]

    def get_deltas_report_list(self):
        # Get delta list of PHOcr on test machine
        phocr_test_machines_deltas = self.phocr_test_machine_informer.get_list_deltas()
        if not phocr_test_machines_deltas:
            self.logger.log_and_print("No data available!")
            sys.exit(0)

        min_delta = phocr_test_machines_deltas[0] - PDPConfiguration.RANGE_LAST_DELTA
        # Get list delta on board
        phocr_on_board_deltas = self.phocr_on_board_informer.get_list_deltas()
        on_board_deltas_has_performance = \
            self.get_delta_has_performance(self.phocr_on_board_informer, phocr_on_board_deltas)
        current_index = -1
        for delta in on_board_deltas_has_performance:
            if delta > min_delta:
                self.phocr_on_board_deltas.append(delta)
                current_index += 1
            else:
                break
        if on_board_deltas_has_performance:
            self.phocr_on_board_deltas.append(on_board_deltas_has_performance[current_index])

        # Get list delta on test machine
        test_machine_deltas_has_performance = \
            self.get_delta_has_performance(self.phocr_test_machine_informer,
                                           phocr_test_machines_deltas)
        # Set condition
        # If number of deltas which have performance data, we will get current delta and nearest
        # deltas
        if len(test_machine_deltas_has_performance) >= PDPConfiguration.NUM_LAST_DELTA:
            for i in range(0, PDPConfiguration.NUM_LAST_DELTA + 1):
                self.phocr_test_machine_deltas.append(test_machine_deltas_has_performance[i])
            # Get all delta in range last delta
            for i in range(PDPConfiguration.NUM_LAST_DELTA + 1,
                           len(test_machine_deltas_has_performance)):
                delta = test_machine_deltas_has_performance[i]
                if (delta >= min_delta) and (delta % PDPConfiguration.DELTA_STEP == 0):
                    self.phocr_test_machine_deltas.append(delta)
        else:
            for i in range(0, len(test_machine_deltas_has_performance)):
                delta = test_machine_deltas_has_performance[i]
                if (delta >= min_delta) and (delta % PDPConfiguration.DELTA_STEP == 0):
                    self.phocr_test_machine_deltas.append(delta)
        # Merge two list
        good_deltas = merge_lists(self.phocr_test_machine_deltas, self.phocr_on_board_deltas)
        self.deltas = sorted(good_deltas, reverse=True)
        if not self.deltas:
            self.logger.log_and_print("No delta has machine performance data!")
            sys.exit(0)

        # Get deltas list of e-SDK
        esdk_deltas = self.esdk_informer.get_list_deltas()
        if not esdk_deltas:
            self.logger.log_and_print("No delta has esdk data!")
            sys.exit(0)

        if esdk_deltas:
            self.esdk_newest_version = esdk_deltas[0]

    def get_delta_has_performance(self, product, deltas):
        good_deltas = []
        for delta in deltas:
            if self.is_delta_has_performance(product, delta):
                good_deltas.append(delta)
        return good_deltas

    def is_delta_has_performance(self, product, delta):
        # Get line data
        for test_name in self.list_test_names:
            # PHOcr execute time on test machine of current delta
            phocr_execute_time = product.get_time(test_id=test_name, delta=delta)
            if phocr_execute_time:
                return True

        return False

    def get_list_language(self, test_name):
        list_language = self.tag_data[test_name][SpecKeys.Tags.LANGS]
        return list_language

    def get_list_delta_by_language(self, product, lang):
        list_delta = []
        for test_name in self.list_test_names:
            list_language = self.get_list_language(test_name)
            if lang in list_language:
                test_deltas = product.get_list_deltas_of_test(test_id=test_name)
                for delta in test_deltas:
                    delta_time = product.get_time(test_id=test_name, delta=delta)
                    if delta_time and delta not in list_delta:
                        list_delta.append(delta)
        return sorted(list_delta)

    # Get list delta by language which have time performance
    def get_list_delta_performance_by_language(self, list_delta, language):
        list_delta_on_test_machine_by_lang = \
            self.get_list_delta_by_language(self.phocr_test_machine_informer, language)
        list_delta_on_board_by_lang = \
            self.get_list_delta_by_language(self.phocr_on_board_informer, language)
        if list_delta_on_board_by_lang:
            list_delta_by_lang = merge_lists(list_delta_on_board_by_lang,
                                             list_delta_on_test_machine_by_lang)
            min_delta_on_board = min(list_delta_on_board_by_lang)
        else:
            list_delta_by_lang = list_delta_on_test_machine_by_lang
            min_delta_on_board = min(self.phocr_on_board_deltas)

        for delta in list_delta_by_lang:
            if delta in self.deltas \
                    and delta >= min_delta_on_board \
                    and delta not in list_delta:
                list_delta.append(delta)
        return list_delta

    def recheck_list_test_names(self):
        pass
        # # Check if test cases are not updated performance testing, so remove it from report list
        # final_list_test_names = list()
        # for test_name in self.list_test_names:
        #     time_execute = self.phocr_test_machine_informer.get_time(test_id=test_name,
        #                                                              delta=self.current_delta)
        #     print test_name, self.current_delta, time_execute
        #     if time_execute:
        #         print test_name
