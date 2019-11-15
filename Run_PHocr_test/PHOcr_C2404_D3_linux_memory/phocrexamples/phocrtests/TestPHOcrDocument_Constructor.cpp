/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrDocument_Constructor.cpp
 * @brief   Testing for PHOcrDocument constructor
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Mar 18, 2019
 *****************************************************************************/

#include <cstdio>
#include <cstring>
#include <cstdint>
#include "gtest/gtest.h"

#include "leptonica/include/allheaders.h"
#include "phocrtests/TestDataManager.h"
#include "phocrtests/TestHelper.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrDocumentMaker.h"

class PHOcrDocumentConstructorTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();

    image_path_jpg = data_manager->GetPath("01_0033.jpg");
    jpg_path_ws = phocr::ConvertToWString(image_path_jpg);

    image_path_bmp = data_manager->GetPath("01_0033.bmp");
    bmp_path_ws = phocr::ConvertToWString(image_path_bmp);

    not_image_file_path = data_manager->GetPath("not_image.txt");
    not_image_file_path_ws = phocr::ConvertToWString(not_image_file_path);
  }

 protected:
  phocr::TestDataManager* data_manager;

  std::string image_path_jpg;
  std::wstring jpg_path_ws;

  std::string image_path_bmp;
  std::wstring bmp_path_ws;

  std::string not_image_file_path;
  std::wstring not_image_file_path_ws;
};

TEST_F(PHOcrDocumentConstructorTest, should_be_success_when_construct_empty) {
  phocr::PHOcrDocumentPtr document = nullptr;
  ASSERT_EQ(phocr::PHOcrDocumentMaker::CreateDocument(document),
            phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
}

TEST_F(PHOcrDocumentConstructorTest, should_be_success_when_construct_with_exists_image_path) {
  phocr::PHOcrDocumentPtr document = nullptr;
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, jpg_path_ws),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
}

TEST_F(PHOcrDocumentConstructorTest, should_be_fail_when_construct_with_not_exists_image_path) {
  phocr::PHOcrDocumentPtr document = nullptr;
  ASSERT_NE(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, jpg_path_ws + L"not_exists"),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document, nullptr);
}

TEST_F(PHOcrDocumentConstructorTest, should_be_fail_when_construct_with_not_valid_image_file_path) {
  phocr::PHOcrDocumentPtr document = nullptr;
  ASSERT_NE(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, not_image_file_path_ws),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document, nullptr);
}

TEST_F(PHOcrDocumentConstructorTest, should_be_success_when_construct_with_exists_image_path_and_phocr_settings) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, jpg_path_ws, settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
}

TEST_F(PHOcrDocumentConstructorTest, should_be_fail_when_construct_with_not_exists_image_path_and_phocr_settings) {
  phocr::PHOcrDocumentPtr document = nullptr;
  phocr::PHOcrSettings settings;
  ASSERT_NE(
      phocr::PHOcrDocumentMaker::CreateDocument(
          document, jpg_path_ws + L"not_exists", settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document, nullptr);
}

TEST_F(PHOcrDocumentConstructorTest, should_be_success_when_construct_from_JPG_compressed_image_data) {
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path_jpg, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(document,
          reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size)),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;
}

TEST_F(PHOcrDocumentConstructorTest, should_be_success_when_construct_from_JPG_compressed_image_data_and_PHOcrSettings) {
  phocr::PHOcrSettings settings;
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(image_path_bmp, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_EQ(
      phocr::PHOcrDocumentMaker::CreateDocument(document,
          reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size),
          settings),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_NE(document, nullptr);
  delete[] file_data;
}

TEST_F(PHOcrDocumentConstructorTest, should_be_fail_when_construct_from_data_which_is_not_image) {
  phocr::PHOcrDocumentPtr document = nullptr;
  // Read from file
  size_t file_size;
  int8_t* file_data = ReadDataFromFile(not_image_file_path, file_size);
  ASSERT_NE(file_data, nullptr);
  ASSERT_NE(
      phocr::PHOcrDocumentMaker::CreateDocument(document,
          reinterpret_cast<const unsigned char*>(file_data),
          static_cast<int>(file_size)),
      phocr::PHOcrStatus::PHOCR_OK);
  ASSERT_EQ(document, nullptr);
  delete[] file_data;
}
