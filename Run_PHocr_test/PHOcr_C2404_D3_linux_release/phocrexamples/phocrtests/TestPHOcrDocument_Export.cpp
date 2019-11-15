/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrDocument_Export.cpp
 * @brief   Testing for PHOcrExport function of PHOcrDocument
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Mar 15, 2019
 *****************************************************************************/
#include <cstdint>
#include <boost/filesystem.hpp>
#include "gtest/gtest.h"
#include "phocrtests/TestHelper.h"
#include "phocrtests/TestDataManager.h"
#include "phocrtests/TestHelper.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrDocumentData.h"
#include "phocr/api/PHOcrDocumentMaker.h"
#include "phocr/api/PHOcrPageMaker.h"

namespace fs = boost::filesystem;

static const std::vector<std::string>& ExtensionShouldBeRemoved() {
  static std::vector<std::string> extensions = {
      "xml", "docx", "pptx", "xlsx",
      "docx", "pdf", "pdfa", "txt"
  };
  return extensions;
}

class PHOcrDocumentExportTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();
    image_path = data_manager->GetPath("01_0033.jpg");
    image_path_ws = phocr::ConvertToWString(image_path);
    output_file_name = "output";
    output_file_name_ws = phocr::ConvertToWString(output_file_name);
    phocr::PHOcrDocumentMaker::CreateDocument(document, image_path_ws);

    auto& should_remove_extensions_ = ExtensionShouldBeRemoved();
    for (auto& extension : should_remove_extensions_) {
      RemoveFileIfExists(JoinFileName(output_file_name, extension));
    }
  }

  void TearDown() override {
    auto& should_remove_extensions_ = ExtensionShouldBeRemoved();
    for (auto& extension : should_remove_extensions_) {
      RemoveFileIfExists(JoinFileName(output_file_name, extension));
    }
  }

 protected:
  phocr::TestDataManager* data_manager;
  std::string image_path;
  std::wstring image_path_ws;
  std::string output_file_name;
  std::wstring output_file_name_ws;
  phocr::PHOcrDocumentPtr document;
};

TEST_F(PHOcrDocumentExportTest, should_success_when_export_empty_document) {
  phocr::PHOcrDocumentPtr document_private;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private);
  ASSERT_EQ(
      document->PHOcrExport({{
          phocr::ConvertToWString(output_file_name),
          phocr::PHOcrExportFormat::EF_DOCX
      }}),
      phocr::PHOcrStatus::PHOCR_OK);
}

TEST_F(PHOcrDocumentExportTest, should_success_when_export_docx) {
  ASSERT_EQ(
      document->PHOcrExport({{
          phocr::ConvertToWString(output_file_name),
          phocr::PHOcrExportFormat::EF_DOCX
      }}),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName(output_file_name, "docx")));
}

TEST_F(PHOcrDocumentExportTest, should_success_when_export_pdf) {
  ASSERT_EQ(
      document->PHOcrExport({{
        output_file_name_ws,
        phocr::PHOcrExportFormat::EF_PDF
      }}),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName(output_file_name, "pdf")));
}

TEST_F(PHOcrDocumentExportTest, should_success_when_export_pdfa) {

  std::vector<phocr::PHOcrExportSetting> export_settings;
  export_settings.push_back( { output_file_name_ws,
      phocr::PHOcrExportFormat::EF_PDFA });
  ASSERT_EQ(document->PHOcrExport(export_settings),
            phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName(output_file_name, "pdf")));
}

TEST_F(PHOcrDocumentExportTest, should_success_when_export_pptx) {
  ASSERT_EQ(document->PHOcrExport( { { output_file_name_ws,
      phocr::PHOcrExportFormat::EF_PPTX } }),
            phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName(output_file_name, "pptx")));
}

TEST_F(PHOcrDocumentExportTest, should_success_when_export_txt) {
  ASSERT_EQ(
      document->PHOcrExport({{
        output_file_name_ws,
        phocr::PHOcrExportFormat::EF_TXT}}),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName(output_file_name, "txt")));
}

