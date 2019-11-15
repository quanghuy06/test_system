/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestBarcode_BarcodeMode.cpp
 * @brief   Unit test of SetBarcodeMode API
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    2019-05-28
 *****************************************************************************/

#include <string>
#include <cstdio>
#include <vector>
#include <unordered_map>
#include "TestDataManager.h"
#include "phocr/api/PHOcrStringHelper.h"
#include "phocr/api/PHOcrEnum.h"
#include "phocr/api/PHOcrDocumentMaker.h"
#include "gtest/gtest.h"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>


using namespace phocr;
namespace pt = boost::property_tree;
/**
 * A test class used to testing API SetBarcodeMode in PHOcrSetting class
 */
class BarcodeModeSettingTest : public ::testing::Test {
 protected:
  // Manage test case
  TestDataManager* data_manager_;

  // Path to an image contains all types of barcode that PHOcr support, both 1D
  // and 2D too
  std::wstring all_barcode_image_path_;

  // PHOcrDocument
  PHOcrDocumentPtr document_;

  // PHOcrSetting
  PHOcrSettings setting_;

  // Output file
  std::wstring output_file_ = L"output";

  // Store barcode formar result
  std::vector<std::string> barcode_format_results_;

  static const std::unordered_map<std::string, unsigned int>
  barcode_mode_mapper_;

 public:
  // Default constructor
  BarcodeModeSettingTest() {
    data_manager_ = phocr::TestDataManager::Instance();
    all_barcode_image_path_ = ConvertToWString(
        data_manager_->GetPath("ALL_BARCODE.tif"));
    // Create PHOcrDocument
    PHOcrDocumentMaker::CreateDocument(document_, all_barcode_image_path_);
    // Setup setting
    setting_.SetOCRLanguage(L"english");
  }

  // Destructor
  virtual ~BarcodeModeSettingTest() {
    // Delete xml file after processing at here
    std::string output_file = ConvertToString(output_file_) + std::string(".xml");
    if (remove(output_file.c_str()) != 0) {
      std::cerr << "Failed to delete " << output_file << " file \n";
    }
    // Delete all .jpeg file
    std::string delete_command = "rm *.jpeg";
    auto result = std::system(delete_command.c_str());
    if (result != 0) {
      printf("Run command '%s' failed\n", delete_command.c_str());
    }
  }

  bool IsOnlyOneBarcodeFormat(std::string checking_format) {
    if (barcode_format_results_.empty()) {
      return false;
    }
    for (const auto& format : barcode_format_results_) {
      if (format != checking_format) {
        return false;
      }
    }
    return true;
  }

  bool IsDetecting1DBarcode() {
    bool detected_codabar(false);
    bool detected_code39(false);
    bool detected_code128(false);
    bool detected_standard25(false);
    bool detected_code93(false);
    bool detected_interleaved25(false);
    bool detected_upce(false);
    bool detected_upca(false);
    bool detected_iata25(false);
    bool detected_ean8(false);
    bool detected_ean13(false);
    bool detected_matrix25(false);
    for (const auto& format : barcode_format_results_) {
      if (format == std::string("CODABAR")) {
        detected_codabar = true;
      }
      if (format == std::string("CODE_39")) {
        detected_code39 = true;
      }
      if (format == std::string("CODE_128")) {
        detected_code128 = true;
      }
      if (format == std::string("STANDARD_2_OF_5")) {
        detected_standard25 = true;
      }
      if (format == std::string("CODE_93")) {
        detected_code93 = true;
      }
      if (format == std::string("INTERLEAVED_2_OF_5")) {
        detected_interleaved25 = true;
      }
      if (format == std::string("UPC_E")) {
        detected_upce = true;
      }
      if (format == std::string("UPC_A")) {
        detected_upca = true;
      }
      if (format == std::string("IATA_2_OF_5")) {
        detected_iata25 = true;
      }
      if (format == std::string("EAN_8")) {
        detected_ean8 = true;
      }
      if (format == std::string("EAN_13")) {
        detected_ean13 = true;
      }
      if (format == std::string("MATRIX_2_OF_5")) {
        detected_matrix25 = true;
      }
    }
    if (detected_codabar == true && detected_code39 == true && detected_code128 == true &&
        detected_standard25 == true && detected_code93 == true && detected_interleaved25 == true &&
        detected_upce == true && detected_upca == true && detected_iata25 == true && detected_ean8 == true &&
        detected_ean13 == true && detected_matrix25 == true) {
      return true;
    }
    return false;
  }

