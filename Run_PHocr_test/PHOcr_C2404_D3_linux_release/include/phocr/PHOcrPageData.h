/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrPageData.h
 * @brief   Interface of PHOcrPageData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <memory>
#include <vector>
#include "PHOcrBarcodeData.h"
#include "PHOcrCareaData.h"
#include "PHOcrDefines.h"
#include "PHOcrPageInfoData.h"
#include "PHOcrPhotoData.h"
#include "PHOcrTableData.h"

namespace phocr {

class PHOcrPageData;
typedef std::shared_ptr<PHOcrPageData> PHOcrPageDataPtr;

class PHOCR_API PHOcrPageData : public PHOcrElementData {
 private:
  std::vector<PHOcrBarcodeDataPtr> barcodes_;
  std::vector<PHOcrCareaDataPtr> careas_;
  std::vector<PHOcrTableDataPtr> tables_;
  std::vector<PHOcrPhotoDataPtr> photos_;
  PHOcrPageInfoDataPtr page_info_;

 public:
  PHOcrPageData();
  explicit PHOcrPageData(PHOcrElementDataPtr element);
  explicit PHOcrPageData(const std::vector<PHOcrBarcodeDataPtr>& barcodes,
                const std::vector<PHOcrCareaDataPtr>& careas,
                const std::vector<PHOcrTableDataPtr>& tables,
                const std::vector<PHOcrPhotoDataPtr>& photos,
                const PHOcrPageInfoDataPtr& page_info);

  // Deep copy constructor
  PHOcrPageData(const PHOcrPageData& src);

  virtual ~PHOcrPageData();

  const std::vector<PHOcrBarcodeDataPtr>& GetBarcodes();

  void SetBarcodes(const std::vector<PHOcrBarcodeDataPtr>& barcodes);

  const std::vector<PHOcrCareaDataPtr>& GetCareas();

  void SetCareas(const std::vector<PHOcrCareaDataPtr>& careas);

  const std::vector<PHOcrTableDataPtr>& GetTables();

  void SetTables(const std::vector<PHOcrTableDataPtr>& table);

  const std::vector<PHOcrPhotoDataPtr>& GetPhotos();

  void SetPhotos(const std::vector<PHOcrPhotoDataPtr>& photo);

  const PHOcrPageInfoDataPtr GetPageInfo() const;

  void SetPageInfo(const PHOcrPageInfoDataPtr page_info);
};

}  // namespace phocr
