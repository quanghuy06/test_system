# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      20/01/2017
# Last update:      03/07/2107
# Editor:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Description:      Class to define Barcode entity
from configs.compare_result import BarcodeCmpType


class Barcode:
    def __init__(self, string_format, content):
        self.format = string_format.strip()
        self.content = content.strip()
        self.bbox = None  # Rectangle

    def compare_with(self, bar):

        if self.format == bar.format:
            if self.content == bar.content:
                # Same format, same content
                return BarcodeCmpType.simple.TYPE_1
            else:
                # Same format, different content
                return BarcodeCmpType.simple.TYPE_2
        else:
            if self.content == bar.content:
                # Different format, same content
                return BarcodeCmpType.simple.TYPE_3
            else:
                # Different both format and content
                return BarcodeCmpType.simple.TYPE_4

    # Same location if overlap area is over 0.8
    def compare_location_with(self, bar):

        if (not self.bbox) or (not bar.bbox):
            return BarcodeCmpType.location.DIFFER
        same_location = (self.bbox.GetOverlapPercent(bar.bbox) >= BarcodeCmpType.THRESHOLD) and\
                        (bar.bbox.GetOverlapPercent(self.bbox) >= BarcodeCmpType.THRESHOLD)
        if not same_location:
            return BarcodeCmpType.location.DIFFER
        else:
            if self.compare_with(bar) == BarcodeCmpType.simple.TYPE_1:
                return BarcodeCmpType.location.CORRECT
            else:
                return BarcodeCmpType.location.REPLACE

    def to_string(self):
        return "{0}:{1}".format(self.format, self.content)
