/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrCharacterData.h
 * @brief   Interface of PHOcrCharacterData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <string>
#include "PHOcrDefines.h"
#include "PHOcrElementData.h"

namespace phocr {

class PHOcrCharacterData;
typedef std::shared_ptr<PHOcrCharacterData> PHOcrCharacterDataPtr;

class PHOCR_API PHOcrCharacterData : public PHOcrElementData {
 private:
  std::string value_;  // Value of character
  float black_ratio_;  // Black ratio of character
  float confidence_;   // Confidence of character

 public:
  PHOcrCharacterData();

  // Deep copy
  PHOcrCharacterData(const PHOcrCharacterData& src);

  explicit PHOcrCharacterData(PHOcrElementDataPtr element);

  virtual ~PHOcrCharacterData();

  const std::string& GetValue();

  void SetValue(const std::string& value);

  float GetBlackRatio();

  void SetBlackRatio(float black_ratio);

  float GetConfidence();

  void SetConfidence(float confidence);
};

}  // namespace phocr
