/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrPageInfoData.h
 * @brief   Interface of PHOcrPageInfoData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <string>
#include <memory>
#include "PHOcrDefines.h"
#include "PHOcrEnum.h"
#include "PHOcrDPI.h"

namespace phocr {

using phocr::PHOcrOrientation;
using phocr::PHOcrTextlineOrder;
using phocr::PHOcrWritingDirection;
class PHOcrPageInfoData;
typedef std::shared_ptr<PHOcrPageInfoData> PHOcrPageInfoDataPtr;

class PHOCR_API PHOcrPageInfoData {
 private:
  std::string title_;             // input image path
  double margin_left_;            // margin left of the page (inches)
  double margin_right_;           // margin right of the page (inches)
  double margin_top_;             // margin top of the page (inches)
  double margin_bottom_;          // margin bottom of the page (inches)
  int baseline_;                  // Common base line
  int x_height_;                  // Common x height
  PHOcrDPI dpi_;                  // Page resolution
  float deskew_angle_;            // deskew angle
  PHOcrOrientation orientation_;  // Orientation
  PHOcrWritingDirection writing_direction_;  // Writing direction of page
  PHOcrTextlineOrder textline_order_;        // Text line order in page
  std::string language_;                     // Language of this page
  int width_;                                // Width of page
  int height_;                               // Height of page
  std::string paper_size_;                   // Standard paper size of this page
  std::string paper_orientation_;  // Paper orientation (landscape/portrait)
  double paper_width_;             // Width of paper size (Inch unit)
  double paper_height_;            // Height of paper size (Inch unit)
  unsigned int page_number_;       // Identify the page number of this page

 public:
  PHOcrPageInfoData();

  // Deep copy constructor
  PHOcrPageInfoData(const PHOcrPageInfoData& src);

  ~PHOcrPageInfoData();

  int GetBaseline();

  void SetBaseline(int baseline);

  float GetDeskewAngle();

  void SetDeskewAngle(float deskewAngle);

  const PHOcrDPI& GetDpi() const;

  void SetDpi(const PHOcrDPI& dpi);

  int GetHeight();

  void SetHeight(int height);

  int GetWidth();

  void SetWidth(int width);

  const std::string& GetLanguage() const;

  void SetLanguage(const std::string& language);

  double GetMarginBottom();

  void SetMarginBottom(double marginBottom);

  double GetMarginLeft();

  void SetMarginLeft(double marginLeft);

  double GetMarginRight();

  void SetMarginRight(double marginRight);

  double GetMarginTop();

  void SetMarginTop(double marginTop);

  PHOcrOrientation GetOrientation() const;

  void SetOrientation(PHOcrOrientation orientation);

  double GetPaperHeight();

  void SetPaperHeight(double paperHeight);

  const std::string& GetPaperOrientation() const;

  void SetPaperOrientation(const std::string& paperOrientation);

  const std::string& GetPaperSize() const;

  void SetPaperSize(const std::string& paperSize);

  double GetPaperWidth();

  void SetPaperWidth(double paperWidth);

  PHOcrTextlineOrder GetTextlineOrder() const;

  void SetTextlineOrder(PHOcrTextlineOrder textlineOrder);

  const std::string& GetTitle() const;

  void SetTitle(const std::string& title);

  PHOcrWritingDirection GetWritingDirection() const;

  void SetWritingDirection(PHOcrWritingDirection writingDirection);

  unsigned int GetPageNumber() const;

  void SetPageNumber(unsigned int page_number);
};

}  // namespace phocr
