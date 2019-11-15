/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrPageData_GetPageContent.cpp
 * @brief   Testing for Get page data structure
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Jul 23, 2019
 *****************************************************************************/

#include <array>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <string>
#include "gtest/gtest.h"

#include "leptonica/include/allheaders.h"
#include "phocr/api/PHOcrCareaData.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrDocumentMaker.h"
#include "phocr/api/PHOcrEnum.h"
#include "phocr/api/PHOcrPageData.h"
#include "phocr/api/PHOcrSettings.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocrtests/TestDataManager.h"
#include "phocrtests/TestHelper.h"

class PHOcrPageDataTest : public ::testing::Test {
 public:
  void SetUp() override {
    data_manager = phocr::TestDataManager::Instance();

    std::string contain_only_text_path =
        data_manager->GetPath("A_12895_English_Page0009.tif");
    std::string contain_barcode_path =
        data_manager->GetPath("16_Invoice_Barcode_CODE39_NoHRT.jpg");
    std::string contain_table_path = data_manager->GetPath("39_OCR_Excel1.jpg");
    std::string contain_photo_path =
        data_manager->GetPath("A_12912_English_Page0026_color_200dpi.tif");
    std::string only_photo_path = data_manager->GetPath("flower.jpg");
    std::string no_photo_path =
        data_manager->GetPath("A_10010_Danish_Page0011.jpg");

    only_text_image_wstring = phocr::ConvertToWString(contain_only_text_path);
    contain_barcode_path_wstring =
        phocr::ConvertToWString(contain_barcode_path);
    contain_table_wstring = phocr::ConvertToWString(contain_table_path);
    contain_photo_wstring = phocr::ConvertToWString(contain_photo_path);
    only_photo_wstring = phocr::ConvertToWString(only_photo_path);
    no_photo_wstring = phocr::ConvertToWString(no_photo_path);
  }

 protected:
  phocr::TestDataManager* data_manager;

  // Images path
  std::wstring only_text_image_wstring;
  std::wstring contain_barcode_path_wstring;
  std::wstring contain_table_wstring;
  std::wstring contain_photo_wstring;
  std::wstring only_photo_wstring;
  std::wstring no_photo_wstring;

  // PHOcr Document and Data elements
  phocr::PHOcrPageDataPtr page_data;
  std::vector<phocr::PHOcrBarcodeDataPtr> barcode_data;
  std::vector<phocr::PHOcrCareaDataPtr> carea_data;
  std::vector<phocr::PHOcrPhotoDataPtr> photo_data;
  std::vector<phocr::PHOcrTableDataPtr> table_data;
  std::vector<phocr::PHOcrRowDataPtr> row_data;
  std::vector<phocr::PHOcrCellDataPtr> cell_data;
  std::vector<phocr::PHOcrParagraphDataPtr> paragraph_data;
  std::vector<phocr::PHOcrLineDataPtr> line_data;
  std::vector<phocr::PHOcrWordDataPtr> word_data;
  std::vector<phocr::PHOcrCharacterDataPtr> character_data;

  void SetUpPageData(std::wstring image_path,
                     std::wstring language = L"english",
                     bool get_all_barcode = false) {
    phocr::PHOcrDocumentPtr document;
    phocr::PHOcrSettings setting;
    setting.SetOCRLanguage(language);
    setting.SetDataMode(phocr::PHOcrDataMode::DM_HIGH_CONTENT);
    phocr::PHOcrDocumentMaker::CreateDocument(document, image_path, setting);
    phocr::PHOcrPagePtr page = document->PHOcrGetPage(0);

    std::vector<std::wstring> all_barcode;
    if (get_all_barcode) {  // Some time user don't need to get barcode
      page->PHOcrGetAllBarcodes(all_barcode);
    }

    page->PHOcrGetPageDataStruct(page_data);

    barcode_data = page_data->GetBarcodes();
    photo_data = page_data->GetPhotos();
    table_data = page_data->GetTables();
    carea_data = page_data->GetCareas();

    if (carea_data.size()) paragraph_data = carea_data[0]->GetParagraph();

    if (paragraph_data.size()) line_data = paragraph_data[0]->GetLines();

    if (line_data.size()) word_data = line_data[0]->GetWords();

    if (word_data.size()) character_data = word_data[0]->GetCharacters();

    if (table_data.size()) row_data = table_data[0]->GetRows();

    if (row_data.size()) cell_data = row_data[0]->GetCells();
  }
};

