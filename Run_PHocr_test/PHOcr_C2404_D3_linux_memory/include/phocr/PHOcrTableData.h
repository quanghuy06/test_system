/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrTableData.h
 * @brief   Interface of PHOcrTableData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <memory>
#include <vector>
#include "PHOcrDefines.h"
#include "PHOcrRowData.h"

namespace phocr {

class PHOcrTableData;
typedef std::shared_ptr<PHOcrTableData> PHOcrTableDataPtr;

class PHOCR_API PHOcrTableData : public PHOcrElementData {
 private:
  int num_row_;
  int num_column_;
  std::vector<PHOcrRowDataPtr> rows_;

 public:
  PHOcrTableData();

  // Deep copy
  PHOcrTableData(const PHOcrTableData& src);

  explicit PHOcrTableData(PHOcrElementDataPtr element);

  virtual ~PHOcrTableData();

  int GetNumColumn();

  void SetNumColumn(int numColumn);

  int GetNumRow();

  void SetNumRow(int numRow);

  const std::vector<std::shared_ptr<PHOcrRowData>>& GetRows();

  void SetRows(const std::vector<PHOcrRowDataPtr>& rows);
};

}  // namespace phocr
