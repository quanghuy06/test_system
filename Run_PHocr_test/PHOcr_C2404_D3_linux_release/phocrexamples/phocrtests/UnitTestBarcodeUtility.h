/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    UnitTestBarcodeUtility.h
 * @brief   Implement common functions to avoid duplicated code
 * @author  Hoang Minh Phuc<phuc.hoangminh@toshiba-tsdv.com>
 * @date    Oct 07, 2019
 *****************************************************************************/

#pragma once

#include <vector>
#include <string>

#include "barcode/include/BarcodeTagging.h"
#include "phocr/api/PHOcrBarcodeData.h"

using namespace barcode;
using namespace phocr;

/**
 * This class is created with the idea is make our unit testing more easier by
 * proving some utility function to check status of result after PHOcr process.
 */
class UnitTestBarcodeUtility {
 public:
  UnitTestBarcodeUtility();
  virtual ~UnitTestBarcodeUtility();

  /**
   * Convert from BarcodeTagging to PHOcrBarcodeData
   * @param barcode_tags
   */
  static std::vector<PHOcrBarcodeDataPtr> ConvertBarcodeTaggingToPHOcrBarcodeData(std::vector<BarcodeTagging> barcode_tags);

  /**
   * Check barcode has start/stop code of Code39 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasCode39AndAttachStartStopCode(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has Code39 without start/stop code or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasCode39AndNoAttachStartStopCode(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has Code39 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasCode39(const std::vector<PHOcrBarcodeDataPtr>& barcode_results, int &code39_count);

  /**
   * Check barcode has supplemental code or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasSupplementalCode(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has only supplemental code or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasOnlySupplementalCode(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has supplemental code 2 digits or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasSupplementalCode2Digits(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has supplemental code 5 digits or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasSupplementalCode5Digits(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check format of barcode if UPC-A, UPC-E, EAN-8 or EAN-13
   * @param format
   * @return true or false
   */
  static bool IsUPCEANBarcode(const std::string& format);

  /**
   * Check barcode contains UPC-A, UPC-E, EAN-8, EAN-13 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasUPCEANCode(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode contains UPC-A, UPC-E, EAN-8, EAN-13 with 2 digits or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasUPCEANCodeWith2Digits(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode contains UPC-A, UPC-E, EAN-8, EAN-13 with 5 digits or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasUPCEANCodeWith5Digits(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has EAN-8 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasEAN8(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has EAN-13 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasEAN13(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has UPC-A or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasUPCA(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has UPC-E or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasUPCE(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has Code93 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasCode93(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has Code128 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasCode128(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has Postnet or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasPostnet(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has Industrial 2 of 5 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasIndustrial2of5(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has IATA 2 of 5 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasIATA2of5(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has Patch or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasPatch(const std::vector<PHOcrBarcodeDataPtr>& barcode_results);

  /**
   * Check barcode has Interleaved 2 of 5 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasCodabar(const std::vector<PHOcrBarcodeDataPtr>& barcode_results, int &codabar_count);

  /**
   * Check barcode has Code128 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasInterleaved2of5(const std::vector<PHOcrBarcodeDataPtr>& barcode_results, int &interleaved2of5_cout);

  /**
   * Check barcode has Matrix 2 of 5 or not
   * @param barcode_results
   * @return true or false
   */
  static bool HasMatrix2of5(const std::vector<PHOcrBarcodeDataPtr>& barcode_results, int &matrix2of5_count);

  /**
   * Check returned barcodes has specified barcode by format and data
   * @param barcode_results
   * @return true or false
   */
  static bool HasBarcodeTypeWithData(const std::vector<PHOcrBarcodeDataPtr>& barcode_results, std::string format, std::string data);
};