/**
 * Testing for get data structure a page in document
 */
TEST_F(PHOcrPageDataTest,
       should_be_success_when_get_structure_page_data_successfully) {
  phocr::PHOcrDocumentPtr document;
  phocr::PHOcrSettings setting;
  setting.SetOCRLanguage(L"english");
  setting.SetDataMode(phocr::PHOcrDataMode::DM_HIGH_CONTENT);
  phocr::PHOcrDocumentMaker::CreateDocument(document, only_text_image_wstring,
                                            setting);
  // This test case has only one page
  phocr::PHOcrPagePtr page = document->PHOcrGetPage(0);
  page->PHOcrGetPageDataStruct(page_data);
  ASSERT_NE(page_data, nullptr);
}

/**
 * Testing for get barcodes function with test case which have no barcodes
 * with GetAllBarcode function is called
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_dont_have_barcodes) {
  SetUpPageData(only_text_image_wstring, L"english", true);
  std::vector<phocr::PHOcrBarcodeDataPtr> barcodes;
  barcodes = page_data->GetBarcodes();
  ASSERT_EQ(barcodes.size(), 0);
}

/**
 * Test get barcodes function with test case which have barcodes
 * with GetAllBarcode function is called
 */
TEST_F(PHOcrPageDataTest,
       should_be_have_barcode_when_PHOcrGetAllBarcodes_is_called) {
  SetUpPageData(contain_barcode_path_wstring, L"english", true);
  std::vector<phocr::PHOcrBarcodeDataPtr> barcodes;
  barcodes = page_data->GetBarcodes();
  ASSERT_NE(barcodes.size(), 0);
}

/**
 * Testing for get barcodes function with test case which have no barcodes
 * with GetAllBarcode function is not called
 */
TEST_F(PHOcrPageDataTest,
       should_be_no_barcode_when_PHOcrGetAllBarcodes_is_not_called) {
  SetUpPageData(contain_barcode_path_wstring);
  std::vector<phocr::PHOcrBarcodeDataPtr> barcodes;
  barcodes = page_data->GetBarcodes();
  ASSERT_EQ(barcodes.size(), 0);
}

/**
 * Test get photos function in case there are no photo
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_dont_have_photo) {
  SetUpPageData(no_photo_wstring, L"danish");
  std::vector<phocr::PHOcrPhotoDataPtr> photos;
  photos = page_data->GetPhotos();
  ASSERT_EQ(photos.size(), 0);
}

/**
 * Test get photos function in case there are photo
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_have_photo) {
  SetUpPageData(contain_photo_wstring, L"dutch");
  std::vector<phocr::PHOcrPhotoDataPtr> photos;
  photos = page_data->GetPhotos();
  ASSERT_NE(photos.size(), 0);
}

/**
 * Testing for get some attribute for photo
 * such as: x, y, width, height, etc.
 * We must export to xml file first (for reference)
 */
TEST_F(PHOcrPageDataTest,
       should_be_success_when_attribute_of_photo_same_like_xml_file) {
  SetUpPageData(contain_photo_wstring, L"dutch");
  phocr::PHOcrPhotoDataPtr photo;
  photo = page_data->GetPhotos()[0];
  ASSERT_EQ(photo->GetX(), 1077);
  ASSERT_EQ(photo->GetY(), 198);
  ASSERT_EQ(photo->GetH(), 84);
  ASSERT_EQ(photo->GetW(), 84);
  ASSERT_EQ(photo->IsInsideTable(), false);
}

