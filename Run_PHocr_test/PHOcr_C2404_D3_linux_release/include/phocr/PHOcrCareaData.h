/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrCareaData.h
 * @brief   Interface of PHOcrCareaData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <memory>
#include <vector>
#include "PHOcrDefines.h"
#include "PHOcrParagraphData.h"

namespace phocr {

class PHOcrCareaData;
typedef std::shared_ptr<PHOcrCareaData> PHOcrCareaDataPtr;

class PHOCR_API PHOcrCareaData : public PHOcrElementData {
 private:
  std::vector<PHOcrParagraphDataPtr> paragraphs_;
  int right_padding_;
  unsigned int background_color_;

 public:
  PHOcrCareaData();

  // Deep copy
  PHOcrCareaData(const PHOcrCareaData& src);

  explicit PHOcrCareaData(PHOcrElementDataPtr element);

  virtual ~PHOcrCareaData();

  int GetRightPadding();

  void SetRightPadding(int right_padding);

  const std::vector<PHOcrParagraphDataPtr>& GetParagraph();

  void SetParagraphs(const std::vector<PHOcrParagraphDataPtr>& paragraphs);

  unsigned int GetBackgroundColor();

  void SetBackgroundColor(unsigned int background_color);
};

}  // namespace phocr
