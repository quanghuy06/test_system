/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrSetting_OCRMultiPagesInParallel.cpp
 * @brief   Testing for PHOcr setting functionalities
 *            1. GetOCRMultiPagesInParallel
 *            2. SetOCRMultiPagesInParallel
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    2019-07-23
 *****************************************************************************/
#include <cstdint>
#include <boost/filesystem.hpp>
#include "gtest/gtest.h"
#include "phocrtests/TestHelper.h"
#include "phocrtests/TestDataManager.h"
#include "phocrtests/TestHelper.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrDocumentMaker.h"

using namespace phocr;
class PHOcrSettingOCRMultiPagesInParallelTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();
    one_page_data = data_manager->GetPath("04_2189.jpg");
    one_page_data_ws = phocr::ConvertToWString(one_page_data);
    multipage_page_data = data_manager->GetPath("FULL_COLOR_4_PAGES.tif");
    multipage_page_data_ws = phocr::ConvertToWString(multipage_page_data);
  }

  void TearDown() override {
  }

 protected:
  phocr::TestDataManager* data_manager;
  std::string one_page_data;
  std::wstring one_page_data_ws;
  std::string multipage_page_data;
  std::wstring multipage_page_data_ws;
  phocr::PHOcrDocumentPtr document;
};

TEST_F(PHOcrSettingOCRMultiPagesInParallelTest, should_default_be_automatic_selecting) {
  phocr::PHOcrSettings settings;
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_AUTO_SELECT);
}

TEST_F(PHOcrSettingOCRMultiPagesInParallelTest, should_success_processing_document_when_setting_parallel_inside_page_with_one_page_data) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_INSIDE_ONE_PAGE_PROCESSING);
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_INSIDE_ONE_PAGE_PROCESSING);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, one_page_data_ws, settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(
      document->PHOcrExport({{
        L"should_success_processing_document_when_setting_parallel_inside_page_with_one_page_data",
        phocr::PHOcrExportFormat::EF_PDF}}),
        phocr::PHOcrStatus::PHOCR_OK);
}

TEST_F(PHOcrSettingOCRMultiPagesInParallelTest, should_success_processing_document_when_setting_parallel_inside_page_with_multipages_page_data) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_INSIDE_ONE_PAGE_PROCESSING);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, multipage_page_data_ws, settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(
      document->PHOcrExport({{
        L"should_success_processing_document_when_setting_parallel_inside_page_with_multipages_page_data",
        phocr::PHOcrExportFormat::EF_PDF}}),
        phocr::PHOcrStatus::PHOCR_OK);
}

TEST_F(PHOcrSettingOCRMultiPagesInParallelTest, should_success_processing_document_when_setting_parallel_two_pages_with_one_page_data) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_TWO_PAGES_IN_SAME_TIME);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, one_page_data_ws, settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(
      document->PHOcrExport({{
        L"should_success_processing_document_when_setting_parallel_two_pages_with_one_page_data",
        phocr::PHOcrExportFormat::EF_PDF}}),
        phocr::PHOcrStatus::PHOCR_OK);
}

TEST_F(PHOcrSettingOCRMultiPagesInParallelTest, should_success_processing_document_when_setting_parallel_two_pages_with_multipages_page_data) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_TWO_PAGES_IN_SAME_TIME);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, multipage_page_data_ws, settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(
      document->PHOcrExport({{
        L"should_success_processing_document_when_setting_parallel_two_pages_with_multipages_page_data",
        phocr::PHOcrExportFormat::EF_PDF}}),
        phocr::PHOcrStatus::PHOCR_OK);
}

TEST_F(PHOcrSettingOCRMultiPagesInParallelTest, should_success_processing_document_when_setting_parallel_auto_select_with_one_page_data) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, one_page_data_ws, settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(
      document->PHOcrExport({{
        L"should_success_processing_document_when_setting_parallel_auto_select_with_one_page_data",
        phocr::PHOcrExportFormat::EF_PDF}}),
        phocr::PHOcrStatus::PHOCR_OK);
}

TEST_F(PHOcrSettingOCRMultiPagesInParallelTest, should_success_processing_document_when_setting_parallel_auto_select_with_multipages_page_data) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, multipage_page_data_ws, settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(
      document->PHOcrExport({{
        L"should_success_processing_document_when_setting_parallel_auto_select_with_multipages_page_data",
        phocr::PHOcrExportFormat::EF_PDF}}),
        phocr::PHOcrStatus::PHOCR_OK);
}