/**
 * Test get table function in case there are no table
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_dont_have_table) {
  SetUpPageData(only_text_image_wstring);
  std::vector<phocr::PHOcrTableDataPtr> tables;
  tables = page_data->GetTables();
  ASSERT_EQ(tables.size(), 0);
}

/**
 * Test get table function with test case which have table
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_have_table) {
  SetUpPageData(contain_table_wstring);
  std::vector<phocr::PHOcrTableDataPtr> tables;
  tables = page_data->GetTables();
  ASSERT_NE(tables.size(), 0);
}

/**
 * Testing for get some attribute for table
 * such as: x, y, width, height, etc.
 * We must export to xml file first (for reference)
 */
TEST_F(PHOcrPageDataTest,
       should_be_success_when_attribute_of_table_same_like_xml_file) {
  SetUpPageData(contain_table_wstring);
  auto table = table_data[0];
  ASSERT_NE(table, nullptr);
}

/**
 * Testing for get some attribute for row
 * such as: x, y, width, height, etc.
 * We must export to xml file first (for reference)
 */
TEST_F(PHOcrPageDataTest,
       should_be_success_when_attribute_of_row_same_like_xml_file) {
  SetUpPageData(contain_table_wstring);
  auto row = row_data[0];
  ASSERT_NE(row, nullptr);
}

/**
 * Testing for get some attribute for cell
 * such as: x, y, width, height, etc.
 * We must export to xml file first (for reference)
 */
TEST_F(PHOcrPageDataTest,
       should_be_success_when_attribute_of_cell_same_like_xml_file) {
  SetUpPageData(contain_table_wstring);
  auto cell = cell_data[0];
  ASSERT_NE(cell, nullptr);
}

/**
 * Test get carea function in case there are no carea
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_dont_have_carea) {
  SetUpPageData(only_photo_wstring);
  std::vector<phocr::PHOcrCareaDataPtr> careas;
  careas = page_data->GetCareas();
  ASSERT_EQ(careas.size(), 0);
}

/**
 * Test get carea function in case there are carea
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_have_carea) {
  SetUpPageData(only_text_image_wstring);
  std::vector<phocr::PHOcrCareaDataPtr> careas;
  careas = page_data->GetCareas();
  ASSERT_NE(careas.size(), 0);
}

/**
 * Testing for get some attribute for carea
 * such as: x, y, width, height, etc.
 * We must export to xml file first (for reference).
 */
TEST_F(PHOcrPageDataTest,
       should_be_success_when_attribute_of_carea_same_like_xml_file) {
  SetUpPageData(contain_photo_wstring);
  auto carea = carea_data[0];
  ASSERT_EQ(carea->GetX(), 114);
  ASSERT_EQ(carea->GetY(), 196);
  ASSERT_EQ(carea->GetW(), 1286);
  ASSERT_EQ(carea->GetH(), 114);
  ASSERT_EQ(carea->GetPageDirection(), phocr::PHOcrPageDirection::HORIZONTAL);
  ASSERT_EQ(carea->GetLineDirection(),
            phocr::PHOcrLineDirection::TOP_TO_BOTTOM);
}

/**
 * Test get paragraph function in case there are paragraph
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_have_paragraph) {
  SetUpPageData(only_text_image_wstring);
  ASSERT_NE(paragraph_data.size(), 0);
}

/**
 * Testing for get some attribute for paragraph
 * such as: x, y, width, height, etc.
 * We must export to xml file first (for reference).
 */
TEST_F(PHOcrPageDataTest,
       should_be_success_when_attribute_of_paragraph_same_like_xml_file) {
  SetUpPageData(contain_photo_wstring);
  auto paragraph = paragraph_data[0];
  ASSERT_EQ(paragraph->GetX(), 114);
  ASSERT_EQ(paragraph->GetY(), 196);
  ASSERT_EQ(paragraph->GetW(), 1285);
  ASSERT_EQ(paragraph->GetH(), 113);
  ASSERT_EQ(paragraph->GetLang(), "eng");
}

