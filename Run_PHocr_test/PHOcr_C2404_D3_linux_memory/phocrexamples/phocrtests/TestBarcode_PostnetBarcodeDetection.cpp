/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestBarcode_PostnetBarcodeDetection.cpp
 * @brief   Unit test of SetBarcodeMode API
 * @author  Hoang Minh Phuc<phuc.hoangminh@toshiba-tsdv.com>
 * @date    2019-09-30
 *****************************************************************************/

#include <memory>
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
 * A test class used to testing API SetBarcodeMode in Barcode class
 */
class PostnetBarcodeDetectionSettingTest : public ::testing::Test {
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
  PostnetBarcodeDetectionSettingTest() {
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
    unsigned int barcode_mode = 1 << BarcodeTypesBitMapper::BIT_INDEX_1D_BARCODE;
    barcode->SetBarcodeMode(barcode_mode);
  }

  // Destructor
  virtual ~PostnetBarcodeDetectionSettingTest() {
    delete barcode;
  }

  void DecodeBarcode() {
    Pix* image = pixRead(all_barcode_image_path_.c_str());
    std::vector<BarcodeTagging> barcode_results = barcode->DecodeBarcode(image);
    barcode_results_ = UnitTestBarcodeUtility::ConvertBarcodeTaggingToPHOcrBarcodeData(barcode_results);
    pixDestroy(&image);
  }

  void SetupSetting(unsigned int barcode_code = 0) {
    barcode->SetBarcodeMode(barcode_code);
  }
};

/****************************************************************
 * Set barcode mode is BIT_INDEX_1D_BARCODE
 ***************************************************************/
TEST_F(PostnetBarcodeDetectionSettingTest, Set_barcode_mode_is_BIT_INDEX_1D_BARCODE) {
  unsigned int barcode_mode = 1 << BarcodeTypesBitMapper::BIT_INDEX_1D_BARCODE;
  SetupSetting(barcode_mode);
  DecodeBarcode();
  EXPECT_FALSE(UnitTestBarcodeUtility::HasPostnet(barcode_results_));
}

/****************************************************************
 * Set barcode mode is BIT_INDEX_AUTO
 ***************************************************************/
TEST_F(PostnetBarcodeDetectionSettingTest, Set_barcode_mode_is_BIT_INDEX_AUTO) {
  unsigned int barcode_mode = 1 << BarcodeTypesBitMapper::BIT_INDEX_AUTO;
  SetupSetting(barcode_mode);
  DecodeBarcode();
  EXPECT_FALSE(UnitTestBarcodeUtility::HasPostnet(barcode_results_));
}

/****************************************************************
 * Set barcode mode is BIT_INDEX_POSTNET
 ***************************************************************/
TEST_F(PostnetBarcodeDetectionSettingTest, Set_barcode_mode_is_BIT_INDEX_POSTNET) {
  unsigned int barcode_mode = 1 << BarcodeTypesBitMapper::BIT_INDEX_POSTNET;
  SetupSetting(barcode_mode);
  DecodeBarcode();
  EXPECT_TRUE(UnitTestBarcodeUtility::HasPostnet(barcode_results_));
}
