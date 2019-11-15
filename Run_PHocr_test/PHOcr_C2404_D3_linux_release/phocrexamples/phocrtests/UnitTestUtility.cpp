/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    UnitTestUtility.cpp
 * @brief
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    May 20, 2019
 *****************************************************************************/
#include "phocrtests/UnitTestUtility.h"
#include <sys/stat.h>
#include <cstdio>
#include <fstream>
#include <vector>
#include <cstdlib>
#include <exception>
#include <boost/filesystem.hpp>

namespace fs = boost::filesystem;

UnitTestUtility::UnitTestUtility() {
}

UnitTestUtility::~UnitTestUtility() {
}

std::string UnitTestUtility::GetCurrentPath() {
  return fs::current_path().string();
}

bool UnitTestUtility::IsExistingFile(std::string file_path) {
  struct stat buffer;
  return (stat(file_path.c_str(), &buffer) == 0);
}

void UnitTestUtility::DeleteFile(std::string file_path) {
  if (file_path.empty()) {
    return;
  }
  if (IsExistingFile(file_path)) {
    int result = remove(file_path.c_str());
    if (result != 0) {
      throw std::logic_error("Failed to delete " + file_path);
    }
  }
}

void UnitTestUtility::DeletePossiblePHOcrOutputFile() {
  std::vector<std::string> possible_file_extesion = {
      "*.txt",
      "*.xml",
      "*.jpeg",
      "*.docx",
      "*.xlsx",
      "*.pptx",
      "*.pdf",
      "*.json",
  };
  std::string command("rm ");  // use rm command to remove file
  for (const auto& ext : possible_file_extesion) {
    command += ext + " ";
  }
  command += "2> /dev/null";  // suppress output of command
  std::system(command.c_str());
}

std::wstring UnitTestUtility::GetFilenameFromFilepath(std::wstring file_path) {
  std::wstring file_name;
  for (int i = file_path.size() -1; i >= 0; --i) {
    if (file_path[i] == '/') {
      file_name = file_path.substr(i + 1, file_path.size() - i);
      break;
    }
  }
  return file_name;
}

std::string UnitTestUtility::ReadContent(std::string file_path) {
  std::ifstream file(file_path);
  std::string content(
      (std::istreambuf_iterator<char>(file)),
      (std::istreambuf_iterator<char>()));
  file.close();
  return content;
}

std::string UnitTestUtility::GetCurrentPathToFileName(std::string file_name) {
  fs::path file_path = fs::current_path() / fs::path(file_name);
  return file_path.string();
}

bool UnitTestUtility::CreateNewDirectory(const std::string& path) {
  if (!fs::portable_directory_name(path)) {
    return false;
  }

  // Check if folder exist
  fs::path new_directory(path);
  try {
    if (fs::exists(new_directory)) {
      fs::remove_all(new_directory);
    }
    fs::create_directory(new_directory);
  } catch (...) {
    return false;
  }
  return true;
}

void UnitTestUtility::DeleteDirectoryRecursive(const std::string& path) {
  fs::path targer_path(path);
  if (fs::exists(targer_path)) {
    fs::remove_all(targer_path);
  }
}

int UnitTestUtility::GetFileSize(const std::string& file_path) {
  std::ifstream input_file(
      file_path, std::ifstream::ate | std::ifstream::binary);
  if (!input_file) {
    return -1;
  } else {
    return input_file.tellg();
  }
}
