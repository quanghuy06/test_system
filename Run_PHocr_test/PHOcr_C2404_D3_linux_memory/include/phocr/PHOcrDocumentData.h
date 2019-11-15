/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrDocumentData.h
 * @brief   Interface of PHOcrDocumentData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <vector>
#include "PHOcrPageData.h"
#include "PHOcrDocumentResult.h"

namespace phocr {

class PHOcrDocumentData;
typedef std::shared_ptr<PHOcrDocumentData> PHOcrDocumentDataPtr;

class PHOcrDocumentData : public PHOcrDocumentResult {
 private:
  std::vector<PHOcrPageDataPtr> pages_;

 public:
  PHOcrDocumentData();
  explicit PHOcrDocumentData(const std::vector<PHOcrPageDataPtr>& pages);
  virtual ~PHOcrDocumentData();

  const std::vector<PHOcrPageDataPtr>& GetPages();

  void SetPages(const std::vector<PHOcrPageDataPtr>& pages);

  /**
   * Insert a page data to document data
   * @param page_result A page data
   */
  void InsertPageResult(PHOcrPageDataPtr page_result);
};

}  // namespace phocr
