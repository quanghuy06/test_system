/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrDocument_SetCancelDecisionMethod.cpp
 * @brief
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Mar 21, 2019
 *****************************************************************************/

#include <thread>
#include <functional>
#include <boost/filesystem.hpp>
#include "gtest/gtest.h"
#include "phocrtests/TestDataManager.h"
#include "phocrtests/TestHelper.h"
#include "phocrtests/UnitTestUtility.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocr/api/PHOcrDocumentMaker.h"
#include "phocr/api/PHOcrTiming.h"
#include "phocr/api/PHOcrDeclaration.h"
#include "phocr/api/PHOcrEnum.h"
#include "phocr/api/PHOcrSettings.h"
#include "phocrtests/OutputFileType.h"

using namespace phocr;
namespace fs = boost::filesystem;

// Define the elapsed time required to cancel PHOcr with single page in ms unit
const double kCancelElapsedTime = 2000.0;

// Define the elapsed time required to cancel PHOcr with multiple page in ms unit.
// Now PHOcr is process all pages with 2 threads.
const double kCancelMultiplePagesElapsedTime = 7000.0;

// Global variable for checking cancel flag
bool g_is_phocr_cancelled = false;

// Forward declaration
void CancelPHOcrActivities(int cancel_time_ms);
void ExportDocument(
    phocr::PHOcrCancelDecisionMethod cancel,
    std::wstring image_path,
    OutputFileType type,
    std::string& output_file_path,
    PHOcrStatus& status);
bool IsCancel();

/**
 * Unit testing API PHOcrDocument::SetCancelDecisionMethodTest
 */
class PHOcrDocumentSetCancelDecisionMethodTest : public ::testing::Test {
 public:
  // Constructor
  PHOcrDocumentSetCancelDecisionMethodTest() {
    data_manager = nullptr;
    status = PHOcrStatus::PHOCR_OK;
  }

  // Destructor
  virtual ~PHOcrDocumentSetCancelDecisionMethodTest() {
  }

  void SetUp() override {
    g_is_phocr_cancelled = false;
    data_manager = phocr::TestDataManager::Instance();
    image_path = data_manager->GetPath("01_0033.jpg");
    image_path_ws = phocr::ConvertToWString(image_path);
    table_image_path = phocr::ConvertToWString(
        data_manager->GetPath("WEP_Table_with_image_1.jpg"));
    four_pages_image_path = phocr::ConvertToWString(
        data_manager->GetPath("FULL_COLOR_4_PAGES.tif"));
    ten_pages_image_path = phocr::ConvertToWString(
        data_manager->GetPath("FULL_COLOR_10_PAGES.tif"));
  }

  virtual void TearDown() override {
    UnitTestUtility::DeletePossiblePHOcrOutputFile();
  }

  /**
   * This method create 2 thread, one thread call to PHOcrExport. The other
   * thread will turn on cancel signal after a period of time
   * @param type
   * @param cancel_time_ms
   * @param image_path
   */
  void DoExport(
      OutputFileType type, int cancel_time_ms, std::wstring image_path) {
    std::thread controller(CancelPHOcrActivities, cancel_time_ms);
    std::thread phocr(
        ExportDocument,
        IsCancel,
        image_path,
        type,
        std::ref(output_file_path),
        std::ref(status));
    controller.join();
    phocr.join();
  }

  void CheckPHOcrResult(double target_time) {
    if (status == PHOcrStatus::PHOCR_INTERRUPT_BY_CANCEL) {
      EXPECT_LE(PHOcrTiming::MeasureElapsedTime(), target_time);
    } else {
      ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
    }
  }

 protected:
  phocr::TestDataManager* data_manager;
  std::string image_path;
  std::wstring image_path_ws;
  std::wstring table_image_path;  // An 1 page image with table, photo and text
  std::wstring four_pages_image_path;  // An tiff image with 4 pages inside
  std::wstring ten_pages_image_path;   // An tiff image with 10 pages inside

