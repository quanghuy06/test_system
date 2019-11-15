/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrCellData.h
 * @brief   Interface of PHOcrCellData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <vector>
#include "PHOcrElementData.h"
#include "PHOcrBorderData.h"
#include "PHOcrCareaData.h"
#include "PHOcrPhotoData.h"

namespace phocr {

class PHOcrCellData;
typedef std::shared_ptr<PHOcrCellData> PHOcrCellDataPtr;

class PHOcrTableData;
using PHOcrTableDataPtr = std::shared_ptr<PHOcrTableData>;

class PHOcrCellData : public PHOcrElementData {
 private:
  int col_span_;
  int row_span_;
  PHOcrBorderDataPtr left_border_;         // Left border
  PHOcrBorderDataPtr right_border_;        // Right border
  PHOcrBorderDataPtr top_border_;          // Top border
  PHOcrBorderDataPtr bottom_border_;       // Bottom border
  std::vector<PHOcrCareaDataPtr> careas_;  // List of content areas in cell
  std::vector<PHOcrTableDataPtr> tables_;  // List of tables in cell
  std::vector<PHOcrPhotoDataPtr> photos_;  // List of photos in cell

 public:
  PHOcrCellData();

  // Deep copy
  PHOcrCellData(const PHOcrCellData& src);

  explicit PHOcrCellData(PHOcrElementDataPtr element);

  virtual ~PHOcrCellData();

  int GetColSpan();

  void SetColSpan(int col_span);

  int GetRowSpan();

  void SetRowSpan(int row_span);

  PHOcrBorderDataPtr GetBottomBorder() const;

  void SetBottomBorder(const PHOcrBorderDataPtr& bottom_border);

  PHOcrBorderDataPtr GetLeftBorder() const;

  void SetLeftBorder(const PHOcrBorderDataPtr& left_border);

  PHOcrBorderDataPtr GetRightBorder() const;

  void SetRightBorder(const PHOcrBorderDataPtr& right_border);

  PHOcrBorderDataPtr GetTopBorder() const;

  void SetTopBorder(const PHOcrBorderDataPtr& top_border);

  std::vector<PHOcrCareaDataPtr> GetCAreas() const;

  void SetCAreas(std::vector<PHOcrCareaDataPtr> areas);

  std::vector<PHOcrTableDataPtr> GetTables() const;

  void SetTables(std::vector<PHOcrTableDataPtr> tables);

  std::vector<PHOcrPhotoDataPtr> GetPhotos() const;

  void SetPhotos(std::vector<PHOcrPhotoDataPtr> photos);
};

}  // namespace phocr
