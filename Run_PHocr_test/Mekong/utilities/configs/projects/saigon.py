# Toshiba - TSDV
# Team:     PHOcr
# Author:   Phung Dinh Tai
# Email:    tai.phungdinh@gmail.com
# Date created:     23/06/2017
# Last updated:     23/06/2017
# Description:  This script defines all information for HanoiWorkflow project. The following
#               configuration will be used in whole project. Please give correct information
#               to ensure all work fine.

class SaigonProject:

    NAME = "SaigonDiff"
    PRODUCT = "saigon"

    class components:
        DEFAULT = "SaigonDiff"
        WIN_DEFAULT = "SaigonDiff.exe"

    class functionalities:
        CMP_TEXT = "compare text"
        CMP_BB = "compare bounding box"
        TOTAL_CHARACTER = "total character"
