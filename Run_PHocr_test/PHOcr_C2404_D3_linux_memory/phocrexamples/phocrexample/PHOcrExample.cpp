/*****************************************************************************
 * @file    main.cpp
 * @brief   Provides example for building the application use PHOcr library.
 *
 * (C) TOSHIBA TEC Corporation - 2018
 *****************************************************************************/
#include "PHOcrDocument.h"
#include "PHOcrSettings.h"
#include "PHOcrStringHelper.h"
#include "PHOcrDocumentMaker.h"
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
      <<  "\n\n****PHOcr Sample application\n"
          "Usage: ./main [language] [export_format] [output_base] [image_path]\n\n"
          "[output_base]: Can only be a relative pathfor MS Office output formats at the moment.\n"
          "               Also, use basename only. File suffix is automatically applied\n"
          "[export_format]:\n"
          "                 0 - TXT\n"
          "                 1 - PDF\n"
          "                 2 - PDFA\n"
          "                 3 - DOCX\n"
          "                 4 - XLSX\n"
          "                 5 - PPTX\n"
          "Example: ./main english 0 ./inputfile.tiff ./phocr_output_file\n"
      << std::endl;
}

int main(int argc, char** argv) {
  if (argc < 5) {
    // Not enough parameters, print help to use
    PrintHelp();
    return 1;
  }

  // Create document PHOcrDocument from image path
  std::wstring image_path = phocr::ConvertToWString(argv[argc - 1]);
  phocr::PHOcrDocumentPtr document;
  phocr::PHOcrStatus status =
      phocr::PHOcrDocumentMaker::CreateDocument(document, image_path);
  if (status != phocr::PHOcrStatus::PHOCR_OK) {
    return 1;
  }

  // Get filename
  std::string outputname = argv[argc - 2];
  std::wstring outputname_w = phocr::ConvertToWString(outputname);

  // Get language setting, Just take the parameter before input image,
  // Check is invalid language, then use that for language setting
  std::string language = argv[argc-4];
  std::wstring language_w = phocr::ConvertToWString(language);

  // Initialize Default Settings for PHOcr operation.
  phocr::PHOcrSettings phocrSettings;

  // Set the export format.
  // See definition in PHOcrSettings.h for details.
  phocr::PHOcrExportFormat exportFormat = phocr::PHOcrExportFormat::EF_TXT;

  // Get Export Format from command line.
  switch (atoi(argv[argc-3])) {
    case 0:
      exportFormat = phocr::PHOcrExportFormat::EF_TXT;
      break;
    case 1:
      exportFormat = phocr::PHOcrExportFormat::EF_PDF;
      break;
    case 2:
      exportFormat = phocr::PHOcrExportFormat::EF_PDFA;
      break;
    case 3:
      exportFormat = phocr::PHOcrExportFormat::EF_DOCX;
      break;
    case 4:
      exportFormat = phocr::PHOcrExportFormat::EF_XLSX;
      break;
    case 5:
      exportFormat = phocr::PHOcrExportFormat::EF_PPTX;
      break;
    default:
      std::cout << "Error with Export format. Using EF_TXT" << std::endl;
  }

  // Apply Settings to Document.
  document->PHOcrSetSettings(phocrSettings);

  // Export based on export format.
  document->PHOcrExport({{outputname_w, exportFormat}});
  return 0;
}
