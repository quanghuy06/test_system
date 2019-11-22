# TOSHIBA - TSDV
# Team:             OCRPoc
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      28/12/2016
# Last update:      28/12/2106
# Description:      This configure information for workspace on samba server

import getpass

# Map email address to samba username
email_mapping = {}
email_mapping["tai.phungdinh@toshiba-tsdv.com"] = "taipd"
email_mapping["huan.luongvan@toshiba-tsdv.com"] = "huanlv"
email_mapping["nam.leduc@toshiba-tsdv.com"] = "namld"
email_mapping["thuy.taphuong@toshiba-tsdv.com"] = "thuyttp"
email_mapping["binh.nguyenkhanh@toshiba-tsdv.com"] = "binhnk"
email_mapping["nam.nguyenbao@toshiba-tsdv.com"] = "namnb"
email_mapping["dat.vutien@toshiba-tsdv.com"] = "datvt"

# General information about samba server
general = {}
general["server"] = "10.116.41.96"
general["disk"] = ""
general["directory"] = ""

class WorkSpaceConfig :
    SRC = "SRC"
    TEST_CASE = "TESTS"
    UTILITY = "UTILITIES"
    REVIEW = "REVIEW"
    DEFAULT_MP = "/tmp"
    DEFAULT_WS = "/home/{0}/workspace".format(getpass.getuser())
    DEFAULT_PASSWD = "1"

    CMD_GET_UTILITY = "smbclient //10.116.41.96/Share --directory utilities" \
                      " -U taipd%1 -c \"prompt OFF; recurse ON; mget *\""
