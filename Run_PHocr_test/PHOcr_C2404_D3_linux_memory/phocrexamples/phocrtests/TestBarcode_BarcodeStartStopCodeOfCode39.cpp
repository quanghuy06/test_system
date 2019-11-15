/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestBarcode_BarcodeStartStopCodeForCode39.cpp
 * @brief   Unit test of SetBarcodeMode API
 * @author  Hoang Minh Phuc<phuc.hoangminh@toshiba-tsdv.com>
 * @date    2019-09-30
 *****************************************************************************/

#include <string>
#include <cstdio>
#include <vector>
#include <unordered_map>
#include "TestDataManager.h"
#include "barcode/include/Barcode.h"
#include "barcode/include/BarcodeTypesBitMapper.h"
#include "phocr/api/PHOcrBarcodeData.h"
#include "phocrtests/UnitTestBarcodeUtility.h"
#include "gtest/gtest.h"

using namespace barcode;
using namespace phocr;

/**
 * A test class used to testing API EnableStartStopCodeForCode39 in Barcode class
 */
class BarcodeStartStopCodeForCode39SettingTest : public ::testing::Test {
 protected:
  // Manage test case
  TestDataManager* data_manager_;

  // Path to an image contains all types of barcode that PHOcr support,
  // both 1D and 2D too
  std::string all_barcode_image_path_;

  // PHOcrBarcode
  PHOcrBarcode* barcode;

  // Store barcode result
  std::vector<PHOcrBarcodeDataPtr> barcode_results_;

 public:
  // Default constructor
  BarcodeStartStopCodeForCode39SettingTest() {
    data_manager_ = phocr::TestDataManager::Instance();
    all_barcode_image_path_ = data_manager_->GetPath("ALL_BARCODE.tif");
    // Create PHOcrBarcode
    barcode = new PHOcrBarcode();
    // Setup setting
    BarcodeSearchingMode searching_mode = BarcodeSearchingMode::MULTIPLE_DETECTION;
    barcode->SetBarcodeSearchingMode(searching_mode);
    bool simple = false;
    barcode->SetSimple(simple);
    bool deskew = false;
    barcode->SetDeskew(deskew);
    unsigned int barcode_mode = 1 << BarcodeTypesBitMapper::BIT_INDEX_CODE_39;
    barcode->SetBarcodeMode(barcode_mode);
  }

  // Destructor
  virtual ~BarcodeStartStopCodeForCode39SettingTest() {
    delete barcode;
  }

  void DecodeBarcode() {
    Pix* image = pixRead(all_barcode_image_path_.c_str());
    std::vector<BarcodeTagging> barcode_results = barcode->DecodeBarcode(image);
    barcode_results_ = UnitTestBarcodeUtility::ConvertBarcodeTaggingToPHOcrBarcodeData(barcode_results);
    pixDestroy(&image);
  }

  void SetupSetting(bool value) {
    barcode->WithStartStopCodeForCode39(value);
  }
};

/****************************************************************
 * With start/stop code
 ***************************************************************/
TEST_F(BarcodeStartStopCodeForCode39SettingTest, With_start_stop_code) {
  SetupSetting(true);
  DecodeBarcode();
  int code39_count;
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode39(barcode_results_, code39_count));
  EXPECT_FALSE(UnitTestBarcodeUtility::HasCode39AndAttachStartStopCode(barcode_results_));
  EXPECT_EQ(code39_count, 1);
}

/****************************************************************
 * Without start/stop code
 ***************************************************************/
TEST_F(BarcodeStartStopCodeForCode39SettingTest, Without_start_stop_code) {
  SetupSetting(false);
  DecodeBarcode();
  int code39_count;
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode39(barcode_results_, code39_count));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode39AndAttachStartStopCode(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode39AndNoAttachStartStopCode(barcode_results_));
  EXPECT_EQ(code39_count, 2);
}
