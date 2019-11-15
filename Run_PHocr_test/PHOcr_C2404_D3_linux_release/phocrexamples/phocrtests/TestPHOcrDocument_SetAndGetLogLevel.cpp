/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrDocument_SetAndGetLogLevel.cpp
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

class PHOcrDocumentSetAndGetLogLevelTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();
    image_path = data_manager->GetPath("01_0033.jpg");
    image_path_ws = phocr::ConvertToWString(image_path);
  }

 protected:
  phocr::TestDataManager* data_manager;
  std::string image_path;
  std::wstring image_path_ws;
};

TEST_F(PHOcrDocumentSetAndGetLogLevelTest, should_success_when_set_and_get_diagnostic_log_level_of_empty_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private);
  auto log_level = phocr::PHOcrLogLevel::LL_DIAGNOSTIC;
  ASSERT_NO_THROW(document_private->PHOcrSetLogLevel(log_level));
  ASSERT_EQ(document_private->PHOcrGetLogLevel(), log_level);
}

TEST_F(PHOcrDocumentSetAndGetLogLevelTest, should_success_when_set_and_get_diagnostic_log_level_of_not_empty_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_ws);
  auto log_level = phocr::PHOcrLogLevel::LL_DIAGNOSTIC;
  ASSERT_NO_THROW(document_private->PHOcrSetLogLevel(log_level));
  ASSERT_EQ(document_private->PHOcrGetLogLevel(), log_level);
}

TEST_F(PHOcrDocumentSetAndGetLogLevelTest, should_have_the_same_log_level_when_set_and_get_diagnostic_log_level_of_processed_not_empty_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_ws);
  auto log_level = phocr::PHOcrLogLevel::LL_DIAGNOSTIC;
  ASSERT_NO_THROW(document_private->PHOcrSetLogLevel(log_level));
  ASSERT_EQ(document_private->PHOcrGetLogLevel(), log_level);
  ASSERT_NO_THROW(document_private->PHOcrExport({{L"tmp", phocr::PHOcrExportFormat::EF_TXT}}));
  ASSERT_EQ(document_private->PHOcrGetLogLevel(), log_level);
}

TEST_F(PHOcrDocumentSetAndGetLogLevelTest, should_success_when_set_and_get_off_log_level_of_empty_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private);
  auto log_level = phocr::PHOcrLogLevel::LL_OFF;
  ASSERT_NO_THROW(document_private->PHOcrSetLogLevel(log_level));
  ASSERT_EQ(document_private->PHOcrGetLogLevel(), log_level);
}

TEST_F(PHOcrDocumentSetAndGetLogLevelTest, should_success_when_set_and_get_off_log_level_of_not_empty_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_ws);
  auto log_level = phocr::PHOcrLogLevel::LL_OFF;
  ASSERT_NO_THROW(document_private->PHOcrSetLogLevel(log_level));
  ASSERT_EQ(document_private->PHOcrGetLogLevel(), log_level);
}

TEST_F(PHOcrDocumentSetAndGetLogLevelTest, should_have_the_same_log_level_when_set_and_get_off_log_level_of_processed_not_empty_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_ws);
  auto log_level = phocr::PHOcrLogLevel::LL_OFF;
  ASSERT_NO_THROW(document_private->PHOcrSetLogLevel(log_level));
  ASSERT_EQ(document_private->PHOcrGetLogLevel(), log_level);
  ASSERT_NO_THROW(document_private->PHOcrExport({{L"tmp", phocr::PHOcrExportFormat::EF_TXT}}));
  ASSERT_EQ(document_private->PHOcrGetLogLevel(), log_level);
}

