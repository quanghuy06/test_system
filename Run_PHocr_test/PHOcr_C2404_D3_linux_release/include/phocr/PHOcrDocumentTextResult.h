/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrDocumentTextResult.h
 * @brief   This module is used to show text result of a document
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Oct 2, 2019
 *****************************************************************************/

#ifndef PHOCR_API_PHOCRDOCUMENTTEXTRESULT_H_
#define PHOCR_API_PHOCRDOCUMENTTEXTRESULT_H_

#include <vector>
#include <string>
#include <memory>
#include "PHOcrDocumentResult.h"
#include "PHOcrPageTextResult.h"

namespace phocr {

class PHOcrDocumentTextResult : public PHOcrDocumentResult {
  std::vector<PHOcrPageTextResult> pages_result_;

 public:
  // Default constructor
  PHOcrDocumentTextResult();

  // Destructor
  virtual ~PHOcrDocumentTextResult();

  /**
   * Get the pages result out
   * @return
   */
  const std::vector<PHOcrPageTextResult>& getPagesResult() const;

  /**
   * Set list of page result for the document
   * @param pages_result
   */
  void setPagesResult(std::vector<PHOcrPageTextResult>& pages_result);

  /**
   * Insert a page result to the document result
   * @param page_result Text content of a page
   */
  void InsertPageResult(const PHOcrPageTextResult& page_result);
};

using PHOcrDocumentTextResultPtr = std::shared_ptr<PHOcrDocumentTextResult>;

}  // namespace phocr

#endif  // PHOCR_API_PHOCRDOCUMENTTEXTRESULT_H_ //
