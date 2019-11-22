# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/07/2018
# Updated by:       Phung Dinh Tai
# Description:
from abc import ABCMeta
from report.lib_delta_report.delta_accuracy_reporter import DeltaAccuracyReporter, DARConfiguration
from configs.database import SpecKeys
from configs.projects.phocr import PhocrProject
from report.lib_base.defines import ReportTitles, ReportNames


class PHOcrDeltaTextAccuracyReporter(DeltaAccuracyReporter):

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(PHOcrDeltaTextAccuracyReporter, self).__init__(**kwargs)

    def get_filters(self):
        tags_filter = "{accuracy}:true&{non_integration}:false&{platform_tag}:{platform_value}" \
                      "".format(accuracy=SpecKeys.Tags.ACCURACY,
                                non_integration=SpecKeys.Tags.IS_NON_INTEGRATION,
                                platform_tag=SpecKeys.Tags.PLATFORMS,
                                platform_value=self.platform)
        return {
            SpecKeys.PRODUCT: PhocrProject.PRODUCT,
            SpecKeys.FUNCTIONALITIES: PhocrProject.functionalities.EXPORT_TXT,
            SpecKeys.TAGS: tags_filter
        }

    def prepare_instance_data(self):
        self.output_file = \
            ReportNames.DELTA_TEXT_ACCURACY.format(self.current_delta,
                                                   self.platform)
        self.title = ReportTitles.DELTA_TEXT_ACCURACY
        self.phocr_test_machine_informer.report_title = self.title
        self.esdk_informer.report_title = self.title

    def get_private_headers(self):
        return [DARConfiguration.TEST_NAME,
                DARConfiguration.TOTAL_ERRORS,
                DARConfiguration.ESDK_ERRORS,
                DARConfiguration.TOTAL_CHARACTERS]

    def get_phocr_accuracy_data(self, test_name, delta):
        return self.phocr_test_machine_informer.get_text_accuracy(
            test_id=test_name, delta=delta)

    def get_esdk_accuracy_delta(self, test_name, delta):
        return self.esdk_informer.get_text_total_errors(test_id=test_name,
                                                        delta=delta)
