/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrWordData.h
 * @brief   Interface of PHOcrWordData
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 21, 2019
 *****************************************************************************/

#pragma once

#include <memory>
#include <string>
#include <vector>
#include "PHOcrCharacterData.h"
#include "PHOcrDefines.h"

namespace phocr {

class PHOcrWordData;
typedef std::shared_ptr<PHOcrWordData> PHOcrWordDataPtr;

class PHOCR_API PHOcrWordData : public PHOcrElementData {
 private:
  float x_fsize_;
  // Space before which should set to output
  // Only for non justify paragraph
  int space_before_;
  float x_wconf_;
  bool is_numeric_;
  bool bold_;
  bool italic_;
  bool underline_;
  bool monospace_;
  bool serif_;
  bool smallcaps_;
  std::string lang_;
  std::string value_;
  std::string x_font_;
  std::string direction_;
  std::vector<PHOcrCharacterDataPtr> characters_;

 public:
  PHOcrWordData();

  // Deep copy
  PHOcrWordData(const PHOcrWordData& src);

  explicit PHOcrWordData(PHOcrElementDataPtr element);

  virtual ~PHOcrWordData();

  bool IsNumeric();

  void SetNumeric(bool numeric);

  bool IsBold();

  void SetBold(bool bold);

  bool IsItalic();

  void SetItalic(bool italic);

  bool IsUnderline();

  void SetUnderLine(bool underline);

  bool IsMonospace();

  void SetMonospace(bool monospace);

  bool IsSerif();

  void SetSerif(bool serif);

  bool IsSmallcaps();

  void SetSmallcaps(bool smallcaps);

  const std::vector<PHOcrCharacterDataPtr>& GetCharacters() const;

  void SetCharacters(const std::vector<PHOcrCharacterDataPtr>& characters);

  const std::string& GetDirection() const;

  void SetDirection(const std::string& direction);

  const std::string& GetLang() const;

  void SetLang(const std::string& lang);

  const std::string& GetValue() const;

  void SetValue(const std::string& value);

  const std::string& GetFont() const;

  void SetFont(const std::string& font);

  float GetFsize();

  void SetSize(float fsize);

  float GetWconf();

  void SetWconf(float wconf);

  int GetSpaceBefore();

  void SetSpaceBefore(int space_before);
};

}  // namespace phocr
