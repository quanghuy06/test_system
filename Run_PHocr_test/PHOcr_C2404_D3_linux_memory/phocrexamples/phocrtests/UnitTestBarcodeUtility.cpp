/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    UnitTestBarcodeUtility.cpp
 * @brief   Implement common functions to avoid duplicated code
 * @author  Hoang Minh Phuc<phuc.hoangminh@toshiba-tsdv.com>
 * @date    Oct 07, 2019
 *****************************************************************************/

#include "phocrtests/UnitTestBarcodeUtility.h"

UnitTestBarcodeUtility::UnitTestBarcodeUtility() {
}

UnitTestBarcodeUtility::~UnitTestBarcodeUtility() {
}

std::vector<PHOcrBarcodeDataPtr> UnitTestBarcodeUtility::ConvertBarcodeTaggingToPHOcrBarcodeData(std::vector<BarcodeTagging> barcode_tags) {
  std::vector<PHOcrBarcodeDataPtr> barcode_results;
  if (barcode_tags.size() > 0) {
    for (unsigned int i = 0; i < barcode_tags.size(); i++) {
      PHOcrBarcodeDataPtr barcode = std::make_shared<PHOcrBarcodeData>();
      barcode->SetResult(barcode_tags[i].getResult());
      barcode->SetBarcodeFormat(barcode_tags[i].getBarcodeFormat());
      barcode->SetStartCode(barcode_tags[i].getStartCode());
      barcode->SetStopCode(barcode_tags[i].getStartCode());
      barcode->SetSupplementalCode(barcode_tags[i].getSupplementalCode());
      barcode_results.push_back(barcode);
    }
  }
  return barcode_results;
}

bool UnitTestBarcodeUtility::HasCode39AndAttachStartStopCode(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("CODE_39") &&
        barcode_results[k]->GetStartCode().length() > 0 &&
        barcode_results[k]->GetStopCode().length() > 0) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasCode39AndNoAttachStartStopCode(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("CODE_39") &&
        barcode_results[k]->GetStartCode().length() == 0 &&
        barcode_results[k]->GetStopCode().length() == 0) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasCode39(const std::vector<PHOcrBarcodeDataPtr>& barcode_results, int &code39_count) {
  code39_count = 0;
  if (barcode_results.empty()) {
    return false;
  }
  bool has_code39 = false;
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("CODE_39")) {
      has_code39 = true;
      code39_count++;
    }
  }
  return has_code39;
}

bool UnitTestBarcodeUtility::HasSupplementalCode(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (IsUPCEANBarcode(format) &&
        barcode_results[k]->GetSupplementalCode().length() > 0) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasOnlySupplementalCode(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (!HasSupplementalCode(barcode_results)) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (IsUPCEANBarcode(format) &&
        barcode_results[k]->GetSupplementalCode().length() == 0) {
      return false;
    }
  }
  return true;
}

bool UnitTestBarcodeUtility::HasSupplementalCode2Digits(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (!HasSupplementalCode(barcode_results)) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (IsUPCEANBarcode(format)) {
      if (barcode_results[k]->GetSupplementalCode().length() == 5) {
        return false;
      }
    }
  }
  return true;
}

bool UnitTestBarcodeUtility::HasSupplementalCode5Digits(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (!HasSupplementalCode(barcode_results)) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (IsUPCEANBarcode(format)) {
      if (barcode_results[k]->GetSupplementalCode().length() == 2) {
        return false;
      }
    }
  }
  return true;
}

bool UnitTestBarcodeUtility::HasUPCEANCode(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (IsUPCEANBarcode(format)) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasUPCEANCodeWith2Digits(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (!HasSupplementalCode(barcode_results)) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (IsUPCEANBarcode(format)) {
      if (barcode_results[k]->GetSupplementalCode().length() == 2) {
        return true;
      }
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasUPCEANCodeWith5Digits(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (!HasSupplementalCode(barcode_results)) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (IsUPCEANBarcode(format)) {
      if (barcode_results[k]->GetSupplementalCode().length() == 5) {
        return true;
      }
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::IsUPCEANBarcode(const std::string& format) {
  if (format == std::string("EAN_8") ||
      format == std::string("EAN_13") ||
      format == std::string("UPC_A") ||
      format == std::string("UPC_E"))
    return true;
  return false;
}

bool UnitTestBarcodeUtility::HasEAN8(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("EAN_8")) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasEAN13(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("EAN_13")) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasUPCA(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("UPC_A")) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasUPCE(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("UPC_E")) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasCode93(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("CODE_93")) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasCode128(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("CODE_128")) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasPostnet(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("POSTNET")) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasIndustrial2of5(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("STANDARD_2_OF_5")) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasIATA2of5(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("IATA_2_OF_5")) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasPatch(const std::vector<PHOcrBarcodeDataPtr>& barcode_results) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("PATCH")) {
      return true;
    }
  }
  return false;
}

bool UnitTestBarcodeUtility::HasCodabar(const std::vector<PHOcrBarcodeDataPtr>& barcode_results, int &codabar_count) {
  codabar_count = 0;
  if (barcode_results.empty()) {
    return false;
  }
  bool has_codabar = false;
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("CODABAR")) {
      has_codabar = true;
      codabar_count++;
    }
  }
  return has_codabar;
}

bool UnitTestBarcodeUtility::HasInterleaved2of5(const std::vector<PHOcrBarcodeDataPtr>& barcode_results, int &interleaved2of5_cout) {
  interleaved2of5_cout = 0;
  if (barcode_results.empty()) {
    return false;
  }
  bool has_interleaved2of5 = false;
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("INTERLEAVED_2_OF_5")) {
      has_interleaved2of5 = true;
      interleaved2of5_cout++;
    }
  }
  return has_interleaved2of5;
}

bool UnitTestBarcodeUtility::HasMatrix2of5(const std::vector<PHOcrBarcodeDataPtr>& barcode_results, int &matrix2of5_count) {
  matrix2of5_count = 0;
  if (barcode_results.empty()) {
    return false;
  }
  bool has_matrix2of5 = false;
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    if (format == std::string("MATRIX_2_OF_5")) {
      has_matrix2of5 = true;
      matrix2of5_count++;
    }
  }
  return has_matrix2of5;
}

bool UnitTestBarcodeUtility::HasBarcodeTypeWithData(const std::vector<PHOcrBarcodeDataPtr>& barcode_results, std::string input_format, std::string input_data) {
  if (barcode_results.empty()) {
    return false;
  }
  for (int k = 0; k < barcode_results.size(); k++) {
    std::string format = barcode_results[k]->GetBarcodeFormat();
    std::string result = barcode_results[k]->GetResult();
    if (input_format == format && input_data == result) {
      return true;
    }
  }
  return false;
}
