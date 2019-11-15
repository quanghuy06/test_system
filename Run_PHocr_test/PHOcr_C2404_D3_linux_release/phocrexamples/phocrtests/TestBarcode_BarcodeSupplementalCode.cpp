/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestBarcode_BarcodeSupplementalCode.cpp
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
#include "barcode/include/BarcodeSupplementalCode.h"
#include "phocr/api/PHOcrBarcodeData.h"
#include "phocrtests/UnitTestBarcodeUtility.h"
#include "gtest/gtest.h"

using namespace barcode;
using namespace phocr;

/**
 * A test class used to testing API SetSupplementalCodeMode in Barcode class
 */
class BarcodeSupplementalCodeSettingTest : public ::testing::Test {
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
  BarcodeSupplementalCodeSettingTest() {
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
  virtual ~BarcodeSupplementalCodeSettingTest() {
    delete barcode;
  }

  void DecodeBarcode() {
    Pix* image = pixRead(all_barcode_image_path_.c_str());
    std::vector<BarcodeTagging> barcode_results = barcode->DecodeBarcode(image);
    barcode_results_ = UnitTestBarcodeUtility::ConvertBarcodeTaggingToPHOcrBarcodeData(barcode_results);
    pixDestroy(&image);
  }

  void SetupSetting(BarcodeSupplementalCode supplemental_code = BarcodeSupplementalCode::BSC_AUTOMATIC_DETECTION) {
    barcode->SetSupplementalCodeMode(supplemental_code);
  }
};

/****************************************************************
 * Has supplemental code is Automatic detection
 ***************************************************************/
TEST_F(BarcodeSupplementalCodeSettingTest, Has_supplemental_code_is_auto_detection) {
  SetupSetting(BarcodeSupplementalCode::BSC_AUTOMATIC_DETECTION);
  DecodeBarcode();
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCode(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCodeWith2Digits(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCodeWith5Digits(barcode_results_));
}

/****************************************************************
 * Has supplemental code is Without automatic detection
 ***************************************************************/
TEST_F(BarcodeSupplementalCodeSettingTest, Has_supplemental_code_is_without_automatic_detection) {
  SetupSetting(BarcodeSupplementalCode::BSC_WITHOUT_AUTOMATIC_DETECTION);
  DecodeBarcode();
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCode(barcode_results_));
  EXPECT_FALSE(UnitTestBarcodeUtility::HasSupplementalCode(barcode_results_));
}

/****************************************************************
 * Has supplemental code is With auto detection (No. of digit is automatically detected)
 ***************************************************************/
TEST_F(BarcodeSupplementalCodeSettingTest, Has_supplemental_code_is_with_auto_detection) {
  SetupSetting(BarcodeSupplementalCode::BSC_WITH_AUTO_DETECTION);
  DecodeBarcode();
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCodeWith2Digits(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCodeWith5Digits(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasOnlySupplementalCode(barcode_results_));
}

/****************************************************************
 * Has supplemental code is With auto detection (2 digits)
 ***************************************************************/
TEST_F(BarcodeSupplementalCodeSettingTest, Has_supplemental_code_is_with_auto_detection_2_digits) {
  SetupSetting(BarcodeSupplementalCode::BSC_WITH_AUTO_DETECTION_2_DIGITS);
  DecodeBarcode();
  EXPECT_TRUE(UnitTestBarcodeUtility::HasSupplementalCode2Digits(barcode_results_));
}

/****************************************************************
 * Has supplemental code is With auto detection (5 digits)
 ***************************************************************/
TEST_F(BarcodeSupplementalCodeSettingTest, Has_supplemental_code_is_with_auto_detection_5_digits) {
  SetupSetting(BarcodeSupplementalCode::BSC_WITH_AUTO_DETECTION_5_DIGITS);
  DecodeBarcode();
  EXPECT_TRUE(UnitTestBarcodeUtility::HasSupplementalCode5Digits(barcode_results_));
}
