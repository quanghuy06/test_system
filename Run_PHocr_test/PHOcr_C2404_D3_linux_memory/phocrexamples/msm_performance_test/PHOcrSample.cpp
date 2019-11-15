/*****************************************************************************
 * @file    PHOcrExample.cpp
 * @brief  Provides example for building the application use PHOcr library.
 *
 * (C) TOSHIBA TEC Corporation - 2018
 *****************************************************************************/
#include "PHOcrDocumentMaker.h"
#include "BarcodeMode.h"
#include "PHOcrPageMaker.h"
#include "PHOcrSettings.h"
#include "PHOcrStringHelper.h"
#include "PHOcrStatus.h"
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

bool mem_Log = false;
// For Debug function
void printMemoryStatus()
{
  if (mem_Log == true) {
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
  }
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

double get_dtime(void){
  struct timeval tv;
  gettimeofday(&tv, NULL);
  return ((double)(tv.tv_sec) + (double)(tv.tv_usec) * 0.001 * 0.001);
}

// For Debug function

/**
 * Print help to stdout
*/
void PrintHelp(int line_num) {
  std::cout << line_num << std::endl;
  std::cout
    <<  "Usage: PHOcrExe.exe [Options] language filelistpath\n"
      "Option list: \n"
      "    -word            Export OCR result in MS Word format\n"
      "    -excel           Export OCR result in MS Excel format\n"
      "    -excel_1sheet     Export OCR result in MS Excel format with 1sheet\n"
      "    -pptx            Export OCR result in MS Power Point format\n"
      "    -txt             Export OCR result in txt file\n"
      "    -xml             Export OCR result in xml file\n"
      "    -pdf             Export OCR result in pdf file\n"
      "    -pdfa            Export OCR result in pdf file with PDF/A compliance\n"
      "    -barcode         Get barcode data\n"
      "    -layout          Layout the characters/words following the\n"
      "                     order left to right, top to bottom\n"
      "    -nodeskew        Deskew function OFF\n"
      "    -memLogOut       Output memory Log\n"
      "    -textphoto       Input image is textphoto mode\n"
      "    -photo           Input image is photo mode\n"
      "    -Color           Input image is Color\n"
      "    -Mono            Input image is Mono\n"
      "    -Gray            Input image is Gray\n"
      "    -getStringInZone <x,y,width,height> \n"
      "                     Get text in a zone, export to txt file \n"
      "    -getBarcodeInZone <x,y,width,height> \n"
      "                     Get barcode in a zone, export to txt file \n"
      "    language         Set language for input image, Supported:\n"
      "                         EFGIS languages:     English, French, German, Italian, Spanish,\n"
      "                         Asian languages:     Japanese, ChineseSimplified, ChineseTraditional, Korean, Arabic\n"
      "                         European languages:  Danish, Dutch, Finnish, Greek-Ancient, Greek-Modern, Norwegian,\n"
      "                                              Polish, Portuguese, Russian, Swedish, Turkish\n"
      "                     Language is case insensitive\n"
      "                     Default language: English\n"
    << std::endl;
}

/**
 * Sample main
*/
int main(int argc, char** argv) {
  if (argc < 3) {
    // Not enough parameters, print help to use
    PrintHelp(__LINE__);
    return 1;
  }
  double iProcessStartTime=0;
  double iProcessEndTime=0;
  std::string tmp;

  printf("%s PHOcr Sample running start!!\n", GetTime(tmp));
    iProcessStartTime = get_dtime();

  // Transfer program parameters to variable value
  bool export_word = false;
  bool export_excel = false;
  bool excel_1sheet = false;
  bool export_powerpoint = false;
  bool export_txt = false;
  bool export_xml = false;
  bool export_pdf = false;
  bool export_pdfa = false;
  bool get_barcode = false;
  PHOcrDataMode dataMode = PHOcrDataMode::DM_LOW_CONTENT;
  //Settings for Text ZoneOCR
  bool get_string_in_zone = false;
  int zonestringnum=0;
  std::vector<std::vector<int>> zone_string_array;
  zone_string_array.resize(3);
  //Settings for Barcode ZoneOCR
  bool get_barcode_in_zone = false;
  int zonebarcodenum=0;
  std::vector<std::vector<int>> zone_barcode_array;
  zone_barcode_array.resize(3);
  //Settings for OCR option
  bool deskew_func = true;
  PHOcrInputOriginalMode originalMode = PHOcrInputOriginalMode::IOM_TEXT_MODE;
  PHOcrInputColorMode colorMode = PHOcrInputColorMode::ICM_AUTO_COLOR_MODE;
  bool layout_charater_coordinate = false;
  unsigned int barcode_mode = BarcodeMode::BM_1D_BARCODE;

  PHOcrPagePtr page;
  PHOcrDocumentPtr document;

  FILE* filelist = 0;
  char inputFileName[MAX_PATH];

  //Analyze arg and set settings.
  for (int i = 1; i < argc; i++) {
    //export format arg
    if (strcmp(argv[i], "-word") == 0) {
      export_word = true;
      dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
    }
    if (strcmp(argv[i], "-excel") == 0) {
      export_excel = true;
      dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
    }
    if (strcmp(argv[i], "-excel_1sheet") == 0) {
      export_excel = true;
      excel_1sheet=true;
    }
    if (strcmp(argv[i], "-pptx") == 0) {
      export_powerpoint = true;
      dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
    }
    if (strcmp(argv[i], "-txt") == 0) {
      export_txt = true;
    }
    if (strcmp(argv[i], "-xml") == 0) {
      export_xml = true;
      dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
    }
    if (strcmp(argv[i], "-pdf") == 0) {
      export_pdf = true;
      dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
    }
    if (strcmp(argv[i], "-pdfa") == 0) {
      export_pdfa = true;
      dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
    }
    if (strcmp(argv[i], "-barcode") == 0) {
      get_barcode = true;
    }
    //text zoneOCR rect data
    if (strcmp(argv[i], "-getStringInZone") == 0) {
      get_string_in_zone = true;
      if (i + 1 < argc) {
        std::string zonenum = argv[i + 1];
        zonestringnum=std::stoi(zonenum);
        if (0 >= zonestringnum || 3 < zonestringnum) {
          PrintHelp(__LINE__);
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
              PrintHelp(__LINE__);
              return 1;
            }
            std::cout << "ZoneInfo" << zonecnt << "\t x:" << zone_string_array[zonecnt][0] << "\t y:" << zone_string_array[zonecnt][1] << "\t width:" <<  zone_string_array[zonecnt][2] << "\t height:" <<  zone_string_array[zonecnt][3] << std::endl;
          }
        } else {
          PrintHelp(__LINE__);
          return 1;
        }
      }
    }
    //barcode zoneOCR rect data
    if (strcmp(argv[i], "-getBarcodeInZone") == 0) {
      get_barcode_in_zone = true;
      if (i + 1 < argc) {
        std::string zonenum = argv[i + 1];
        zonebarcodenum=std::stoi(zonenum);
        if (0 >= zonebarcodenum || 3 < zonebarcodenum) {
          PrintHelp(__LINE__);
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
              PrintHelp(__LINE__);
              return 1;
            }
            std::cout << "ZoneInfo(Barcode)" << zonecnt << "\t x:" << zone_barcode_array[zonecnt][0] << "\t y:" << zone_barcode_array[zonecnt][1] << "\t width:" << zone_barcode_array[zonecnt][2] << "\t height:" << zone_barcode_array[zonecnt][3] << std::endl;
          }
        } else {
          PrintHelp(__LINE__);
          return 1;
        }
      }
    }
    //Barcode mode
    if (strcmp(argv[i], "-bm") == 0) {
      if (i + 1 < argc) {
        barcode_mode = stoi(std::string(argv[i + 1]));
      }
      i++;
    }
    //Layout mode
    if (strcmp(argv[i], "-layout") == 0) {
      layout_charater_coordinate = true;
    }
    //Deskew function off
    if (strcmp(argv[i], "-nodeskew") == 0) {
      deskew_func = false;
    }
    //Memory Log output
    if (strcmp(argv[i], "-memLogOut") == 0) {
      mem_Log = true;
    }
    //Original mode
    if (strcmp(argv[i], "-textphoto") == 0) {
      originalMode = PHOcrInputOriginalMode::IOM_TEXT_PHOTO_MODE;
    }
    if (strcmp(argv[i], "-photo") == 0) {
      originalMode = PHOcrInputOriginalMode::IOM_PHOTO_MODE;
    }
    //Color mode
    if (strcmp(argv[i], "-Mono") == 0) {
      colorMode = PHOcrInputColorMode::ICM_BLACK_MODE;
    }
    if (strcmp(argv[i], "-Color") == 0) {
      colorMode = PHOcrInputColorMode::ICM_FULL_COLOR_MODE;
    }
    if (strcmp(argv[i], "-Gray") == 0) {
      colorMode = PHOcrInputColorMode::ICM_GRAY_SCALE_MODE;
    }

  }

  // Check condition of program parameters
  if (!export_pdf && !export_pdfa && !export_txt && !export_xml && !export_word && !export_excel && !export_powerpoint && !get_string_in_zone && !get_barcode_in_zone && !get_barcode) {
    PrintHelp(__LINE__);
    return 0;
  }

  strcpy(inputFileName,argv[argc - 1]);
  std::wstring filename = ConvertToWString(argv[argc - 1]);

  //get image path from file list
  filelist = fopen( argv[argc -1],"r" );
  if( filelist == 0 ) {
    PrintHelp(__LINE__);
    return 1;
  }
  //Create Document obj
  try {
    PHOcrDocumentMaker::CreateDocument(document);
    if (document == NULL) {
      printf("can not create document\n");
      return 1;
    }
  } catch (...) {
    PrintHelp(__LINE__);
    return 1;
  }
  // Get output filename
  std::string outputname="AllPages";
  std::wstring outputname_w;
  outputname_w = ConvertToWString(outputname);

  std::string language;
  language = argv[argc - 2];
  if (language.at(0) == '-') {
    language = "English";
  }
  std::wstring language_w = ConvertToWString(language);

  PHOcrSettings phocrSettings;
  phocrSettings.SetOCRLanguage(language_w);
  phocrSettings.SetBarcodeMode(barcode_mode);
  phocrSettings.SetPdfImageExportMode(PHOcrImageExportMode::IEM_ORIGINAL);
  phocrSettings.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
  phocrSettings.SetExportInOneSheet(excel_1sheet);
  phocrSettings.SetUsingImageBandingMechanism(false);
  // Deskew function
  phocrSettings.SetAutoDeskew(deskew_func);
  phocrSettings.SetAutoOrientation(deskew_func);
  //
  phocrSettings.SetInputDocumentType(PHOcrInputDocumentType::IDT_SCANNED_DOCUMENT);
  //
  phocrSettings.SetInputOriginalMode(originalMode);
  //
  phocrSettings.SetInputColorMode(colorMode);
  //
  phocrSettings.SetDataMode(dataMode);
  //
  phocrSettings.SetProductSetting(PHOcrSupportProduct::SP_SING20_PRODUCTNAME);
  // Configure for document
  document->PHOcrSetSettings(phocrSettings);
  printf("%s PHOcr Processing start!!\n", GetTime(tmp));
  /**************/
  /* Processing */
  /**************/
  try {
    /********************/
    /* Text OCR process */
    /********************/
    if(export_pdf || export_pdfa || export_txt || export_xml || export_word || export_excel || export_powerpoint) {
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
          PHOcrPageMaker::CreatePage(page, filename);
          page->PHOcrSetSettings(phocrSettings);
          page->PHOcrSetLogLevel(PHOcrLogLevel::LL_DIAGNOSTIC);
          document->PHOcrAppendPages({page});
          document->PHOcrSetSettings(phocrSettings);
          printMemoryStatus();
        } catch (...) {
          PrintHelp(__LINE__);
          return 1;
        }
      }
    }
    /********************************/
    /* Barcode recoginition process */
    /********************************/
    if (get_barcode) {
      long pagenum; /* Decode target page number */
      std::vector<std::wstring> barcodes;   /* decoded barcode data */
      // add page from filelist
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
          PHOcrPageMaker::CreatePage(page, filename);
          document->PHOcrAppendPages({page});
        } catch (...) {
          PrintHelp(__LINE__);
          return 1;
        }
      }
      long numberPages = document->PHOcrGetNumberOfPages(); /* Total page number */
      //Decode Barcode and print
      for (pagenum=0;pagenum < numberPages;pagenum++) {
        std::cout << "Barcode PageNo:" << pagenum+1 << std::endl;
        page=document->PHOcrGetPage(pagenum);
        //ToDo:Why  does not page object inherit document object settings?
        phocrSettings.SetBarcodeMode(barcode_mode);
        page->PHOcrSetSettings(phocrSettings);
        std::string tmp;
        page->PHOcrGetAllBarcodes(barcodes);
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
    printf("%s PHOcr Processing end!!\n", GetTime(tmp));
    if (document->PHOcrGetNumberOfPages() == 1) {
      outputname_w = L"MSM_01_TableLayout_Page01_JPN_ColorToMono200dpi";
    }
    /******************/
    /* Export process */
    /******************/
    // Export TXT format
    if (export_txt) {
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_TXT}});
    }
    // Export XML format
    if (export_xml) {
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_XML}});
    }
    // Exporting PDF format
    if (export_pdf) {
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_PDF}});
    }
    // Exporting PDF format
    if (export_pdfa) {
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_PDFA}});
    }
    // Exporting Word format
    if (export_word) {
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_DOCX}});
    }
    // Exporting Excel format
    if (export_excel) {
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_XLSX}});
    }
    // Exporting PPT format
    if (export_powerpoint) {
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_PPTX}});
    }
    // Export bounding box file
    if (layout_charater_coordinate) {
      document->PHOcrExport({{outputname_w, PHOcrExportFormat::EF_BB}});
    }
    /**************************************/
    /* Output Text zoneOCR result process */
    /**************************************/
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
          page->PHOcrGetStringInAZone(str, zone, L".*");
          std::string outstring = ConvertToString(str);
          std::string sep_str = "\n===================================================================\n";
          std::string header = "Zone <" + std::to_string(zone_string_array[zonecnt][0]) + "x" + std::to_string(zone_string_array[zonecnt][1]) + "x" + std::to_string(zone_string_array[zonecnt][2]) + "x" + std::to_string(zone_string_array[zonecnt][3]) + ">\nText: \n";
          fwrite(header.c_str(), sizeof(char), strlen(header.c_str()), fout_);
          fwrite(outstring.c_str(), sizeof(char), strlen(outstring.c_str()), fout_);
          fwrite(sep_str.c_str(), sizeof(char), strlen(sep_str.c_str()), fout_);
        }
        fclose(fout_);
      }
    }
    /*****************************************/
    /* Output Barcode zoneOCR result process */
    /*****************************************/
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
          page->PHOcrGetBarcodeInAZone(str, zone, L".*");
          std::string outstring = ConvertToString(str);
          std::string sep_str = "\n===================================================================\n";
          std::string header = "Zone <" + std::to_string(zone_barcode_array[zonecnt][0]) + "x" + std::to_string(zone_barcode_array[zonecnt][1]) + "x" + std::to_string(zone_barcode_array[zonecnt][2]) + "x" + std::to_string(zone_barcode_array[zonecnt][3]) + ">\nBarcode: \n";
          fwrite(header.c_str(), sizeof(char), strlen(header.c_str()), fout_);
          fwrite(outstring.c_str(), sizeof(char), strlen(outstring.c_str()), fout_);
          fwrite(sep_str.c_str(), sizeof(char), strlen(sep_str.c_str()), fout_);
        }
        fclose(fout_);
      }
    }
    printf("%s PHOcr export end!!\n", GetTime(tmp));

  } catch (...) {
    if (filelist != 0) {
      fclose(filelist);
    }
    return 1;
  }
  if (filelist != 0) {
    fclose(filelist);
  }
  printf("%s PHOcr Sample running end!!\n", GetTime(tmp));
    iProcessEndTime = get_dtime();

    printf("Process_Time %.3f\n", iProcessEndTime-iProcessStartTime);

  return 0;
}