TEST_F(PHOcrDocumentExportTest, should_success_when_export_xlsx) {
  ASSERT_EQ(
      document->PHOcrExport({{
        output_file_name_ws,
        phocr::PHOcrExportFormat::EF_XLSX}}),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName(output_file_name, "xlsx")));
}

TEST_F(PHOcrDocumentExportTest, should_success_when_export_xml) {
  ASSERT_EQ(
      document->PHOcrExport({{
        output_file_name_ws,
        phocr::PHOcrExportFormat::EF_XML}}),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName(output_file_name, "xml")));
}

TEST_F(PHOcrDocumentExportTest, should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;

  ASSERT_EQ(
      document->PHOcrExport({{
          L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings",
          phocr::PHOcrExportFormat::EF_PPTX }}),
      phocr::PHOcrStatus::PHOCR_OK);

  ASSERT_EQ(
      document->PHOcrExport({{
          L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings",
          phocr::PHOcrExportFormat::EF_DOCX}}),
      phocr::PHOcrStatus::PHOCR_OK);

  ASSERT_EQ(
      document->PHOcrExport({{
          L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings",
          phocr::PHOcrExportFormat::EF_XLSX}}),
      phocr::PHOcrStatus::PHOCR_OK);

  ASSERT_EQ(
      document->PHOcrExport({{
          L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings_PDF",
          phocr::PHOcrExportFormat::EF_PDF}}),
      phocr::PHOcrStatus::PHOCR_OK);

  ASSERT_EQ(
      document->PHOcrExport({{
          L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings_PDFA",
          phocr::PHOcrExportFormat::EF_PDFA}}),
      phocr::PHOcrStatus::PHOCR_OK);

  ASSERT_EQ(
      document->PHOcrExport({{
          L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings",
          phocr::PHOcrExportFormat::EF_TXT}}),
      phocr::PHOcrStatus::PHOCR_OK);

  ASSERT_EQ(
      document->PHOcrExport({{
          L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings",
          phocr::PHOcrExportFormat::EF_XML}}),
      phocr::PHOcrStatus::PHOCR_OK);
}

TEST_F(PHOcrDocumentExportTest, should_be_success_when_export_by_using_begin_and_end_mode) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;

  auto config_result = document->PHOcrConfigureForExporting({
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_XLSX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PDF
    }
  });
  ASSERT_EQ(config_result, phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrBeginExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrEndExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "xlsx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pdf")));
}

TEST_F(PHOcrDocumentExportTest, should_be_success_when_export_by_using_begin_and_end_mode_when_appending_pages_after_config) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;

  auto config_result = document->PHOcrConfigureForExporting({
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_XLSX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PDF
    }
  });

  phocr::PHOcrPagePtr page1;
  phocr::PHOcrPageMaker::CreatePage(page1, image_path_ws);
  phocr::PHOcrPagePtr page2;
  phocr::PHOcrPageMaker::CreatePage(page2, image_path_ws);
  document->PHOcrAppendPages({page1, page2});

  ASSERT_EQ(config_result, phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrBeginExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrEndExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "xlsx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pdf")));
}

TEST_F(PHOcrDocumentExportTest, should_be_success_when_export_by_using_begin_and_end_mode_when_appending_pages_before_config) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;


  phocr::PHOcrPagePtr page1;
  phocr::PHOcrPageMaker::CreatePage(page1, image_path_ws);
  phocr::PHOcrPagePtr page2;
  phocr::PHOcrPageMaker::CreatePage(page2, image_path_ws);
  document->PHOcrAppendPages({page1, page2});

  auto config_result = document->PHOcrConfigureForExporting({
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_XLSX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PDF
    }
  });

  ASSERT_EQ(config_result, phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrBeginExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrEndExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "xlsx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pdf")));
}

