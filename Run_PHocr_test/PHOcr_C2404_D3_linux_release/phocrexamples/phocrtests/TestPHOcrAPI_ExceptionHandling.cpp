/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrCell_Constructor.cpp
 * @brief   Testing for PHOcrDocument constructor
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Jun 18, 2019
 *****************************************************************************/

#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include "gtest/gtest.h"

#include <boost/regex.hpp>
#include "TestHelper.h"
#include "leptonica/include/allheaders.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrDocumentMaker.h"
#include "phocr/api/PHOcrEnum.h"
#include "phocr/api/PHOcrPageMaker.h"
#include "phocr/api/PHOcrSettings.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocrtests/TestDataManager.h"
#include "phocrtests/TestHelper.h"
#include "utility/include/DirectoryManagement.h"
#include "utility/include/FileManagerBuilder.h"
#include "utility/include/IPHOcrWriter.h"

class PHOcrExceptionHandlingTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();

    contain_text_and_image_path =
        data_manager->GetPath("A_12912_English_Page0026_color_200dpi.tif");
    std::string text_and_chart = data_manager->GetPath(
        "MSM_11963_Japanese004_Page0046_GrayToMono200dpi.tif");

    std::string have_barcode =
        data_manager->GetPath("15_Invoice_Barcode_CODE39_HRT.jpg");

    // This test case have 5 pages
    std::string multiple_pages = data_manager->GetPath("44_01-05.tif");

    contain_text_and_image_path_wstring =
        phocr::ConvertToWString(contain_text_and_image_path);

    std::string ten_pages_image_path =
        data_manager->GetPath("FULL_COLOR_10_PAGES.tif");
    text_and_chart_wstring = phocr::ConvertToWString(text_and_chart);
    multiple_pages_wstring = phocr::ConvertToWString(multiple_pages);
    have_barcode_wstring = phocr::ConvertToWString(have_barcode);
    ten_pages_image_path_wstring =
        phocr::ConvertToWString(ten_pages_image_path);
  }

 protected:
  // PHOcr Data elements
  phocr::PHOcrPageDataPtr page_data;

  phocr::TestDataManager* data_manager;

  // Images path
  std::wstring contain_text_and_image_path_wstring;
  std::wstring text_and_chart_wstring;
  std::wstring multiple_pages_wstring;
  std::wstring have_barcode_wstring;
  std::wstring invalid_path_wstring = L"/home/ocrdev/aaaaa";
  std::string contain_text_and_image_path;
  std::wstring ten_pages_image_path_wstring;

  phocr::PHOcrDocumentPtr document;
  phocr::PHOcrPagePtr page;
  void SetUpPageData(std::wstring image_path, std::wstring language) {
    document = nullptr;
    page = nullptr;
    phocr::PHOcrSettings setting;
    setting.SetOCRLanguage(language);
    setting.SetDataMode(phocr::PHOcrDataMode::DM_HIGH_CONTENT);
    phocr::PHOcrDocumentMaker::CreateDocument(document, image_path, setting);
  }
};

/**
 * List function are tested:
 * PHOcrDocument::ProcessPage
 * PHOcrDocument::PHOcrExport
 * PHOcrDocument::PHOcrGetPage
 * PHOcrDocument::PHOcrRemovePage
 * PHOCrDocumentMaker::CreateDocument
 * PHOCrPage::PHOcrGetStringInAZone
 * PHOCrPage::PHOcrGetBarcodeInAZone
 * PHOCrPage::PHOcrExport
 * PHOcrSettings::SetOCRLanguage
 * PHOcrSettings::SetPdfOutputDpi
 * PHOcrSettings::SetBarcodeMode
 */

