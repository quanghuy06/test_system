/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrDocument_GetPage.cpp
 * @brief
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Mar 21, 2019
 *****************************************************************************/

#include "gtest/gtest.h"
#include "phocrtests/TestDataManager.h"
#include "phocrtests/TestHelper.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocr/api/PHOcrDocumentMaker.h"

class PHOcrDocumentGetPageTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();
    image_path = data_manager->GetPath("01_0033.jpg");
    image_path_ws = phocr::ConvertToWString(image_path);
    image_path_tif_2_pages = data_manager->GetPath("2pages.tif");
    image_path_tif_2_pages_ws = phocr::ConvertToWString(image_path_tif_2_pages);
  }

 protected:
  phocr::TestDataManager* data_manager;
  std::string image_path;
  std::wstring image_path_ws;
  std::string image_path_tif_2_pages;
  std::wstring image_path_tif_2_pages_ws;
};

TEST_F(PHOcrDocumentGetPageTest, should_return_nullptr_when_get_page_empty_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private);
  ASSERT_EQ(document_private->PHOcrGetPage(0), nullptr);
  ASSERT_EQ(document_private->PHOcrGetPage(1), nullptr);
  ASSERT_EQ(document_private->PHOcrGetPage(2), nullptr);
  ASSERT_EQ(document_private->PHOcrGetPage(3), nullptr);
}

TEST_F(PHOcrDocumentGetPageTest, should_return_not_nullptr_when_get_page_0_from_1page_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_ws);
  ASSERT_NE(document_private->PHOcrGetPage(0), nullptr);
  ASSERT_EQ(document_private->PHOcrGetPage(1), nullptr);
}

TEST_F(PHOcrDocumentGetPageTest, should_return_not_nullptr_when_get_page_0_from_2page_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_tif_2_pages_ws);
  ASSERT_NE(document_private->PHOcrGetPage(0), nullptr);
  ASSERT_NE(document_private->PHOcrGetPage(1), nullptr);
  ASSERT_EQ(document_private->PHOcrGetPage(2), nullptr);
}
