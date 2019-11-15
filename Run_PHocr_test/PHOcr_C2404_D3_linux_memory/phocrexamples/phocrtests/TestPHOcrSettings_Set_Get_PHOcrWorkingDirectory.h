/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrSettingsSetGetPHOcrWorkingDirectory.h
 * @brief   This module is used to
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Aug 30, 2019
 *****************************************************************************/

#ifndef PHOCRTESTS_TESTPHOCRSETTINGS_SET_GET_PHOCRWORKINGDIRECTORY_H_
#define PHOCRTESTS_TESTPHOCRSETTINGS_SET_GET_PHOCRWORKINGDIRECTORY_H_

#include <string>
#include <atomic>
#include <vector>
#include "gtest/gtest.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrSettings.h"
#include "phocr/api/PHOcrExportSetting.h"

using phocr::PHOcrDocumentPtr;
using phocr::PHOcrSettings;
using phocr::PHOcrExportSetting;

class TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory : public ::testing::Test {
 protected:
  std::wstring image_path_;  // Path to image
  std::wstring result_name_;  // Name of result file (not include extension yet)
  std::string phocr_working_dir_;  // Name of PHOcr working directory
  const char* permission_denied_dir_;  // Name of permission denied directory

 public:
  // Constructor
  TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory();

  // Destructor
  ~TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory();

  /**
   * This method check if folder phocr_working_dir_ is stored data of PHOcr
   * export in my scenario
   * @return
   */
  bool IsPHOcrDirectoryWorked(std::atomic<bool>& is_done);

  /**
   * Run PHOcr export
   * @param document
   * @param setting
   * @param export_setting
   * @return
   */
  void DoPHOcrExport(
      PHOcrDocumentPtr document,
      PHOcrSettings setting,
      std::vector<PHOcrExportSetting> export_setting,
      std::atomic<bool>& is_done);
};

#endif  // PHOCRTESTS_TESTPHOCRSETTINGS_SET_GET_PHOCRWORKINGDIRECTORY_H_ //