/**
 * Test for PHOcrDocument::PHOcrExport function when invalid file name
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_export_with_invalid_file_name) {
  SetUpPageData(text_and_chart_wstring, L"japanese");
  ASSERT_EQ(document->PHOcrExport({{ L"\0", phocr::PHOcrExportFormat::EF_PDF}}),
            phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
  ASSERT_EQ(document->PHOcrExport({{ L"/", phocr::PHOcrExportFormat::EF_PDF}}),
            phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
  ASSERT_EQ(document->PHOcrExport({{ L"", phocr::PHOcrExportFormat::EF_PDF}}),
            phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOcrDocument::PHOcrExport function when valid file name
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_success_when_export_with_valid_file_name) {
  SetUpPageData(text_and_chart_wstring, L"japanese");
  ASSERT_EQ(document->PHOcrExport({{
    L"valid_file_name", phocr::PHOcrExportFormat::EF_PDF}}),
            phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOcrDocument::PHOcrGetPage when page number valid
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_success_when_get_page_number_in_range) {
  SetUpPageData(multiple_pages_wstring, L"english");
  phocr::PHOcrPagePtr page = document->PHOcrGetPage(3);
  ASSERT_NE(page, nullptr);
}

/**
 * Test for PHOcrDocument::PHOcrGetPage when page number out of range
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_return_null_when_get_page_number_out_of_range) {
  SetUpPageData(multiple_pages_wstring, L"english");
  phocr::PHOcrPagePtr page = document->PHOcrGetPage(10);
  ASSERT_EQ(page, nullptr);
}

/**
 * Test for PHOcrDocument::PHOcrRemovePage when page number out of range
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_remove_page_number_out_of_range) {
  SetUpPageData(multiple_pages_wstring, L"english");
  ASSERT_EQ(document->PHOcrRemovePage(6),
            phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrDocument::PHOcrRemovePage when page number in range
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_success_when_remove_valid_page_number) {
  SetUpPageData(multiple_pages_wstring, L"english");
  ASSERT_EQ(document->PHOcrRemovePage(3), phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOCrDocumentMaker::CreateDocument with valid path
 */
