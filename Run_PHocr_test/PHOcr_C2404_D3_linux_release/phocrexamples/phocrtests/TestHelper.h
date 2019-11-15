/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestHelper.h
 * @brief
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Mar 21, 2019
 *****************************************************************************/
#pragma once
#include <cstdio>
#include <cstring>
#include <cstdint>
#include <string>
#include <boost/filesystem.hpp>

namespace fs = boost::filesystem;

int8_t* ReadDataFromFile(std::string file_path, size_t& size);

bool RemoveFileIfExists(fs::path file_path);

fs::path JoinFileName(
    std::string file_name,
    std::string extension);