TEST_F(PHOcrDocumentExportTest, should_be_success_when_export_by_using_begin_and_end_mode_when_appending_pages_after_begin) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;

  auto config_result = document->PHOcrConfigureForExporting({
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_XLSX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PDF
    }
  });

  ASSERT_EQ(config_result, phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrBeginExporting(), phocr::PHOcrStatus::PHOCR_OK);

  phocr::PHOcrPagePtr page1;
  phocr::PHOcrPageMaker::CreatePage(page1, image_path_ws);
  phocr::PHOcrPagePtr page2;
  phocr::PHOcrPageMaker::CreatePage(page2, image_path_ws);
  document->PHOcrAppendPages({page1, page2});

  ASSERT_EQ(document->PHOcrEndExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "xlsx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pdf")));
}

TEST_F(PHOcrDocumentExportTest, should_be_success_when_export_by_using_begin_and_end_mode_when_appending_pages_after_export) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;

  auto config_result = document->PHOcrConfigureForExporting({
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_XLSX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PDF
    }
  });

  ASSERT_EQ(config_result, phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrBeginExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrEndExporting(), phocr::PHOcrStatus::PHOCR_OK);

  phocr::PHOcrPagePtr page1;
  phocr::PHOcrPageMaker::CreatePage(page1, image_path_ws);
  phocr::PHOcrPagePtr page2;
  phocr::PHOcrPageMaker::CreatePage(page2, image_path_ws);
  document->PHOcrAppendPages({page1, page2});

  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "xlsx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pdf")));
}

TEST_F(PHOcrDocumentExportTest, should_be_fail_when_call_begin_without_config) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;

  ASSERT_EQ(document->PHOcrBeginExporting(), phocr::PHOcrStatus::PHOCR_ERROR_NOT_YET_CONFIG_FOR_EXPORT);
}

TEST_F(PHOcrDocumentExportTest, should_be_fail_when_call_end_without_call_begin) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;

  ASSERT_EQ(document->PHOcrEndExporting(), phocr::PHOcrStatus::PHOCR_ERROR_NOT_YET_CALL_BEGIN_EXPORT);
}

TEST_F(PHOcrDocumentExportTest, should_be_fail_when_call_config_after_begin) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;
  auto config_result = document->PHOcrConfigureForExporting({
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_XLSX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PDF
    }
  });

  ASSERT_EQ(config_result, phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrBeginExporting(), phocr::PHOcrStatus::PHOCR_OK);
  config_result = document->PHOcrConfigureForExporting({
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1",
      phocr::PHOcrExportFormat::EF_PPTX
    }
  });
  ASSERT_EQ(config_result, phocr::PHOcrStatus::PHOCR_ERROR_CONFIG_FOR_EXPORT_AFTER_BEGIN);
}

TEST_F(PHOcrDocumentExportTest, should_be_success_when_call_export_after_begin_and_end_mode) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;
  auto config_result = document->PHOcrConfigureForExporting({
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_XLSX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PDF
    }
  });

  ASSERT_EQ(config_result, phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrBeginExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrEndExporting(), phocr::PHOcrStatus::PHOCR_OK);

  document->PHOcrExport({
    {
      L"should_be_success_when_call_export_after_begin_and_end_mode1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_call_export_after_begin_and_end_mode2",
      phocr::PHOcrExportFormat::EF_DOCX
    }
  });

  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "xlsx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pdf")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_call_export_after_begin_and_end_mode1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_call_export_after_begin_and_end_mode2", "docx")));
}