TEST_F(PHOcrExceptionHandlingTest, should_be_return_PHOCR_OK_when_create_document_successfully) {
  document = nullptr;
  phocr::PHOcrSettings setting;
  setting.SetDataMode(phocr::PHOcrDataMode::DM_HIGH_CONTENT);
  phocr::PHOcrStatus status = phocr::PHOcrDocumentMaker::CreateDocument(
      document, text_and_chart_wstring);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOCrDocumentMaker::CreateDocument when invalid path
 */
TEST_F(PHOcrExceptionHandlingTest, should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_cannot_create_document) {
  document = nullptr;
  phocr::PHOcrSettings setting;
  setting.SetOCRLanguage(L"japanese");
  setting.SetDataMode(phocr::PHOcrDataMode::DM_HIGH_CONTENT);
  phocr::PHOcrStatus status = phocr::PHOcrDocumentMaker::CreateDocument(
      document, invalid_path_wstring, setting);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrDocumentMaker::CreateDocument when length of input data is
 * invalid (negative number)
 */
TEST_F(
    PHOcrExceptionHandlingTest,
    should_be_return_not_PHOCR_OK_when_pass_a_negative_value_to_data_size) {
  phocr::PHOcrDocumentPtr document_data;
  size_t size;
  int8_t* image_data = ReadDataFromFile(contain_text_and_image_path, size);

  phocr::PHOcrStatus status = phocr::PHOcrDocumentMaker::CreateDocument(
      document_data, reinterpret_cast<const unsigned char*>(image_data), -1);

  // ReadDataFromFile return a pointer but it's not deleted
  // to pass leak-check by valgrind
  delete image_data;
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrDocumentMaker::CreateDocument when length of input data is
 * invalid (data_size = 0)
 */
TEST_F(
    PHOcrExceptionHandlingTest,
    should_be_return_not_PHOCR_OK_when_pass_0_to_data_size) {
  phocr::PHOcrDocumentPtr document_data;
  size_t size;
  int8_t* image_data = ReadDataFromFile(contain_text_and_image_path, size);

  phocr::PHOcrStatus status = phocr::PHOcrDocumentMaker::CreateDocument(
      document_data, reinterpret_cast<const unsigned char*>(image_data), 0);

  // ReadDataFromFile return a pointer but it's not deleted
  // to pass leak-check by valgrind
  delete image_data;
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrDocumentMaker::CreateDocument when length of input data is
 * valid
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_return_not_PHOCR_OK_when_pass_a_valid_length_data_file_to_create_document) {
  phocr::PHOcrDocumentPtr document_data;
  size_t size;
  int8_t* image_data = ReadDataFromFile(contain_text_and_image_path, size);

  phocr::PHOcrStatus status = phocr::PHOcrDocumentMaker::CreateDocument(
      document_data, reinterpret_cast<const unsigned char*>(image_data), size);

  // ReadDataFromFile return a pointer but it's not deleted
  // to pass leak-check by valgrind
  delete image_data;
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOCrPageMaker::CreatePage with valid path
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_success_when_create_page_with_valid_path) {
  phocr::PHOcrPagePtr page_data;
  phocr::PHOcrSettings setting;
  setting.SetDataMode(phocr::PHOcrDataMode::DM_HIGH_CONTENT);
  phocr::PHOcrStatus status =
      phocr::PHOcrPageMaker::CreatePage(page_data, text_and_chart_wstring);

  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOCrPageMaker::CreatePage with invalid path
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_create_page_fail_with_invalid_path) {
  phocr::PHOcrPagePtr page_data;
  phocr::PHOcrStatus status =
      phocr::PHOcrPageMaker::CreatePage(page_data, invalid_path_wstring);

  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrPageMaker::CreatePage with input data length is valid
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_success_when_create_page_with_valid_length_data) {
  phocr::PHOcrPagePtr page_data;
  size_t size;
  int8_t* image_data = ReadDataFromFile(contain_text_and_image_path, size);

  phocr::PHOcrStatus status = phocr::PHOcrPageMaker::CreatePage(
      page_data, reinterpret_cast<const unsigned char*>(image_data), size);

  // ReadDataFromFile return a pointer but it's not deleted
  // to pass leak-check by valgrind
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOCrPageMaker::CreatePage with input data length is invalid
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_create_page_fail_with_invalid_length_data) {
  phocr::PHOcrPagePtr page_data = nullptr;
  size_t size;
  int8_t* image_data = ReadDataFromFile(contain_text_and_image_path, size);
  phocr::PHOcrStatus status = phocr::PHOcrPageMaker::CreatePage(
      page_data, reinterpret_cast<const unsigned char*>(image_data), -10);

  // ReadDataFromFile return a pointer but it's not deleted
  // to pass leak-check by valgrind
  delete image_data;
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrPage::PHOcrGetStringInAZone when x parameter of Rectangle is
 * invalid
 */
TEST_F(PHOcrExceptionHandlingTest, should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_x_rectangle_invalid) {
  SetUpPageData(contain_text_and_image_path_wstring, L"english");
  phocr::PHOcrRectangle<long> rec(-1, 1, 100, 100);
  std::wstring result;
  std::wstring regex(L"ab+");
  page = document->PHOcrGetPage(0);
  phocr::PHOcrStatus status = page->PHOcrGetStringInAZone(result, rec, regex);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrPage::PHOcrGetStringInAZone when y parameter of Rectangle is
 * invalid
 */
TEST_F(PHOcrExceptionHandlingTest, should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_y_rectangle_invalid) {
  SetUpPageData(contain_text_and_image_path_wstring, L"english");
  phocr::PHOcrRectangle<long> rec(1, -10, 100, 100);
  std::wstring result;
  std::wstring regex(L"ab+");
  page = document->PHOcrGetPage(0);
  phocr::PHOcrStatus status = page->PHOcrGetStringInAZone(result, rec, regex);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrPage::PHOcrGetStringInAZone when width parameter of Rectangle
 * is invalid
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_width_rectangle_invalid) {
  SetUpPageData(contain_text_and_image_path_wstring, L"english");
  phocr::PHOcrRectangle<long> rec(10, 10, -90, 100);
  std::wstring result;
  std::wstring regex(L"ab+");
  page = document->PHOcrGetPage(0);
  phocr::PHOcrStatus status = page->PHOcrGetStringInAZone(result, rec, regex);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrPage::PHOcrGetStringInAZone when height parameter of Rectangle
 * is invalid
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_height_rectangle_invalid) {
  SetUpPageData(contain_text_and_image_path_wstring, L"english");
  phocr::PHOcrPagePtr page;
  phocr::PHOcrRectangle<long> rec(10, 10, 90, -100);
  std::wstring result;
  std::wstring regex(L"ab+");
  page = document->PHOcrGetPage(0);
  phocr::PHOcrStatus status = page->PHOcrGetStringInAZone(result, rec, regex);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrPage::PHOcrGetStringInAZone when parameter of Rectangle is
 * valid and regex is valid
 */
TEST_F(PHOcrExceptionHandlingTest, should_be_success_when_rectangle_valid) {
  SetUpPageData(contain_text_and_image_path_wstring, L"english");
  phocr::PHOcrRectangle<long> rec(2, 1, 100, 100);
  std::wstring result;
  std::wstring regex(L"ab+");
  page = document->PHOcrGetPage(0);
  phocr::PHOcrStatus status = page->PHOcrGetStringInAZone(result, rec, regex);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOCrPage::PHOcrGetStringInAZone when regex of Rectangle is invalid
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_return_PHOCR_INVALID_ARGUMENT_ERROR_when_regex_invalid_to_get_string) {
  SetUpPageData(contain_text_and_image_path_wstring, L"english");
  phocr::PHOcrRectangle<long> rec(2, 1, 100, 100);
  std::wstring result;
  std::wstring regex(L"(");
  page = document->PHOcrGetPage(0);
  phocr::PHOcrStatus status = page->PHOcrGetStringInAZone(result, rec, regex);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrPage::PHOcrGetBarcodeInAZone when parameters of rectangle is
 * invalid
 */
TEST_F(PHOcrExceptionHandlingTest, should_return_PHOCR_INVALID_ARGUMENT_ERROR_when_width_rectangle_invalid) {
  SetUpPageData(have_barcode_wstring, L"english");
  phocr::PHOcrRectangle<long> rec(2, 1, -100, 100);
  std::wstring result;
  std::wstring regex(L"(");
  page = document->PHOcrGetPage(0);
  phocr::PHOcrStatus status = page->PHOcrGetBarcodeInAZone(result, rec, regex);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrPage::PHOcrGetBarcodeInAZone when regex is invalid
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_return_PHOCR_INVALID_ARGUMENT_ERROR_when_regex_invalid_to_get_barcode) {
  SetUpPageData(have_barcode_wstring, L"english");
  phocr::PHOcrRectangle<long> rec(20, 20, 100, 100);
  std::wstring result;
  std::wstring regex(L")");
  page = document->PHOcrGetPage(0);
  phocr::PHOcrStatus status = page->PHOcrGetBarcodeInAZone(result, rec, regex);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOcrPage::PHOcrExport when file name is invalid
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_return_PHOCR_INVALID_ARGUMENT_ERROR_when_file_name_export_page_invalid) {
  SetUpPageData(text_and_chart_wstring, L"japanese");
  page = document->PHOcrGetPage(0);
  ASSERT_EQ(page->PHOcrExport({{ L"\0", phocr::PHOcrExportFormat::EF_TXT}}),
            phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
  ASSERT_EQ(page->PHOcrExport({{ L"/", phocr::PHOcrExportFormat::EF_TXT}}),
            phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
  ASSERT_EQ(page->PHOcrExport({{ L"", phocr::PHOcrExportFormat::EF_TXT}}),
            phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOCrPage::PHOcrExport when file name is valid
 */
TEST_F(PHOcrExceptionHandlingTest, should_success_when_export_page_ok) {
  SetUpPageData(text_and_chart_wstring, L"japanese");
  page = document->PHOcrGetPage(0);
  phocr::PHOcrStatus status =
      page->PHOcrExport({{L"file_name_txt", phocr::PHOcrExportFormat::EF_TXT}});
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOcrSettings::SetOCRLanguage when pass a wrong language name or
 * language is not supported
 */
TEST_F(PHOcrExceptionHandlingTest, should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_language_invalid) {
  phocr::PHOcrSettings setting;
  phocr::PHOcrStatus status = setting.SetOCRLanguage(L"muong");
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOcrSettings::SetOCRLanguage when pass a valid language
 */
TEST_F(PHOcrExceptionHandlingTest, should_be_success_when_language_valid) {
  phocr::PHOcrSettings setting;
  phocr::PHOcrStatus status = setting.SetOCRLanguage(L"spanish");
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOcrSettings::SetPdfOutputDpi when pass an invalid DPI value
 */
TEST_F(PHOcrExceptionHandlingTest, should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_dpi_greater_than_2000) {
  phocr::PHOcrSettings setting;
  phocr::PHOcrStatus status = setting.SetPdfOutputDpi(50000);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOcrSettings::SetPdfOutputDpi when pass an invalid DPI value
 */
TEST_F(PHOcrExceptionHandlingTest, should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_dpi_less_than_100) {
  phocr::PHOcrSettings setting;
  phocr::PHOcrStatus status = setting.SetPdfOutputDpi(89);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOcrSettings::SetPdfOutputDpi when pass a valid DPI value
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_success_when_dpi_between_100_to_2000) {
  phocr::PHOcrSettings setting;
  phocr::PHOcrStatus status = setting.SetPdfOutputDpi(300);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOcrSettings::SetPdfOutputDpi when pass a valid DPI value
 */
TEST_F(PHOcrExceptionHandlingTest, should_be_success_when_dpi_is_0) {
  phocr::PHOcrSettings setting;
  phocr::PHOcrStatus status = setting.SetPdfOutputDpi(0);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOcrSettings::SetBarcodeMode when pass a value greater than BM
 * maximum value
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_barcode_mode_value_greater_than_max_value) {
  phocr::PHOcrSettings setting;
  phocr::PHOcrStatus status = setting.SetBarcodeMode(8388708);  // > 2^23
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOcrSettings::SetBarcodeMode when pass a negative value
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_return_PHOCR_INVALID_ARGUMENT_ERROR_when_pass_a_negative_barcode_mode_value) {
  phocr::PHOcrSettings setting;
  phocr::PHOcrStatus status = setting.SetBarcodeMode(-1);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

/**
 * Test for PHOcrSettings::SetBarcodeMode when pass a valid value
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_be_success_when_pass_a_valid_barcode_mode_value) {
  phocr::PHOcrSettings setting;
  phocr::PHOcrStatus status = setting.SetBarcodeMode(10);
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_OK);
}

/**
 * Test for PHOcrDocument::PHOcrExport when meet disk error
 */
TEST_F(PHOcrExceptionHandlingTest,
       should_handle_error_successfully_when_disk_is_full) {
  using utility::IPHOcrWriter;
  class FullDiskWriter : public IPHOcrWriter {
   public:
    FullDiskWriter() {}
    ~FullDiskWriter() {}

    void WriteToFile(std::string file_path, const char* data) override {
      throw std::ios_base::failure("Cannot write file " + file_path +
                                   " to disk.");
    }

    void AppendToFile(std::string file_path, const char* data) override {
      throw std::ios_base::failure("Cannot write file " + file_path +
                                   " to disk.");
    }
  };

  utility::FileManagerBuilder::Instance()->SetWriter(
      std::make_shared<FullDiskWriter>());

  phocr::PHOcrSettings setting;
  setting.SetDataMode(phocr::PHOcrDataMode::DM_HIGH_CONTENT);
  phocr::PHOcrDocumentPtr doc;
  phocr::PHOcrDocumentMaker::CreateDocument(doc, text_and_chart_wstring,
                                            setting);
  phocr::PHOcrStatus status = doc->PHOcrExport({{
      L"test_disk_error_result", phocr::PHOcrExportFormat::EF_DOCX}});
  ASSERT_EQ(status, phocr::PHOcrStatus::PHOCR_FULL_DISK_ERROR);
}