  // Absolute path to output file when call to API PHOcrExport
  std::string output_file_path;
  PHOcrStatus status;  // Status of PHOcr export
};

bool CancelDecisionMethod() {
  return true;
}

/**
 * Check if we are canceling PHOcr
 * @return
 */
bool IsCancel() {
  return g_is_phocr_cancelled;
}

/**
 * This static method cancel all PHOcr activities after cancel_time_ms
 * If the input is -1 then PHOcr isn't cancelled and it must work normally
 * @param cancel_time_ms
 */
void CancelPHOcrActivities(int cancel_time_ms)
{
  // If user don't want to cancel PHOcr when run this test
  if (cancel_time_ms == -1) {
    g_is_phocr_cancelled = false;
  } else {
    // Sleep this thread in cancel_time seconds
    std::this_thread::sleep_for(std::chrono::milliseconds(cancel_time_ms));
    phocr::PHOcrTiming::SetStartTimeNow();
    g_is_phocr_cancelled = true;
  }
}

/**
 * PHOcr is running this to export a document
 * @param cancelDecisionMethod
 */
void ExportDocument(
    phocr::PHOcrCancelDecisionMethod cancel,
    std::wstring image_path,
    OutputFileType type,
    std::string& output_file_path,
    PHOcrStatus& status) {
  PHOcrExportFormat format;
  PHOcrSettings setting;

  // Output name have the same name with input image
  std::wstring output_name =
      UnitTestUtility::GetFilenameFromFilepath(image_path);
  std::string output_full_name(ConvertToString(output_name));

  // Get the output format
  if  (type == OutputFileType::OCR_TEXT) {
      format = PHOcrExportFormat::EF_TXT;
      output_full_name += ".txt";
  } else if (type == OutputFileType::BB_TEXT) {
      format = PHOcrExportFormat::EF_BB;
      // Assume we only work with 1 page test case
      output_full_name += "_0.txt";
  } else if (type == OutputFileType::DOCX) {
      format = PHOcrExportFormat::EF_DOCX;
      setting.SetDataMode(PHOcrDataMode::DM_HIGH_CONTENT);
      output_full_name += ".docx";
  } else if (type == OutputFileType::PDF) {
      format = PHOcrExportFormat::EF_PDF;
      setting.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
      output_full_name += ".pdf";
  } else if (type == OutputFileType::NO_OCR_PDF) {
      format = PHOcrExportFormat::EF_PDF;
      setting.SetPdfExportMode(PHOcrPDFExportMode::PEM_ONLY_IMAGE);
      output_full_name += ".pdf";
  } else if (type == OutputFileType::XML) {
    format = PHOcrExportFormat::EF_XML;
    setting.SetDataMode(PHOcrDataMode::DM_HIGH_CONTENT);
    output_full_name += ".xml";
  } else {
    throw std::logic_error("Not support this output file type yet");
  }
  // Save absolute path to output file
  auto output_path = fs::path(UnitTestUtility::GetCurrentPath()) /
      fs::path(output_full_name);

  // Save the list of output file path
  output_file_path = output_path.string();

  PHOcrDocumentPtr document;
  PHOcrDocumentMaker::CreateDocument(document, image_path, setting);
  document->PHOcrSetCancelDecisionMethod(cancel);
  status = document->PHOcrExport({{output_name, format}});
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, should_success_when_set_cancel_decision_method) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_ws);
  ASSERT_NO_THROW(document_private->PHOcrSetCancelDecisionMethod(&CancelDecisionMethod));
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, should_success_when_set_empty_cancel_decision_method) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_ws);
  ASSERT_NO_THROW(document_private->PHOcrSetCancelDecisionMethod(0));
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, should_success_when_set_cancel_decision_method_and_process) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_ws);
  ASSERT_NO_THROW(document_private->PHOcrSetCancelDecisionMethod(&CancelDecisionMethod));
  ASSERT_NO_THROW(document_private->PHOcrExport({{L"tmp", PHOcrExportFormat::EF_TXT}}));
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, should_success_when_set_empty_cancel_decision_method_and_process) {
  phocr::PHOcrDocumentPtr document_private = nullptr;
  phocr::PHOcrDocumentMaker::CreateDocument(document_private, image_path_ws);
  ASSERT_NO_THROW(document_private->PHOcrSetCancelDecisionMethod(0));
  ASSERT_NO_THROW(document_private->PHOcrExport({{L"tmp", PHOcrExportFormat::EF_TXT}}));
}

