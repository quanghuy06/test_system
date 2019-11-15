/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrPage_GetTextResult.cpp
 * @brief
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    May 24, 2019
 *****************************************************************************/

#include "gtest/gtest.h"
#include "phocrtests/TestDataManager.h"
#include "phocrtests/TestHelper.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocr/api/PHOcrDocumentMaker.h"
#include "phocr/api/PHOcrPageMaker.h"
#include "phocr/api/PHOcrPage.h"

class PHOcrPageGetTextResultTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();
    image_path_single_page = data_manager->GetPath("01_0033.bmp");
    image_path_multi_page = data_manager->GetPath("44_01-05.tif");
    not_image_file_path = data_manager->GetPath("not_image.txt");
    white_image = data_manager->GetPath("white-image.bmp");

    image_path_single_page_ws = phocr::ConvertToWString(image_path_single_page);
    image_path_multi_page_ws = phocr::ConvertToWString(image_path_multi_page);
    not_image_file_path_ws = phocr::ConvertToWString(not_image_file_path);
    white_image_ws = phocr::ConvertToWString(white_image);
  }

 protected:
   phocr::TestDataManager* data_manager;
   std::string image_path_single_page, image_path_multi_page,
               not_image_file_path, white_image;
   std::wstring image_path_single_page_ws, image_path_multi_page_ws,
                not_image_file_path_ws, white_image_ws;
};

TEST_F(PHOcrPageGetTextResultTest, should_not_empty_when_get_from_single_page) {
  phocr::PHOcrPagePtr page = nullptr;
  phocr::PHOcrPageMaker::CreatePage(page, image_path_single_page_ws);
  std::string text_result;
  if (page.get() != nullptr) {
    ASSERT_NO_THROW(page->PHOcrGetTextResult(text_result));
  }
  ASSERT_NE(text_result, "");
}

TEST_F(PHOcrPageGetTextResultTest, should_not_empty_when_get_from_multi_page) {
  phocr::PHOcrPagePtr page = nullptr;
  phocr::PHOcrPageMaker::CreatePage(page, image_path_multi_page_ws);
  std::string text_result;
  if (page.get() != nullptr) {
    ASSERT_NO_THROW(page->PHOcrGetTextResult(text_result));
  }
  ASSERT_NE(text_result, "");
}

TEST_F(PHOcrPageGetTextResultTest, should_not_empty_when_get_from_not_image_document) {
  phocr::PHOcrPagePtr page = nullptr;
  phocr::PHOcrPageMaker::CreatePage(page, not_image_file_path_ws);
  std::string text_result;
  if (page.get() != nullptr) {
    ASSERT_NO_THROW(page->PHOcrGetTextResult(text_result));
  }
  ASSERT_EQ(text_result, "");
}

TEST_F(PHOcrPageGetTextResultTest, should_be_empty_with_white_image) {
  phocr::PHOcrPagePtr page = nullptr;
  phocr::PHOcrPageMaker::CreatePage(page, white_image_ws);
  std::string text_result;
  if (page.get() != nullptr) {
      ASSERT_NO_THROW(page->PHOcrGetTextResult(text_result));
  }
  ASSERT_EQ(text_result, "");
}
