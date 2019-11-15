/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrDocument_RemovePage.cpp
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

class PHOcrDocumentRemovePageTest : public ::testing::Test {
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

TEST_F(PHOcrDocumentRemovePageTest, should_not_crash_when_remove_page_from_empty_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private);
  ASSERT_NO_THROW(document_private->PHOcrRemovePage(0));
  ASSERT_NO_THROW(document_private->PHOcrRemovePage(1));
}

TEST_F(PHOcrDocumentRemovePageTest, should_reduce_page_count_when_remove_first_page_from_2pages_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_tif_2_pages_ws);
  ASSERT_EQ(document_private->PHOcrGetNumberOfPages(), 2);
  ASSERT_NO_THROW(document_private->PHOcrRemovePage(0));
  ASSERT_EQ(document_private->PHOcrGetNumberOfPages(), 1);
}

TEST_F(PHOcrDocumentRemovePageTest, should_reduce_page_count_when_remove_last_page_from_2pages_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_tif_2_pages_ws);
  ASSERT_EQ(document_private->PHOcrGetNumberOfPages(), 2);
  ASSERT_NO_THROW(document_private->PHOcrRemovePage(1));
  ASSERT_EQ(document_private->PHOcrGetNumberOfPages(), 1);
}

TEST_F(PHOcrDocumentRemovePageTest, should_not_reduce_page_count_when_remove_invalid_page_number_from_2pages_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_tif_2_pages_ws);
  ASSERT_EQ(document_private->PHOcrGetNumberOfPages(), 2);
  ASSERT_NO_THROW(document_private->PHOcrRemovePage(10));
  ASSERT_EQ(document_private->PHOcrGetNumberOfPages(), 2);
}
