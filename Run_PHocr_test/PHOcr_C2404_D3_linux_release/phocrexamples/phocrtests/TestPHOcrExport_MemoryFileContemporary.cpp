/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrExport_MemoryFileContemporary.cpp
 * @brief   This module is used to implement for class
 * TestPHOcrExportMemoryFileContemporary
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Oct 7, 2019
 *****************************************************************************/

#include "phocrtests/TestPHOcrExport_MemoryFileContemporary.h"
#include "PHOcrDocumentTextResult.h"
#include "PHOcrDocumentData.h"
#include "PHOcrDocument.h"
#include "PHOcrPage.h"
#include "PHOcrPageMaker.h"
#include "PHOcrExportSetting.h"
#include "PHOcrEnum.h"
#include "PHOcrMemoryDataFilter.h"
#include "PHOcrStringHelper.h"
#include "PHOcrDocumentMaker.h"
#include "phocrtests/UnitTestUtility.h"
#include "phocrtests/TestDataManager.h"

const char* kTextResult = "text_result.txt";
const char* kCompleteResult = "complete_result.json";

TestPHOcrExportMemoryFileContemporary::TestPHOcrExportMemoryFileContemporary() {
  first_page_path_ = ConvertToWString(TestDataManager::Instance()->GetPath(
      "first_page.jpg"));
  second_page_path_ = ConvertToWString(TestDataManager::Instance()->GetPath(
      "second_page.jpg"));
  PrepareTest();
}

void TestPHOcrExportMemoryFileContemporary::RunExport(
    const std::vector<PHOcrExportSetting>& settings) {
  PHOcrStatus status;
  status = document_->PHOcrConfigureForExporting(settings);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
  status = document_->PHOcrBeginExporting();
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
  status = document_->PHOcrEndExporting();
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);
}

TestPHOcrExportMemoryFileContemporary::~TestPHOcrExportMemoryFileContemporary() {
  UnitTestUtility::DeletePossiblePHOcrOutputFile();
}

void TestPHOcrExportMemoryFileContemporary::PrepareTest() {
  PHOcrPagePtr first_page;
  PHOcrPageMaker::CreatePage(first_page, first_page_path_);
  PHOcrPagePtr second_page;
  PHOcrPageMaker::CreatePage(second_page, second_page_path_);
  PHOcrDocumentMaker::CreateDocument(document_);
  document_->PHOcrAppendPages({first_page, second_page});
}

int TestPHOcrExportMemoryFileContemporary::DetectExtensionSeparatorPos(
    const std::string& file_name) {
  int idx = file_name.size() - 1;
  for (; idx >= 0; --idx) {
    if (file_name[idx] == '.') {
      break;
    }
  }
  return idx;
}

// User exports only text result to a place in memory
TEST_F(TestPHOcrExportMemoryFileContemporary, user_export_text_result_in_memory) {
  PHOcrDocumentTextResult text_result;
  std::vector<PHOcrExportSetting> setting{
    {&text_result, PHOcrExportFormat::EF_MEMORY_TXT}
  };
  RunExport(setting);

  // Check the result inside memory
  std::vector<PHOcrPageTextResult> pages_res = text_result.getPagesResult();
  EXPECT_EQ(pages_res.size(), 2);

  // Dump data to text file
  filter_.DumpTextFile(&text_result, kTextResult);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(kTextResult) > 0);
}

// User exports complete result to a place in memory
TEST_F(TestPHOcrExportMemoryFileContemporary, user_export_complete_result_in_memory) {
  PHOcrDocumentData complete_result;
  std::vector<PHOcrExportSetting> setting{
    {&complete_result, PHOcrExportFormat::EF_MEMORY_COMPLETE}
  };
  RunExport(setting);

  // Check the result inside memory
  std::vector<PHOcrPageDataPtr> pages_res = complete_result.GetPages();
  EXPECT_EQ(pages_res.size(), 2);

  // Dump data to json file
  filter_.DumpJsonFile(&complete_result, kCompleteResult);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(kCompleteResult) > 0);

}

// User exports text and complete result memory
TEST_F(TestPHOcrExportMemoryFileContemporary, user_export_text_and_complete_result_in_memory) {
  PHOcrDocumentTextResult text_result;
  PHOcrDocumentData complete_result;
  std::vector<PHOcrExportSetting> setting{
    {&complete_result, PHOcrExportFormat::EF_MEMORY_COMPLETE},
    {&text_result, PHOcrExportFormat::EF_MEMORY_TXT}
  };
  RunExport(setting);

  std::vector<PHOcrPageTextResult> text_res = text_result.getPagesResult();
  std::vector<PHOcrPageDataPtr> complete_res = complete_result.GetPages();
  EXPECT_EQ(text_res.size(), 2);
  EXPECT_EQ(complete_res.size(), 2);
  filter_.DumpTextFile(&text_result, kTextResult);
  filter_.DumpJsonFile(&complete_result, kCompleteResult);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(kTextResult) > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(kCompleteResult) > 0);
}

