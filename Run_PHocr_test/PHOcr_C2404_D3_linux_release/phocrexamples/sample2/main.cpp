/*****************************************************************************
 * @file    main.cpp
 * @brief   Provides example for building the application use PHOcr library.
 *
 * (C) TOSHIBA TEC Corporation - 2018
 *****************************************************************************/
#include "PHOcrDocument.h"
#include "PHOcrSettings.h"
#include "PHOcrStringHelper.h"
#include "PHOcrPageMaker.h"
#ifndef _WIN32
#include <execinfo.h>
#endif
#include <signal.h>
#include <stdlib.h>
#ifndef _WIN32
#include <unistd.h>
#endif

/**
 * Print help to stdout
 */
void PrintHelp() {
  std::cout
      <<  "\n\n****PHOcr Sample application for OCR to output format.\n"
          "Usage: main [image_path] \n\n"
          "Example: ./main ./inputfile.tiff\n"
      << std::endl;
}

int main(int argc, char** argv) {
  if (argc < 2) {
    // Not enough parameters, print help to use
    PrintHelp();
    return 1;
  }

  // Create a PHOcr Page representation from image path
  std::wstring filename = phocr::ConvertToWString(argv[argc - 1]);
  phocr::PHOcrPagePtr pagePtr;
  phocr::PHOcrStatus status =
      phocr::PHOcrPageMaker::CreatePage(pagePtr, filename);
  if (status != phocr::PHOcrStatus::PHOCR_OK) {
    return 1;
  }

  std::vector<std::wstring> barcodes;

  // Decode Barcodes from Page.
  if (pagePtr->PHOcrGetAllBarcodes(barcodes) !=
      phocr::PHOcrStatus::PHOCR_OK) {
    std::cerr << "Can't get all barcode" << std::endl;
    return 1;
  }

  std::wcout << "Page Barcodes: "<< std::endl;

  //Print string representation of barcodes found in page.
  if(barcodes.size() == 0)
      std::wcout << "\tNone!\n";
  else
  {
      for(size_t i = 0; i < barcodes.size() ; i++)
      {
          std::wcout << "\tBarcode_" << i << "," << barcodes.at(i) << std::endl;
      }
  }

  return 0;
}