  bool IsDetecting2DBarcode() {
    bool detected_qr_code(false);
    bool detected_pdf417_code(false);
    bool detected_maxicode_code(false);
    bool detected_datamatrix_code(false);
    bool detected_aztec_code(false);
    for (const auto& format : barcode_format_results_) {
      if (format == std::string("QR_CODE")) {
        detected_qr_code = true;
      }
      if (format == std::string("DATA_MATRIX")) {
        detected_datamatrix_code = true;
      }
      if (format == std::string("AZTEC")) {
        detected_aztec_code = true;
      }
      if (format == std::string("PDF_417")) {
        detected_pdf417_code = true;
      }
      if (format == std::string("MAXI_CODE")) {
        detected_maxicode_code = true;
      }
    }
    if (detected_qr_code == true && detected_pdf417_code == true &&
        detected_maxicode_code == true && detected_datamatrix_code == true &&
        detected_aztec_code == true) {
      return true;
    }
    return false;
  }

  /**
   * Check if the barcode result contains only formats defined in the input
   * @param formats
   * @return
   */
  bool IsOnlyContainBarcode(std::vector<std::string> formats) {
    // Because we don't support PATCH now. just remove the first PATCH out of
    // result
    auto patch_it = std::find(formats.begin(), formats.end(), "PATCH");
    if (patch_it != formats.end()) {
      formats.erase(patch_it);
    }

    if (barcode_format_results_.empty()) {
      return false;
    }

    bool found_barcode(true);

    // Check if in the result, exist the input barcode format
    for (const auto& input : formats) {
      auto it = std::find(
          barcode_format_results_.begin(),
          barcode_format_results_.end(),
          input);
      if (it == barcode_format_results_.end()) {
        found_barcode = false;
        break;
      }
    }

    // Check if in the result, has only the input barcode format
    for (const auto& result : barcode_format_results_) {
      auto it = std::find(formats.begin(), formats.end(), result);
      if (it == formats.end()) {
        found_barcode = false;
        break;
      }
    }
    return found_barcode;
  }

  bool IsEmptyResult() {
    if (barcode_format_results_.empty()) {
      return true;
    }
    return false;
  }

  bool ContainBarcode(std::string barcode) {
    auto it = std::find(barcode_format_results_.begin(), barcode_format_results_.end(), barcode);
    if (it != barcode_format_results_.end()) {
      return true;
    }
    return false;
  }

  void ParseBarcodeFormatFromOutputXMLFile() {
    // Parse XML file to check the barcode result
    pt::ptree pt;
    std::string xml_file_name = ConvertToString(output_file_) +
        std::string(".xml");
    try {
      pt::xml_parser::read_xml(xml_file_name, pt);
    } catch (pt::xml_parser_error& e) {
      std::cerr << "output.xml file is invalid \n";
      return;
    }
    for (const auto& e : pt.get_child("ocr_pages.ocr_page")) {
      if (e.first == "ocr_barcode") {
        barcode_format_results_.push_back(
            e.second.get<std::string>("<xmlattr>.format"));
      }
    }
  }

  void SetupSettingAndExport(std::vector<std::string> formats) {
    unsigned int barcode_mode = 0;
    for (const auto& format : formats) {
      barcode_mode |= barcode_mode_mapper_.at(format);
    }
    setting_.SetBarcodeMode(barcode_mode);
    document_->PHOcrSetSettings(setting_);
    document_->PHOcrExport({{output_file_, PHOcrExportFormat::EF_XML}});

    // Parse barcode format
    ParseBarcodeFormatFromOutputXMLFile();
  }
};

