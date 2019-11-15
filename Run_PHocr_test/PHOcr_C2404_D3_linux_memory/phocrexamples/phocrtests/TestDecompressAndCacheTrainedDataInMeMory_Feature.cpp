/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestDecompressAndCacheTrainedDataInMeMory_Feature.cpp
 * @brief   This module is used to
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Jul 24, 2019
 *****************************************************************************/

#include <string>
#include <iostream>
#include "phocrtests/TestDataManager.h"
#include "gtest/gtest.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrSettings.h"
#include "phocr/api/PHOcrDocumentMaker.h"
#include "phocrtests/UnitTestUtility.h"

using namespace phocr;

/**
 * Test feature decompress trained data and cache the trained data inside
 * memory.
 */
class DecompressAndCacheTrainedData : public ::testing::Test {
 protected:
  std::wstring small_image_path_;  // Small test case
  std::wstring eng_image_path_;  // English 1 page
  std::wstring eng_four_pages_image_path_;  // English 4 pages
  std::wstring jap_image_path_;  // Japanese
  std::wstring tur_image_path_;  // Turkish
  std::wstring por_image_path_;  // Portuguese
  std::wstring chi_tra_image_path_;  // Chinese traditional
  std::wstring chi_sim_image_path_;  // Chinese simplified
  std::wstring rus_image_path_;  // Russian
  std::wstring spa_image_path_;  // Spanish
  std::wstring swe_image_path_;  // Swedish
  std::wstring pol_image_path_;  // Polish
  std::wstring fra_image_path_;  // French
  std::wstring fin_image_path_;  // Finnish
  std::wstring deu_image_path_;  // Deutch
  std::wstring dan_image_path_;  // Danish
  std::wstring nor_image_path_;  // Norwegian
  std::wstring dut_image_path_;  // Dutch
  std::wstring ita_image_path_;  // Italian

 public:
  DecompressAndCacheTrainedData() {
    TestDataManager* data_manager = TestDataManager::Instance();
    small_image_path_ = ConvertToWString(data_manager->GetPath("small_image.bmp"));
    eng_image_path_ = ConvertToWString(data_manager->GetPath("English.jpg"));
    eng_four_pages_image_path_ = ConvertToWString(data_manager->GetPath("FULL_COLOR_4_PAGES.tif"));
    jap_image_path_ = ConvertToWString(data_manager->GetPath("Japanese.jpg"));
    tur_image_path_ = ConvertToWString(data_manager->GetPath("Turkish.jpg"));
    por_image_path_ = ConvertToWString(data_manager->GetPath("Portuguese.jpg"));
    chi_tra_image_path_ = ConvertToWString(data_manager->GetPath("ChineseTraditional.jpg"));
    chi_sim_image_path_ = ConvertToWString(data_manager->GetPath("ChineseSimplified.jpg"));
    rus_image_path_ = ConvertToWString(data_manager->GetPath("Russian.jpg"));
    spa_image_path_ = ConvertToWString(data_manager->GetPath("Spanish.jpg"));
    swe_image_path_ = ConvertToWString(data_manager->GetPath("Swedish.jpg"));
    pol_image_path_ = ConvertToWString(data_manager->GetPath("Polish.jpg"));
    fra_image_path_ = ConvertToWString(data_manager->GetPath("French.jpg"));
    fin_image_path_ = ConvertToWString(data_manager->GetPath("Finnish.jpg"));
    deu_image_path_ = ConvertToWString(data_manager->GetPath("Deutch.jpg"));
    dan_image_path_ = ConvertToWString(data_manager->GetPath("Danish.jpg"));
    nor_image_path_ = ConvertToWString(data_manager->GetPath("Norwegian.jpg"));
    dut_image_path_ = ConvertToWString(data_manager->GetPath("Dutch.jpg"));
    ita_image_path_ = ConvertToWString(data_manager->GetPath("Italian.jpg"));
  }

  ~DecompressAndCacheTrainedData() {
    UnitTestUtility::DeletePossiblePHOcrOutputFile();
  }

  PHOcrStatus ExportTextDocument(
      const std::wstring& img_path,
      const PHOcrSettings& setting,
      std::wstring& output_name) {
    PHOcrDocumentPtr document;
    PHOcrDocumentMaker::CreateDocument(document, img_path, setting);
    output_name = UnitTestUtility::GetFilenameFromFilepath(img_path);
    PHOcrStatus status = document->PHOcrExport({{output_name, PHOcrExportFormat::EF_TXT}});
    output_name += L".txt";
    return status;
  }

  static std::string ReadContent(std::wstring output_name) {
    std::string output_file_path = UnitTestUtility::GetCurrentPathToFileName(
        ConvertToString(output_name));
    return UnitTestUtility::ReadContent(output_file_path);
  }

  void TestDecompressAndCacheTrainedData(
      const std::wstring& image_path,
      const PHOcrSettings& setting) {
    std::wstring output_name;
    PHOcrStatus status = ExportTextDocument(image_path, setting, output_name);
    ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
    std::string content = ReadContent(output_name);
    EXPECT_FALSE(content.empty());
  }
};

// Test with small image to check that PHOcr can load LSTM traineddata (*.traineddata.best.gz)
TEST_F(DecompressAndCacheTrainedData, test_with_small_image) {
  PHOcrSettings setting;
  TestDecompressAndCacheTrainedData(small_image_path_, setting);
}

// Test with english test case
TEST_F(DecompressAndCacheTrainedData, test_with_normal_english_image) {
  PHOcrSettings setting;
  TestDecompressAndCacheTrainedData(eng_image_path_, setting);
}

