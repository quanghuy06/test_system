/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrStringHelper.cpp
 * @brief   Helper interface for converting between string and wstring
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    2018-12-19
 *****************************************************************************/

#pragma once

#include <string>
#include <iostream>
#include <vector>
#include "PHOcrDefines.h"

namespace phocr {

// Convert the wstring to string
// If false, return empty string
std::string PHOCR_API ConvertToString(const std::wstring& wstr);

// Convert from string to wstring
// If false, return empty wstring
std::wstring PHOCR_API ConvertToWString(const std::string& str);

}  // namespace phocr
