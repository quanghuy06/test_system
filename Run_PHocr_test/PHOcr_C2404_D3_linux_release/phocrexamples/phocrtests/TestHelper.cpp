/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestHelper.cpp
 * @brief
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Mar 21, 2019
 *****************************************************************************/

#include "phocrtests/TestHelper.h"
#include <boost/filesystem.hpp>

namespace fs = boost::filesystem;

int8_t* ReadDataFromFile(std::string file_path, size_t& size) {
  std::FILE* image_fp = std::fopen(file_path.c_str(), "rb");
  std::fseek(image_fp, 0, SEEK_END);
  size_t file_size = std::ftell(image_fp);
  int8_t* file_data_not_free_by_this_area = new int8_t[file_size];
  std::fseek(image_fp, 0, SEEK_SET);
  size = std::fread(file_data_not_free_by_this_area, sizeof(int8_t),
                    file_size, image_fp);
  std::fclose(image_fp);
  return file_data_not_free_by_this_area;
}

fs::path JoinFileName(
    std::string file_name,
    std::string extension) {
  return fs::path(file_name + "." + extension);
}

bool RemoveFileIfExists(fs::path file_path) {
  if (fs::exists(file_path)) {
    return fs::remove(file_path) == 0;
  }
  return true;
}
