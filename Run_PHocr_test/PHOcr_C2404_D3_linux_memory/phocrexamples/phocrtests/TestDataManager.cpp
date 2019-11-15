/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestDataManager.cpp
 * @brief   Source file for class TessDataManager
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Mar 15, 2019
 *****************************************************************************/

#include "phocrtests/TestDataManager.h"
#include <string>
#include <boost/filesystem.hpp>

namespace phocr {

std::mutex TestDataManager::m_Mutex;
TestDataManager* TestDataManager::m_Instance = nullptr;

TestDataManager::TestDataManager(std::string data_path) {
  m_DataPath = data_path;
}

TestDataManager::~TestDataManager() {
}

////////////////////////////// STATIC FUNCTION
TestDataManager* TestDataManager::Instance(std::string data_path) {
  if (!m_Instance && data_path != "") {
    std::lock_guard<std::mutex> lock(TestDataManager::m_Mutex);
    m_Instance = new TestDataManager(data_path);
  }
  return m_Instance;
}

void TestDataManager::DeleteInstance() {
  if (m_Instance) {
    std::lock_guard<std::mutex> lock(TestDataManager::m_Mutex);
    delete m_Instance;
  }
}

////////////////////////////// NON-STATIC FUNCTION

std::string TestDataManager::GetPath(std::string relative_path) {
  namespace fs = boost::filesystem;
  return (fs::path(m_DataPath) / fs::path(relative_path)).string();
}

}  // namespace phocr
