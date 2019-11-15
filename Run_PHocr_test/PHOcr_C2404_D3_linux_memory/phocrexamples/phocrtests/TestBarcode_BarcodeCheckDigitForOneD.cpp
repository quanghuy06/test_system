/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestBarcode_BarcodeCheckDigitForOneD.cpp
 * @brief   Unit test of SetBarcodeMode API
 * @author  Hoang Minh Phuc<phuc.hoangminh@toshiba-tsdv.com>
 * @date    2019-10-08
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
 * A test class used to testing API EnableCheckDigitForOneDBarcode in Barcode class
 */
/*
For EAN-8, EAN-13, UPC-A, UPC-E:
=> ALWAYS use check digit calculation
- If equal with the final digit, the data of the check digit should be outputted as the bar code data.
- If not equal, the bar code data cannot be outputted since it is judged as wrong.

For Code 93, Code 128, UCC 128, Postnet (Drop):
=> ALWAYS use check digit calculation
- If equal with the final digit, the data of the check digit should not be outputted as the bar code data.
- If not equal, the bar code data cannot be outputted since it is judged as wrong.

For Industrial 2 of 5, IATA 2 of 5, PATCH:
- Do not use check digit calculation
- The data of all digit should be outputed as the bar code data.

For Code 39, Codabar, Interleaved 2 of 5, Matrix 2 of 5:
- If enable check digit => use check digit calculation
  + If equal with the final digit, the data of the check digit should not be outputted as the bar code data.
  + If not equal, the bar code data cannot be outputted since it is judged as wrong.
- If disable check digit:
  + Do not use check digit calculation.
  + The data of all digit should be outputed as the bar code data.
*/
class BarcodeCheckDigitForOneDSettingTest : public ::testing::Test {
 protected:
  // Manage test case
  TestDataManager* data_manager_;

  // Path to an image contains 1D barcode types
  std::string oned_barcode_image_path_;

  // Path to an image contains 1D error checkdigit barcode types
  std::string error_check_digit_barcode_image_path_;

  // PHOcrBarcode
  PHOcrBarcode* barcode;

  // Store barcode result
  std::vector<PHOcrBarcodeDataPtr> barcode_results_;

 public:
  // Default constructor
  BarcodeCheckDigitForOneDSettingTest() {
    data_manager_ = phocr::TestDataManager::Instance();
    oned_barcode_image_path_ = data_manager_->GetPath("barcodes.jpg");
    error_check_digit_barcode_image_path_ = data_manager_->GetPath("barcodes_error_check_digit.jpg");
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
  virtual ~BarcodeCheckDigitForOneDSettingTest() {
    delete barcode;
  }

  void DecodeBarcode(bool error_checkdigit_image=false) {
    Pix* image = nullptr;
    if (error_checkdigit_image) {
      image = pixRead(error_check_digit_barcode_image_path_.c_str());
    } else {
      image = pixRead(oned_barcode_image_path_.c_str());
    }
    std::vector<BarcodeTagging> barcode_results = barcode->DecodeBarcode(image);
    barcode_results_ = UnitTestBarcodeUtility::ConvertBarcodeTaggingToPHOcrBarcodeData(barcode_results);
    pixDestroy(&image);
  }

  void SetupSetting(bool value) {
    barcode->EnableCheckDigitForOneDBarcode(value);
  }
};

/****************************************************************
 * Enable check digit for 1D barcode
 ***************************************************************/
TEST_F(BarcodeCheckDigitForOneDSettingTest, Enable_check_digit_for_oned_barcode) {
  SetupSetting(true);
  DecodeBarcode();
  /**
   * For EAN-8, EAN-13, UPC-A, UPC-E:
   * => ALWAYS use check digit calculation
   * - If equal with the final digit, the data of the check digit should be outputted as the bar code data.
   * - If not equal, the bar code data cannot be outputted since it is judged as wrong.
   */
  // For EAN-8, EAN-13, UPC-A, UPC-E:
  EXPECT_TRUE(UnitTestBarcodeUtility::HasEAN8(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasEAN13(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCA(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCE(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "EAN_8", "4412345"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "EAN_13", "551234567890"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "UPC_A", "99012345678"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "UPC_E", "0001234"));

  /**
   * For Code 93, Code 128, UCC 128, Postnet:
   * => ALWAYS use check digit calculation
   * - If equal with the final digit, the data of the check digit should not be outputted as the bar code data.
   * - If not equal, the bar code data cannot be outputted since it is judged as wrong.
   */
  // For Code 93, Code 128, UCC 128, Postnet (Drop):
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode93(barcode_results_));
  // Code128 and UCC 128 is the same
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode128(barcode_results_));
  EXPECT_FALSE(UnitTestBarcodeUtility::HasPostnet(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODE_93", "Code93_ABCDEFG"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODE_128", "Code128_ABCDEFGHIJKLMNOPQR"));

  /**
   * For Industrial 2 of 5, IATA 2 of 5, PATCH:
   * - Do not use check digit calculation
   * - The data of all digit should be outputed as the bar code data.
   */
  // For Industrial 2 of 5, IATA 2 of 5, PATCH:
  EXPECT_TRUE(UnitTestBarcodeUtility::HasIndustrial2of5(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasIATA2of5(barcode_results_));
  EXPECT_FALSE(UnitTestBarcodeUtility::HasPatch(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "STANDARD_2_OF_5", "22678909876"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "IATA_2_OF_5", "111234567890"));

  /**
   * For Code 39, Codabar, Interleaved 2 of 5, Matrix 2 of 5:
   * - If enable check digit => use check digit calculation
   *   + If equal with the final digit, the data of the check digit should not be outputted as the bar code data.
   *   + If not equal, the bar code data cannot be outputted since it is judged as wrong.
   * - If disable check digit:
   *   + Do not use check digit calculation.
   *   + The data of all digit should be outputed as the bar code data.
   */
  // For Code 39, Codabar, Interleaved 2 of 5, Matrix 2 of 5:
  int code39_count, codabar_count, interleaved2of5_cout, matrix2of5_count;
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode39(barcode_results_, code39_count));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCodabar(barcode_results_, codabar_count));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasInterleaved2of5(barcode_results_, interleaved2of5_cout));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasMatrix2of5(barcode_results_, matrix2of5_count));
  EXPECT_EQ(code39_count, 1);
  EXPECT_EQ(codabar_count, 1);
  EXPECT_EQ(interleaved2of5_cout, 1);
  EXPECT_EQ(matrix2of5_count, 1);
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODE_39", "CODE39-VWZY"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODABAR", "1234567890"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "INTERLEAVED_2_OF_5", "33123456789"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "MATRIX_2_OF_5", "66098765432"));
}

