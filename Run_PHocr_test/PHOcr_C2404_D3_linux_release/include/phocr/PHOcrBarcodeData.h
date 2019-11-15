/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrBarcodeData.h
 * @brief   Interface of PHOcrBarcodeData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <memory>
#include <vector>
#include <string>
#include "PHOcrDefines.h"
#include "PHOcrElementData.h"

namespace phocr {

class PHOcrBarcodeData;
typedef std::shared_ptr<PHOcrBarcodeData> PHOcrBarcodeDataPtr;

class PHOCR_API PHOcrBarcodeData : public PHOcrElementData {
 private:
  std::string result_;
  std::string format_;
  std::string start_code_;
  std::string stop_code_;
  std::string supplemental_code_;
  std::string check_digit_;

 public:
  PHOcrBarcodeData();

  explicit PHOcrBarcodeData(PHOcrElementDataPtr element);

  // Deep copy
  PHOcrBarcodeData(const PHOcrBarcodeData& src);

  explicit PHOcrBarcodeData(const std::string& result,
                            const std::string& format,
                            const std::string& start_code,
                            const std::string& stop_code,
                            const std::string& supplemental_code,
                            const std::string& check_digit);

  virtual ~PHOcrBarcodeData();

  const std::string& GetResult();

  void SetResult(const std::string& result);

  const std::string& GetBarcodeFormat();

  void SetBarcodeFormat(const std::string& format);

  void SetCheckDigit(const std::string& check_digit);

  const std::string& GetCheckDigit();

  void SetStartCode(const std::string& start_code);

  const std::string& GetStartCode();

  void SetStopCode(const std::string& stop_code);

  const std::string& GetStopCode();

  void SetSupplementalCode(const std::string& supplemental_code);

  const std::string& GetSupplementalCode();
};

}  // namespace phocr
