# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      03/07/2018
# Updated by:       Phung Dinh Tai
# Description:      Define base class for cell format in excel


COLH = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J","K", "L", "M", "N", "O", "P", "Q", "R",
        "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH",
        "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AU", "AV", "AW", "AX",
        "AY", "AZ", "BA", "BB", "BC", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BK", "BL", "BM",
        "BN", "BO", "BP", "BQ", "BR", "BS", "BT", "BU", "BV", "BW", "BX", "BY", "BZ"]


class Color(object):
    CUSTOM_GREEN = "#A9D08E"
    GREEN = "green"
    CUSTOM_YELLOW = "#FFF2CC"
    YELLOW = "yellow"
    CUSTOM_RED = "#F8CBAD"
    RED = "red"
    ORANGE = "#FFC000"
    CUSTOM_GREY = "#C0C0C0"
    GREY = "#ACB9CA"
    WHITE = 'white'
    BLACK = 'black'
    BROWN = "#DA9694"
    SLIGHT_BROWN = "#F2DCDB"
    BLUE = "#92CDDC"
    HEAVY_RED = "#D40139"
    LIGHT_GREEN = "#C2DFAB"
    LIGHT_ORANGE = "#FAEBB0"


class Align(object):
    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
