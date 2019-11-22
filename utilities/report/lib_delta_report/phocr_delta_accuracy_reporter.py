# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Le Thi Thanh
# Email:            thanh.lethi@toshiba-tsdv.com
# Date create:      22/05/2019
from abc import ABCMeta
from configs.database import SpecKeys
from configs.projects.phocr import PhocrProject
from report.lib_delta_report.delta_accuracy_reporter import DeltaAccuracyReporter, DARConfiguration
from report.lib_base.defines import ReportTitles, ReportNames


class PHOcrDeltaAccuracyReporter(DeltaAccuracyReporter):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(PHOcrDeltaAccuracyReporter, self).__init__(**kwargs)

    def prepare_instance_data(self):
        self.output_file = ReportNames.DELTA_ACCURACY.format(self.current_delta,
                                                             self.platform)
        self.title = ReportTitles.DELTA_ACCURACY
        self.phocr_test_machine_informer.report_title = self.title
        self.esdk_informer.report_title = self.title

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
        return [DARConfiguration.TEST_NAME,
                DARConfiguration.DELETE_ERRORS,
                DARConfiguration.INSERT_ERRORS,
                DARConfiguration.REPLACE_ERRORS,
                DARConfiguration.TOTAL_ERRORS,
                DARConfiguration.ESDK_ERRORS,
                DARConfiguration.TOTAL_CHARACTERS]

    def get_phocr_accuracy_data(self, test_name, delta):
        list_functions = self.test_cases_manager.get_functions(test_name)
        if PhocrProject.functionalities.TEXT_LAYOUT in list_functions:
            return self.phocr_test_machine_informer.get_bb_accuracy(
                test_id=test_name, delta=delta)
        elif PhocrProject.functionalities.EXPORT_TXT in list_functions:
            return self.phocr_test_machine_informer.get_text_accuracy(
                test_id=test_name, delta=delta)
        else:
            return []

    def get_esdk_accuracy_delta(self, test_name, delta):
        return self.esdk_informer.get_text_total_errors(test_id=test_name,
                                                        delta=delta)
