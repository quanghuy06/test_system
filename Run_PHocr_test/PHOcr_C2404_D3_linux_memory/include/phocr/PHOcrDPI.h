/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrDPI.h
 * @brief   This module is used to abstract DPI information in PHOcr
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Sep 18, 2019
 *****************************************************************************/

#ifndef PHOCR_API_PHOCRDPI_H_
#define PHOCR_API_PHOCRDPI_H_

#include "PHOcrDefines.h"

namespace phocr {
/**
 * Present DPI information in PHOcr
 */
class PHOCR_API PHOcrDPI {
  unsigned int horizontal_resolution_;
  unsigned int vertical_resolution_;

 public:
  PHOcrDPI();

  PHOcrDPI(unsigned int horizontal_res, unsigned int vertical_res);

  PHOcrDPI(const PHOcrDPI& src);

  ~PHOcrDPI();

  unsigned int GetHorizontalResolution() const;

  void SetHorizontalResolution(unsigned int horizontal_resolution);

  unsigned int GetVerticalResolution() const;

  void SetVerticalResolution(unsigned int vertical_resolution);

  const PHOcrDPI& operator=(const PHOcrDPI& other);
};

}  // namespace phocr

#endif  // PHOCR_API_PHOCRDPI_H_ //
