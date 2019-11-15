/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrDocumentData_GetDocumentContent.cpp
 * @brief   Testing for Get document data structure
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Jul 23, 2019
 *****************************************************************************/

#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include "gtest/gtest.h"

#include "leptonica/include/allheaders.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrDocumentData.h"
#include "phocr/api/PHOcrDocumentMaker.h"
#include "phocr/api/PHOcrEnum.h"
#include "phocr/api/PHOcrPageData.h"
#include "phocr/api/PHOcrSettings.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocrtests/TestDataManager.h"
#include "phocrtests/TestHelper.h"

// using phocr::PHOcrPageData;

class PHOcrDocumentDataTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();

    std::string single_page =
        data_manager->GetPath("A_10010_Danish_Page0011.jpg");
    // this test case have 5 pages
    std::string multiple_page_path = data_manager->GetPath("44_01-05.tif");

    single_page_wstring = phocr::ConvertToWString(single_page);
    multiple_page_wstring = phocr::ConvertToWString(multiple_page_path);
  }

 protected:
  phocr::TestDataManager* data_manager;
  // Images path
  std::wstring single_page_wstring;
  std::wstring multiple_page_wstring;

  // PHOcr Document and Data elements
  phocr::PHOcrDocumentDataPtr document_data;
  phocr::PHOcrPageDataPtr page_data;

  void SetUpDocumentData(std::wstring image_path,
                         std::wstring language = L"english") {
    phocr::PHOcrDocumentPtr document;
    phocr::PHOcrSettings setting;
    setting.SetOCRLanguage(language);
    setting.SetDataMode(phocr::PHOcrDataMode::DM_HIGH_CONTENT);
    phocr::PHOcrDocumentMaker::CreateDocument(document, image_path, setting);

    document->PHOcrGetDocumentStructData(document_data);
  }
};

/**
 * Testing for get document data structure from single image
 */
TEST_F(PHOcrDocumentDataTest,
       should_be_not_null_when_get_document_data_successfully_with_one_page) {
  phocr::PHOcrDocumentPtr document;
  phocr::PHOcrSettings phocrSettings;
  phocrSettings.SetOCRLanguage(L"danish");
  phocrSettings.SetDataMode(phocr::PHOcrDataMode::DM_HIGH_CONTENT);
  phocr::PHOcrDocumentMaker::CreateDocument(document, multiple_page_wstring,
                                            phocrSettings);
  phocr::PHOcrDocumentDataPtr _document_data;
  document->PHOcrGetDocumentStructData(_document_data);
  ASSERT_NE(_document_data, nullptr);
}

/**
 * Testing for get document data structure from multiple image in a tiff file
 */
TEST_F(PHOcrDocumentDataTest,
       should_be_not_null_when_get_document_data_successfully_with_five_pages) {
  phocr::PHOcrDocumentPtr document;
  phocr::PHOcrSettings phocrSettings;
  phocrSettings.SetOCRLanguage(L"english");
  phocrSettings.SetDataMode(phocr::PHOcrDataMode::DM_HIGH_CONTENT);
  phocr::PHOcrDocumentMaker::CreateDocument(document, multiple_page_wstring,
                                            phocrSettings);
  phocr::PHOcrDocumentDataPtr _document_data;
  document->PHOcrGetDocumentStructData(_document_data);
  ASSERT_NE(_document_data, nullptr);
}

/**
 * Testing for get list page in document
 * In this test case we have 5 pages
 */
TEST_F(PHOcrDocumentDataTest, should_be_not_null_when_get_a_page_from_document_successfully) {
  SetUpDocumentData(multiple_page_wstring);
  std::vector<phocr::PHOcrPageDataPtr> list_page_data;
  list_page_data = document_data->GetPages();
  ASSERT_EQ(list_page_data.size(), 5);
}

/**
 * Testing for get data structure a page in document
 */
TEST_F(PHOcrDocumentDataTest, should_be_not_null_when_get_structure_page_data_successfully) {
  phocr::PHOcrDocumentPtr document;
  phocr::PHOcrSettings setting;
  setting.SetOCRLanguage(L"english");
  setting.SetDataMode(phocr::PHOcrDataMode::DM_HIGH_CONTENT);
  phocr::PHOcrDocumentMaker::CreateDocument(document, multiple_page_wstring,
                                            setting);

  document->PHOcrGetPage(3)->PHOcrGetPageDataStruct(page_data);
  ASSERT_NE(page_data, nullptr);
}

/**
 * Testing for set page data method
 * In this test case we have 5 pages
 */
TEST_F(PHOcrDocumentDataTest,
       should_be_not_null_when_construct_a_list_page_for_empty_document_successfully) {
  SetUpDocumentData(multiple_page_wstring);
  std::vector<phocr::PHOcrPageDataPtr> list_page_data;
  list_page_data = document_data->GetPages();
  phocr::PHOcrDocumentDataPtr new_document =
      std::make_shared<phocr::PHOcrDocumentData>();
  new_document->SetPages(list_page_data);
  ASSERT_EQ(new_document->GetPages().size(), 5);
}