// Test with multiple pages test case
TEST_F(DecompressAndCacheTrainedData, test_with_multiple_pages_image) {
  PHOcrSettings setting;
  TestDecompressAndCacheTrainedData(eng_four_pages_image_path_, setting);
}

// Test when user run with alot of languages. In this case, the trained cache
// must operate as expect. When the cache is full, it will remove old trained
// data and replace with the new one
TEST_F(DecompressAndCacheTrainedData, test_with_many_language_image) {
  PHOcrSettings setting;
  // english
  TestDecompressAndCacheTrainedData(small_image_path_, setting);
  TestDecompressAndCacheTrainedData(eng_image_path_, setting);
  // japanese
  setting.SetOCRLanguage(L"japanese");
  TestDecompressAndCacheTrainedData(jap_image_path_, setting);
  // turkish
  setting.SetOCRLanguage(L"turkish");
  TestDecompressAndCacheTrainedData(tur_image_path_, setting);
  // portuguese
  setting.SetOCRLanguage(L"portuguese");
  TestDecompressAndCacheTrainedData(por_image_path_, setting);
  // chinese traditional
  setting.SetOCRLanguage(L"chinesetraditional");
  TestDecompressAndCacheTrainedData(chi_tra_image_path_, setting);
  // chinese simplified
  setting.SetOCRLanguage(L"chinesesimplified");
  TestDecompressAndCacheTrainedData(chi_sim_image_path_, setting);
  // russian
  setting.SetOCRLanguage(L"russian");
  TestDecompressAndCacheTrainedData(rus_image_path_, setting);
  // spanish
  setting.SetOCRLanguage(L"spanish");
  TestDecompressAndCacheTrainedData(spa_image_path_, setting);
  // swedish
  setting.SetOCRLanguage(L"swedish");
  TestDecompressAndCacheTrainedData(swe_image_path_, setting);
  // polish
  setting.SetOCRLanguage(L"polish");
  TestDecompressAndCacheTrainedData(pol_image_path_, setting);
  // french
  setting.SetOCRLanguage(L"french");
  TestDecompressAndCacheTrainedData(fra_image_path_, setting);
  // finnish
  setting.SetOCRLanguage(L"finnish");
  TestDecompressAndCacheTrainedData(swe_image_path_, setting);
  // german
  setting.SetOCRLanguage(L"german");
  TestDecompressAndCacheTrainedData(deu_image_path_, setting);
  // danish
  setting.SetOCRLanguage(L"danish");
  TestDecompressAndCacheTrainedData(dan_image_path_, setting);
  // norwegian
  setting.SetOCRLanguage(L"norwegian");
  TestDecompressAndCacheTrainedData(nor_image_path_, setting);
  // dutch
  setting.SetOCRLanguage(L"dutch");
  TestDecompressAndCacheTrainedData(dut_image_path_, setting);
  // italian
  setting.SetOCRLanguage(L"italian");
  TestDecompressAndCacheTrainedData(ita_image_path_, setting);
}

// Test the API to release TrainedDataCache memory
TEST_F(DecompressAndCacheTrainedData, test_release_trained_data_cache_memory) {
  PHOcrSettings setting;
  TestDecompressAndCacheTrainedData(eng_image_path_, setting);
  PHOcrDocumentPtr document;
  PHOcrDocumentMaker::CreateDocument(document);
  document->ReleaseTrainedDataCacheMemory();
}

// Test the API to change the cache memory
TEST_F(DecompressAndCacheTrainedData, test_change_trained_data_memory_caching_threshold) {
  PHOcrDocumentPtr document;
  PHOcrSettings setting;
  PHOcrDocumentMaker::CreateDocument(document);
  PHOcrStatus status = document->SetTrainedDataCacheMemory(50.0);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
  TestDecompressAndCacheTrainedData(eng_image_path_, setting);
}

// Test the API to change the cache memory when PHOcr has worked
TEST_F(DecompressAndCacheTrainedData, test_change_trained_data_memory_caching_threshold_when_the_cache_has_worked) {
  PHOcrDocumentPtr document;
  PHOcrSettings setting;
  PHOcrDocumentMaker::CreateDocument(document);
  TestDecompressAndCacheTrainedData(eng_image_path_, setting);
  PHOcrStatus status = document->SetTrainedDataCacheMemory(30.0);
  TestDecompressAndCacheTrainedData(small_image_path_, setting);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INTERNAL_ERROR);
}

// Test the API to disable the cache memory
TEST_F(DecompressAndCacheTrainedData, test_disable_trained_data_cache) {
  PHOcrSettings setting;
  PHOcrDocumentPtr document;
  PHOcrDocumentMaker::CreateDocument(document);
  document->ReleaseTrainedDataCacheMemory();
  PHOcrStatus status = document->DisableTrainedDataCache(true);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
  TestDecompressAndCacheTrainedData(eng_image_path_, setting);
}

// Test the API to disable the cache memory when PHOcr has worked
TEST_F(DecompressAndCacheTrainedData, test_disable_trained_data_cache_when_the_cache_has_worked) {
  PHOcrSettings setting;
  PHOcrDocumentPtr document;
  PHOcrDocumentMaker::CreateDocument(document);
  document->ReleaseTrainedDataCacheMemory();
  TestDecompressAndCacheTrainedData(eng_image_path_, setting);
  PHOcrStatus status = document->DisableTrainedDataCache(true);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INTERNAL_ERROR);
  TestDecompressAndCacheTrainedData(small_image_path_, setting);
}
