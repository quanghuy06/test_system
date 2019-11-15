/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrSetting_SetAndGetIccSourceProfile.cpp
 * @brief   Testing for PHOcr setting functionalities
 *            1. SetIccSourceProfile
 *            2. GetIccSourceProfile
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    2019-08-14
 *****************************************************************************/
#include <cstdint>
#include <boost/filesystem.hpp>
#include "gtest/gtest.h"
#include "phocrtests/TestHelper.h"
#include "phocrtests/TestDataManager.h"
#include "phocrtests/TestHelper.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocr/include/PHOcrStringHelperInternal.h"
#include "phocr/api/PHOcrSettings.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrDocumentMaker.h"
#include "utility/include/PHOcrIO.h"
#include "utility/include/Common.h"
#include "utility/include/DirectoryManagement.h"

using namespace phocr;
using namespace utility;
using phocr::GetFileName;
using phocr::ConvertToWString;
using phocr::ConvertToString;
namespace fs = boost::filesystem;

class PHOcrSettingSetAndGetIccSourceProfileTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();
    icc_source_profile_path_for_text_mode = data_manager->GetPath("eBN_TextMode_Default.bin");
    icc_source_profile_path_for_photo_mode = data_manager->GetPath("eBN_PhotoMode_Default.bin");
    icc_source_profile_path_for_text_photo_mode = data_manager->GetPath("eBN_TextPhotoMode_Default.bin");
    one_page_data = data_manager->GetPath("33_ALICE_1.jpg");
    multipage_page_data = data_manager->GetPath("FULL_COLOR_4_PAGES.tif");
  }

  void TearDown() override {
  }

 protected:
  phocr::TestDataManager* data_manager;
  std::string icc_source_profile_path_for_text_mode;
  std::string icc_source_profile_path_for_photo_mode;
  std::string icc_source_profile_path_for_text_photo_mode;
  std::string one_page_data;
  std::string multipage_page_data;

  char separator() {
#if defined(_WIN32)
    return '\\';
#else
    return '/';
#endif
  }
};

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_default_be_nullptr) {
  phocr::PHOcrSettings settings;
  ASSERT_EQ(settings.GetIccSourceProfile(), nullptr);
  ASSERT_EQ(settings.GetIccSourceProfileSize(), 0);
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_setting_icc_source_profile_path_for_text_mode) {
  phocr::PHOcrSettings settings;
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_mode));
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_setting_icc_source_profile_path_for_photo_mode) {
  phocr::PHOcrSettings settings;
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_photo_mode));
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_setting_icc_source_profile_path_for_text_photo_mode) {
  phocr::PHOcrSettings settings;
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_photo_mode));
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_setting_icc_source_profile_data_stream_with_one_page) {
  phocr::PHOcrSettings settings;
  char* icc_source_profile = nullptr;
  size_t icc_source_profile_size = 0;
  icc_source_profile = PHOcrIO::ReadDataStream(icc_source_profile_path_for_text_photo_mode.c_str(), icc_source_profile_size);
  settings.SetIccSourceProfile(icc_source_profile, icc_source_profile_size);
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
  free(icc_source_profile);
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_export_pdf_with_icc_source_profile) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  settings.SetDataMode(PHOcrDataMode::DM_LOW_CONTENT);
  settings.SetUsingImageBandingMechanism(true);
  settings.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  settings.UseIccSourceProfile(true);
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_photo_mode));
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(settings.GetDataMode(), PHOcrDataMode::DM_LOW_CONTENT);
  ASSERT_TRUE(settings.GetUsingImageBandingMechanism());
  ASSERT_EQ(settings.GetPdfExportMode(), PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
  ASSERT_EQ(PHOcrDocumentMaker::CreateDocument(document, ConvertToWString(one_page_data), settings),
            PHOcrStatus::PHOCR_OK);
  std::vector<PHOcrExportSetting> export_settings;
  // Get filename
  std::string outputname = GetFileName(one_page_data.c_str());
  std::wstring outputname_w = ConvertToWString(outputname);
  export_settings.push_back({outputname_w, PHOcrExportFormat::EF_PDF});
  ASSERT_EQ(document->PHOcrExport(export_settings), PHOcrStatus::PHOCR_OK);
  std::string output_pdf = DirectoryManagement::GetCurrentPath() + separator() + outputname + ".pdf";
  ASSERT_TRUE(fs::exists(output_pdf));
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_export_pdfa_with_icc_source_profile) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  settings.SetDataMode(PHOcrDataMode::DM_LOW_CONTENT);
  settings.SetUsingImageBandingMechanism(true);
  settings.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  settings.UseIccSourceProfile(true);
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_photo_mode));
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(settings.GetDataMode(), PHOcrDataMode::DM_LOW_CONTENT);
  ASSERT_TRUE(settings.GetUsingImageBandingMechanism());
  ASSERT_EQ(settings.GetPdfExportMode(), PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
  ASSERT_EQ(PHOcrDocumentMaker::CreateDocument(document, ConvertToWString(one_page_data), settings),
            PHOcrStatus::PHOCR_OK);
  std::vector<PHOcrExportSetting> export_settings;
  // Get filename
  std::string outputname = GetFileName(one_page_data.c_str());
  std::wstring outputname_w = ConvertToWString(outputname);
  export_settings.push_back({outputname_w, PHOcrExportFormat::EF_PDFA});
  ASSERT_EQ(document->PHOcrExport(export_settings), PHOcrStatus::PHOCR_OK);
  std::string output_pdf = DirectoryManagement::GetCurrentPath() + separator() + outputname + ".pdf";
  ASSERT_TRUE(fs::exists(output_pdf));
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_export_pdf_with_icc_source_profile_for_multiple_pages) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  settings.SetDataMode(PHOcrDataMode::DM_LOW_CONTENT);
  settings.SetUsingImageBandingMechanism(true);
  settings.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  settings.UseIccSourceProfile(true);
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_photo_mode));
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(settings.GetDataMode(), PHOcrDataMode::DM_LOW_CONTENT);
  ASSERT_TRUE(settings.GetUsingImageBandingMechanism());
  ASSERT_EQ(settings.GetPdfExportMode(), PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
  ASSERT_EQ(PHOcrDocumentMaker::CreateDocument(document, ConvertToWString(multipage_page_data), settings),
            PHOcrStatus::PHOCR_OK);
  std::vector<PHOcrExportSetting> export_settings;
  // Get filename
  std::string outputname = GetFileName(multipage_page_data.c_str());
  std::wstring outputname_w = ConvertToWString(outputname);
  export_settings.push_back({outputname_w, PHOcrExportFormat::EF_PDF});
  ASSERT_EQ(document->PHOcrExport(export_settings), PHOcrStatus::PHOCR_OK);
  std::string output_pdf = DirectoryManagement::GetCurrentPath() + separator() + outputname + ".pdf";
  ASSERT_TRUE(fs::exists(output_pdf));
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_export_pdfa_with_icc_source_profile_for_multiple_pages) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  settings.SetDataMode(PHOcrDataMode::DM_LOW_CONTENT);
  settings.SetUsingImageBandingMechanism(true);
  settings.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  settings.UseIccSourceProfile(true);
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_photo_mode));
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(settings.GetDataMode(), PHOcrDataMode::DM_LOW_CONTENT);
  ASSERT_TRUE(settings.GetUsingImageBandingMechanism());
  ASSERT_EQ(settings.GetPdfExportMode(), PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
  ASSERT_EQ(PHOcrDocumentMaker::CreateDocument(document, ConvertToWString(multipage_page_data), settings),
            PHOcrStatus::PHOCR_OK);
  std::vector<PHOcrExportSetting> export_settings;
  // Get filename
  std::string outputname = GetFileName(multipage_page_data.c_str());
  std::wstring outputname_w = ConvertToWString(outputname);
  export_settings.push_back({outputname_w, PHOcrExportFormat::EF_PDFA});
  ASSERT_EQ(document->PHOcrExport(export_settings), PHOcrStatus::PHOCR_OK);
  std::string output_pdf = DirectoryManagement::GetCurrentPath() + separator() + outputname + ".pdf";
  ASSERT_TRUE(fs::exists(output_pdf));
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_export_pdf_with_optimise_file_size_and_icc_source_profile) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  settings.SetDataMode(PHOcrDataMode::DM_LOW_CONTENT);
  settings.SetUsingImageBandingMechanism(true);
  settings.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  bool optimize_pdf_file_size = true;
  // Set optimize file size of PDF output
  if (optimize_pdf_file_size) {
    settings.SetOptimizeFileSizePDFOutput(true);
    settings.SetMinimumHybridSegmentRegion(10);
    ASSERT_TRUE(settings.GetOptimizeFileSizePDFOutput());
    ASSERT_EQ(settings.GetMinimumAreaHybridSegmentRegion(), 10);
  }
  settings.UseIccSourceProfile(true);
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_photo_mode));
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(settings.GetDataMode(), PHOcrDataMode::DM_LOW_CONTENT);
  ASSERT_TRUE(settings.GetUsingImageBandingMechanism());
  ASSERT_EQ(settings.GetPdfExportMode(), PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
  ASSERT_EQ(PHOcrDocumentMaker::CreateDocument(document, ConvertToWString(one_page_data), settings),
            PHOcrStatus::PHOCR_OK);
  std::vector<PHOcrExportSetting> export_settings;
  // Get filename
  std::string outputname = GetFileName(one_page_data.c_str());
  std::wstring outputname_w = ConvertToWString(outputname);
  export_settings.push_back({outputname_w, PHOcrExportFormat::EF_PDF});
  ASSERT_EQ(document->PHOcrExport(export_settings), PHOcrStatus::PHOCR_OK);
  std::string output_pdf = DirectoryManagement::GetCurrentPath() + separator() + outputname + ".pdf";
  ASSERT_TRUE(fs::exists(output_pdf));
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_export_pdfa_with_optimise_file_size_and_icc_source_profile) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  settings.SetDataMode(PHOcrDataMode::DM_LOW_CONTENT);
  settings.SetUsingImageBandingMechanism(true);
  settings.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  bool optimize_pdf_file_size = true;
  // Set optimize file size of PDF output
  if (optimize_pdf_file_size) {
    settings.SetOptimizeFileSizePDFOutput(true);
    settings.SetMinimumHybridSegmentRegion(10);
    ASSERT_TRUE(settings.GetOptimizeFileSizePDFOutput());
    ASSERT_EQ(settings.GetMinimumAreaHybridSegmentRegion(), 10);
  }
  settings.UseIccSourceProfile(true);
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_photo_mode));
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(settings.GetDataMode(), PHOcrDataMode::DM_LOW_CONTENT);
  ASSERT_TRUE(settings.GetUsingImageBandingMechanism());
  ASSERT_EQ(settings.GetPdfExportMode(), PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
  ASSERT_EQ(PHOcrDocumentMaker::CreateDocument(document, ConvertToWString(one_page_data), settings),
            PHOcrStatus::PHOCR_OK);
  std::vector<PHOcrExportSetting> export_settings;
  // Get filename
  std::string outputname = GetFileName(one_page_data.c_str());
  std::wstring outputname_w = ConvertToWString(outputname);
  export_settings.push_back({outputname_w, PHOcrExportFormat::EF_PDFA});
  ASSERT_EQ(document->PHOcrExport(export_settings), PHOcrStatus::PHOCR_OK);
  std::string output_pdf = DirectoryManagement::GetCurrentPath() + separator() + outputname + ".pdf";
  ASSERT_TRUE(fs::exists(output_pdf));
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_export_pdf_with_only_image_and_optimise_file_size_and_icc_source_profile) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  settings.SetDataMode(PHOcrDataMode::DM_LOW_CONTENT);
  settings.SetUsingImageBandingMechanism(true);
  settings.SetPdfExportMode(PHOcrPDFExportMode::PEM_ONLY_IMAGE);
  bool optimize_pdf_file_size = true;
  // Set optimize file size of PDF output
  if (optimize_pdf_file_size) {
    settings.SetOptimizeFileSizePDFOutput(true);
    settings.SetMinimumHybridSegmentRegion(10);
    ASSERT_TRUE(settings.GetOptimizeFileSizePDFOutput());
    ASSERT_EQ(settings.GetMinimumAreaHybridSegmentRegion(), 10);
  }
  settings.UseIccSourceProfile(true);
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_photo_mode));
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(settings.GetDataMode(), PHOcrDataMode::DM_LOW_CONTENT);
  ASSERT_TRUE(settings.GetUsingImageBandingMechanism());
  ASSERT_EQ(settings.GetPdfExportMode(), PHOcrPDFExportMode::PEM_ONLY_IMAGE);
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
  ASSERT_EQ(PHOcrDocumentMaker::CreateDocument(document, ConvertToWString(one_page_data), settings),
            PHOcrStatus::PHOCR_OK);
  std::vector<PHOcrExportSetting> export_settings;
  // Get filename
  std::string outputname = GetFileName(one_page_data.c_str());
  std::wstring outputname_w = ConvertToWString(outputname);
  export_settings.push_back({outputname_w, PHOcrExportFormat::EF_PDF});
  ASSERT_EQ(document->PHOcrExport(export_settings), PHOcrStatus::PHOCR_OK);
  std::string output_pdf = DirectoryManagement::GetCurrentPath() + separator() + outputname + ".pdf";
  ASSERT_TRUE(fs::exists(output_pdf));
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_export_pdfa_with_bin_and_optimise_file_size_and_icc_source_profile) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  settings.SetDataMode(PHOcrDataMode::DM_LOW_CONTENT);
  settings.SetUsingImageBandingMechanism(true);
  settings.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  settings.SetPdfImageExportMode(phocr::PHOcrImageExportMode::IEM_BINARY);
  bool optimize_pdf_file_size = true;
  // Set optimize file size of PDF output
  if (optimize_pdf_file_size) {
    settings.SetOptimizeFileSizePDFOutput(true);
    settings.SetMinimumHybridSegmentRegion(10);
    ASSERT_TRUE(settings.GetOptimizeFileSizePDFOutput());
    ASSERT_EQ(settings.GetMinimumAreaHybridSegmentRegion(), 10);
  }
  settings.UseIccSourceProfile(true);
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_photo_mode));
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(settings.GetDataMode(), PHOcrDataMode::DM_LOW_CONTENT);
  ASSERT_TRUE(settings.GetUsingImageBandingMechanism());
  ASSERT_EQ(settings.GetPdfExportMode(), PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  ASSERT_EQ(settings.GetPdfImageExportMode(), PHOcrImageExportMode::IEM_BINARY);
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
  ASSERT_EQ(PHOcrDocumentMaker::CreateDocument(document, ConvertToWString(one_page_data), settings),
            PHOcrStatus::PHOCR_OK);
  std::vector<PHOcrExportSetting> export_settings;
  // Get filename
  std::string outputname = GetFileName(one_page_data.c_str());
  std::wstring outputname_w = ConvertToWString(outputname);
  export_settings.push_back({outputname_w, PHOcrExportFormat::EF_PDFA});
  ASSERT_EQ(document->PHOcrExport(export_settings), PHOcrStatus::PHOCR_OK);
  std::string output_pdf = DirectoryManagement::GetCurrentPath() + separator() + outputname + ".pdf";
  ASSERT_TRUE(fs::exists(output_pdf));
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_export_pdfa_with_halftone_and_optimise_file_size_and_icc_source_profile) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  settings.SetDataMode(PHOcrDataMode::DM_LOW_CONTENT);
  settings.SetUsingImageBandingMechanism(true);
  settings.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  settings.SetPdfImageExportMode(phocr::PHOcrImageExportMode::IEM_HALFTONE);
  bool optimize_pdf_file_size = true;
  // Set optimize file size of PDF output
  if (optimize_pdf_file_size) {
    settings.SetOptimizeFileSizePDFOutput(true);
    settings.SetMinimumHybridSegmentRegion(10);
    ASSERT_TRUE(settings.GetOptimizeFileSizePDFOutput());
    ASSERT_EQ(settings.GetMinimumAreaHybridSegmentRegion(), 10);
  }
  settings.UseIccSourceProfile(true);
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_photo_mode));
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(settings.GetDataMode(), PHOcrDataMode::DM_LOW_CONTENT);
  ASSERT_TRUE(settings.GetUsingImageBandingMechanism());
  ASSERT_EQ(settings.GetPdfExportMode(), PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  ASSERT_EQ(settings.GetPdfImageExportMode(), PHOcrImageExportMode::IEM_HALFTONE);
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
  ASSERT_EQ(PHOcrDocumentMaker::CreateDocument(document, ConvertToWString(one_page_data), settings),
            PHOcrStatus::PHOCR_OK);
  std::vector<PHOcrExportSetting> export_settings;
  // Get filename
  std::string outputname = GetFileName(one_page_data.c_str());
  std::wstring outputname_w = ConvertToWString(outputname);
  export_settings.push_back({outputname_w, PHOcrExportFormat::EF_PDFA});
  ASSERT_EQ(document->PHOcrExport(export_settings), PHOcrStatus::PHOCR_OK);
  std::string output_pdf = DirectoryManagement::GetCurrentPath() + separator() + outputname + ".pdf";
  ASSERT_TRUE(fs::exists(output_pdf));
}

