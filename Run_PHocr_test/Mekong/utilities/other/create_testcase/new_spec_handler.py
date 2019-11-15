from baseapi.file_access import *
class SpecKeys:
    PRODUCT = "product"
    ENABLE = "enable"
    FUNCTIONALITIES = "functionalities"
    WEIGHT = "weight"
    TAGS = "tags"
    COMPONENT = "component"
    ID = "_id"
    HISTORY = "history"
    class Tags:
        DOC_NAME = "DocumentName"
        DOC_TYPE = "DocumentType"
        DOC_PAGE = "DocumentPage"
        LANGS = "Language"
        ACCURACY = "GetAccuracy"
        IS_INVOICE = "IsInvoice"
        IS_PURCHASE_ORDER = "IsPurchaseOrder"
        IS_FORM = "IsForm"
        IS_MAINLY_TEXT = "IsMainlyText"
        IS_LETTER = "IsLetter"
        BUG_LIST = "BugNumbers"
        IS_PRESENTATION = "IsPresentation"
        IS_LEGAL = "IsLegalDocument"
        IS_COURT = "IsCourtDocument"
        IS_MULTI_COL = "IsMultiColumn"
        IS_MULTI_BYTE_LANG = "IsMultiByteLanguage"
        HAS_TABLE = "HasTable"
        HAS_IMAGE = "HasImage"
        HAS_CHART = "HasChart"
        HAS_CONTRAST = "HasContrast"
        HAS_WATER_MASK = "HasWaterMask"
        HAS_LOGO = "HasLogoCompany"
        IS_ET_DEFAULT = "IsETDefault"
    class Functionalities:
        OCR = "OCR"
        SEGMENTATION = "Segmentation"

class NewSpecHandler:

    def __init__(self, spec_file):
        self.src_file = spec_file
        self.specs = read_json(spec_file)
        self.spec_info = self.specs[0]

    # Check if test case has a tag or not
    def HasTag(self, tag):
        if tag in self.spec_info[SpecKeys.TAGS]:
            return True
        else:
            return False

    # Add a tag
    def AddTag(self, key, value):
        if self.HasTag(key):
            print "Tag {0} has already existed!"
        else:
            self.spec_info[SpecKeys.TAGS][key] = value

    # Update a tag
    def UpdateTag(self, key, value):
        if self.HasTag(key):
            self.spec_info[SpecKeys.TAGS][key] = value
        else:
            print "Tag {0} does not exist!"

    # Remove a tag
    def RemoveATag(self, key):
        del self.spec_info[SpecKeys.TAGS][key]

    # Check if test case has a functionality or not
    def HasFunctionality(self, func):
        if func in self.spec_info[SpecKeys.FUNCTIONALITIES]:
            return True
        else:
            return False

    # Add functionality
    def AddFunctionality(self, func):
        if func in self.spec_info[SpecKeys.FUNCTIONALITIES]:
            print "Functionality {0} has already existed!"
        else:
            self.spec_info[SpecKeys.FUNCTIONALITIES].append(func)

    # Remove a functionality
    def RemoveAFunction(self, func):
        if func in self.spec_info[SpecKeys.FUNCTIONALITIES]:
            self.spec_info[SpecKeys.FUNCTIONALITIES].remove(func)
        else:
            print "Functionality {0} does not exist!"

    # Set functionalities
    def SetFunctionalities(self, value):
        self.spec_info[SpecKeys.FUNCTIONALITIES] = value

    # Get document type of test case
    def GetDocumentType(self):
        try:
            return self.spec_info[SpecKeys.TAGS][SpecKeys.Tags.DOC_TYPE]
        except:
            return ""

    # Set Document type
    def SetDocumentType(self, value):
        self.UpdateTag(SpecKeys.Tags.DOC_TYPE, value)

    # Check if test case has a language
    def HasLanguage(self, language):
        if language.lower() in self.GetLanguage():
            return True
        else:
            return False

    # Get language of test case
    def GetLanguage(self):
        try:
            return self.spec_info[SpecKeys.TAGS][SpecKeys.Tags.LANGS]
        except:
            return []

    # Set languages
    def SetLanguage(self, langs):
        self.UpdateTag([SpecKeys.Tags.LANGS], langs)

    # Get product of test case
    def GetProduct(self):
        try:
            return self.spec_info[SpecKeys.PRODUCT]
        except:
            return ""

    # Set product
    def SetProduct(self, product):
        self.spec_info[SpecKeys.PRODUCT] = product

    # Get component
    def GetComponent(self):
        try:
            return self.spec_info[SpecKeys.COMPONENT]
        except:
            return ""

    # Set component
    def SetComponent(self, value):
        self.spec_info[SpecKeys.COMPONENT] = value

    # Save updated specs
    def Save(self, target_file = None):
        if not target_file:
            target_file = self.src_file
        write_json(self.specs, target_file)