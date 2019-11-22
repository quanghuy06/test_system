# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/07/2018
# Updated by:       Le Thi Thanh
# Description:
import sys
from abc import ABCMeta, abstractmethod
from report.lib_delta_report.delta_reporter import DeltaReporter
from configs.database import SpecKeys
from report.lib_base.cell_format import Color, Align
from baseapi.common import get_list_defined_string


class DARConfiguration(object):
    # Sheet name
    SHEET_PHOCR_VS_ESDK = "PHOCR vs eSDK"
    SHEET_PHOCR_ACCURACY = "PHOcr Accuracy "
    SHEET_BY_USE_CASE = "Accuracy by use case"
    SHEET_BY_LANGUAGE = "Accuracy by language"

    # Header
    TEST_NAME = "Test case"
    INSERT_ERRORS = "Insert errors"
    DELETE_ERRORS = "Delete errors"
    REPLACE_ERRORS = "Replace errors"
    ESDK_ERRORS = "e-SDK errors"
    TOTAL_ERRORS = "Total errors"
    TOTAL_CHARACTERS = "Total characters"
    MAINLY_TEXT = "Mainly Text"
    CLIPPED_IMAGE = "Clipped Image"
    DOCUMENT_TYPE = "Document Type"

    VERSION = "Product version"
    LANGUAGE = "Language"
    USE_CASES = "User case"
    NUM_PAGES = "Number of pages"
    ACCURACY = "Accuracy"

    # Value
    HAS_VALUE = "\"x\""
    IS_EMPTY = "\"\""
    NOT_EMPTY = "\"<>\""

    # Product
    PHOCR = "PHOcr"
    ESDK = "e-SDK"

    # Supported dpi
    DPI_300 = "300dpi"
    DPI_200 = "200dpi"

    # List deltas to report
    NUM_LAST_DELTA = 5
    RANGE_LAST_DELTA = 50
    DELTA_STEP = 10

    LANG_BY_ORDER = sorted(get_list_defined_string(SpecKeys.Tags.Language))
    LIST_TAGS = sorted(get_list_defined_string(SpecKeys.Tags))

    LIST_USE_CASES = [SpecKeys.Tags.IS_MAINLY_TEXT,
                      SpecKeys.Tags.IS_INVOICE,
                      SpecKeys.Tags.IS_FORM,
                      SpecKeys.Tags.HAS_CONTRAST,
                      SpecKeys.Tags.IS_MULTI_COL,
                      SpecKeys.Tags.IS_PRESENTATION,
                      SpecKeys.Tags.IS_DESKEW,
                      SpecKeys.Tags.IS_ROTATE]

    @staticmethod
    def get_sheet_name_by_dpi(dpi):
        """
        Get sheet name by dpi.

        Parameters
        ----------
        dpi: dpi supported

        Returns
        -------

        """
        sheet_name = "{sheet_name}{dpi}".format(
            sheet_name=DARConfiguration.SHEET_PHOCR_ACCURACY, dpi=dpi)
        return sheet_name

    @staticmethod
    def get_dpi_tag_by_dpi(dpi):
        """
        Get corresponding tags with input dpi.
        Parameters
        ----------
        dpi: dpi supported

        Returns
        -------
        str: Tag corresponding with input dpi

        """
        return "Is{dpi}".format(dpi=dpi)


