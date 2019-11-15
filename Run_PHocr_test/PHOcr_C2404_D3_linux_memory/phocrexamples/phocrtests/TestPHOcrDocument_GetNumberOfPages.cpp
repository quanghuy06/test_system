/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrDocument_GetNumberOfPages.cpp
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

class PHOcrDocumentGetNumberOfPagesTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();
    image_path_tif_2_pages = data_manager->GetPath("2pages.tif");
    image_path_tif_2_pages_ws = phocr::ConvertToWString(image_path_tif_2_pages);
    image_path_tif_4_pages = data_manager->GetPath("4pages.tif");
    image_path_tif_4_pages_ws = phocr::ConvertToWString(image_path_tif_4_pages);
  }

 protected:
  phocr::TestDataManager* data_manager;
  std::string image_path_tif_2_pages;
  std::wstring image_path_tif_2_pages_ws;
  std::string image_path_tif_4_pages;
  std::wstring image_path_tif_4_pages_ws;
};

TEST_F(PHOcrDocumentGetNumberOfPagesTest, should_be_0_when_get_from_empty_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private);
  ASSERT_EQ(document_private->PHOcrGetNumberOfPages(), 0);
}

TEST_F(PHOcrDocumentGetNumberOfPagesTest, should_be_2_when_get_from_2pages_image_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_tif_2_pages_ws);
  ASSERT_EQ(document_private->PHOcrGetNumberOfPages(), 2);
}

TEST_F(PHOcrDocumentGetNumberOfPagesTest, should_be_4_when_get_from_4pages_image_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_tif_4_pages_ws);
  ASSERT_EQ(document_private->PHOcrGetNumberOfPages(), 4);
}

TEST_F(PHOcrDocumentGetNumberOfPagesTest, should_be_0_when_remove_all_pages) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_tif_2_pages_ws);
  document_private->PHOcrRemovePage(1);
  document_private->PHOcrRemovePage(0);
  ASSERT_EQ(document_private->PHOcrGetNumberOfPages(), 0);
}
