/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrAPI_BarcodeStartStopCodeOfCode39.cpp
 * @brief   Unit test of SetBarcodeMode API
 * @author  Hoang Minh Phuc<phuc.hoangminh@toshiba-tsdv.com>
 * @date    2019-09-30
 *****************************************************************************/

#include <string>
#include <cstdio>
#include <vector>
#include <unordered_map>
#include "TestDataManager.h"
#include "barcode/include/BarcodeTypesBitMapper.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocr/api/PHOcrPageMaker.h"
#include "phocr/api/PHOcrPage.h"
#include "phocr/api/PHOcrPageData.h"
#include "phocr/api/PHOcrBarcodeData.h"
#include "phocrtests/UnitTestBarcodeUtility.h"
#include "gtest/gtest.h"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>

using namespace barcode;
using namespace phocr;
namespace pt = boost::property_tree;

/**
 * A test class used to testing API WithStartStopCodeForCode39 in PHOcrSetting class
 */
class PHOcrBarcodeStartStopCodeOfCode39SettingTest : public ::testing::Test {
 protected:
  // Manage test case
  TestDataManager* data_manager_;

  // Path to an image contains all types of barcode that PHOcr support,
  // both 1D and 2D too
  std::wstring all_barcode_image_path_;

  // PHOcrPage
  PHOcrPagePtr page_;

  // PHOcrPageData
  PHOcrPageDataPtr page_data_;

  // PHOcrSetting
  PHOcrSettings setting_;

  // Store barcode result
  std::vector<PHOcrBarcodeDataPtr> barcode_results_;

  static const std::unordered_map<std::string, unsigned int>
  barcode_mode_mapper_;

 public:
  // Default constructor
  PHOcrBarcodeStartStopCodeOfCode39SettingTest() {
    data_manager_ = phocr::TestDataManager::Instance();
    all_barcode_image_path_ = ConvertToWString(
        data_manager_->GetPath("ALL_BARCODE.tif"));
    // Create PHOcrDocument
    PHOcrPageMaker::CreatePage(page_, all_barcode_image_path_);
  }

  // Destructor
  virtual ~PHOcrBarcodeStartStopCodeOfCode39SettingTest() {
  }

  void SetupSetting(bool value) {
    unsigned int barcode_mode = 1 << BarcodeTypesBitMapper::BIT_INDEX_1D_BARCODE;
    setting_.SetBarcodeMode(barcode_mode);
    setting_.WithStartStopCodeForCode39(value);
  }

  void Export() {
    page_->PHOcrSetSettings(setting_);
    std::vector<std::wstring> barcodes;
    page_->PHOcrGetAllBarcodes(barcodes);
    page_->PHOcrGetPageDataStruct(page_data_);
    barcode_results_ = page_data_->GetBarcodes();
  }
};

/****************************************************************
 * With start/stop code
 ***************************************************************/
TEST_F(PHOcrBarcodeStartStopCodeOfCode39SettingTest, With_start_stop_code) {
  SetupSetting(true);
  Export();
  int code39_count;
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode39(barcode_results_, code39_count));
  EXPECT_FALSE(UnitTestBarcodeUtility::HasCode39AndAttachStartStopCode(barcode_results_));
  EXPECT_EQ(code39_count, 1);
}

/****************************************************************
 * Without start/stop code
 ***************************************************************/
TEST_F(PHOcrBarcodeStartStopCodeOfCode39SettingTest, Without_start_stop_code) {
  SetupSetting(false);
  Export();
  int code39_count;
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode39(barcode_results_, code39_count));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode39AndAttachStartStopCode(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode39AndNoAttachStartStopCode(barcode_results_));
  EXPECT_EQ(code39_count, 2);
}
