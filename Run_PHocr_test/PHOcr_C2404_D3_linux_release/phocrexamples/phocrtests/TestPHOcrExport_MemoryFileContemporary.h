/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrExport_MemoryFileContemporary.h
 * @brief   This module is used to unit test the feature export to file and
 * memory at the same time
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Oct 7, 2019
 *****************************************************************************/

#ifndef PHOCRTESTS_TESTPHOCREXPORT_MEMORYFILECONTEMPORARY_H_
#define PHOCRTESTS_TESTPHOCREXPORT_MEMORYFILECONTEMPORARY_H_

#include <string>
#include "gtest/gtest.h"
#include "PHOcrDocument.h"
#include "PHOcrMemoryDataFilter.h"
#include "PHOcrExportSetting.h"

using namespace phocr;

class TestPHOcrExportMemoryFileContemporary : public ::testing::Test {
 protected:
  std::wstring first_page_path_;  // path to first page
  std::wstring second_page_path_;  // path to second page
  PHOcrDocumentPtr document_;  // the document
  PHOcrMemoryDataFilter filter_;  // the filter to dump file

  void PrepareTest();

  void RunExport(const std::vector<PHOcrExportSetting>& settings);

  int DetectExtensionSeparatorPos(const std::string& file_name);

 public:
  TestPHOcrExportMemoryFileContemporary();
  virtual ~TestPHOcrExportMemoryFileContemporary();
};

#endif  // PHOCRTESTS_TESTPHOCREXPORT_MEMORYFILECONTEMPORARY_H_ //
