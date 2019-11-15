/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrParagraphData.h
 * @brief   Interface of PHOcrParagraphData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <memory>
#include <vector>
#include <string>
#include "PHOcrDefines.h"
#include "PHOcrEnum.h"
#include "PHOcrLineData.h"
#include "PHOcrListInfo.h"

namespace phocr {

using phocr::PHOcrListType;
using phocr::PHOcrTextAlignment;

class PHOcrParagraphData;
typedef std::shared_ptr<PHOcrParagraphData> PHOcrParagraphDataPtr;

class PHOCR_API PHOcrParagraphData : public PHOcrElementData {
 private:
  std::string lang_;
  std::string direction_;

  // Text alignment for this
  PHOcrTextAlignment alignment_;

  // Lines inside paragraph
  std::vector<PHOcrLineDataPtr> lines_;

  // List information
  PHOcrListInfo list_info_;

  // Indentation in pixel count
  int left_indent_;
  int right_indent_;
  int first_line_indent_;

  int right_padding_;

 public:
  PHOcrParagraphData();

  // Deep copy
  PHOcrParagraphData(const PHOcrParagraphData& src);

  explicit PHOcrParagraphData(PHOcrElementDataPtr element);

  virtual ~PHOcrParagraphData();

  const std::string& GetLang();

  void SetLang(const std::string& lang);

  const std::string& GetDirection();

  void SetDirection(const std::string& direction);

  const std::vector<PHOcrLineDataPtr>& GetLines();

  void SetLines(const std::vector<PHOcrLineDataPtr>& lines);

  PHOcrTextAlignment GetAlignment();

  void SetAlignment(PHOcrTextAlignment alignment);

  int GetFirstLineIndent();

  void SetFirstLineIndent(int firstLineIndent);

  int GetLeftIndent();

  void SetLeftIndent(int leftIndent);

  int GetRightIndent();

  void SetRightIndent(int rightIndent);

  int GetRightPadding();

  void SetRightPadding(int rightPadding);

  const PHOcrListInfo& GetListInfo() const;

  void SetListInfo(const PHOcrListInfo& info);
};

}  // namespace phocr
