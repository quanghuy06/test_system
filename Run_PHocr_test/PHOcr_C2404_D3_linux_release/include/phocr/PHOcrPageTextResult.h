/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrPageTextResult.h
 * @brief   This module is used to contains text result of a page
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Oct 2, 2019
 *****************************************************************************/

#ifndef PHOCR_API_PHOCRPAGETEXTRESULT_H_
#define PHOCR_API_PHOCRPAGETEXTRESULT_H_

#include <string>

namespace phocr {

class PHOcrPageTextResult {
  int page_number_;
  std::string contents_;
public:
  // Default constructor
  PHOcrPageTextResult();

  // Optional constructor
  PHOcrPageTextResult(const std::string& contents, int page_number);

  // Copy constructor
  PHOcrPageTextResult(const PHOcrPageTextResult& src);

  // Destructor
  virtual ~PHOcrPageTextResult();

  /**
   * Get the text content of this page
   * @return
   */
  const std::string& getContents() const;

  /**
   * Set text content for this page
   * @param contents
   */
  void setContents(const std::string& contents);

  /**
   * Get the page number
   * @return
   */
  int getPageNumber() const;

  /**
   * Set the page number of this page
   * @param page_number
   */
  void setPageNumber(int page_number);

  /**
   * Overloading operator=
   * @param other
   * @return
   */
  const PHOcrPageTextResult& operator=(const PHOcrPageTextResult& other);
};

}  // namespace phocr

#endif  // PHOCR_API_PHOCRPAGETEXTRESULT_H_ //
