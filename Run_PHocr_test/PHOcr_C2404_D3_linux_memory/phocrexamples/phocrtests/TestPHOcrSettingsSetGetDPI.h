/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrSettingsSetGetDPI.h
 * @brief   This module is used to unit test for PHOcrSettings.SetDPI and
 * PHOcrSettings.SetDPI
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Sep 23, 2019
 *****************************************************************************/

#ifndef PHOCRTESTS_TESTPHOCRSETTINGSSETGETDPI_H_
#define PHOCRTESTS_TESTPHOCRSETTINGSSETGETDPI_H_

#include <string>
#include "gtest/gtest.h"

class TestPHOcrSettings_Set_Get_DPI : public ::testing::Test {
 protected:
  std::wstring low_dpi_image;
  std::wstring high_dpi_image;

 public:
  TestPHOcrSettings_Set_Get_DPI();

  virtual ~TestPHOcrSettings_Set_Get_DPI();

  void TestSetDPI(
      const std::wstring& file_path,
      unsigned int horizontal_res,
      unsigned int vertical_res);
};

#endif  // PHOCRTESTS_TESTPHOCRSETTINGSSETGETDPI_H_ //