/****************************************************************
 * Disable check digit for 1D barcode
 ***************************************************************/
TEST_F(BarcodeCheckDigitForOneDSettingTest, Disable_check_digit_for_oned_barcode) {
  SetupSetting(false);
  DecodeBarcode();
  /**
   * For EAN-8, EAN-13, UPC-A, UPC-E:
   * => ALWAYS use check digit calculation
   * - If equal with the final digit, the data of the check digit should be outputted as the bar code data.
   * - If not equal, the bar code data cannot be outputted since it is judged as wrong.
   */
  // For EAN-8, EAN-13, UPC-A, UPC-E:
  EXPECT_TRUE(UnitTestBarcodeUtility::HasEAN8(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasEAN13(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCA(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCE(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "EAN_8", "4412345"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "EAN_13", "551234567890"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "UPC_A", "99012345678"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "UPC_E", "0001234"));

  /**
   * For Code 93, Code 128, UCC 128, Postnet:
   * => ALWAYS use check digit calculation
   * - If equal with the final digit, the data of the check digit should not be outputted as the bar code data.
   * - If not equal, the bar code data cannot be outputted since it is judged as wrong.
   */
  // For Code 93, Code 128, UCC 128, Postnet (Drop):
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode93(barcode_results_));
  // Code128 and UCC 128 is the same
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode128(barcode_results_));
  EXPECT_FALSE(UnitTestBarcodeUtility::HasPostnet(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODE_93", "Code93_ABCDEFG"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODE_128", "Code128_ABCDEFGHIJKLMNOPQR"));

  /**
   * For Industrial 2 of 5, IATA 2 of 5, PATCH:
   * - Do not use check digit calculation
   * - The data of all digit should be outputed as the bar code data.
   */
  // For Industrial 2 of 5, IATA 2 of 5, PATCH:
  EXPECT_TRUE(UnitTestBarcodeUtility::HasIndustrial2of5(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasIATA2of5(barcode_results_));
  // We don't support PATCH for now
  EXPECT_FALSE(UnitTestBarcodeUtility::HasPatch(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "STANDARD_2_OF_5", "22678909876"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "IATA_2_OF_5", "111234567890"));

  /**
   * For Code 39, Codabar, Interleaved 2 of 5, Matrix 2 of 5:
   * - If enable check digit => use check digit calculation
   *   + If equal with the final digit, the data of the check digit should not be outputted as the bar code data.
   *   + If not equal, the bar code data cannot be outputted since it is judged as wrong.
   * - If disable check digit:
   *   + Do not use check digit calculation.
   *   + The data of all digit should be outputed as the bar code data.
   */
  // For Code 39, Codabar, Interleaved 2 of 5, Matrix 2 of 5:
  int code39_count, codabar_count, interleaved2of5_cout, matrix2of5_count;
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode39(barcode_results_, code39_count));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCodabar(barcode_results_, codabar_count));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasInterleaved2of5(barcode_results_, interleaved2of5_cout));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasMatrix2of5(barcode_results_, matrix2of5_count));
  EXPECT_EQ(code39_count, 2);
  EXPECT_EQ(codabar_count, 2);
  EXPECT_EQ(interleaved2of5_cout, 2);
  EXPECT_EQ(matrix2of5_count, 2);
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODE_39", "CODE39-VWXYZ"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODE_39", "CODE39-VWZYS"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODABAR", "1234567890"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODABAR", "12345678903"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "INTERLEAVED_2_OF_5", "331234567890"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "INTERLEAVED_2_OF_5", "331234567893"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "MATRIX_2_OF_5", "660987654321"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "MATRIX_2_OF_5", "660987654322"));
}