TEST_F(PHOcrDocumentExportTest, should_be_success_when_call_begin_and_end_mode_after_export) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;

  document->PHOcrExport({
    {
      L"should_be_success_when_call_export_after_begin_and_end_mode1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_call_export_after_begin_and_end_mode2",
      phocr::PHOcrExportFormat::EF_DOCX
    }
  });

  auto config_result = document->PHOcrConfigureForExporting({
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_XLSX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PDF
    }
  });

  ASSERT_EQ(config_result, phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrBeginExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrEndExporting(), phocr::PHOcrStatus::PHOCR_OK);

  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "xlsx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pdf")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_call_export_after_begin_and_end_mode1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_call_export_after_begin_and_end_mode2", "docx")));
}

TEST_F(PHOcrDocumentExportTest, should_be_success_when_call_begin_and_end_mode_export_after_append_pages_after_export) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;

  document->PHOcrExport({
    {
      L"should_be_success_when_call_export_after_begin_and_end_mode1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_call_export_after_begin_and_end_mode2",
      phocr::PHOcrExportFormat::EF_DOCX
    }
  });

  phocr::PHOcrPagePtr page1;
  phocr::PHOcrPageMaker::CreatePage(page1, image_path_ws);
  phocr::PHOcrPagePtr page2;
  phocr::PHOcrPageMaker::CreatePage(page2, image_path_ws);
  document->PHOcrAppendPages({page1, page2});
  page1 = nullptr;
  page2 = nullptr;

  auto config_result = document->PHOcrConfigureForExporting({
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_XLSX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PDF
    }
  });

  ASSERT_EQ(config_result, phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrBeginExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrEndExporting(), phocr::PHOcrStatus::PHOCR_OK);

  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "xlsx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pdf")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_call_export_after_begin_and_end_mode1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_call_export_after_begin_and_end_mode2", "docx")));
}

TEST_F(PHOcrDocumentExportTest, should_be_fail_when_call_export_during_begin_end_mode) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size), settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;

  auto config_result = document->PHOcrConfigureForExporting({
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_XLSX
    },
    {
      L"should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3",
      phocr::PHOcrExportFormat::EF_PDF
    }
  });

  ASSERT_EQ(config_result, phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document->PHOcrBeginExporting(), phocr::PHOcrStatus::PHOCR_OK);

  // Call export
  auto status = document->PHOcrExport({
    {
      L"should_be_success_when_call_export_after_begin_and_end_mode1",
      phocr::PHOcrExportFormat::EF_PPTX
    },
    {
      L"should_be_success_when_call_export_after_begin_and_end_mode2",
      phocr::PHOcrExportFormat::EF_DOCX
    }
  });
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_ERROR_CALL_EXPORT_DURING_BEGIN_END_MODE);

  // Call get text result
  std::string text_result;
  status = document->PHOcrGetTextResults(text_result);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_ERROR_CALL_EXPORT_DURING_BEGIN_END_MODE);

  // Call get document structure
  phocr::PHOcrDocumentDataPtr document_data;
  status = document->PHOcrGetDocumentStructData(document_data);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_ERROR_CALL_EXPORT_DURING_BEGIN_END_MODE);

  ASSERT_EQ(document->PHOcrEndExporting(), phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings2", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "xlsx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_export_from_document_construct_from_JPG_compressed_image_data_and_PHOcrSettings3", "pdf")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_call_export_after_begin_and_end_mode1", "pptx")));
  ASSERT_TRUE(fs::exists(JoinFileName("should_be_success_when_call_export_after_begin_and_end_mode2", "docx")));
}

TEST_F(PHOcrDocumentExportTest, should_fail_when_export_with_filename_contains_forward_slash) {
  ASSERT_EQ(
      document->PHOcrExport({{
        L"/",
        phocr::PHOcrExportFormat::EF_TXT}}),
      phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

TEST_F(PHOcrDocumentExportTest, should_success_when_export_with_filename_contains_forbidden_printable_characters_on_windows_without_forward_slash) {
  ASSERT_EQ(
      document->PHOcrExport({{
        L"\\ : * ? \" < > |",
        phocr::PHOcrExportFormat::EF_TXT}}),
      phocr::PHOcrStatus::PHOCR_OK);
}
