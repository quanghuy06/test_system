/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrDocument_GetSettings.cpp
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

class PHOcrDocumentGetOrSetSettingsTest : public ::testing::Test {
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

TEST_F(PHOcrDocumentGetOrSetSettingsTest, should_success_when_get_setting_from_empty_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private);
  ASSERT_NO_THROW(document_private->PHOcrGetSettings());
}

TEST_F(PHOcrDocumentGetOrSetSettingsTest, should_success_when_set_default_setting_to_empty_document) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private);
  ASSERT_NO_THROW(document_private->PHOcrSetSettings(settings));
  ASSERT_NO_THROW(document_private->PHOcrGetSettings());
}

TEST_F(PHOcrDocumentGetOrSetSettingsTest, should_success_when_set_setting_after_document_process) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_ws);
  document_private->PHOcrExport({{L"tmp", phocr::PHOcrExportFormat::EF_TXT}});
  ASSERT_NO_THROW(document_private->PHOcrSetSettings(settings));
  ASSERT_NO_THROW(document_private->PHOcrGetSettings());
}
