/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    MemoryCounting.cpp
 * @brief   Provides example for building the application use PHOcr library.
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Apr 6, 2019
 *****************************************************************************/

#include "PHOcrDocumentMaker.h"
#include "PHOcrPageMaker.h"
#include "PHOcrSettings.h"
#include "PHOcrStringHelper.h"
#include "PHOcrStatus.h"
#include "BarcodeMode.h"
#include <sys/time.h>
#include <iostream>
#include <sstream>
#include <time.h>
#include <cstring>
#ifndef _WIN32
#include <execinfo.h>
#endif
#include <signal.h>
#include <stdlib.h>
#ifndef _WIN32
#include <unistd.h>
#endif
#include "PHOcrStringHelper.h"

#ifndef MAX_PATH
#define MAX_PATH 4096
#endif

using namespace phocr;
void printMemoryStatus()
{
  char *line = NULL;
  size_t line_len=0;
  FILE *status;
  int peak = 0;
  int rss = 0;
  status = fopen("/proc/self/status", "r");
  if (!status) return;
  /* Read memory size data from /proc/pid/status */
  while ( getline( &line, &line_len, status) != -1 ) {
    if( !strncmp(line, "VmPeak:", 6) ) {
      sscanf(&line[7],"%d",&peak);
    } else if( !strncmp(line, "VmRSS:", 6) ) {
      sscanf(&line[7],"%d",&rss);
    }
  }
  std::cout<<"\t\tVmPeak size is :"<<peak<<"KB"<<std::endl;
  std::cout<<"\t\tVmRSS size is :"<<rss<<"KB"<<std::endl;
  free(line);
  fclose(status);
  return;
}

const char *GetTime(const std::string &buf)
{
    struct timeval tv;
    gettimeofday(&tv,0);

    struct tm ltm;
    localtime_r(&tv.tv_sec, &ltm);

    char timeret[80];
    size_t len = strftime(timeret, sizeof timeret, "%m/%d %H:%M:%S", &ltm);
    sprintf(timeret+len, "%06ld", tv.tv_usec);

    const_cast<std::string&>(buf) = timeret;
    return buf.c_str();
}

void handler(int sig) {
  // Print out message
  fprintf(stderr, "Something wrong with PHOcr!\n");
  exit(1);
}

/**
 * Print help to stdout
 */
void PrintHelp() {
  std::cout
    <<  "Usage: PHOcrExe.exe [Options] [language] image_path\n"
      "Option list: \n"
      "    -reg_data        Export region data when process image\n"
      "    -word            Export OCR result in MS Word format\n"
      "    -excel           Export OCR result in MS Excel format\n"
      "    -pptx            Export OCR result in MS Power Point format\n"
      "    -txt             Export OCR result in txt file\n"
      "    -pdf             Export OCR result in pdf file\n"
      "    -pdfa            Export OCR result in pdf file with PDF/A compliance\n"
      "    -barcode         Get barcode data\n"
      "    -d               Show time of each process\n"
      "    --no-parallel   Disable parallel for PHOcr\n"
      "    -no_ocr          Do not OCR on image, only export segmentation\n"
      "    -ocr             OCR and remove blank lines\n"
      "    -db_ma level     Macro segmentation debug level\n"
      "    -db_bc level     Barcode debug level\n"
      "    -db_pp level     PreProcess debug level\n"
      "    -db_ocr settings Settings for ocr variable, format will be\n"
      "                     \"var1=val1,var1=val1\", if val have \",\" inside, please use \"\\,\"\n"
      "    -layout          Layout the characters/words following the\n"
      "                     order left to right, top to bottom\n"
      "    -noocrwhitetext  Set for disable ocr white text on black background\n"
      "                     Default white text on black background will be ocred\n"
      "    -getStringInZone <x,y,width,height> \n"
      "                     Get text in a zone, export to txt file \n"
      "    -getBarcodeInZone <x,y,width,height> \n"
      "                     Get barcode in a zone, export to txt file \n"
      "    -bin [global|local|adaptive]:\n"
      "                     Settings binarization process, using three method thresholding:\n"
      "                          1. Global adaptive thresholding\n"
      "                          2. Local adaptive thresholding\n"
      "                          3. Adaptive selection between global or local by analyzing\n"
      "                          standard deviation of gray level\n"
      "                     Default is (3) adaptive selection thresholding\n"
      "    language         Set language for input image, Supported:\n"
      "                         EFGIS languages:     English, French, German, Italian, Spanish,\n"
      "                         Asian languages:     Japanese, ChineseSimplified, ChineseTraditional, Korean, Arabic\n"
      "                         European languages:  Danish, Dutch, Finnish, Greek-Ancient, Greek-Modern, Norwegian,\n"
      "                                              Polish, Portuguese, Russian, Swedish, Turkish\n"
      "                     Language is case insensitive\n"
      "                     Default language: English\n"
    << std::endl;
}

