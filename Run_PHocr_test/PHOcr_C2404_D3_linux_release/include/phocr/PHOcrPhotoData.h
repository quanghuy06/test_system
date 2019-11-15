/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrPhotoData.h
 * @brief   Interface of PHOcrPhotoData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <memory>
#include "PHOcrDefines.h"
#include "PHOcrElementData.h"

namespace phocr {

class PHOcrPhotoData;
typedef std::shared_ptr<PHOcrPhotoData> PHOcrPhotoDataPtr;

class PHOCR_API PHOcrPhotoData : public PHOcrElementData {
 private:
  std::shared_ptr<unsigned char> image_data_;
  unsigned long image_size_;
  bool is_inside_table_;
  bool is_containing_table_;
  bool is_intersected_with_text_in_table_;

 public:
  PHOcrPhotoData();

  // Deep copy
  PHOcrPhotoData(const PHOcrPhotoData& src);

  explicit PHOcrPhotoData(PHOcrElementDataPtr element);

  virtual ~PHOcrPhotoData();

  void SetImage(std::shared_ptr<unsigned char> image_data);

  std::shared_ptr<unsigned char> GetImage();

  unsigned long GetImageSize();

  void SetImageSize(unsigned long image_size);

  bool IsInsideTable();

  void SetIsInsideTable(bool isInsideTable);

  void SetIsContainingTable(bool isContainingTable);

  bool IsContainingTable();

  void SetIsIntersectedWithTextTable(bool isIntersectedWithTextTable);

  bool IsIntersectedWithTextTable();
};

}  // namespace phocr
