/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrRowData.h
 * @brief   Interface of PHOcrRowData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <memory>
#include <vector>
#include "PHOcrCellData.h"
#include "PHOcrDefines.h"
#include "PHOcrRectangle.h"

namespace phocr {

class PHOcrRowData;
typedef std::shared_ptr<PHOcrRowData> PHOcrRowDataPtr;

class PHOCR_API PHOcrRowData : public PHOcrElementData {
 private:
  std::vector<PHOcrCellDataPtr> cells_;
  unsigned long num_cols_;

 public:
  PHOcrRowData();

  // Deep copy
  PHOcrRowData(const PHOcrRowData& src);

  explicit PHOcrRowData(PHOcrElementDataPtr element);

  ~PHOcrRowData();

  const std::vector<PHOcrCellDataPtr>& GetCells();

  void SetCells(const std::vector<PHOcrCellDataPtr>& cells);

  unsigned long GetCellSize();

  void SetCellSize(unsigned long num_cols);
};

}  // namespace phocr