const std::unordered_map<std::string, unsigned int>
BarcodeModeSettingTest::barcode_mode_mapper_ = {
  {"AUTO", 1 << 0},
  {"1D_BARCODE", 1 << 1  },
  {"2D_BARCODE", 1 << 2  },
  {"CODE_39", 1 << 3  },
  {"CODE_93", 1 << 4  },
  {"CODE_128", 1 << 5  },
  {"CODABAR", 1 << 6  },
  {"IATA_2_OF_5", 1 << 7  },
  {"INTERLEAVED_2_OF_5", 1 << 8  },
  {"STANDARD_2_OF_5", 1 << 9  },
  {"MATRIX_2_OF_5", 1 << 10 },
  {"UCC_128", 1 << 11 },
  {"UPC_A", 1 << 12 },
  {"UPC_E", 1 << 13 },
  {"PATCH", 1 << 14 },
  {"POSTNET", 1 << 15 },
  {"AZTEC", 1 << 16 },
  {"DATA_MATRIX", 1 << 17 },
  {"MAXI_CODE", 1 << 18 },
  {"PDF_417", 1 << 19 },
  {"QR_CODE", 1 << 20 },
  {"EAN_8", 1 << 21 },
  {"EAN_13", 1 << 22 },
};


/****************************************************************
 * Detect only one barcode
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_only_EAN_8) {
  SetupSettingAndExport(std::vector<std::string>{"EAN_8"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("EAN_8"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_AZTEC) {
  SetupSettingAndExport(std::vector<std::string>{"AZTEC"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("AZTEC"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_QRCODE) {
  SetupSettingAndExport(std::vector<std::string>{"QR_CODE"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("QR_CODE"));
}

// Because we don't support patch barcode now, id detect patch barcode only,
// result will be empty
TEST_F(BarcodeModeSettingTest, Detect_only_PATCH) {
  SetupSettingAndExport(std::vector<std::string>{"PATCH"});
  EXPECT_TRUE(IsEmptyResult());
}

TEST_F(BarcodeModeSettingTest, Detect_only_EAN_13) {
  SetupSettingAndExport(std::vector<std::string>{"EAN_13"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("EAN_13"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_DATAMATRIX) {
  SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("DATA_MATRIX"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_UPC_A) {
  SetupSettingAndExport(std::vector<std::string>{"UPC_A"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("UPC_A"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_UPC_E) {
  SetupSettingAndExport(std::vector<std::string>{"UPC_E"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("UPC_E"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_MATRIX_2_OF_5) {
  SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("MATRIX_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_INDUSTRIAL_2_OF_5) {
  SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("STANDARD_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_IATA_2_OF_5) {
  SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("IATA_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_CODE_128) {
  SetupSettingAndExport(std::vector<std::string>{"CODE_128"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("CODE_128"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_PDF417) {
  SetupSettingAndExport(std::vector<std::string>{"PDF_417"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("PDF_417"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_POSTNET) {
  SetupSettingAndExport(std::vector<std::string>{"POSTNET"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("POSTNET"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_UCC_128) {
  SetupSettingAndExport(std::vector<std::string>{"CODE_128"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("CODE_128"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_CODABAR) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("CODABAR"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_CODE_93) {
  SetupSettingAndExport(std::vector<std::string>{"CODE_93"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("CODE_93"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_INTERLEAVED_2_OF_5) {
  SetupSettingAndExport(std::vector<std::string>{"INTERLEAVED_2_OF_5"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("INTERLEAVED_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_CODE_39) {
  SetupSettingAndExport(std::vector<std::string>{"CODE_39"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("CODE_39"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_MAXICODE) {
  SetupSettingAndExport(std::vector<std::string>{"MAXI_CODE"});
  EXPECT_TRUE(IsOnlyOneBarcodeFormat("MAXI_CODE"));
}

TEST_F(BarcodeModeSettingTest, Detect_only_2D_BARCODE) {
  SetupSettingAndExport(std::vector<std::string>{"2D_BARCODE"});
  EXPECT_EQ(5, barcode_format_results_.size());
  EXPECT_TRUE(IsDetecting2DBarcode());
}

TEST_F(BarcodeModeSettingTest, Detect_only_1D_BARCODE) {
  SetupSettingAndExport(std::vector<std::string>{"1D_BARCODE"});
  EXPECT_EQ(13, barcode_format_results_.size());
  EXPECT_TRUE(IsDetecting1DBarcode());
}

TEST_F(BarcodeModeSettingTest, Detect_all_barcode) {
  SetupSettingAndExport(std::vector<std::string>{"AUTO"});
  EXPECT_TRUE(IsDetecting1DBarcode());
  EXPECT_TRUE(IsDetecting2DBarcode());
}

/****************************************************************
 * Detect combine of 2 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_AZTEC) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "AZTEC"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "AZTEC"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_QRCODE) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "QR_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "QR_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_PATCH) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "PATCH"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "PATCH"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_EAN_13) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "EAN_13"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "EAN_13"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_DATAMATRIX) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "DATA_MATRIX"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "DATA_MATRIX"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_UPC_A) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "UPC_A"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "UPC_A"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_UPC_E) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "UPC_E"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "UPC_E"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_MATRIX_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "MATRIX_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "MATRIX_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_INDUSTRIAL_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "STANDARD_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "STANDARD_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_IATA_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "IATA_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_CODE_128) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_8", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("EAN_8"));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_8_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_8", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("EAN_8"));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_QRCODE) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "QR_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "QR_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_PATCH) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "PATCH"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "PATCH"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_EAN_13) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "EAN_13"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "EAN_13"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_DATAMATRIX) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "DATA_MATRIX"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "DATA_MATRIX"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_UPC_A) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "UPC_A"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "UPC_A"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_UPC_E) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "UPC_E"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "UPC_E"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_MATRIX_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "MATRIX_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "MATRIX_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_INDUSTRIAL_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "STANDARD_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "STANDARD_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_IATA_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "IATA_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_CODE_128) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"AZTEC", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("AZTEC"));
}

TEST_F(BarcodeModeSettingTest, Detect_AZTEC_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"AZTEC", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("AZTEC"));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_PATCH) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "PATCH"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "PATCH"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_EAN_13) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "EAN_13"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "EAN_13"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_DATAMATRIX) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "DATA_MATRIX"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "DATA_MATRIX"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_UPC_A) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "UPC_A"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "UPC_A"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_UPC_E) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "UPC_E"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "UPC_E"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_MATRIX_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "MATRIX_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "MATRIX_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_INDUSTRIAL_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "STANDARD_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "STANDARD_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_IATA_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "IATA_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_CODE_128) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"QR_CODE", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("QR_CODE"));
}

TEST_F(BarcodeModeSettingTest, Detect_QRCODE_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"QR_CODE", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("QR_CODE"));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_EAN_13) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "EAN_13"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "EAN_13"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_DATAMATRIX) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "DATA_MATRIX"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "DATA_MATRIX"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_UPC_A) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "UPC_A"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "UPC_A"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_UPC_E) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "UPC_E"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "UPC_E"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_MATRIX_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "MATRIX_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "MATRIX_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_INDUSTRIAL_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "STANDARD_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "STANDARD_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_IATA_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "IATA_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_CODE_128) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PATCH", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
}

TEST_F(BarcodeModeSettingTest, Detect_PATCH_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"PATCH", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_DATAMATRIX) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "DATA_MATRIX"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "DATA_MATRIX"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_UPC_A) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "UPC_A"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "UPC_A"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_UPC_E) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "UPC_E"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "UPC_E"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_MATRIX_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "MATRIX_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "MATRIX_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_INDUSTRIAL_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "STANDARD_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "STANDARD_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_IATA_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "IATA_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_CODE_128) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"EAN_13", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("EAN_13"));
}

TEST_F(BarcodeModeSettingTest, Detect_EAN_13_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"EAN_13", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("EAN_13"));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_UPC_A) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "UPC_A"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "UPC_A"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_UPC_E) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "UPC_E"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "UPC_E"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_MATRIX_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "MATRIX_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "MATRIX_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_INDUSTRIAL_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "STANDARD_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "STANDARD_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_IATA_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "IATA_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_CODE_128) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"DATA_MATRIX", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("DATA_MATRIX"));
}

TEST_F(BarcodeModeSettingTest, Detect_DATAMATRIX_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"DATA_MATRIX", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("DATA_MATRIX"));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_UPC_E) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "UPC_E"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "UPC_E"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_MATRIX_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "MATRIX_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "MATRIX_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_INDUSTRIAL_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "STANDARD_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "STANDARD_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_IATA_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "IATA_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_CODE_128) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_A", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("UPC_A"));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_A_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_A", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("UPC_A"));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_MATRIX_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "MATRIX_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "MATRIX_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_INDUSTRIAL_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "STANDARD_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "STANDARD_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_IATA_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "IATA_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_CODE_128) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"UPC_E", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("UPC_E"));
}

TEST_F(BarcodeModeSettingTest, Detect_UPC_E_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"UPC_E", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("UPC_E"));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_INDUSTRIAL_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "STANDARD_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"MATRIX_2_OF_5", "STANDARD_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_IATA_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "IATA_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"MATRIX_2_OF_5", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_CODE_128) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"MATRIX_2_OF_5", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"MATRIX_2_OF_5", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"MATRIX_2_OF_5", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"MATRIX_2_OF_5", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"MATRIX_2_OF_5", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"MATRIX_2_OF_5", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"MATRIX_2_OF_5", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"MATRIX_2_OF_5", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"MATRIX_2_OF_5", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("MATRIX_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_MATRIX_2_OF_5_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"MATRIX_2_OF_5", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("MATRIX_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_IATA_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "IATA_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"STANDARD_2_OF_5", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_CODE_128) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"STANDARD_2_OF_5", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"STANDARD_2_OF_5", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"STANDARD_2_OF_5", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"STANDARD_2_OF_5", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"STANDARD_2_OF_5", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"STANDARD_2_OF_5", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"STANDARD_2_OF_5", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"STANDARD_2_OF_5", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"STANDARD_2_OF_5", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("STANDARD_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_INDUSTRIAL_2_OF_5_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"STANDARD_2_OF_5", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("STANDARD_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_IATA_2_OF_5_and_CODE_128) {
 SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"IATA_2_OF_5", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_IATA_2_OF_5_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"IATA_2_OF_5", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_IATA_2_OF_5_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"IATA_2_OF_5", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_IATA_2_OF_5_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"IATA_2_OF_5", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_IATA_2_OF_5_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"IATA_2_OF_5", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_IATA_2_OF_5_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"IATA_2_OF_5", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_IATA_2_OF_5_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"IATA_2_OF_5", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_IATA_2_OF_5_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"IATA_2_OF_5", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_IATA_2_OF_5_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"IATA_2_OF_5", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_IATA_2_OF_5_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("IATA_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_IATA_2_OF_5_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"IATA_2_OF_5", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("IATA_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_128_and_PDF417) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "PDF_417"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "PDF_417"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_128_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_128_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_128_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_128_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_128_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_128_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_128_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_128_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("CODE_128"));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_128_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("CODE_128"));
}

TEST_F(BarcodeModeSettingTest, Detect_PDF417_and_POSTNET) {
 SetupSettingAndExport(std::vector<std::string>{"PDF_417", "POSTNET"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PDF_417", "POSTNET"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PDF417_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"PDF_417", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PDF_417", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PDF417_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"PDF_417", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PDF_417", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PDF417_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"PDF_417", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PDF_417", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PDF417_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"PDF_417", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PDF_417", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PDF417_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"PDF_417", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PDF_417", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PDF417_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"PDF_417", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"PDF_417", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_PDF417_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"PDF_417", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("PDF_417"));
}

TEST_F(BarcodeModeSettingTest, Detect_PDF417_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"PDF_417", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("PDF_417"));
}

TEST_F(BarcodeModeSettingTest, Detect_POSTNET_and_UCC_128) {
 SetupSettingAndExport(std::vector<std::string>{"POSTNET", "CODE_128"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"POSTNET", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_POSTNET_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"POSTNET", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"POSTNET", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_POSTNET_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"POSTNET", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"POSTNET", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_POSTNET_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"POSTNET", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"POSTNET", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_POSTNET_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"POSTNET", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"POSTNET", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_POSTNET_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"POSTNET", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"POSTNET", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_POSTNET_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"POSTNET", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("POSTNET"));
}

TEST_F(BarcodeModeSettingTest, Detect_POSTNET_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"POSTNET", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("POSTNET"));
}

TEST_F(BarcodeModeSettingTest, Detect_UCC_128_and_CODABAR) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "CODABAR"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "CODABAR"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UCC_128_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UCC_128_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UCC_128_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UCC_128_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_128", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_UCC_128_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("CODE_128"));
}

TEST_F(BarcodeModeSettingTest, Detect_UCC_128_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_128", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("CODE_128"));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_93) {
 SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_93"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"CODABAR", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODABAR", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODABAR", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("CODABAR"));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODABAR", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("CODABAR"));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_93_and_INTERLEAVED_2_OF_5) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_93", "INTERLEAVED_2_OF_5"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_93", "INTERLEAVED_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_93_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_93", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_93", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_93_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_93", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_93", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_93_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_93", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("CODE_93"));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_93_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_93", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("CODE_93"));
}

TEST_F(BarcodeModeSettingTest, Detect_INTERLEAVED_2_OF_5_and_CODE_39) {
 SetupSettingAndExport(std::vector<std::string>{"INTERLEAVED_2_OF_5", "CODE_39"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"INTERLEAVED_2_OF_5", "CODE_39"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INTERLEAVED_2_OF_5_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"INTERLEAVED_2_OF_5", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"INTERLEAVED_2_OF_5", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_INTERLEAVED_2_OF_5_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"INTERLEAVED_2_OF_5", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("INTERLEAVED_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_INTERLEAVED_2_OF_5_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"INTERLEAVED_2_OF_5", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("INTERLEAVED_2_OF_5"));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_39_and_MAXICODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_39", "MAXI_CODE"});
 EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODE_39", "MAXI_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_39_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_39", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("CODE_39"));
}

TEST_F(BarcodeModeSettingTest, Detect_CODE_39_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_39", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("CODE_39"));
}

TEST_F(BarcodeModeSettingTest, Detect_MAXICODE_and_2D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"CODE_39", "2D_BARCODE"});
 EXPECT_TRUE(IsDetecting2DBarcode());
 EXPECT_TRUE(ContainBarcode("CODE_39"));
}

TEST_F(BarcodeModeSettingTest, Detect_MAXICODE_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"MAXI_CODE", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(ContainBarcode("MAXI_CODE"));
}

TEST_F(BarcodeModeSettingTest, Detect_2D_BARCODE_and_1D_BARCODE) {
 SetupSettingAndExport(std::vector<std::string>{"2D_BARCODE", "1D_BARCODE"});
 EXPECT_TRUE(IsDetecting1DBarcode());
 EXPECT_TRUE(IsDetecting2DBarcode());
}

/****************************************************************
 * Combine 3 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_IATA_2_OF_5) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "IATA_2_OF_5"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_128) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_128"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_QR_CODE) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "QR_CODE"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "QR_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_AZTEC_and_QR_CODE) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "AZTEC", "QR_CODE"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "AZTEC", "QR_CODE"}));
}

/****************************************************************
 * Combine 4 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_CODE_128) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "CODE_128"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_QR_CODE) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "QR_CODE"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "QR_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_AZTEC_and_QR_CODE) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "AZTEC", "QR_CODE"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "AZTEC", "QR_CODE"}));
}

/****************************************************************
 * Combine 5 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_QR_CODE) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "QR_CODE"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "QR_CODE"}));
}

TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_AZTEC_and_QR_CODE) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "AZTEC", "QR_CODE"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "AZTEC", "QR_CODE"}));
}

/****************************************************************
 * Combine 6 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE"}));
}

/****************************************************************
 * Combine 7 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC"}));
}

/****************************************************************
 * Combine 8 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC_and_MATRIX_2_OF_5) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5"}));
}

/****************************************************************
 * Combine 9 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC_and_MATRIX_2_OF_5_and_UPC_A) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "MATRIX_2_OF_5", "UPC_A"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A"}));
}

/****************************************************************
 * Combine 10 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC_and_MATRIX_2_OF_5_and_UPC_A_and_UPC_E) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E"}));
}

/****************************************************************
 * Combine 11 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC_and_MATRIX_2_OF_5_and_UPC_A_and_UPC_E_and_POSTNET) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET"}));
}

/****************************************************************
 * Combine 12 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC_and_MATRIX_2_OF_5_and_UPC_A_and_UPC_E_and_POSTNET_and_DATAMATRIX) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX"}));
}

/****************************************************************
 * Combine 13 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC_and_MATRIX_2_OF_5_and_UPC_A_and_UPC_E_and_POSTNET_and_DATAMATRIX_and_MAXICODE) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE"}));
}

/****************************************************************
 * Combine 14 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC_and_MATRIX_2_OF_5_and_UPC_A_and_UPC_E_and_POSTNET_and_DATAMATRIX_and_MAXICODE_and_PDF417) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE", "PDF_417"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE", "PDF_417"}));
}

/****************************************************************
 * Combine 15 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC_and_MATRIX_2_OF_5_and_UPC_A_and_UPC_E_and_POSTNET_and_DATAMATRIX_and_MAXICODE_and_PDF417_and_EAN_8) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE", "PDF_417", "EAN_8"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE", "PDF_417", "EAN_8"}));
}


/****************************************************************
 * Combine 16 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC_and_MATRIX_2_OF_5_and_UPC_A_and_UPC_E_and_POSTNET_and_DATAMATRIX_and_MAXICODE_and_PDF417_and_EAN_8_and_EAN_13) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE", "PDF_417", "EAN_8", "EAN_13"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE", "PDF_417", "EAN_8", "EAN_13"}));
}

/****************************************************************
 * Combine 17 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC_and_MATRIX_2_OF_5_and_UPC_A_and_UPC_E_and_POSTNET_and_DATAMATRIX_and_MAXICODE_and_PDF417_and_EAN_8_and_EAN_13_and_INTERLEAVED_2_OF_5) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE", "PDF_417", "EAN_8", "EAN_13", "INTERLEAVED_2_OF_5"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE", "PDF_417", "EAN_8", "EAN_13", "INTERLEAVED_2_OF_5"}));
}

/****************************************************************
 * Combine 18 barcodes
 ***************************************************************/
TEST_F(BarcodeModeSettingTest, Detect_CODABAR_and_CODE_39_and_CODE_93_and_IATA_2_OF_5_and_CODE_128_and_QR_CODE_and_AZTEC_and_MATRIX_2_OF_5_and_UPC_A_and_UPC_E_and_POSTNET_and_DATAMATRIX_and_MAXICODE_and_PDF417_and_EAN_8_and_EAN_13_and_INTERLEAVED_2_OF_5_and_INDUSTRIAL_2_OF_5) {
  SetupSettingAndExport(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE", "PDF_417", "EAN_8", "EAN_13", "INTERLEAVED_2_OF_5", "STANDARD_2_OF_5"});
  EXPECT_TRUE(IsOnlyContainBarcode(std::vector<std::string>{"CODABAR", "CODE_39", "CODE_93", "IATA_2_OF_5", "CODE_128", "QR_CODE", "AZTEC", "MATRIX_2_OF_5", "UPC_A", "UPC_E", "POSTNET", "DATA_MATRIX", "MAXI_CODE", "PDF_417", "EAN_8", "EAN_13", "INTERLEAVED_2_OF_5", "STANDARD_2_OF_5"}));
}
