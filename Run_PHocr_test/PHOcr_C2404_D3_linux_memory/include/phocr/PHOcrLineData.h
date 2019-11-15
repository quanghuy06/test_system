/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrLineData.h
 * @brief   Interface of PHOcrLineData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <memory>
#include <vector>
#include "PHOcrDefines.h"
#include "PHOcrWordData.h"
#include "PHOcrListInfo.h"

namespace phocr {

class PHOcrLineData;
typedef std::shared_ptr<PHOcrLineData> PHOcrLineDataPtr;

class PHOCR_API PHOcrLineData : public PHOcrElementData {
 private:
  int text_angle_;
  double baseline_;
  int x_height_;
  float x_size_;
  float x_descenders_;
  float x_ascenders_;
  std::vector<PHOcrWordDataPtr> words_;
  PHOcrListInfo list_info_;

 public:
  PHOcrLineData();

  // Deep copy
  PHOcrLineData(const PHOcrLineData& src);

  explicit PHOcrLineData(PHOcrElementDataPtr element);

  virtual ~PHOcrLineData();

  int GetTextAngle();

  void SetTextAngle(int text_angle);

  double GetBaseline();

  void SetBaseline(double baseline);

  int GetXHeight();

  void SetXHeight(int x_height);

  float GetSize();

  void SetSize(float x_size);

  float GetDescenders();

  void SetDescenders(float x_descenders);

  float GetAscenders();

  void SetAscenders(float x_ascenders);

  const std::vector<PHOcrWordDataPtr>& GetWords();

  void SetWords(const std::vector<PHOcrWordDataPtr>& words);

  const PHOcrListInfo& GetListInfo() const;

  void SetListInfo(const PHOcrListInfo& info);
};

}  // namespace phocr
