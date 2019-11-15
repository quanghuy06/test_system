/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrDocumentResult.h
 * @brief   This module is used to abstract result of PHOcr inside memory
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Oct 2, 2019
 *****************************************************************************/

#ifndef PHOCR_API_PHOCRDOCUMENTRESULT_H_
#define PHOCR_API_PHOCRDOCUMENTRESULT_H_

namespace phocr {

class PHOcrDocumentResult {
public:
  PHOcrDocumentResult();
  virtual ~PHOcrDocumentResult();
};

}  // namespace phocr

#endif  // PHOCR_API_PHOCRDOCUMENTRESULT_H_ //