// User exports text and complete result to many place inside memory
TEST_F(TestPHOcrExportMemoryFileContemporary, user_export_text_and_complete_result_in_many_place_in_memory) {
  PHOcrDocumentTextResult text_result1, text_result2;
  PHOcrDocumentData complete_result1, complete_result2;
  std::vector<PHOcrExportSetting> setting{
    {&complete_result1, PHOcrExportFormat::EF_MEMORY_COMPLETE},
    {&complete_result2, PHOcrExportFormat::EF_MEMORY_COMPLETE},
    {&text_result1, PHOcrExportFormat::EF_MEMORY_TXT},
    {&text_result2, PHOcrExportFormat::EF_MEMORY_TXT}
  };
  RunExport(setting);

  std::vector<PHOcrPageTextResult> text_res1 = text_result1.getPagesResult();
  std::vector<PHOcrPageTextResult> text_res2 = text_result2.getPagesResult();
  std::vector<PHOcrPageDataPtr> complete_res1 = complete_result1.GetPages();
  std::vector<PHOcrPageDataPtr> complete_res2 = complete_result2.GetPages();
  EXPECT_EQ(text_res1.size(), 2);
  EXPECT_EQ(text_res2.size(), 2);
  EXPECT_EQ(complete_res1.size(), 2);
  EXPECT_EQ(complete_res2.size(), 2);

  // Dump result to file
  int txt_separator_pos = DetectExtensionSeparatorPos(kTextResult);
  int json_separator_pos = DetectExtensionSeparatorPos(kCompleteResult);
  std::string text_path1 = std::string(kTextResult).insert(
      txt_separator_pos, "_1");
  std::string text_path2 = std::string(kTextResult).insert(
      txt_separator_pos, "_2");
  std::string json_path1 = std::string(kCompleteResult).insert(
      json_separator_pos, "_1");
  std::string json_path2 = std::string(kCompleteResult).insert(
      json_separator_pos, "_2");
  filter_.DumpTextFile(&text_result1, text_path1);
  filter_.DumpTextFile(&text_result2, text_path2);
  filter_.DumpJsonFile(&complete_result1, json_path1);
  filter_.DumpJsonFile(&complete_result2, json_path2);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(text_path1) > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(text_path2) > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(json_path1) > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(json_path2) > 0);
}

// User exports result to file and memory at the same time
TEST_F(TestPHOcrExportMemoryFileContemporary, user_export_file_and_memory_contemporary) {
  PHOcrDocumentTextResult text_result1, text_result2;
  PHOcrDocumentData complete_result1, complete_result2;
  std::vector<PHOcrExportSetting> setting{
    {&complete_result1, PHOcrExportFormat::EF_MEMORY_COMPLETE},
    {&complete_result2, PHOcrExportFormat::EF_MEMORY_COMPLETE},
    {&text_result1, PHOcrExportFormat::EF_MEMORY_TXT},
    {&text_result2, PHOcrExportFormat::EF_MEMORY_TXT},
    {L"text_file", PHOcrExportFormat::EF_TXT},
    {L"xml_file", PHOcrExportFormat::EF_XML},
    {L"docx_file", PHOcrExportFormat::EF_DOCX}
  };
  RunExport(setting);

  std::vector<PHOcrPageTextResult> text_res1 = text_result1.getPagesResult();
  std::vector<PHOcrPageTextResult> text_res2 = text_result2.getPagesResult();
  std::vector<PHOcrPageDataPtr> complete_res1 = complete_result1.GetPages();
  std::vector<PHOcrPageDataPtr> complete_res2 = complete_result2.GetPages();
  EXPECT_EQ(text_res1.size(), 2);
  EXPECT_EQ(text_res2.size(), 2);
  EXPECT_EQ(complete_res1.size(), 2);
  EXPECT_EQ(complete_res2.size(), 2);

  // Dump result to file
  int txt_separator_pos = DetectExtensionSeparatorPos(kTextResult);
  int json_separator_pos = DetectExtensionSeparatorPos(kCompleteResult);
  std::string text_path1 = std::string(kTextResult).insert(
      txt_separator_pos, "_1");
  std::string text_path2 = std::string(kTextResult).insert(
      txt_separator_pos, "_2");
  std::string json_path1 = std::string(kCompleteResult).insert(
      json_separator_pos, "_1");
  std::string json_path2 = std::string(kCompleteResult).insert(
      json_separator_pos, "_2");
  filter_.DumpTextFile(&text_result1, text_path1);
  filter_.DumpTextFile(&text_result2, text_path2);
  filter_.DumpJsonFile(&complete_result1, json_path1);
  filter_.DumpJsonFile(&complete_result2, json_path2);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(text_path1) > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(text_path2) > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(json_path1) > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(json_path2) > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize("text_file.txt") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize("xml_file.xml") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize("docx_file.docx") > 0);
}

TEST_F(TestPHOcrExportMemoryFileContemporary, user_set_wrong_PHOcr_export_setting) {
  PHOcrExportSetting wrong_file_setting(
      L"result", PHOcrExportFormat::EF_MEMORY_COMPLETE);
  PHOcrStatus status = document_->PHOcrConfigureForExporting(
      {wrong_file_setting});
  EXPECT_EQ(status, PHOcrStatus::PHOCR_INTERNAL_ERROR);

  PHOcrDocumentTextResult text_result;
  PHOcrExportSetting wrong_memory_setting(
      &text_result, PHOcrExportFormat::EF_TXT);
  status = document_->PHOcrConfigureForExporting({wrong_memory_setting});
  EXPECT_EQ(status, PHOcrStatus::PHOCR_INTERNAL_ERROR);

  PHOcrDocumentData complete_result;
  wrong_memory_setting = PHOcrExportSetting
      (&complete_result, PHOcrExportFormat::EF_MEMORY_TXT);
  status = document_->PHOcrConfigureForExporting({wrong_memory_setting});
  EXPECT_EQ(status, PHOcrStatus::PHOCR_INTERNAL_ERROR);
}