TEST_F(PHOcrSettingSetAndGetIccSourceProfileTest, should_success_when_export_pdfa_with_halftone_photo_and_optimise_file_size_and_icc_source_profile) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  settings.SetOCRMultiPagesInParallel(PHOcrParallelType::PARALLEL_AUTO_SELECT);
  settings.SetDataMode(PHOcrDataMode::DM_LOW_CONTENT);
  settings.SetUsingImageBandingMechanism(true);
  settings.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  settings.SetPdfImageExportMode(phocr::PHOcrImageExportMode::IEM_HALFTONE_PHOTO);
  bool optimize_pdf_file_size = true;
  // Set optimize file size of PDF output
  if (optimize_pdf_file_size) {
    settings.SetOptimizeFileSizePDFOutput(true);
    settings.SetMinimumHybridSegmentRegion(10);
    ASSERT_TRUE(settings.GetOptimizeFileSizePDFOutput());
    ASSERT_EQ(settings.GetMinimumAreaHybridSegmentRegion(), 10);
  }
  settings.UseIccSourceProfile(true);
  settings.SetIccSourceProfile(ConvertToWString(icc_source_profile_path_for_text_photo_mode));
  ASSERT_EQ(settings.GetOCRMultiPagesInParallel(), PHOcrParallelType::PARALLEL_AUTO_SELECT);
  ASSERT_EQ(settings.GetDataMode(), PHOcrDataMode::DM_LOW_CONTENT);
  ASSERT_TRUE(settings.GetUsingImageBandingMechanism());
  ASSERT_EQ(settings.GetPdfExportMode(), PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  ASSERT_EQ(settings.GetPdfImageExportMode(), PHOcrImageExportMode::IEM_HALFTONE_PHOTO);
  ASSERT_NE(settings.GetIccSourceProfile(), nullptr);
  ASSERT_GT(settings.GetIccSourceProfileSize(), 0);
  ASSERT_EQ(PHOcrDocumentMaker::CreateDocument(document, ConvertToWString(one_page_data), settings),
            PHOcrStatus::PHOCR_OK);
  std::vector<PHOcrExportSetting> export_settings;
  // Get filename
  std::string outputname = GetFileName(one_page_data.c_str());
  std::wstring outputname_w = ConvertToWString(outputname);
  export_settings.push_back({outputname_w, PHOcrExportFormat::EF_PDFA});
  ASSERT_EQ(document->PHOcrExport(export_settings), PHOcrStatus::PHOCR_OK);
  std::string output_pdf = DirectoryManagement::GetCurrentPath() + separator() + outputname + ".pdf";
  ASSERT_TRUE(fs::exists(output_pdf));
}