/**
 * Test get paragraph function in case there are no paragraph
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_dont_have_paragraph) {
  SetUpPageData(only_photo_wstring);
  ASSERT_EQ(paragraph_data.size(), 0);
}

/**
 * Test get line function in case there are line
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_have_line) {
  SetUpPageData(only_text_image_wstring);
  std::array<std::string, 37> lst_line = {
      "ment",    "started",       "intense",    "propaganda",
      "against", "Shias",         "and",        "named",
      "all",     "the",           "protesters", "‘national",
      "trai-",   "tors.’",        "After",      "the",
      "GCC",     "intervention,", "the",        "monarchy",
      "quickly", "repressed",     "dissent.",   "Meanwhile,",
      "the",     "Emir",          "promised",   "reforms,",
      "but",     "has",           "yet",        "failed",
      "to",      "deliver",       "them",       "(Ismail",
      "2013)."};
  ASSERT_EQ(line_data.size(), 3);
  int count = 0;
  for (auto& line : line_data) {
    for (auto& word : line->GetWords()) {
      ASSERT_EQ(word->GetValue(), lst_line[count++]);
    }
  }
}

/**
 * Testing for get some attribute for line
 * such as: x, y, width, height, etc.
 * We must export to xml file first (for reference).
 */
TEST_F(PHOcrPageDataTest,
       should_be_success_when_attribute_of_line_same_like_xml_file) {
  SetUpPageData(contain_photo_wstring);
  auto line = line_data[0];
  ASSERT_EQ(line->GetX(), 114);
  ASSERT_EQ(line->GetY(), 196);
  ASSERT_EQ(line->GetW(), 1284);
  ASSERT_EQ(line->GetH(), 112);
  ASSERT_EQ(line->GetTextAngle(), -1);
}

/**
 * Test get line function in case there are no line
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_dont_have_line) {
  SetUpPageData(only_photo_wstring);
  ASSERT_EQ(line_data.size(), 0);
}

/**
 * Test get word function in case there are word
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_have_word) {
  SetUpPageData(only_text_image_wstring);
  std::array<std::string, 13> lst_str = {
      "ment",  "started", "intense", "propaganda", "against",   "Shias", "and",
      "named", "all",     "the",     "protesters", "‘national", "trai-"};
  int count = 0;
  ASSERT_EQ(word_data.size(), lst_str.size());
  for (auto word : word_data) {
    ASSERT_EQ(word->GetValue(), lst_str[count++]);
  }
}

/**
 * Testing for get some attribute for word
 * such as: x, y, width, height, etc.
 * We must export to xml file first (for reference).
 */
TEST_F(PHOcrPageDataTest,
       should_be_success_when_attribute_of_word_same_like_xml_file) {
  SetUpPageData(contain_photo_wstring);
  auto word = word_data[0];
  ASSERT_EQ(word->GetX(), 114);
  ASSERT_EQ(word->GetY(), 196);
  ASSERT_EQ(word->GetW(), 379);
  ASSERT_EQ(word->GetH(), 111);
  ASSERT_EQ(word->GetSpaceBefore(), 0);
}

/**
 * Test get word function in case there are no word
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_dont_have_word) {
  SetUpPageData(only_photo_wstring);
  ASSERT_EQ(word_data.size(), 0);
}

/**
 * Test get character function in case there are character
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_have_character) {
  SetUpPageData(only_text_image_wstring);
  std::array<std::string, 4> lst_char = {"m", "e", "n", "t"};
  int count = 0;
  ASSERT_EQ(character_data.size(), lst_char.size());
  for (auto cha_r : character_data) {
    ASSERT_EQ(cha_r->GetValue(), lst_char[count++]);
  }
}

/**
 * Testing for get some attribute for character
 * such as: x, y, width, height, etc.
 * We must export to xml file first (for reference).
 */
TEST_F(PHOcrPageDataTest,
       should_be_success_when_attribute_of_character_same_like_xml_file) {
  SetUpPageData(contain_photo_wstring);
  auto character = character_data[0];
  ASSERT_EQ(character->GetX(), 114);
  ASSERT_EQ(character->GetY(), 202);
  EXPECT_FLOAT_EQ(character->GetConfidence(), 67.6663);
}

/**
 * Test get character function in case there are no character
 */
TEST_F(PHOcrPageDataTest, should_be_success_when_dont_have_character) {
  SetUpPageData(only_photo_wstring);
  ASSERT_EQ(character_data.size(), 0);
}