/****************************************************************
 * Enable check digit for 1D barcode with mandatory barcode types
 ***************************************************************/
TEST_F(BarcodeCheckDigitForOneDSettingTest, Enable_check_digit_for_oned_barcode_with_mandatory_barcode_types) {
  SetupSetting(true);
  DecodeBarcode(true);
  /**
   * For EAN-8, EAN-13, UPC-A, UPC-E:
   * => ALWAYS use check digit calculation
   * - If equal with the final digit, the data of the check digit should be outputted as the bar code data.
   * - If not equal, the bar code data cannot be outputted since it is judged as wrong.
   */
  // For EAN-8, EAN-13, UPC-A, UPC-E:
  EXPECT_TRUE(UnitTestBarcodeUtility::HasEAN8(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasEAN13(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCA(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCE(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "EAN_8", "4412345"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "EAN_13", "551234567890"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "UPC_A", "99012345678"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "UPC_E", "0001234"));

  /**
   * For Code 93, Code 128, UCC 128, Postnet:
   * => ALWAYS use check digit calculation
   * - If equal with the final digit, the data of the check digit should not be outputted as the bar code data.
   * - If not equal, the bar code data cannot be outputted since it is judged as wrong.
   */
  // For Code 93, Code 128, UCC 128, Postnet (Drop):
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode93(barcode_results_));
  // Code128 and UCC 128 is the same
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode128(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODE_93", "Code93_ABCDEFG"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODE_128", "Code128_ABCDEFGHIJKLMNOPQR"));
}

/****************************************************************
 * Disable check digit for 1D barcode with mandatory barcode types
 ***************************************************************/
TEST_F(BarcodeCheckDigitForOneDSettingTest, Disable_check_digit_for_oned_barcode_with_mandatory_barcode_types) {
  SetupSetting(false);
  DecodeBarcode(true);
  /**
   * For EAN-8, EAN-13, UPC-A, UPC-E:
   * => ALWAYS use check digit calculation
   * - If equal with the final digit, the data of the check digit should be outputted as the bar code data.
   * - If not equal, the bar code data cannot be outputted since it is judged as wrong.
   */
  // For EAN-8, EAN-13, UPC-A, UPC-E:
  EXPECT_TRUE(UnitTestBarcodeUtility::HasEAN8(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasEAN13(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCA(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasUPCE(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "EAN_8", "4412345"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "EAN_13", "551234567890"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "UPC_A", "99012345678"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "UPC_E", "0001234"));

  /**
   * For Code 93, Code 128, UCC 128, Postnet:
   * => ALWAYS use check digit calculation
   * - If equal with the final digit, the data of the check digit should not be outputted as the bar code data.
   * - If not equal, the bar code data cannot be outputted since it is judged as wrong.
   */
  // For Code 93, Code 128, UCC 128, Postnet (Drop):
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode93(barcode_results_));
  // Code128 and UCC 128 is the same
  EXPECT_TRUE(UnitTestBarcodeUtility::HasCode128(barcode_results_));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODE_93", "Code93_ABCDEFG"));
  EXPECT_TRUE(UnitTestBarcodeUtility::HasBarcodeTypeWithData(barcode_results_, "CODE_128", "Code128_ABCDEFGHIJKLMNOPQR"));
}