int main(int argc, char** argv) {
  std::cout<< "PHOcr start" << std::endl;
  if (argc < 3) {
    // Not enough parameters, print help to use
    PrintHelp();
    return 1;
  }

  // Transfer program parameters to variable value
  bool export_word = false;
  bool export_excel = false;
  bool export_powerpoint = false;
  bool export_txt = false;
  bool export_pdf = false;
  bool export_pdfa = false;
  bool get_barcode = false;
  bool debug = false;
  bool export_reg_data = false;
  bool get_string_in_zone = false;
  bool get_barcode_in_zone = false;
  bool ocr_remove_blank_lines = false;
  bool layout_charater_coordinate = false;
  int zonestringnum=0;
  int zonebarcodenum=0;
  std::vector<std::vector<int>> zone_string_array;
  zone_string_array.resize(3);
  std::vector<std::vector<int>> zone_barcode_array;
  zone_barcode_array.resize(3);
  bool is_input_table_detect_type = false;
  bool ocr_white_text_on_black_background = true;
  unsigned int barcode_mode = BarcodeMode::BM_1D_BARCODE;
  PHOcrPagePtr page;
  for (int i = 1; i < argc; i++) {
    if (strcmp(argv[i], "-word") == 0) {
      export_word = true;
    }
    if (strcmp(argv[i], "-excel") == 0) {
      export_excel = true;
    }
    if (strcmp(argv[i], "-pptx") == 0) {
      export_powerpoint = true;
    }
    if (strcmp(argv[i], "-txt") == 0) {
      export_txt = true;
    }
    if (strcmp(argv[i], "-pdf") == 0) {
      export_pdf = true;
    }
    if (strcmp(argv[i], "-pdfa") == 0) {
      export_pdfa = true;
    }
    if (strcmp(argv[i], "-barcode") == 0) {
      get_barcode = true;
    }
    if (strcmp(argv[i], "-reg_data") == 0) {
      export_reg_data = true;
    }
    if (strcmp(argv[i], "-d") == 0) {
      debug = true;
    }
    if (strcmp(argv[i], "-getStringInZone") == 0) {
      get_string_in_zone = true;
      if (i + 1 < argc) {
        std::string zonenum = argv[i + 1];
        zonestringnum=std::stoi(zonenum);
        if (0 >= zonestringnum || 3 < zonestringnum) {
            PrintHelp();
            return 1;
        }
        if (i + 1 + zonestringnum < argc) {
          int zonecnt;
          for (zonecnt=0;zonecnt<zonestringnum;zonecnt++){
            std::string zone = argv[i + 2 + zonecnt];
            std::stringstream zone_stream(zone);
            std::string token;
            while (std::getline(zone_stream, token, ',')) {
              zone_string_array[zonecnt].push_back(std::stoi(token));
            }
          if (zone_string_array[zonecnt].size() != 4) {
            PrintHelp();
            return 1;
          }
          std::cout << "ZoneInfo" << zonecnt << "\t x:" << zone_string_array[zonecnt][0] <<
                              "\t y:" << zone_string_array[zonecnt][1] <<
                              "\t width:" <<  zone_string_array[zonecnt][2] <<
                              "\t height:" << zone_string_array[zonecnt][3] << std::endl;
          }
        } else {
            PrintHelp();
            return 1;
        }
      }
    }
    if (strcmp(argv[i], "-getBarcodeInZone") == 0) {
      get_barcode_in_zone = true;
      if (i + 1 < argc) {
        std::string zonenum = argv[i + 1];
        zonebarcodenum=std::stoi(zonenum);
        if (0 >= zonebarcodenum || 3 < zonebarcodenum) {
            PrintHelp();
            return 1;
        }
        if (i + 1 + zonebarcodenum < argc) {
          int zonecnt;
          for (zonecnt=0;zonecnt<zonebarcodenum;zonecnt++){
            std::string zone = argv[i + 2 + zonecnt];
            std::stringstream zone_stream(zone);
            std::string token;
            while (std::getline(zone_stream, token, ',')) {
              zone_barcode_array[zonecnt].push_back(std::stoi(token));
            }
            if (zone_barcode_array[zonecnt].size() != 4) {
              PrintHelp();
              return 1;
            }
            std::cout << "ZoneInfo(Barcode)" << zonecnt << "\t x:" << zone_barcode_array[zonecnt][0] <<
                                    "\t y:" << zone_barcode_array[zonecnt][1] <<
                                    "\t width:" <<  zone_barcode_array[zonecnt][2] <<
                                    "\t height:" << zone_barcode_array[zonecnt][3] << std::endl;
          }
        } else {
            PrintHelp();
            return 1;
        }
      }
    }
    if (strcmp(argv[i], "-bm") == 0) {
      if (i + 1 < argc) {
        barcode_mode = stoi(std::string(argv[i + 1]));
      }
      i++;
    }
    if (strcmp(argv[i], "-ocr") == 0) {
      ocr_remove_blank_lines = true;
    }
    if (strcmp(argv[i], "-layout") == 0) {
      layout_charater_coordinate = true;
    }
    if (strcmp(argv[i], "-noocrwhitetext") == 0) {
      ocr_white_text_on_black_background = false;
    }
  }
  // Check condition of program parameters
  if (!ocr_remove_blank_lines && !export_pdf && !export_pdfa && !export_txt
      && !export_word && !export_excel && !export_powerpoint && !export_reg_data
      && !layout_charater_coordinate && !get_string_in_zone
      && !get_barcode_in_zone &&!get_barcode) {
    PrintHelp();
    return 0;
  }
  FILE* filelist = 0;
  bool MultipageProc =false;
  char inputFileName[MAX_PATH];
  PHOcrDocumentPtr document;
  strcpy(inputFileName,argv[argc - 1]);
  std::wstring filename = ConvertToWString(argv[argc - 1]);

  // Create document PHOcrDocument from image path
  if (filename == L"filelist.txt") {
    std::cout<<"filelist get" <<std::endl;
    filelist = fopen( argv[argc -1],"r" );
    if( filelist == 0 ) {
      PrintHelp();
      return 1;
    }
    MultipageProc=true;
    char* ret = fgets( inputFileName, MAX_PATH, filelist );
    int len = strlen( inputFileName );
    //fgets returns additional symbols( \n or \r\n )
    //--------------remove \r\n ...
    if( inputFileName[len-1] < ' ' ) {
      inputFileName[len-1] = 0;
      if( inputFileName[len-2] < ' ' ) {
        inputFileName[len-2] = 0;
      }
    }
    filename = ConvertToWString(inputFileName);
  }
  try {
    std::wcout << filename << " input!!" << std::endl;
    PHOcrDocumentMaker::CreateDocument(document,filename);
    if (document == NULL) {
      printf("can not create document\n");
      return 1;
    }
  } catch (...) {
  PrintHelp();
  return 1;
  }
  // Get filename
  std::string outputname(inputFileName);
  std::wstring outputname_w;
  if (MultipageProc) {
    outputname_w = ConvertToWString("AllPages");
  } else {
    outputname_w = ConvertToWString(outputname);
  }

  // Get language setting, Just take the parameter before input image,
  // Check is invalid language, then use that for language setting
  std::string language;
  if ((strcmp(argv[argc - 3], "-getStringInZone") != 0 )
      && (strcmp(argv[argc - 3], "-getBarcodeInZone") != 0)
      && (get_barcode == true)) {
    language = argv[argc - 2];
    if (language.at(0) == '-') {
      language = "English";
    }
  } else {
    language = "English";
  }
  std::wstring language_w = ConvertToWString(language);

  PHOcrSettings phocrSettings;
  phocrSettings.SetOCRLanguage(language_w);
  phocrSettings.SetBarcodeMode(barcode_mode);
  phocrSettings.SetPdfImageExportMode(PHOcrImageExportMode::IEM_ORIGINAL);
  phocrSettings.SetUsingImageBandingMechanism(true);
  printf("UsingImageBandingMechanism is :%d\n",phocrSettings.GetUsingImageBandingMechanism());
  // Set table detection type for each output type of document.
  // If user do not input table detect type, default set simple for txt, pdf format
  // set complex for excel, word format
  if (!is_input_table_detect_type) {
    if (export_word || export_excel || export_powerpoint) {
      // If export docx, xlsx, pptx --> don't ocr white text on black background
      ocr_white_text_on_black_background = false;
    }
  }

  // Configure for document
  document->PHOcrSetSettings(phocrSettings);

  clock_t start_s = clock();
  if (debug) {
    std::cout << "Process: " << std::endl;
  }
  try {
    if(export_pdf || export_pdfa || export_txt || export_word || export_excel || export_powerpoint) {
      if (MultipageProc == true) {
        // Analysis layout and recognize document
        long numberPages = document->PHOcrGetNumberOfPages();
        std::cout << "PageNo:" << numberPages << "Start!!" << std::endl;
        printMemoryStatus();
        if (debug) {
          std::cout << "\t" << (clock() - start_s) / double(CLOCKS_PER_SEC) << "s"
              << std::endl;
        }
        std::cout << "PageNo:" << numberPages << "Finish!!" << std::endl;
        printMemoryStatus();
        while(0 != fgets( inputFileName, MAX_PATH, filelist )) {
          int len = strlen( inputFileName );
          clock_t start_s = clock();
          //fgets returns additional symbols( \n or \r\n )
          //--------------remove \r\n ...
          if( inputFileName[len-1] < ' ' ) {
            inputFileName[len-1] = 0;
            if( inputFileName[len-2] < ' ' ) {
              inputFileName[len-2] = 0;
            }
          }
          filename = ConvertToWString(inputFileName);
          try {
            PHOcrPageMaker::CreatePage(page, filename);
            page->PHOcrSetSettings(phocrSettings);
            document->PHOcrAppendPages({page});
            document->PHOcrSetSettings(phocrSettings);
            numberPages = document->PHOcrGetNumberOfPages();
            std::cout << "PageNo:" << numberPages << "Start!!" << std::endl;
            printMemoryStatus();
            if (debug) {
              std::cout << "\t" << (clock() - start_s) / double(CLOCKS_PER_SEC) << "s"
                  << std::endl;
            }
            std::cout << "PageNo:" << numberPages << "Finish!!" << std::endl;
            printMemoryStatus();

          } catch (...) {
            PrintHelp();
            return 1;
          }
        }
      } else {
        // Analysis layout and recognize document
        long numberPages = document->PHOcrGetNumberOfPages();
        std::cout << "PageNo:" << numberPages << "Start!!" << std::endl;
        printMemoryStatus();
        if (debug) {
          std::cout << "\t" << (clock() - start_s) / double(CLOCKS_PER_SEC) << "s"
              << std::endl;
        }
        std::cout << "PageNo:" << numberPages << "Finish!!" << std::endl;
        printMemoryStatus();
      }
    }

    if (get_barcode) {
      PHOcrPagePtr pagePtr; /* page object */
      long pagenum; /* Decode target page number */
      std::vector<std::wstring> barcodes;   /* decoded barcode data */

      // add page from filelist
      if (MultipageProc == true) {
        while(0 != fgets( inputFileName, MAX_PATH, filelist )) {
          int len = strlen( inputFileName );
          //fgets returns additional symbols( \n or \r\n )
          //--------------remove \r\n ...
          if( inputFileName[len-1] < ' ' ) {
            inputFileName[len-1] = 0;
            if( inputFileName[len-2] < ' ' ) {
              inputFileName[len-2] = 0;
            }
          }
          filename = ConvertToWString(inputFileName);
          try {
            PHOcrPageMaker::CreatePage(pagePtr, filename);
            document->PHOcrAppendPages({pagePtr});
          } catch (...) {
            PrintHelp();
            return 1;
          }
        }
      }
      long numberPages = document->PHOcrGetNumberOfPages(); /* Total page number */
      //Decode Barcode and print
      for (pagenum=0;pagenum < numberPages;pagenum++) {
        std::cout << "Barcode PageNo:" << pagenum+1 << std::endl;
        pagePtr=document->PHOcrGetPage(pagenum);
        //Decode Barcodes from Page.
        /*
        PHOcrSettings prev_phocrSettings;
        prev_phocrSettings = document->PHOcrGetSettings();
        std::cout << "Previous barcode mode is " << prev_phocrSettings.GetBarcodeMode() << std::endl;
        */
        //ToDo:Why  does not page object inherit document object settings?
        phocrSettings.SetBarcodeMode(barcode_mode);
        pagePtr->PHOcrSetSettings(phocrSettings);
        std::string tmp;

        printf("\t%s Before PHOcrGetAllBarcodes\n", GetTime(tmp));
        pagePtr->PHOcrGetAllBarcodes(barcodes);
        printf("\t%s After PHOcrGetAllBarcodes\n", GetTime(tmp));
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
      }
    }

    // Export TXT format
    if (export_txt || ocr_remove_blank_lines) {
      clock_t start_s = clock();
      if (debug) {
        std::cout << "export_txt: ";
      }
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_TXT}});
      if (debug) {
        std::cout << (clock() - start_s) / double(CLOCKS_PER_SEC) << "s"
            << std::endl;
      }
    }

    if (layout_charater_coordinate) {
      clock_t start_s = clock();
      if (debug) {
        std::cout << "export_bb: ";
      }
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_BB}});
      if (debug) {
        std::cout << (clock() - start_s) / double(CLOCKS_PER_SEC) << "s"
            << std::endl;
      }
    }

    // Exporting PDF format
    if (export_pdf) {
      clock_t start_s = clock();
      if (debug) {
        std::cout << "export_pdf: ";
      }
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_PDF}});
      if (debug) {
        std::cout << (clock() - start_s) / double(CLOCKS_PER_SEC) << "s"
            << std::endl;
      }
    }

    // Exporting PDF format
    if (export_pdfa) {
      clock_t start_s = 0;
      if (debug) {
        start_s = clock();
        std::cout << "export_pdfa: ";
      }
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_PDF}});
      if (debug) {
        std::cout << (clock() - start_s) / double(CLOCKS_PER_SEC) << "s"
            << std::endl;
      }
    }

    if (export_word) {
      clock_t start_s = 0;
      if (debug) {
        start_s = clock();
        std::cout << "export_word: ";
      }
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_DOCX}});
      if (debug) {
        std::cout << (clock() - start_s) / double(CLOCKS_PER_SEC) << "s"
            << std::endl;
      }
    }

    if (export_excel) {
      clock_t start_s = 0;
      if (debug) {
        start_s = clock();
        std::cout << "export_excel: ";
      }
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_XLSX}});
      if (debug) {
        std::cout << (clock() - start_s) / double(CLOCKS_PER_SEC) << "s"
            << std::endl;
      }
    }

    if (export_powerpoint) {
      clock_t start_s = 0;
      if (debug) {
        start_s = clock();
        std::cout << "export_powerpoint: ";
      }
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_PPTX}});
      if (debug) {
        std::cout << (clock() - start_s) / double(CLOCKS_PER_SEC) << "s"
            << std::endl;
      }
    }

    if (get_string_in_zone) {
      if (document != NULL) {
        PHOcrDocumentMaker::CreateDocument(document, filename);
        document->PHOcrSetSettings(phocrSettings);
      }
      long numberPages = document->PHOcrGetNumberOfPages();
      if (numberPages > 0) {
        PHOcrPagePtr page = (document->PHOcrGetPage(0));
        int zonecnt;
        std::string outfile = outputname + "_inzone.txt";
        FILE* fout_ = fopen(outfile.c_str(), "wb");
        for (zonecnt=0;zonecnt<zonestringnum;zonecnt++) {
          PHOcrRectangle<long> zone(zone_string_array[zonecnt][0], zone_string_array[zonecnt][1],
              zone_string_array[zonecnt][2], zone_string_array[zonecnt][3]);
          std::wstring str;
          page->PHOcrGetStringInAZone(str, zone, L"([A-Z])*");
          std::string outstring = ConvertToString(str);
          std::string sep_str = "\n===================================================================\n";
          std::string header = "Zone <" + std::to_string(zone_string_array[zonecnt][0])
              + "x" + std::to_string(zone_string_array[zonecnt][1]) + "x"
              + std::to_string(zone_string_array[zonecnt][2]) + "x"
              + std::to_string(zone_string_array[zonecnt][3]) + ">\nText: \n";
          fwrite(header.c_str(), sizeof(char), strlen(header.c_str()), fout_);
          fwrite(outstring.c_str(), sizeof(char), strlen(outstring.c_str()),
              fout_);
          fwrite(sep_str.c_str(), sizeof(char), strlen(sep_str.c_str()), fout_);
        }
        fclose(fout_);
      }
    }

    if (get_barcode_in_zone) {
      if (document != NULL) {
        PHOcrDocumentMaker::CreateDocument(document, filename);
        document->PHOcrSetSettings(phocrSettings);
      }
      long numberPages = document->PHOcrGetNumberOfPages();
      if (numberPages > 0) {
        PHOcrPagePtr page = (document->PHOcrGetPage(0));
        int zonecnt;
        std::string outfile = outputname + "_barcode_inzone.txt";
        FILE* fout_ = fopen(outfile.c_str(), "wb");
        for (zonecnt=0;zonecnt<zonebarcodenum;zonecnt++) {
          PHOcrRectangle<long> zone(zone_barcode_array[zonecnt][0], zone_barcode_array[zonecnt][1],
              zone_barcode_array[zonecnt][2], zone_barcode_array[zonecnt][3]);
          std::wstring str;
          page->PHOcrGetBarcodeInAZone(str, zone, L".");
          std::string outstring = ConvertToString(str);
          std::string sep_str = "\n===================================================================\n";
          std::string header = "Zone <" + std::to_string(zone_barcode_array[zonecnt][0])
              + "x" + std::to_string(zone_barcode_array[zonecnt][1]) + "x"
              + std::to_string(zone_barcode_array[zonecnt][2]) + "x"
              + std::to_string(zone_barcode_array[zonecnt][3]) + ">\nBarcode: \n";
          fwrite(header.c_str(), sizeof(char), strlen(header.c_str()), fout_);
          fwrite(outstring.c_str(), sizeof(char), strlen(outstring.c_str()),
              fout_);
          fwrite(sep_str.c_str(), sizeof(char), strlen(sep_str.c_str()), fout_);
        }
        fclose(fout_);
      }
    }
  } catch (...) {
    if (filelist != 0) {
      fclose(filelist);
    }
    return 1;
  }
  if (filelist != 0) {
    fclose(filelist);
  }
  char *line = NULL;
  size_t line_len=0;
  FILE *status;
  int peak = 0;
  int rss = 0;
  status = fopen("/proc/self/status", "r");
  if (!status) return 1;
  /* Read memory size data from /proc/pid/status */
  while ( getline( &line, &line_len, status) != -1 ) {
    if( !strncmp(line, "VmPeak:", 6) ) {
      sscanf(&line[7],"%d",&peak);
    } else if( !strncmp(line, "VmRSS:", 6) ) {
      sscanf(&line[7],"%d",&rss);
    }
  }
  std::cout<<"VmPeak size is :"<<peak<<"KB"<<std::endl;
  std::cout<<"VmRSS size is :"<<rss<<"KB"<<std::endl;
  free(line);
  fclose(status);
  return 0;
}
