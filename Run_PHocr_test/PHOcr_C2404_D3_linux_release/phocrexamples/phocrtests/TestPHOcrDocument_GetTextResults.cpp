/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrDocument_GetTextResults.cpp
 * @brief
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 24, 2019
 *****************************************************************************/

#include "gtest/gtest.h"
#include "phocrtests/TestDataManager.h"
#include "phocrtests/TestHelper.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocr/api/PHOcrDocumentMaker.h"

class PHOcrDocumentGetTextResultTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();

    image_path_multi_page = data_manager->GetPath("44_01-05.tif");
    image_path_single_page = data_manager->GetPath("01_0033.bmp");
    not_image_file_path = data_manager->GetPath("not_image.txt");
    white_image_path = data_manager->GetPath("white-image.bmp");

    not_image_file_path_ws = phocr::ConvertToWString(not_image_file_path);
    image_path_single_page_ws = phocr::ConvertToWString(image_path_single_page);
    image_path_multi_page_ws = phocr::ConvertToWString(image_path_multi_page);
    white_image_path_ws = phocr::ConvertToWString(white_image_path);
  }

 protected:
  phocr::TestDataManager* data_manager;
  std::string image_path_multi_page, image_path_single_page,
              not_image_file_path, white_image_path;
  std::wstring not_image_file_path_ws, image_path_single_page_ws,
              image_path_multi_page_ws, white_image_path_ws;
};

TEST_F(PHOcrDocumentGetTextResultTest, should_be_successful_when_get_from_empty_document) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document);
  std::string doc_text_result;
  if (document.get() != nullptr) {
    ASSERT_NO_THROW(document->PHOcrGetTextResults(doc_text_result));
  }
  ASSERT_EQ(doc_text_result, "");
}

TEST_F(PHOcrDocumentGetTextResultTest, should_not_empty_when_get_from_single_page_document) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document, image_path_single_page_ws);
  std::string doc_text_result;
  if (document.get() != nullptr) {
    ASSERT_NO_THROW(document->PHOcrGetTextResults(doc_text_result));
  }
  ASSERT_NE(doc_text_result, "");
}

TEST_F(PHOcrDocumentGetTextResultTest, should_not_empty_when_get_from_multi_page_document) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document, image_path_multi_page_ws);
  std::string doc_text_result;
  if (document.get() != nullptr) {
    ASSERT_NO_THROW(document->PHOcrGetTextResults(doc_text_result));
  }
  ASSERT_NE(doc_text_result, "");
}

TEST_F(PHOcrDocumentGetTextResultTest, should_be_empty_string_when_get_from_not_image_document) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document, not_image_file_path_ws);
  std::string doc_text_result;
  if (document.get() != nullptr) {
    ASSERT_NO_THROW(document->PHOcrGetTextResults(doc_text_result));
  }
  ASSERT_EQ(doc_text_result, "");
}

TEST_F(PHOcrDocumentGetTextResultTest, should_be_empty_when_get_from_white_image) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document, white_image_path_ws);
  std::string doc_text_result;
  if (document.get() != nullptr) {
    ASSERT_NO_THROW(document->PHOcrGetTextResults(doc_text_result));
  }
  ASSERT_EQ(doc_text_result, "");
}