/**
 * EXPORT DOCUMENT WHEN DOESN'T CANCEL PHOCR
 */
TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_never_cancelled_when_export_ocr_text) {
  // Setup environment for testing
  DoExport(OutputFileType::OCR_TEXT, -1, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
  // Check whether output file is exist or not
  EXPECT_TRUE(UnitTestUtility::IsExistingFile(output_file_path));
  std::string file_content = UnitTestUtility::ReadContent(output_file_path);
  EXPECT_TRUE(file_content.empty() == false);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_never_cancelled_when_export_bounding_box_text) {
  // Setup environment for testing
  DoExport(OutputFileType::BB_TEXT, -1, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
  // Check whether output file is exist or not
  EXPECT_TRUE(UnitTestUtility::IsExistingFile(output_file_path));
  std::string file_content = UnitTestUtility::ReadContent(output_file_path);
  EXPECT_TRUE(file_content.empty() == false);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_never_cancelled_when_export_xml) {
  // Setup environment for testing
  DoExport(OutputFileType::XML, -1, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
  // Check whether output file is exist or not
  EXPECT_TRUE(UnitTestUtility::IsExistingFile(output_file_path));
  std::string file_content = UnitTestUtility::ReadContent(output_file_path);
  EXPECT_TRUE(file_content.empty() == false);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_never_cancelled_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, -1, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
  // Check whether output file is exist or not
  EXPECT_TRUE(UnitTestUtility::IsExistingFile(output_file_path));
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_never_cancelled_when_export_pdf) {
  // Setup environment for testing
  DoExport(OutputFileType::PDF, -1, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
  // Check whether output file is exist or not
  EXPECT_TRUE(UnitTestUtility::IsExistingFile(output_file_path));
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_never_cancelled_when_export_no_ocr_pdf) {
  // Setup environment for testing
  DoExport(OutputFileType::NO_OCR_PDF, -1, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
  // Check whether output file is exist or not
  EXPECT_TRUE(UnitTestUtility::IsExistingFile(output_file_path));
}

/**
 * EXPORT DOCUMENT WHEN CANCEL PHOCR IMMEDIATELY
 */
TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_immedially_when_export_ocr_text) {
  // Setup environment for testing
  DoExport(OutputFileType::OCR_TEXT, 0, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INTERRUPT_BY_CANCEL);
  // Check whether output file is exist or not
  EXPECT_FALSE(UnitTestUtility::IsExistingFile(output_file_path));
  std::string file_content = UnitTestUtility::ReadContent(output_file_path);
  EXPECT_TRUE(file_content.empty());
  EXPECT_LE(PHOcrTiming::MeasureElapsedTime(), kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_immedially_when_export_bounding_box_text) {
  // Setup environment for testing
  DoExport(OutputFileType::BB_TEXT, 0, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INTERRUPT_BY_CANCEL);
  // Check whether output file is exist or not
  EXPECT_FALSE(UnitTestUtility::IsExistingFile(output_file_path));
  std::string file_content = UnitTestUtility::ReadContent(output_file_path);
  EXPECT_TRUE(file_content.empty());
  EXPECT_LE(PHOcrTiming::MeasureElapsedTime(), kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_immedially_when_export_xml) {
  // Setup environment for testing
  DoExport(OutputFileType::XML, 0, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INTERRUPT_BY_CANCEL);
  EXPECT_LE(PHOcrTiming::MeasureElapsedTime(), kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_immedially_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 0, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INTERRUPT_BY_CANCEL);
  EXPECT_LE(PHOcrTiming::MeasureElapsedTime(), kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_immedially_when_export_pdf) {
  // Setup environment for testing
  DoExport(OutputFileType::PDF, 0, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INTERRUPT_BY_CANCEL);
  EXPECT_LE(PHOcrTiming::MeasureElapsedTime(), kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_immedially_when_export_no_ocr_pdf) {
  // Setup environment for testing
  DoExport(OutputFileType::NO_OCR_PDF, 0, image_path_ws);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INTERRUPT_BY_CANCEL);
  EXPECT_LE(PHOcrTiming::MeasureElapsedTime(), kCancelElapsedTime);
}

/**
 * EXPORT DOCUMENT WHEN CANCEL PHOCR AFTER each 1000 milliseconds
 */
TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_immedially_when_export_docx_to_check_memory_leak) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 0, table_image_path);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INTERRUPT_BY_CANCEL);
  EXPECT_LE(PHOcrTiming::MeasureElapsedTime(), kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_1000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 1000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_2000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 2000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_3000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 3000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_4000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 4000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_5000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 5000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_6000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 6000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_7000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 7000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_8000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 8000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_9000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 9000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_10000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 10000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_11000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 11000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_12000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 12000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_13000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 13000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_14000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 14000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_15000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 15000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

// In this case, PHOcr will export docx file successfully before it is
// cancelled
TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_16000ms_when_export_docx) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 16000, table_image_path);
  CheckPHOcrResult(kCancelElapsedTime);
}

/**
 * TESTING WITH 4 PAGES TEST CASE
 */
TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_never_cancelled_when_export_docx_with_4_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, -1, four_pages_image_path);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
  // Check whether output file is exist or not
  EXPECT_TRUE(UnitTestUtility::IsExistingFile(output_file_path));
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_immediately_when_export_docx_with_4_pages_to_check_memory_leak) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 0, four_pages_image_path);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INTERRUPT_BY_CANCEL);
  EXPECT_LE(PHOcrTiming::MeasureElapsedTime(), kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_1000ms_when_export_docx_with_4_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 1000, four_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_2000ms_when_export_docx_with_4_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 2000, four_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_3000ms_when_export_docx_with_4_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 3000, four_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_4000ms_when_export_docx_with_4_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 4000, four_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_5000ms_when_export_docx_with_4_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 5000, four_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_6000ms_when_export_docx_with_4_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 6000, four_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_7000ms_when_export_docx_with_4_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 7000, four_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_8000ms_when_export_docx_with_4_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 8000, four_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_9000ms_when_export_docx_with_4_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 9000, four_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_10000ms_when_export_docx_with_4_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 10000, four_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

/**
 * TESTING WITH 10 PAGES TEST CASE
 */
TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_immediately_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 0, ten_pages_image_path);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INTERRUPT_BY_CANCEL);
  EXPECT_LE(PHOcrTiming::MeasureElapsedTime(), kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_1000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 1000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_2000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 2000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_3000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 3000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_4000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 4000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_5000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 5000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_6000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 6000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_7000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 7000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_8000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 8000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_9000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 9000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_10000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 10000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_11000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 11000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_12000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 12000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_13000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 13000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_14000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 14000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_15000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 15000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_16000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 16000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_17000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 17000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_18000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 18000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_19000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 19000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}

TEST_F(PHOcrDocumentSetCancelDecisionMethodTest, PHOcr_is_cancelled_after_20000ms_when_export_docx_with_10_pages) {
  // Setup environment for testing
  DoExport(OutputFileType::DOCX, 20000, ten_pages_image_path);
  CheckPHOcrResult(kCancelMultiplePagesElapsedTime);
}
