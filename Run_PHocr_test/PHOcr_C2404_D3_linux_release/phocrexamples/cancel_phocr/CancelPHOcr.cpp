/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    CancelPHOcr.cpp
 * @brief
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    May 2, 2019
 *****************************************************************************/
// This file is created for testing purpose only
#include <thread>
#include <iostream>
#include <chrono>
#include <ctime>
#include <cstring>
#include <string>
#include <sstream>
#include "PHOcrDocument.h"
#include "PHOcrDocumentMaker.h"
#include "PHOcrDeclaration.h"
#include "PHOcrTiming.h"
#include "PHOcrStringHelper.h"
#include "PHOcrSettings.h"

using namespace phocr;

// Global variable for checking cancel flag
bool is_phocr_cancelled = false;

/**
 * Check if we are canceling PHOcr
 * @return
 */
bool IsCancel() {
  return is_phocr_cancelled;
}

/**
 * MFP controler is running this
 */
void MFPControllerRunning(int cancel_time_ms) {
  // If user don't want to cancel PHOcr when run this test
  if (cancel_time_ms == -1) {
    std::cout << "***** PHOcr won't be cancelled in this scenario ***** \n";
    is_phocr_cancelled = false;
  } else {
    // Sleep this thread in cancel_time seconds
    std::this_thread::sleep_for(std::chrono::milliseconds(cancel_time_ms));
    std::cout << "PHOcr is cancelled now, after " << cancel_time_ms << " ms \n";
    PHOcrTiming::PrintSystemTimeNow();
    PHOcrTiming::SetStartTimeNow();
    is_phocr_cancelled = true;
  }
}

/**
 * PHOcr is running this to export a document
 * @param cancelDecisionMethod
 */
void PHOcrProcess(
    PHOcrCancelDecisionMethod cancel,
    std::string image_path,
    std::string output_format) {
  // Get the image path
  std::wstring image_path_input = ConvertToWString(image_path);
  PHOcrExportFormat format;
  PHOcrSettings setting;

  // Output name have the same name with input image
  std::string output_name;
  for (int i = image_path.size() -1; i >= 0; --i) {
    if (image_path[i] == '/') {
      output_name = image_path.substr(i + 1, image_path.size() - i);
      break;
    }
  }
  std::wstring output_name_value = ConvertToWString(output_name);

  // Get the output format
  std::cout << output_format << "\n";
  if  (output_format == std::string("txt")) {
      format = PHOcrExportFormat::EF_TXT;
  } else if (output_format == std::string("txt_bb")) {
      format = PHOcrExportFormat::EF_BB;
  } else if (output_format == std::string("docx")) {
      format = PHOcrExportFormat::EF_DOCX;
      setting.SetDataMode(PHOcrDataMode::DM_HIGH_CONTENT);
  } else if (output_format == std::string("pdf")) {
      format = PHOcrExportFormat::EF_PDF;
  } else if (output_format == std::string("no_ocr_pdf")) {
      format = PHOcrExportFormat::EF_PDF;
      setting.SetPdfExportMode(PHOcrPDFExportMode::PEM_ONLY_IMAGE);
  }

  PHOcrDocumentPtr document;
  PHOcrDocumentMaker::CreateDocument(document, image_path_input, setting);
  document->PHOcrSetCancelDecisionMethod(cancel);
  document->PHOcrExport({{output_name_value, format}});
}

void PrintHelp() {
  std::cout << "Please run CancelPHOcr follow bellow instruction: \n";
  std::cout << "/path/to/CancelPHOcr -i image_path "
               "-o output_format[txt, txt_bb, docx, pdf, no_ocr_pdf] "
               "-c cancel_time(milliseconds) \n";
  std::cout << "If you don't want to cancel PHOcr, don't set -c option \n";
  exit(1);
}

int main(int argc, char **argv) {
  std::string image_path;
  std::string output_format;
  int cancel_time_ms(-1);

  // Parse the program argument
  for (int i = 1; i < argc; ++i) {
    if (strcmp(argv[i], "-i") == 0) {
      image_path = std::string(argv[i + 1]);
    }

    if (strcmp(argv[i], "-o") == 0) {
      output_format = std::string(argv[i + 1]);
    }

    if (strcmp(argv[i], "-c") == 0) {
      try {
        cancel_time_ms = std::stoi(std::string(argv[i + 1]));
      } catch(const std::invalid_argument& e) {
        std::cout << "cancel_time is in wrong format \n";
        PrintHelp();
      }
    }
  }

  // image path and output format is required argument
  if (image_path.empty() || output_format.empty()) {
    PrintHelp();
  }

  std::thread controller(MFPControllerRunning, cancel_time_ms);
  std::thread processing(PHOcrProcess, IsCancel, image_path, output_format);

  controller.join();
  processing.join();

  return 0;
}
