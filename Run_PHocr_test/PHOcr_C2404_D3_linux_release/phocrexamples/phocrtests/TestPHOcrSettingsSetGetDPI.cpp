/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrSettingsSetGetDPI.cpp
 * @brief   This module is used to
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Sep 23, 2019
 *****************************************************************************/

#include "TestPHOcrSettingsSetGetDPI.h"
#include <vector>
#include "phocr/api/PHOcrSettings.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrDocumentMaker.h"
#include "phocr/api/PHOcrExportSetting.h"
#include "phocr/api/PHOcrDocumentData.h"
#include "phocr/api/PHOcrMemoryDataFilter.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "TestDataManager.h"
#include "UnitTestUtility.h"

using phocr::PHOcrSettings;
using phocr::PHOcrStatus;
using phocr::TestDataManager;
using phocr::PHOcrDocumentPtr;
using phocr::PHOcrDocumentMaker;
using phocr::PHOcrDocumentDataPtr;
using phocr::PHOcrMemoryDataFilter;
using phocr::PHOcrExportSetting;
using phocr::PHOcrExportFormat;

const char* low_dpi = "204_196_dpi.tiff";
const char* high_dpi = "408_391_dpi.tiff";

TestPHOcrSettings_Set_Get_DPI::TestPHOcrSettings_Set_Get_DPI() {
  low_dpi_image = phocr::ConvertToWString(
      TestDataManager::Instance()->GetPath(low_dpi));
  high_dpi_image = phocr::ConvertToWString(
      TestDataManager::Instance()->GetPath(high_dpi));
}

TestPHOcrSettings_Set_Get_DPI::~TestPHOcrSettings_Set_Get_DPI() {
  UnitTestUtility::DeletePossiblePHOcrOutputFile();
}

void TestPHOcrSettings_Set_Get_DPI::TestSetDPI(
    const std::wstring& file_path,
    unsigned int horizontal_res,
    unsigned int vertical_res) {
  PHOcrSettings settings;
  PHOcrStatus dpi_status = settings.SetDPI(horizontal_res, vertical_res);
  ASSERT_EQ(dpi_status, PHOcrStatus::PHOCR_OK);

  // Make PHOcr document
  PHOcrDocumentPtr document;
  PHOcrStatus maker_status = PHOcrDocumentMaker::CreateDocument(
      document, file_path, settings);
  ASSERT_EQ(maker_status, PHOcrStatus::PHOCR_OK);

  // Get PHOcr data structure
  PHOcrDocumentDataPtr document_data;
  PHOcrStatus get_data_status = document->PHOcrGetDocumentStructData(
      document_data);
  ASSERT_EQ(get_data_status, PHOcrStatus::PHOCR_OK);

  // Dump data structure to json file
  PHOcrMemoryDataFilter filter;
  std::string json_file = "document_data.json";
  filter.DumpJsonFile(document_data.get(), json_file);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(json_file) > 0);

  // Export document. Since this feature used for docx, pptx and xlsx
  std::vector<PHOcrExportSetting> export_settings = {
      {
          L"result",
          PHOcrExportFormat::EF_DOCX,
      },
      {
          L"result",
          PHOcrExportFormat::EF_PPTX,
      },
      {
          L"result",
          PHOcrExportFormat::EF_XLSX,
      },
  };
  PHOcrStatus export_status = document->PHOcrExport(export_settings);
  ASSERT_EQ(export_status, PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(UnitTestUtility::GetFileSize("result.docx") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize("result.pptx") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize("result.xlsx") > 0);
}

TEST_F(TestPHOcrSettings_Set_Get_DPI, user_define_dpi_for_low_dpi_document) {
  TestSetDPI(low_dpi_image, 204, 196);
}

TEST_F(TestPHOcrSettings_Set_Get_DPI, user_define_dpi_for_high_dpi_document) {
  TestSetDPI(high_dpi_image, 408, 391);
}

TEST_F(TestPHOcrSettings_Set_Get_DPI, user_get_dpi_without_setup) {
  PHOcrSettings settings;
  unsigned int horizontal_dpi, vertical_dpi;
  settings.GetDPI(horizontal_dpi, vertical_dpi);
  ASSERT_EQ(horizontal_dpi, 0);
  ASSERT_EQ(vertical_dpi, 0);
}

TEST_F(TestPHOcrSettings_Set_Get_DPI, user_get_dpi_after_setup) {
  PHOcrSettings settings;
  unsigned int horizontal_dpi, vertical_dpi;
  settings.SetDPI(200, 400);
  settings.GetDPI(horizontal_dpi, vertical_dpi);
  ASSERT_EQ(horizontal_dpi, 200);
  ASSERT_EQ(vertical_dpi, 400);
}
