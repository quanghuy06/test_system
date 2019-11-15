/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestDataManager.h
 * @brief   Header file for class TessDataManager
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Mar 15, 2019
 *****************************************************************************/
#pragma once

#include <mutex>
#include <string>

namespace phocr {

/**
 * Contain API for manage the test data for unit testing
 * This class will be singleton
 */
class TestDataManager {
 public:
  /**
   * Get singleton object
   */
  static TestDataManager* Instance(std::string data_path = "");

  /**
   * This function will delete all engine to avoid memory leaks
   * Call when destroy PHOcrDocumentImpl
   * Refer to bug number 24294
   */
  static void DeleteInstance();

  //////////////////////////////////////////

  // Get absolute path which is combination of
  // relative path and data path
  std::string GetPath(std::string relative_path);

 private:
  static TestDataManager *m_Instance;
  static std::mutex m_Mutex;

  // Where contain all image and data of test case inside
  std::string m_DataPath;

  // Internal constructor
  explicit TestDataManager(std::string data_path);

  // Internal destructor
  ~TestDataManager();
};

}  // namespace phocr
