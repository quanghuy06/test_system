# TOSHIBA - Toshiba Software Development Vietnam
# Team:             PHOcr
# Author:           Tai Phung Dinh
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      02/01/2019
from abc import ABCMeta

from database.lib_test_case.lib_specification.lib_tags.language_enum import \
    LanguageEnum
from database.lib_test_case.lib_specification.lib_tags.platform_enum import \
    PlatformEnum
from validate.lib_base.mekong_int import MekongInt
from validate.lib_base.mekong_object import MekongObject
from validate.lib_base.mekong_parser import MekongParser
from validate.lib_base.mekong_string import MekongString
from validate.lib_base.mekong_bool import MekongBool


class Tags(MekongObject):
    """
    Class presents some useful information of test case. Tags' name is
    defined in SpecKeys.Tags
    Tag can have multiple types of value:
        - Bool tag: IsETDefault, HasTable,...
        - Int tag: DocumentPage
        - String tag: DocumentName, CommandLineOption,...
        - List of string: Language, Platforms

    """

    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):
        super(Tags, self).__init__(**kwargs)
        self.BugNumbers = MekongParser.generate_list_form_json(
            self._get_json_for("BugNumbers"),
            class_name=MekongString,
            empty_available=True)
        self.CommandLineOptions = MekongParser.generate_object_from_json(
            self._get_json_for("CommandLineOptions"),
            class_name=MekongString,
            empty_available=True)
        self.DocumentName = MekongParser.generate_object_from_json(
            self._get_json_for("DocumentName"),
            class_name=MekongString,
            empty_available=True)
        self.DocumentPage = MekongParser.generate_object_from_json(
            self._get_json_for("DocumentPage"),
            class_name=MekongInt)
        self.DocumentType = MekongParser.generate_object_from_json(
            self._get_json_for("DocumentType"),
            class_name=MekongString,
            empty_available=True)
        self.GetAccuracy = MekongParser.generate_object_from_json(
            self._get_json_for("GetAccuracy"),
            class_name=MekongBool)
        self.HasBarcode = MekongParser.generate_object_from_json(
            self._get_json_for("HasBarcode"),
            class_name=MekongBool)
        self.HasChart = MekongParser.generate_object_from_json(
            self._get_json_for("HasChart"),
            class_name=MekongBool)
        self.HasContrast = MekongParser.generate_object_from_json(
            self._get_json_for("HasContrast"),
            class_name=MekongBool)
        self.HasImage = MekongParser.generate_object_from_json(
            self._get_json_for("HasImage"),
            class_name=MekongBool)
        self.HasLogoCompany = MekongParser.generate_object_from_json(
            self._get_json_for("HasLogoCompany"),
            class_name=MekongBool)
        self.HasTable = MekongParser.generate_object_from_json(
            self._get_json_for("HasTable"),
            class_name=MekongBool)
        self.HasTextbox = MekongParser.generate_object_from_json(
            self._get_json_for("HasTextbox"),
            class_name=MekongBool)
        self.HasWaterMask = MekongParser.generate_object_from_json(
            self._get_json_for("HasWaterMask"),
            class_name=MekongBool)
        self.IsCourtDocument = MekongParser.generate_object_from_json(
            self._get_json_for("IsCourtDocument"),
            class_name=MekongBool)
        self.IsETDefault = MekongParser.generate_object_from_json(
            self._get_json_for("IsETDefault"),
            class_name=MekongBool)
        self.IsExcel = MekongParser.generate_object_from_json(
            self._get_json_for("IsExcel"),
            class_name=MekongBool)
        self.IsExtremeTest = MekongParser.generate_object_from_json(
            self._get_json_for("IsExtremeTest"),
            class_name=MekongBool)
        self.IsForm = MekongParser.generate_object_from_json(
            self._get_json_for("IsForm"),
            class_name=MekongBool)
        self.IsInvoice = MekongParser.generate_object_from_json(
            self._get_json_for("IsInvoice"),
            class_name=MekongBool)
        self.IsLegalDocument = MekongParser.generate_object_from_json(
            self._get_json_for("IsLegalDocument"),
            class_name=MekongBool)
        self.IsLetter = MekongParser.generate_object_from_json(
            self._get_json_for("IsLetter"),
            class_name=MekongBool)
        self.IsMainlyText = MekongParser.generate_object_from_json(
            self._get_json_for("IsMainlyText"),
            class_name=MekongBool)
        self.IsMemCheckTest = MekongParser.generate_object_from_json(
            self._get_json_for("IsMemCheckTest"),
            class_name=MekongBool)
        self.IsMemCheckPeak = MekongParser.generate_object_from_json(
            self._get_json_for("IsMemCheckPeak"),
            class_name=MekongBool)
        self.IsMultiByteLanguage = MekongParser.generate_object_from_json(
            self._get_json_for("IsMultiByteLanguage"),
            class_name=MekongBool)
        self.IsMultiColumn = MekongParser.generate_object_from_json(
            self._get_json_for("IsMultiColumn"),
            class_name=MekongBool)
        self.IsMultiPages = MekongParser.generate_object_from_json(
            self._get_json_for("IsMultiPages"),
            class_name=MekongBool)
        self.IsPresentation = MekongParser.generate_object_from_json(
            self._get_json_for("IsPresentation"),
            class_name=MekongBool)
        self.IsPurchaseOrder = MekongParser.generate_object_from_json(
            self._get_json_for("IsPurchaseOrder"),
            class_name=MekongBool)
        self.IsFaxDocument = MekongParser.generate_object_from_json(
            self._get_json_for("IsFaxDocument"),
            class_name=MekongBool)
        self.IsUNLV = MekongParser.generate_object_from_json(
            self._get_json_for("IsUNLV"),
            class_name=MekongBool)
        self.Language = MekongParser.generate_list_form_json(
            self._get_json_for("Language"),
            class_name=LanguageEnum)
        self.NonIntegration = MekongParser.generate_object_from_json(
            self._get_json_for("NonIntegration"),
            class_name=MekongBool)
        self.Platform = MekongParser.generate_list_form_json(
            self._get_json_for("Platform"),
            class_name=PlatformEnum)
        self.IsPrintAsColor = MekongParser.generate_object_from_json(
            self._get_json_for("IsPrintAsColor"),
            class_name=MekongBool)
        self.IsPrintAsGray = MekongParser.generate_object_from_json(
            self._get_json_for("IsPrintAsGray"),
            class_name=MekongBool)
        self.IsPrintAsMono = MekongParser.generate_object_from_json(
            self._get_json_for("IsPrintAsMono"),
            class_name=MekongBool)
        self.Is200dpi = MekongParser.generate_object_from_json(
            self._get_json_for("Is200dpi"),
            class_name=MekongBool)
        self.Is300dpi = MekongParser.generate_object_from_json(
            self._get_json_for("Is300dpi"),
            class_name=MekongBool)
        self.IsDeskew = MekongParser.generate_object_from_json(
            self._get_json_for("IsDeskew"),
            class_name=MekongBool)
        self.IsRotate = MekongParser.generate_object_from_json(
            self._get_json_for("IsRotate"),
            class_name=MekongBool)
        self.IsClippedImage = MekongParser.generate_object_from_json(
            self._get_json_for("IsClippedImage"),
            class_name=MekongBool)
