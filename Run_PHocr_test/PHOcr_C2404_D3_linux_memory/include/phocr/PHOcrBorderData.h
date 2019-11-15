/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrBorderData.h
 * @brief   This module is used to
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Sep 16, 2019
 *****************************************************************************/

#ifndef PHOCR_API_PHOCRBORDERDATA_H_
#define PHOCR_API_PHOCRBORDERDATA_H_

#include <memory>
#include "PHOcrDefines.h"

namespace phocr {

class PHOCR_API PHOcrBorderData {
  bool missing_;  // True if this border is missing
  int color_;  // Color of border
  int thickness_;  // Thickness of border

 public:
  // Default constructor
  PHOcrBorderData();

  // Copy constructor
  PHOcrBorderData(const PHOcrBorderData& src);

  virtual ~PHOcrBorderData();

  int getColor() const;

  void setColor(int color);

  bool isMissing() const;

  void setMissing(bool missing);

  int getThickness() const;

  void setThickness(int thickness);
};

using PHOcrBorderDataPtr = std::shared_ptr<PHOcrBorderData>;

}  // namespace phocr

#endif  // PHOCR_API_PHOCRBORDERDATA_H_ //
