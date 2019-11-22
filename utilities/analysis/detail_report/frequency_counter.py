# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      17/05/2017
# Last update:      17/05/2107
# Description:      Count frequency of list string

class FreqData:
    def __init__(self, content = None, freq = 0, replace = None):
        self.content = None
        self.frequency = 0
        self.replace = None

class FrequencyCounter:
    # Initial
    def __init__(self):
        self.data = []      # List of FreqData

    # @return: data
    def CountListString(self, string_list):
        self.data = []

        for s in string_list:
            founded = False

            for element in self.data:

                if s == element.content:
                    founded = True
                    element.frequency += 1

            if not founded:
                self.data.append(FreqData(s, 1))

        return self.data

    # @return: data
    def CountListString2D(self, list_data):
        self.data = []

        for arr in list_data:
            founded = False
            content = arr[0]
            replace = arr[1]

            for element in self.data:

                if (content == element.content) and (replace == element.replace):
                    founded = True
                    element.frequency += 1

            if not founded:
                self.data.append(FreqData(content, 1, replace))

        return self.data
