# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      28/06/2017
# Last update:      03/07/2107
# Editor:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Description:      Change specification of test case from old format to new format of
#                   tags attributes

import sys_path
sys_path.insert_sys_path()
import argparse
import sys

from baseapi.file_access import *

DEFAULT_TAGS = {
    "DocumentName" : "",
    "DocumentType" : "",
    "DocumentPage" : "",
    "Language" : [],
    "GetAccuracy" : False,
    "IsInvoice" : False,
    "IsPurchaseOrder" : False,
    "IsForm" : False,
    "IsMainlyText" : False,
    "IsLetter" : False,
    "BugNumbers" : [],
    "IsPresentation" : False,
    "IsLegalDocument" : False,
    "IsCourtDocument" : False,
    "IsMultiColumn" : False,
    "IsMultiByteLanguage" : False,
    "HasTable" : False,
    "HasImage" : False,
    "HasChart" : False,
    "HasContrast" : False,
    "HasWaterMask" : False,
    "HasLogoCompany" : False,
    "IsETDefault" : False,
    "IsError" : False
}

class spec:
    PRODUCT = "product"
    ENABLE = "enable"
    FUNCTIONALITIES = "functionalities"
    WEIGHT = "weight"
    TAGS = "tags"
    COMPONENT = "component"
    ID = "_id"
    class tags:
        ACCURACY = "accuracy"
        BASIC = "basic"
        DOC_TYPE = "document_type"
        LANGUAGE = "language"
    class functionalities:
        OCR = "ocr"
        BARCODE = "barcode"

class SpecHandler:

    def __init__(self, spec_file):
        self.spec_info = read_json(spec_file)


    # Check if test case has a tag or not
    def HasTag(self, tag):
        if tag in self.spec_info[spec.TAGS]:
            return True
        else:
            return False

    # Check if test case has a functionality or not
    def HasFunctionality(self, func):
        if func in self.spec_info[spec.FUNCTIONALITIES]:
            return True
        else:
            return False

    # Get document type of test case
    def GetDocumentType(self):
        try:
            tags = self.spec_info[spec.TAGS]
            for tag in tags:
                if spec.tags.DOC_TYPE in tag:
                    doc_type = tag.split(":")[1]
                    doc_type = doc_type.strip()
                    return doc_type.lower()
            return ""
        except:
            return ""

            # Get language of test case

    def GetLanguage(self):
        try:
            tags = self.spec_info[spec.TAGS]
            for tag in tags:
                if spec.tags.LANGUAGE in tag:
                    language = tag.split(":")[1]
                    language = language.strip()
                    return language.lower()
            return "english"
        except:
            return "english"

    # Get product of test case
    def GetProduct(self):
        try:
            return self.spec_info[spec.PRODUCT]
        except:
            return ""

def parse_argument():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--test-folder", required=True,
                        help="Folder contains test cases")
    parser.add_argument("--renew-spec", default=False, action="store_true",
                        help="Change tag from old structure to new structure")
    parser.add_argument("--update-tags", default=False, action="store_true",
                        help="Update existed tags using format"
                             " <tag_name>:<type>:<value>|<tag_name>:<type>:<value>"
                             "\nType available: bool, string, list"
                             "\nValue of type list using comma to seperate components")
    parser.add_argument("--add-tags", default=False, action="store_true",
                        help="Insert new tags using format"
                             " <tag_name>:<type>:<value>|<tag_name>:<type>:<value>"
                             "\nType available: bool, string, list"
                             "\nValue of type list using comma to seperate components")
    return parser

def main():
    parser = parse_argument()
    args = parser.parse_args()
    # Change tag from old structure to new structure
    if args.renew_spec:
        target_folder = "TESTS_RENEWED"
        if os.path.isdir(target_folder):
            remove_globs(os.path.join(target_folder, "*"))
        else:
            os.makedirs(target_folder)
        for test_case in sorted(os.listdir(args.test_folder)):
            print test_case
            test_case_path = os.path.join(args.test_folder, test_case)
            copy_paths(test_case_path, target_folder)
            spec_file = os.path.join(target_folder, test_case, "spec.json")
            spec_old = read_json(spec_file)
            # Renew tags attribute
            tags = DEFAULT_TAGS
            spec_handler = SpecHandler(spec_file)
            tags["Language"] = [spec_handler.GetLanguage()]
            tags["DocumentType"] = spec_handler.GetDocumentType()
            if spec_handler.HasTag("accuracy"):
                tags["GetAccuracy"] = True
            else:
                tags["GetAccuracy"] = False
            if spec_handler.HasTag("ET-default"):
                tags["IsETDefault"] = True
            else:
                tags["IsETDefault"] = False
            spec_old["tags"] = tags
            # Renew functionalities and component
            if spec_handler.GetProduct() == "phocr":
                if spec_handler.HasFunctionality("barcode"):
                    spec_old["component"] = "barcode"
                    spec_old["functionalities"] = ["barcode"]
                else:
                    spec_old["component"] = "PHOcrExe"
                    spec_old["functionalities"] = ["OCR", "Segmentation"]
            if spec_handler.GetProduct() == "hanoi":
                spec_old["component"] = "HanoiWorkflow"
            # Add History attribute
            from configs.database import SpecKeys
            spec_old[SpecKeys.HISTORY] = {}
            spec_old[SpecKeys.HISTORY][SpecKeys.History.PHOCR_TEST_MACHINE] = []
            spec_old[SpecKeys.HISTORY][SpecKeys.History.PHOCR_ON_BOARD] = []
            spec_old[SpecKeys.HISTORY][SpecKeys.History.ESDK] = []
            spec_old[SpecKeys.HISTORY][SpecKeys.History.TESSERACT] = []
            spec_old[SpecKeys.HISTORY][SpecKeys.History.ABBYY] = []
            spec_new = [spec_old]
            # Write new spec file
            write_json(spec_new[0], spec_file)
        sys.exit(0)

    # No options is requested
    parser.print_help()
    sys.exit(1)


if __name__ == "__main__":
    main()