class DeltaAccuracyReporter(DeltaReporter):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(DeltaAccuracyReporter, self).__init__(**kwargs)
        self.phocr_errors_range = {}
        self.phocr_chars_range = {}
        self.esdk_errors_range = {}
        self.esdk_chars_range = {}
        self.block_progress_headers = []
        self.newest_esdk_version = 1
        self.list_supported_dpi = [DARConfiguration.DPI_300,
                                   DARConfiguration.DPI_200]

    def get_list_tags_value(self, tag_name, list_tag_condition):
        list_value = list()
        for test_name in self.list_test_names:
            is_get_value = True
            tag_value = self.test_cases_manager.get_tag(test_id=test_name,
                                                        tag_name=tag_name)
            for tag in list_tag_condition:
                con_value = self.test_cases_manager.get_tag(test_id=test_name,
                                                            tag_name=tag)
                if not con_value:
                    is_get_value = False
                    break
            if is_get_value:
                if tag_value and (tag_value not in list_value):
                    list_value.append(tag_value)
        list_value = sorted(list_value)
        return list_value

    def add_sheets(self):
        # Add progress sheet
        self.add_phocr_vs_esdk_sheet()

        # Add sheet for each dpi type
        for dpi in self.list_supported_dpi:
            self.add_phocr_accuracy_sheet(dpi)

        # Add accuracy by use case sheet
        self.add_accuracy_by_use_case_sheet(self.list_supported_dpi)

        # Add accuracy by language sheet
        self.add_accuracy_by_language_sheet(self.list_supported_dpi)

        # Add deltas sheets
        self.logger.start_step("Make delta version sheets")
        for delta in self.deltas:
            self.add_delta_sheet(delta=delta)
        self.logger.end_step(True)

    def add_phocr_vs_esdk_sheet(self):
        # Initial sheet
        self.logger.start_step(
            "Make {0} sheet".format(DARConfiguration.SHEET_PHOCR_VS_ESDK))
        sheet = self.book.add_worksheet(
            name=DARConfiguration.SHEET_PHOCR_VS_ESDK)

        # Product line
        line = 1
        start_position = 3
        product_format = self.get_cell_format(set_bold=True,
                                              set_border=True,
                                              align=Align.CENTER,
                                              bg_color=Color.CUSTOM_GREEN)
        sheet.merge_range(line, start_position, line, start_position + 2,
                          data=DARConfiguration.PHOCR,
                          cell_format=product_format)
        start_position += 3
        sheet.merge_range(line, start_position, line, start_position + 2,
                          data=DARConfiguration.ESDK,
                          cell_format=product_format)
        line += 1
        start_column = 1
        # Initial used cell format
        header_format = self.get_cell_format(set_border=True,
                                             set_bold=True,
                                             align=Align.CENTER,
                                             bg_color=Color.CUSTOM_GREEN)
        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True,
                                             align=Align.RIGHT,
                                             num_format='#,##0',
                                             bg_color=Color.CUSTOM_YELLOW)
        accuracy_format = self.get_cell_format(set_border=True,
                                               align=Align.RIGHT,
                                               num_format='0.00%',
                                               bg_color=Color.CUSTOM_RED)
        # Formats for line data
        line_formats = [text_format,
                        number_format,
                        number_format,
                        number_format,
                        accuracy_format,
                        number_format,
                        number_format,
                        accuracy_format]
        # Progress by language
        # Headers of this sheet
        headers = [DARConfiguration.LANGUAGE,
                   DARConfiguration.NUM_PAGES,
                   DARConfiguration.TOTAL_ERRORS,
                   DARConfiguration.TOTAL_CHARACTERS,
                   DARConfiguration.ACCURACY,
                   DARConfiguration.TOTAL_ERRORS,
                   DARConfiguration.TOTAL_CHARACTERS,
                   DARConfiguration.ACCURACY]
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=headers,
                        start_position=start_column,
                        cell_format=header_format)

        line += 1
        binding_condition = {
            SpecKeys.Tags.IS_MAINLY_TEXT: DARConfiguration.HAS_VALUE,
            DARConfiguration.ESDK_ERRORS: DARConfiguration.NOT_EMPTY,
            SpecKeys.Tags.HAS_CONTRAST: DARConfiguration.IS_EMPTY,
            SpecKeys.Tags.IS_PRESENTATION: DARConfiguration.IS_EMPTY,
            SpecKeys.Tags.IS_CLIPPED_IMAGE: DARConfiguration.IS_EMPTY
        }
        for language in DARConfiguration.LANG_BY_ORDER:

            # Get filter string
            conditions_string = self.get_filter_string_language_for_all_deltas(
                language,
                binding_condition=binding_condition)

            # Get line data
            line_data = self.get_progress_line_data(line_header=language,
                                                    line=line,
                                                    conditions_string=conditions_string[self.current_delta],
                                                    start_column=start_column)
            # Write data
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_formats,
                                         start_position=start_column)

            line += 1

        # Add an empty line between two tables
        line += 2
        # Product line
        start_position = 3
        sheet.merge_range(line, start_position, line, start_position + 2,
                          data=DARConfiguration.PHOCR,
                          cell_format=product_format)
        start_position += 3
        sheet.merge_range(line, start_position, line, start_position + 2,
                          data=DARConfiguration.ESDK,
                          cell_format=product_format)
        line += 1
        # Add header line
        use_case_headers = [DARConfiguration.USE_CASES,
                            DARConfiguration.NUM_PAGES,
                            DARConfiguration.TOTAL_ERRORS,
                            DARConfiguration.TOTAL_CHARACTERS,
                            DARConfiguration.ACCURACY,
                            DARConfiguration.TOTAL_ERRORS,
                            DARConfiguration.TOTAL_CHARACTERS,
                            DARConfiguration.ACCURACY]
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=use_case_headers,
                        start_position=start_column,
                        cell_format=header_format)
        line += 1
        binding_condition = {
            DARConfiguration.ESDK_ERRORS: DARConfiguration.NOT_EMPTY
        }
        # Progress by use case
        for use_case in DARConfiguration.LIST_USE_CASES:

            # Get filter string
            conditions_string = self.get_filter_string_use_case_for_all_deltas(
                use_case=use_case,
                binding_condition=binding_condition)

            # Get line data
            line_data = self.get_progress_line_data(line_header=use_case,
                                                    line=line,
                                                    conditions_string=conditions_string[self.current_delta],
                                                    start_column=start_column)
            # Write data
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_formats,
                                         start_position=start_column)

            line += 1

        sheet.set_column(0, 7, 15)

        self.logger.end_step(True)

    def add_phocr_accuracy_sheet(self, dpi):
        """
        Add Accuracy report for image as specific dpi

        Parameters
        ----------
        dpi: dpi of image will be reported

        Returns
        -------

        """
        # Report accuracy for MainlyText and not ClippedImage
        self.logger.start_step(
            "Make {0} sheet".format(DARConfiguration.get_sheet_name_by_dpi(dpi=dpi)))
        sheet = self.book.add_worksheet(
            name=DARConfiguration.get_sheet_name_by_dpi(dpi=dpi))

        # Product line
        line = 1
        start_position = 1
        product_format = self.get_cell_format(set_bold=True,
                                              set_border=True,
                                              align=Align.CENTER,
                                              bg_color=Color.CUSTOM_GREEN)
        sheet.merge_range(line, start_position, line, start_position + 4,
                          data=DARConfiguration.MAINLY_TEXT,
                          cell_format=product_format)
        start_position += 6
        sheet.merge_range(line, start_position, line, start_position + 4,
                          data=DARConfiguration.CLIPPED_IMAGE,
                          cell_format=product_format)
        line += 2

        start_column = 1
        # Initial used cell format
        header_format = self.get_cell_format(set_border=True,
                                             set_bold=True,
                                             align=Align.CENTER,
                                             bg_color=Color.CUSTOM_GREEN)
        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True,
                                             align=Align.RIGHT,
                                             num_format='#,##0',
                                             bg_color=Color.CUSTOM_YELLOW)
        accuracy_format = self.get_cell_format(set_border=True,
                                               align=Align.RIGHT,
                                               num_format='0.00%',
                                               bg_color=Color.CUSTOM_RED)
        # Formats for line data
        line_formats = [text_format,
                        number_format,
                        number_format,
                        number_format,
                        accuracy_format]
        # Accuracy by language
        # Headers of this sheet
        headers = [DARConfiguration.LANGUAGE,
                   DARConfiguration.NUM_PAGES,
                   DARConfiguration.TOTAL_ERRORS,
                   DARConfiguration.TOTAL_CHARACTERS,
                   DARConfiguration.ACCURACY]
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=headers,
                        start_position=start_column,
                        cell_format=header_format)

        line += 1
        binding_condition = {
            SpecKeys.Tags.IS_MAINLY_TEXT: DARConfiguration.HAS_VALUE,
            DARConfiguration.get_dpi_tag_by_dpi(dpi): DARConfiguration.HAS_VALUE,
            SpecKeys.Tags.HAS_CONTRAST: DARConfiguration.IS_EMPTY,
            SpecKeys.Tags.IS_PRESENTATION: DARConfiguration.IS_EMPTY,
            SpecKeys.Tags.IS_CLIPPED_IMAGE: DARConfiguration.IS_EMPTY
        }
        for language in DARConfiguration.LANG_BY_ORDER:
            # Get filter string
            conditions_string = self.get_filter_string_language_for_all_deltas(
                language,
                binding_condition=binding_condition)

            # Get line data
            line_data = self.get_accuracy_line_data(line_header=language,
                                                    line=line,
                                                    conditions_string=
                                                    conditions_string[
                                                        self.current_delta],
                                                    start_column=start_column)
            # Write data
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_formats,
                                         start_position=start_column)

            line += 1

        # Add an empty line between two tables
        line += 2
        # Add header line
        use_case_headers = [DARConfiguration.USE_CASES,
                            DARConfiguration.NUM_PAGES,
                            DARConfiguration.TOTAL_ERRORS,
                            DARConfiguration.TOTAL_CHARACTERS,
                            DARConfiguration.ACCURACY]
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=use_case_headers,
                        start_position=start_column,
                        cell_format=header_format)
        line += 1
        # Progress by use case
        binding_condition = {
            DARConfiguration.get_dpi_tag_by_dpi(dpi): DARConfiguration.HAS_VALUE
        }
        for use_case in DARConfiguration.LIST_USE_CASES:
            # Get filter string
            conditions_string = self.get_filter_string_use_case_for_all_deltas(
                use_case=use_case,
                binding_condition=binding_condition)

            # Get line data
            line_data = self.get_accuracy_line_data(line_header=use_case,
                                                    line=line,
                                                    conditions_string=
                                                    conditions_string[
                                                        self.current_delta],
                                                    start_column=start_column)
            # Write data
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_formats,
                                         start_position=start_column)

            line += 1

        sheet.set_column(0, 7, 15)

        # -------------------------------------------------------------------- #
        # Report Accuracy for ClippedImage
        start_column = 7
        line = 3
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=headers,
                        start_position=start_column,
                        cell_format=header_format)

        line += 1
        binding_condition = {
            SpecKeys.Tags.IS_CLIPPED_IMAGE: DARConfiguration.HAS_VALUE,
            DARConfiguration.get_dpi_tag_by_dpi(dpi): DARConfiguration.HAS_VALUE,
            SpecKeys.Tags.HAS_CONTRAST: DARConfiguration.IS_EMPTY,
            SpecKeys.Tags.IS_PRESENTATION: DARConfiguration.IS_EMPTY
        }
        for language in DARConfiguration.LANG_BY_ORDER:
            # Get filter string
            conditions_string = self.get_filter_string_language_for_all_deltas(
                language,
                binding_condition=binding_condition)

            # Get line data
            line_data = self.get_accuracy_line_data(line_header=language,
                                                    line=line,
                                                    conditions_string=
                                                    conditions_string[
                                                        self.current_delta],
                                                    start_column=start_column)
            # Write data
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_formats,
                                         start_position=start_column)

            line += 1
        sheet.set_column(8, 8, 25)
        sheet.set_column(8, 12, 15)

        line += 2
        # Add header line
        use_case_headers = [DARConfiguration.DOCUMENT_TYPE,
                            DARConfiguration.NUM_PAGES,
                            DARConfiguration.TOTAL_ERRORS,
                            DARConfiguration.TOTAL_CHARACTERS,
                            DARConfiguration.ACCURACY]
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=use_case_headers,
                        start_position=start_column,
                        cell_format=header_format)
        line += 1
        list_pos_condition = [SpecKeys.Tags.IS_CLIPPED_IMAGE,
                              DARConfiguration.get_dpi_tag_by_dpi(dpi)]
        for doc_type in self.get_list_tags_value(SpecKeys.Tags.DOC_TYPE, list_pos_condition):
            # Get filter string
            conditions_string = self.get_filter_string_document_type_for_all_deltas(
                doc_type=doc_type,
                dpi_tags=DARConfiguration.get_dpi_tag_by_dpi(dpi))

            # Get line data
            line_data = self.get_accuracy_line_data(line_header=doc_type,
                                                    line=line,
                                                    conditions_string=
                                                    conditions_string[
                                                        self.current_delta],
                                                    start_column=start_column)
            # Write data
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_formats,
                                         start_position=start_column)

            line += 1

        sheet.set_column(0, 7, 15)

        self.logger.end_step(True)

    def add_accuracy_by_use_case_sheet(self, list_supported_dpi):
        self.logger.start_step(
            "Make {0} sheet".format(DARConfiguration.SHEET_BY_USE_CASE))
        sheet = self.book.add_worksheet(name=DARConfiguration.SHEET_BY_USE_CASE)
        start_column = 1
        start_position = 1
        product_format = self.get_cell_format(set_bold=True,
                                              set_border=True,
                                              align=Align.CENTER,
                                              bg_color=Color.CUSTOM_GREEN)
        for dpi in list_supported_dpi:
            start_line = 1
            if not dpi == list_supported_dpi[0]:
                start_column += 6
                start_position += 6
            sheet.merge_range(start_line, start_position, start_line,
                              start_position + 4,
                              data=DARConfiguration.get_dpi_tag_by_dpi(dpi),
                              cell_format=product_format)
            start_line += 2
            binding_condition = {
                DARConfiguration.get_dpi_tag_by_dpi(dpi): DARConfiguration.HAS_VALUE
            }
            for use_case in DARConfiguration.LIST_USE_CASES:
                conditions_string = \
                    self.get_filter_string_use_case_for_all_deltas(
                        use_case=use_case,
                        binding_condition=binding_condition)
                start_line += \
                    self.write_block_accuracy_progress(sheet=sheet,
                                                       block_name=use_case,
                                                       conditions_string=conditions_string,
                                                       start_line=start_line,
                                                       start_column=start_column)
                start_line += 2

            sheet.set_column(start_column, start_column, 20)
            sheet.set_column(start_column + 1, start_column + 5, 15)
        self.logger.end_step(True)

    def add_accuracy_by_language_sheet(self, list_supported_dpi):
        self.logger.start_step("Make {0} sheet".format(DARConfiguration.SHEET_BY_LANGUAGE))
        sheet = self.book.add_worksheet(name=DARConfiguration.SHEET_BY_LANGUAGE)
        start_column = 1
        start_position = 1
        product_format = self.get_cell_format(set_bold=True,
                                              set_border=True,
                                              align=Align.CENTER,
                                              bg_color=Color.CUSTOM_GREEN)
        for dpi in list_supported_dpi:
            binding_condition = {
                SpecKeys.Tags.IS_MAINLY_TEXT: DARConfiguration.HAS_VALUE,
                SpecKeys.Tags.HAS_CONTRAST: DARConfiguration.IS_EMPTY,
                SpecKeys.Tags.IS_PRESENTATION: DARConfiguration.IS_EMPTY,
                SpecKeys.Tags.IS_CLIPPED_IMAGE: DARConfiguration.IS_EMPTY
            }
            binding_condition.update({DARConfiguration.get_dpi_tag_by_dpi(
                dpi): DARConfiguration.HAS_VALUE})
            start_line = 1
            if not dpi == list_supported_dpi[0]:
                start_column += 6
                start_position += 6
            sheet.merge_range(start_line, start_position, start_line,
                              start_position + 4,
                              data=DARConfiguration.get_dpi_tag_by_dpi(dpi),
                              cell_format=product_format)
            start_line += 2
            for language in DARConfiguration.LANG_BY_ORDER:
                conditions_string = self.get_filter_string_language_for_all_deltas(
                    language=language,
                    binding_condition=binding_condition)
                start_line += self.write_block_accuracy_progress(sheet=sheet,
                                                                 block_name=language,
                                                                 conditions_string=conditions_string,
                                                                 start_line=start_line,
                                                                 start_column=start_column)
                start_line += 2

            sheet.set_column(start_column, start_column, 20)
            sheet.set_column(start_column + 1, start_column + 5, 15)
        self.logger.end_step(True)

    def add_delta_sheet(self, delta):
        # Initial sheet
        sheet_name = self.get_delta_sheet_name(delta=delta)
        sheet = self.book.add_worksheet(name=sheet_name)
        line = 0
        header_format = self.get_cell_format(set_bold=True, bg_color=Color.CUSTOM_GREEN, set_border=True,
                                             align=Align.CENTER)
        self.logger.add_line("Headers: " + ",".join(self.headers))
        self.write_line(sheet=sheet, line=line, value_array=self.headers, cell_format=header_format)

        # Write test data
        total = len(self.list_test_names)
        count = 0
        test_name_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True, align=Align.RIGHT, num_format='#,##0')
        tag_value_format = self.get_cell_format(set_border=True, align=Align.CENTER)
        # Test name format
        line_formats = [test_name_format]
        # Errors and total characters format
        for i in range(0, len(self.private_headers) -1):
            line_formats.append(number_format)
        # Tags
        for i in range(0, len(self.tag_headers)):
            line_formats.append(tag_value_format)
        # Get data line
        for test_name in self.list_test_names:
            count += 1
            line += 1
            # Create line mapping for test case
            self.logger.add_line("[{0}/{1}] Test case {2}".format(count, total, test_name))
            # Test name
            line_data = [test_name]

            phocr_data = self.get_phocr_accuracy_data(test_name, delta)
            esdk_total_errors = \
                self.get_esdk_accuracy_delta(test_name=test_name, delta=self.newest_esdk_version)
            phocr_data.insert(-1, esdk_total_errors)
            line_data += phocr_data
            # Tags value
            line_data += self.tags_informer.get_tags_value(test_id=test_name,
                                                           list_tags=self.tag_headers)

            # Write line data
            self.write_line_multi_format(sheet=sheet, line=line, values=line_data,
                                         formats=line_formats)

        # Specific column width
        # Test name column
        sheet.set_column(0, 0, 36)
        # Errors columns
        last_col = 7 + len(self.tag_headers)
        sheet.set_column(1, last_col, 15)
        if delta != self.current_delta:
            sheet.hide()

    @abstractmethod
    def get_phocr_accuracy_data(self, test_name, delta):
        pass

    @abstractmethod
    def get_esdk_accuracy_delta(self, test_name, delta):
        pass

    def get_filter_string_language_for_all_deltas(self, language,
                                                  binding_condition=None):
        """

        Parameters
        ----------
        language: specific language to get condition
        binding_condition: condition of data correspond with header

        Returns
        -------

        """
        filters = {}
        for delta in self.deltas:
            # Some additional conditions
            conditions = list()
            for item in binding_condition:
                conditions.append(
                    self.get_condition_string(delta=delta,
                                              header=item,
                                              value=binding_condition[item]))
            # Language condition
            conditions.append(self.get_condition_string(delta=delta,
                                                        header=SpecKeys.Tags.LANGS,
                                                        value="\"{0}\"".format(language)))
            if self.primary_conditions_string[delta]:
                conditions.append(self.primary_conditions_string[delta])
            conditions_string = ",".join(conditions)
            filters[delta] = conditions_string
        return filters

    def get_filter_string_use_case_for_all_deltas(self, use_case,
                                                  binding_condition=None):
        """

        Parameters
        ----------
        use_case: use case to get condition
        binding_condition: condition of data correspond with header

        Returns
        -------

        """
        filters = {}
        for delta in self.deltas:
            conditions = list()
            if binding_condition:
                for item in binding_condition:
                    conditions.append(
                        self.get_condition_string(delta=delta,
                                                  header=item,
                                                  value=binding_condition[item]))
            conditions.append(self.get_condition_string(delta=delta,
                                                        header=use_case,
                                                        value="\"x\""))
            if self.primary_conditions_string[delta]:
                conditions.append(self.primary_conditions_string[delta])
            conditions_string = ",".join(conditions)
            filters[delta] = conditions_string
        return filters

    def get_filter_string_document_type_for_all_deltas(self, doc_type, dpi_tags=None):
        """
        Get data filter by document type.
        Parameters
        ----------
        doc_type: document type
        dpi_tags: image dpi will be filtered by (if have)

        Returns
        -------

        """
        filters = {}
        for delta in self.deltas:
            conditions = list()
            conditions.append(self.get_condition_string(delta=delta,
                                                        header=SpecKeys.Tags.DOC_TYPE,
                                                        value="\"{0}\"".format(
                                                            doc_type)))
            if dpi_tags:
                conditions.append(self.get_condition_string(delta=delta,
                                                            header=dpi_tags,
                                                            value="\"x\""))
            if self.primary_conditions_string[delta]:
                conditions.append(self.primary_conditions_string[delta])
            conditions_string = ",".join(conditions)
            filters[delta] = conditions_string
        return filters

    def get_progress_line_data(self, line_header, line, conditions_string, start_column=0):
        # Get line data
        line_data = [line_header]
        # Number of pages
        num_pages_formula = self.get_count_formula(
            conditions_string=conditions_string)
        line_data.append(num_pages_formula)
        # PHOcr total errors
        phocr_errors_column = start_column + len(line_data)
        phocr_errors_formula = self.get_sum_formula(
            self.phocr_errors_range[self.current_delta],
            conditions_string)
        line_data.append(phocr_errors_formula)
        # PHOcr total characters
        phocr_chars_column = start_column + len(line_data)
        phocr_chars_formula = self.get_sum_formula(
            self.phocr_chars_range[self.current_delta],
            conditions_string)
        line_data.append(phocr_chars_formula)
        # PHOcr accuracy
        phocr_errors_cell = self.get_cell_str(line_idx=line,
                                              col_idx=phocr_errors_column)
        phocr_chars_cell = self.get_cell_str(line_idx=line,
                                             col_idx=phocr_chars_column)
        phocr_accuracy_formula = self.get_accuracy_formula(
            errors_cell=phocr_errors_cell,
            total_cell=phocr_chars_cell)
        line_data.append(phocr_accuracy_formula)
        # e-SDK total errors
        esdk_errors_column = start_column + len(line_data)
        esdk_errors_formula = self.get_sum_formula(
            self.esdk_errors_range[self.current_delta],
            conditions_string)
        line_data.append(esdk_errors_formula)
        # e-SDK total characters
        esdk_chars_column = start_column + len(line_data)
        esdk_chars_formula = self.get_sum_formula(
            self.esdk_chars_range[self.current_delta],
            conditions_string)
        line_data.append(esdk_chars_formula)
        # e-SDK accuracy
        esdk_errors_cell = self.get_cell_str(line_idx=line,
                                             col_idx=esdk_errors_column)
        esdk_chars_cell = self.get_cell_str(line_idx=line,
                                            col_idx=esdk_chars_column)
        esdk_accuracy_formula = self.get_accuracy_formula(
            errors_cell=esdk_errors_cell,
            total_cell=esdk_chars_cell)
        line_data.append(esdk_accuracy_formula)
        return line_data

    def get_accuracy_line_data(self, line_header, line, conditions_string, start_column=0):
        """
        Get Accuracy line data
        Parameters
        ----------
        line_header: line header
        line
        conditions_string: condition to get data
        start_column: start column in output file

        Returns
        -------

        """
        # Get line data
        line_data = [line_header]
        # Number of pages
        num_pages_formula = self.get_count_formula(
            conditions_string=conditions_string)
        line_data.append(num_pages_formula)
        # PHOcr total errors
        phocr_errors_column = start_column + len(line_data)
        phocr_errors_formula = self.get_sum_formula(
            self.phocr_errors_range[self.current_delta],
            conditions_string)
        line_data.append(phocr_errors_formula)
        # PHOcr total characters
        phocr_chars_column = start_column + len(line_data)
        phocr_chars_formula = self.get_sum_formula(
            self.phocr_chars_range[self.current_delta],
            conditions_string)
        line_data.append(phocr_chars_formula)
        # PHOcr accuracy
        phocr_errors_cell = self.get_cell_str(line_idx=line,
                                              col_idx=phocr_errors_column)
        phocr_chars_cell = self.get_cell_str(line_idx=line,
                                             col_idx=phocr_chars_column)
        phocr_accuracy_formula = self.get_accuracy_formula(
            errors_cell=phocr_errors_cell,
            total_cell=phocr_chars_cell)
        line_data.append(phocr_accuracy_formula)
        return line_data

    # This function write a block data (corresponding to a filter by conditions)
    # Block name
    # Product version, total errors, total characters, accuracy, number of pages
    def write_block_accuracy_progress(self, sheet, block_name,
                                      conditions_string, start_line,
                                      start_column=0):
        header_format = self.get_cell_format(set_border=True,
                                             align=Align.CENTER,
                                             set_bold=True,
                                             bg_color=Color.CUSTOM_GREEN)
        text_format = self.get_cell_format(set_border=True, align=Align.LEFT)
        number_format = self.get_cell_format(set_border=True,
                                             num_format='#,##0',
                                             align=Align.RIGHT,
                                             bg_color=Color.CUSTOM_YELLOW)
        accuracy_format = self.get_cell_format(set_border=True,
                                               num_format='0.00%',
                                               align=Align.RIGHT,
                                               bg_color=Color.CUSTOM_RED)
        line_formats = [text_format,
                        number_format,
                        number_format,
                        number_format,
                        accuracy_format]
        # Write block name
        line = start_line
        self.write_cell(sheet=sheet,
                        line=line,
                        column=start_column,
                        cell_format=header_format,
                        value=block_name)
        # Header line
        line += 1
        self.write_line(sheet=sheet,
                        line=line,
                        value_array=self.block_progress_headers,
                        cell_format=header_format,
                        start_position=start_column)
        # Accuracy of PHOcr deltas
        for delta in sorted(self.deltas):
            line += 1
            product_name = self.get_delta_sheet_name(delta=delta)
            line_data = [product_name]
            delta_filter = conditions_string[delta]
            # Number of pages
            num_pages_formula = self.get_count_formula(
                conditions_string=delta_filter)
            line_data.append(num_pages_formula)
            # PHOcr total errors
            phocr_errors_column = start_column + len(line_data)
            phocr_errors_formula = self.get_sum_formula(
                self.phocr_errors_range[delta],
                delta_filter)
            line_data.append(phocr_errors_formula)
            # PHOcr total characters
            phocr_chars_column = start_column + len(line_data)
            phocr_chars_formula = \
                self.get_sum_formula(self.phocr_chars_range[delta],
                                     delta_filter)
            line_data.append(phocr_chars_formula)
            # PHOcr accuracy
            phocr_errors_cell = self.get_cell_str(line_idx=line,
                                                  col_idx=phocr_errors_column)
            phocr_chars_cell = self.get_cell_str(line_idx=line,
                                                 col_idx=phocr_chars_column)
            phocr_accuracy_formula = self.get_accuracy_formula(
                errors_cell=phocr_errors_cell,
                total_cell=phocr_chars_cell)
            line_data.append(phocr_accuracy_formula)
            self.write_line_multi_format(sheet=sheet,
                                         line=line,
                                         values=line_data,
                                         formats=line_formats,
                                         start_position=start_column)
        return line - start_line + 1

    def get_some_history_informers(self):
        pass

    def get_deltas_report_list(self):
        all_deltas = self.phocr_test_machine_informer.get_list_deltas()
        if not all_deltas:
            self.logger.log_and_print("No data available!")
            sys.exit(0)
        min_near_delta = all_deltas[0] - DARConfiguration.NUM_LAST_DELTA
        min_delta = all_deltas[0] - DARConfiguration.RANGE_LAST_DELTA
        for i in range(0, len(all_deltas)):
            delta = all_deltas[i]
            if delta > min_near_delta:
                self.deltas.append(delta)
            elif (delta > min_delta) and (delta % DARConfiguration.DELTA_STEP == 0):
                self.deltas.append(delta)

    def get_primary_conditions_string_for_all_delta(self):
        # Need to have phocr errors, esdk errors and total characters
        filters = {}
        for delta in self.deltas:
            conditions = list()
            conditions.append(
                self.get_condition_string(delta=delta,
                                          header=DARConfiguration.TOTAL_ERRORS, value="\"<>\""))
            conditions.append(
                self.get_condition_string(delta=delta,
                                          header=DARConfiguration.TOTAL_CHARACTERS, value="\"<>\""))
            filters[delta] = ",".join(conditions)

        return filters

    def get_delta_sheet_name(self, delta):
        return "D{0}".format(delta)

    def prepare_private_data(self):
        # Get some information range
        # Get some information range: PHOcr total errors, e-SDK total errors, total characters
        for delta in self.deltas:
            self.phocr_errors_range[delta] = self.get_range_string(delta=delta,
                                                            header=DARConfiguration.TOTAL_ERRORS)
            self.phocr_chars_range[delta] = self.get_range_string(delta=delta,
                                                           header=DARConfiguration.TOTAL_CHARACTERS)
            self.esdk_errors_range[delta] = self.get_range_string(delta=delta,
                                                           header=DARConfiguration.ESDK_ERRORS)
            self.esdk_chars_range[delta] = self.get_range_string(delta=delta,
                                                          header=DARConfiguration.TOTAL_CHARACTERS)
        # Headers of a block data progress
        self.block_progress_headers = [DARConfiguration.VERSION,
                                       DARConfiguration.NUM_PAGES,
                                       DARConfiguration.TOTAL_ERRORS,
                                       DARConfiguration.TOTAL_CHARACTERS,
                                       DARConfiguration.ACCURACY]

        # Prepare instance report data
        self.prepare_instance_data()
        esdk_deltas = self.esdk_informer.get_list_deltas()
        if esdk_deltas:
            self.newest_esdk_version = esdk_deltas[0]
        else:
            self.newest_esdk_version = []

    def recheck_list_test_names(self):
        pass

    @abstractmethod
    def prepare_instance_data(self):
         pass
