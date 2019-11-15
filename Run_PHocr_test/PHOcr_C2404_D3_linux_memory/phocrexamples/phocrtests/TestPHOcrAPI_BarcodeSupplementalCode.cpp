/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrAPI_BarcodeSupplementalCode.cpp
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
 * A test class used to testing API SetSupplementalCodeMode in PHOcrSetting class
 */
class PHOcrBarcodeSupplementalCodeSettingTest : public ::testing::Test {
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
  PHOcrBarcodeSupplementalCodeSettingTest() {
    data_manager_ = phocr::TestDataManager::Instance();
    all_barcode_image_path_ = ConvertToWString(
        data_manager_->GetPath("ALL_BARCODE.tif"));
    // Create PHOcrDocument
    PHOcrPageMaker::CreatePage(page_, all_barcode_image_path_);
  }

  // Destructor
  virtual ~PHOcrBarcodeSupplementalCodeSettingTest() {
  }

  void SetupSetting(PHOcrBarcodeSupplementalCode supplemental_code = PHOcrBarcodeSupplementalCode::BSC_AUTOMATIC_DETECTION) {
    unsigned int barcode_mode = 1 << BarcodeTypesBitMapper::BIT_INDEX_1D_BARCODE;
    setting_.SetBarcodeMode(barcode_mode);
    setting_.SetSupplementalCodeMode(supplemental_code);
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
 * Has supplemental code is Automatic detection
 ***************************************************************/
TEST_F(PHOcrBarcodeSupplementalCodeSettingTest, Has_supplemental_code_is_auto_detection) {
  SetupSetting(PHOcrBarcodeSupplementalCode::BSC_AUTOMATIC_DETECTION);
  Export();
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCode(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCodeWith2Digits(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCodeWith5Digits(barcode_results_));
}

/****************************************************************
 * Has supplemental code is Without automatic detection
 ***************************************************************/
TEST_F(PHOcrBarcodeSupplementalCodeSettingTest, Has_supplemental_code_is_without_automatic_detection) {
  SetupSetting(PHOcrBarcodeSupplementalCode::BSC_WITHOUT_AUTOMATIC_DETECTION);
  Export();
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCode(barcode_results_));
  EXPECT_FALSE(UnitTestBarcodeUtility::HasSupplementalCode(barcode_results_));
}

/****************************************************************
 * Has supplemental code is With auto detection (No. of digit is automatically detected)
 ***************************************************************/
TEST_F(PHOcrBarcodeSupplementalCodeSettingTest, Has_supplemental_code_is_with_auto_detection) {
  SetupSetting(PHOcrBarcodeSupplementalCode::BSC_WITH_AUTO_DETECTION);
  Export();
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCodeWith2Digits(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCEANCodeWith5Digits(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasOnlySupplementalCode(barcode_results_));
}

/****************************************************************
 * Has supplemental code is With auto detection (2 digits)
 ***************************************************************/
TEST_F(PHOcrBarcodeSupplementalCodeSettingTest, Has_supplemental_code_is_with_auto_detection_2_digits) {
  SetupSetting(PHOcrBarcodeSupplementalCode::BSC_WITH_AUTO_DETECTION_2_DIGITS);
  Export();
  EXPECT_TRUE(UnitTestBarcodeUtility::HasSupplementalCode2Digits(barcode_results_));
}

/****************************************************************
 * Has supplemental code is With auto detection (5 digits)
 ***************************************************************/
TEST_F(PHOcrBarcodeSupplementalCodeSettingTest, Has_supplemental_code_is_with_auto_detection_5_digits) {
  SetupSetting(PHOcrBarcodeSupplementalCode::BSC_WITH_AUTO_DETECTION_5_DIGITS);
  Export();
  EXPECT_TRUE(UnitTestBarcodeUtility::HasSupplementalCode5Digits(barcode_results_));
}
