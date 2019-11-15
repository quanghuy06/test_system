/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrListInfo.h
 * @brief   This module is used to
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Sep 17, 2019
 *****************************************************************************/

#ifndef PHOCR_API_PHOCRLISTINFO_H_
#define PHOCR_API_PHOCRLISTINFO_H_

#include <string>
#include "PHOcrEnum.h"
#include "PHOcrDefines.h"

namespace phocr {
/**
 * Present information about list and numbering from PHOcr
 */
class PHOCR_API PHOcrListInfo {
  bool  is_list_;             // is list or not
  PHOcrListType  list_type_;  // bullet or numbering
  std::string  list_name_;    // name of bullet and numbering
  int  list_level_;           // level of numbering or bullets
  int  start_value_;          // start value of numbering

 public:
  PHOcrListInfo();

  PHOcrListInfo(
      bool is_list, PHOcrListType list_type, const std::string& list_name,
      int list_level, int start_value);

  PHOcrListInfo(const PHOcrListInfo& src);

  ~PHOcrListInfo();

  bool isList() const;

  void setIsList(bool is_list);

  int getListLevel() const;

  void setListLevel(int list_level);

  const std::string& getListName() const;

  void setListName(const std::string& list_name);

  PHOcrListType getListType() const;

  void setListType(PHOcrListType list_type);

  int getStartValue() const;

  void setStartValue(int start_value);
};

}  // namespace phocr

#endif  // PHOCR_API_PHOCRLISTINFO_H_ //
