/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrElementData.h
 * @brief   Interface of PHOcrElementData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <memory>
#include <string>
#include "PHOcrDefines.h"
#include "PHOcrEnum.h"

namespace phocr {

using phocr::PHOcrLineDirection;
using phocr::PHOcrPageDirection;

class PHOcrElementData;
typedef std::shared_ptr<PHOcrElementData> PHOcrElementDataPtr;

class PHOCR_API PHOcrElementData {
 private:
  int id_;
  int x_;
  int y_;
  int w_;
  int h_;
  bool is_noise_;

  // Direction
  PHOcrPageDirection page_dir_;
  PHOcrLineDirection line_dir_;

 protected:
  bool have_color_;
  bool have_highlight_color_;
  unsigned int color_;
  unsigned int highlight_color_;
  const char* working_directory_;

 public:
  PHOcrElementData();

  // Deep copy
  PHOcrElementData(const PHOcrElementData& src);

  explicit PHOcrElementData(PHOcrElementDataPtr src);

  virtual ~PHOcrElementData();

  int GetId();

  void SetId(int id);

  virtual int GetX();

  virtual void SetX(int x);

  virtual int GetY();

  virtual void SetY(int y);

  virtual int GetW();

  virtual void SetW(int w);

  virtual int GetH();

  virtual void SetH(int h);

  bool IsNoise();

  void SetNoise(bool is_noise);

  PHOcrPageDirection GetPageDirection();

  void SetPageDirection(const PHOcrPageDirection& page_dir);

  PHOcrLineDirection GetLineDirection();

  void SetLineDireciton(const PHOcrLineDirection& line_dir);

  bool IsHaveColor();

  void SetHaveColor(bool have_color);

  bool IsHaveHighlightColor();

  void SetIsHaveHighlightColor(bool have_highlight_color);

  unsigned int GetColor();

  void SetColor(unsigned int color);

  unsigned int GetHighlightColor();

  void SetHighlightColor(unsigned int highlight_color);

  const char* GetWorkingDirectory() const;

  void SetWorkingDirectory(const char* working_directory);
};

}  // namespace phocr
