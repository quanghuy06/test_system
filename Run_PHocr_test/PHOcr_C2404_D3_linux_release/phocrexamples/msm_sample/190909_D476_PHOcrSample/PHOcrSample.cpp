/*****************************************************************************
 * @file		PHOcrExample.cpp
 * @brief	 Provides example for building the application use PHOcr library.
 *
 * (C) TOSHIBA TEC Corporation - 2018
 *****************************************************************************/
#include "PHOcrDocumentMaker.h"
#include "PHOcrPageMaker.h"
#include "PHOcrSettings.h"
#include "PHOcrStringHelper.h"
#include "PHOcrStatus.h"
#include <sys/time.h>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <fstream>
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
#include <map>
#include "BarcodeMode.h"
#ifndef MAX_PATH
#define MAX_PATH 4096
#endif

using namespace phocr;

bool mem_Log = false;

bool CancelDecisionMethod() {
	std::ifstream ifs("./cancel");
	std::string str;
	ifs>>str;
	if (str == "1") {
		std::cout << "cancel!!!" <<std::endl;
		return true;
	} else {
		return false;
	}
}

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
		<<	"Usage: PHOcrExe.exe [Options] language filelistpath\n"
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
			"    -memory          OCR result get using memory structure\n"
			"    -nodeskew        Deskew function OFF\n"
			"    -memLogOut       Output memory Log\n"
			"    -textphoto       Input image is textphoto mode\n"
			"    -photo           Input image is photo mode\n"
			"    -Color           Input image is Color\n"
			"    -Mono            Input image is Mono\n"
			"    -Gray            Input image is Gray\n"
			"    -res             Change output resolution(only effect PDF)\n"
			"    -iem             Change output image mode(only effect PDF)\n"
			"                     0:IEM_ORIGINAL,1:IEM_BINARY,2:IEM_HALFTONE,3:IEM_HALFTONE_PHOTO\n"
			"    -ImageBanding    SetUsingImageBandingMechanism is true\n"
			"    -getStringInZone <x,y,width,height> \n"
			"                     Get text in a zone, export to txt file \n"
			"    -getBarcodeInZone <x,y,width,height> \n"
			"                     Get barcode in a zone, export to txt file \n"
			"    -PSMode      \n"
			"                 Enter size in pages before OCR\n"
			"    -PaperSize      \n"
			"                 A4_PORTRAIT        11\n"
			"                 A4_LANDSCAPE       12\n"
			"                 and more       \n"
			"    -OutFile     <FileName> \n"
			"    language         Set language for input image, Supported:\n"
			"                         EFGIS languages:     English, French, German, Italian, Spanish,\n"
			"                         Asian languages:     Japanese, ChineseSimplified, ChineseTraditional, Korean, Arabic\n"
			"                         European languages:  Danish, Dutch, Finnish, Greek-Ancient, Greek-Modern, Norwegian,\n"
			"                                              Polish, Portuguese, Russian, Swedish, Turkish\n"
			"                     Language is case insensitive\n"
			"                     Default language: English\n"
		<< std::endl;
}

void PrintHelpBarcodeParameter(int line_num) {
    std::cout << line_num << std::endl;
    std::cout
        <<  "Usage: PHOcrExe.exe [Parameters]\n"
            "Barcode START=========================\n"
            "    BarcodeMode::BM_AUTO               = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_AUTO << "\n"
            "    BarcodeMode::BM_1D_BARCODE         = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_1D_BARCODE << "\n"
            "    BarcodeMode::BM_2D_BARCODE         = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_2D_BARCODE << "\n"
            "    BarcodeMode::BM_CODE_39            = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_CODE_39 << "\n"
            "    BarcodeMode::BM_CODE_93            = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_CODE_93 << "\n"
            "    BarcodeMode::BM_CODE_128           = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_CODE_128 << "\n"
            "    BarcodeMode::BM_CODABAR            = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_CODABAR << "\n"
            "    BarcodeMode::BM_IATA_2_OF_5        = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_IATA_2_OF_5 << "\n"
            "    BarcodeMode::BM_INTERLEAVED_2_OF_5 = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_INTERLEAVED_2_OF_5 << "\n"
            "    BarcodeMode::BM_INDUSTRIAL_2_OF_5  = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_INDUSTRIAL_2_OF_5 << "\n"
            "    BarcodeMode::BM_MATRIX_2_OF_5      = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_MATRIX_2_OF_5 << "\n"
            "    BarcodeMode::BM_UCC_128            = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_UCC_128 << "\n"
            "    BarcodeMode::BM_UPC_A              = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_UPC_A << "\n"
            "    BarcodeMode::BM_UPC_E              = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_UPC_E << "\n"
            "    BarcodeMode::BM_PATCH              = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_PATCH << "\n"
            "    BarcodeMode::BM_POSTNET            = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_POSTNET << "\n"
            "    BarcodeMode::BM_AZTEC              = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_AZTEC << "\n"
            "    BarcodeMode::BM_DATAMATRIX         = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_DATAMATRIX << "\n"
            "    BarcodeMode::BM_MAXICODE           = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_MAXICODE << "\n"
            "    BarcodeMode::BM_PDF417             = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_PDF417 << "\n"
            "    BarcodeMode::BM_QRCODE             = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_QRCODE << "\n"
            "    BarcodeMode::BM_EAN_8              = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_EAN_8 << "\n"
            "    BarcodeMode::BM_EAN_13             = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_EAN_13 << "\n"
            "    BarcodeMode::BM_MAXIMUM_VALUE      = 0x"<< std::hex << std::setw(8) << std::setfill('0') << BarcodeMode::BM_MAXIMUM_VALUE << "\n"
            "Barcode END=========================\n"
        << std::endl;
}
/**
 * Sample main
*/
int main(int argc, char** argv) {
    double iProcessStartTime=0;
    double iProcessEndTime=0;
    double i1ProcStartTime=0;
    double i1ProcEndTime=0;

	if ((argc < 3) ||  (strcmp(argv[1], "-help") == 0)){
		// Not enough parameters, print help to use
		PrintHelp(__LINE__);
        PrintHelpBarcodeParameter(__LINE__);
		return 1;
	}
	std::string tmp;
    std::map<std::string, int> mp;
    std::map<int, std::string> mp2;

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
	bool output_memory = false;
	bool get_barcode = false;
	int resolution = 0;
	PHOcrDataMode dataMode = PHOcrDataMode::DM_LOW_CONTENT;
	PHOcrImageExportMode imageExportMode = PHOcrImageExportMode::IEM_ORIGINAL;
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
	bool ImageBanding = false;
	PHOcrInputOriginalMode originalMode = PHOcrInputOriginalMode::IOM_TEXT_MODE;
	PHOcrInputColorMode colorMode = PHOcrInputColorMode::ICM_AUTO_COLOR_MODE;
	bool layout_charater_coordinate = false;
	unsigned int barcode_mode = 0;
    std::string target_paper_size;
    PHOcrStandardPaperName export_paper_size=PHOcrStandardPaperName::SP_A4_PORTRAIT;
    bool PSMode = false;
	std::string out_file_name="";

	//Settings for Barcode
    long pagenum;                       /* Decode target page number */
    std::vector<std::wstring> barcodes; /* decoded barcode data */
    long numberPages;                   /* Total page number */

    //OCR Result
    PHOcrStatus ocr_result = PHOcrStatus::PHOCR_OK;

	//OCR result data ptr
	PHOcrDocumentDataPtr DocData;
	std::vector<PHOcrPageDataPtr> PagesData;
	std::vector<PHOcrCareaDataPtr> CareaData;
	std::vector<PHOcrParagraphDataPtr> ParagraphData;
	std::vector<PHOcrLineDataPtr> LineData;
	std::vector<PHOcrWordDataPtr> WordData;
	std::vector<PHOcrCharacterDataPtr> CharData;

    std::vector<PHOcrBarcodeDataPtr> Barcodedata;

    // Setting output path before add any page
    std::vector<phocr::PHOcrExportSetting> phocrexportSettings;
    phocr::PHOcrExportSetting temp_phocrexportSettings;

	PHOcrPagePtr page;
	PHOcrDocumentPtr document;

	FILE* filelist = 0;
	char inputFileName[MAX_PATH];

    /*__mano__*/
    std::wstring testmano;
    std::string str = "�܂�";
    setlocale(LC_CTYPE, "");

    wchar_t *wcs = new wchar_t[str.length() + 1];
    mbstowcs(wcs, str.c_str(), str.length() + 1);

	testmano = wcs;
	delete [] wcs;

	std::wcout << testmano <<std::endl;

    /*__mano__*/




	//Analyze arg and set settings.
	for (int i = 1; i < argc; i++) {
		//export format arg
		if (strcmp(argv[i], "-word") == 0) {
            printf("%s ", argv[i]);
			export_word = true;
			export_xml = true;
			dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
            temp_phocrexportSettings.setExportFormat(PHOcrExportFormat::EF_DOCX);
            phocrexportSettings.push_back(temp_phocrexportSettings);
		}
		if (strcmp(argv[i], "-excel") == 0) {
            printf("%s ", argv[i]);
			export_excel = true;
			export_xml = true;
			dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
            temp_phocrexportSettings.setExportFormat(PHOcrExportFormat::EF_XLSX);
            phocrexportSettings.push_back(temp_phocrexportSettings);
		}
		if (strcmp(argv[i], "-excel_1sheet") == 0) {
            printf("%s ", argv[i]);
			export_excel = true;
			export_xml = true;
			excel_1sheet=true;
            temp_phocrexportSettings.setExportFormat(PHOcrExportFormat::EF_XLSX);
            phocrexportSettings.push_back(temp_phocrexportSettings);
		}
		if (strcmp(argv[i], "-pptx") == 0) {
            printf("%s ", argv[i]);
			export_powerpoint = true;
			export_xml = true;
			dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
            temp_phocrexportSettings.setExportFormat(PHOcrExportFormat::EF_PPTX);
            phocrexportSettings.push_back(temp_phocrexportSettings);
		}
		if (strcmp(argv[i], "-txt") == 0) {
            printf("%s ", argv[i]);
			export_txt = true;
            temp_phocrexportSettings.setExportFormat(PHOcrExportFormat::EF_TXT);
            phocrexportSettings.push_back(temp_phocrexportSettings);
		}
		if (strcmp(argv[i], "-xml") == 0) {
            printf("%s ", argv[i]);
			export_xml = true;
			dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
            temp_phocrexportSettings.setExportFormat(PHOcrExportFormat::EF_XML);
            phocrexportSettings.push_back(temp_phocrexportSettings);
		}
		if (strcmp(argv[i], "-pdf") == 0) {
            printf("%s ", argv[i]);
			export_pdf = true;
			dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
            temp_phocrexportSettings.setExportFormat(PHOcrExportFormat::EF_PDF);
            phocrexportSettings.push_back(temp_phocrexportSettings);
		}
		if (strcmp(argv[i], "-pdfa") == 0) {
            printf("%s ", argv[i]);
			export_pdfa = true;
			dataMode = PHOcrDataMode::DM_HIGH_CONTENT;
            temp_phocrexportSettings.setExportFormat(PHOcrExportFormat::EF_PDFA);
            phocrexportSettings.push_back(temp_phocrexportSettings);
		}
		if (strcmp(argv[i], "-barcode") == 0) {
            printf("%s ", argv[i]);
			get_barcode = true;
		}
		//text zoneOCR rect data
		if (strcmp(argv[i], "-getStringInZone") == 0) {
            printf("%s ", argv[i]);
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
						std::cout << "ZoneInfo" << zonecnt << "\t x:" << zone_string_array[zonecnt][0] << "\t y:" << zone_string_array[zonecnt][1] << "\t width:" <<	zone_string_array[zonecnt][2] << "\t height:" <<	zone_string_array[zonecnt][3] << std::endl;
					}
				} else {
					PrintHelp(__LINE__);
					return 1;
				}
			}
		}
		//barcode zoneOCR rect data
		if (strcmp(argv[i], "-getBarcodeInZone") == 0) {
            printf("%s ", argv[i]);
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
						std::cout << "ZoneInfo(Barcode)" << zonecnt << "\t x:" << zone_barcode_array[zonecnt][0] << "\t y:" << zone_barcode_array[zonecnt][1] << "\t width:" <<	zone_barcode_array[zonecnt][2] << "\t height:" <<	zone_barcode_array[zonecnt][3] << std::endl;
					}
				} else {
					PrintHelp(__LINE__);
					return 1;
				}
			}
		}
		//Barcode mode
		if (strcmp(argv[i], "-bm") == 0) {
            int b_Mode=0;
            printf("%s ", argv[i]);
            std::string target_BarcodeMode;
			if (i + 1 < argc) {
                mp["BM_AUTO"]=BarcodeMode::BM_AUTO;
                mp["BM_1D_BARCODE"]=BarcodeMode::BM_1D_BARCODE;
                mp["BM_2D_BARCODE"]=BarcodeMode::BM_2D_BARCODE;
                mp["BM_CODE_39"]=BarcodeMode::BM_CODE_39;
                mp["BM_CODE_93"]=BarcodeMode::BM_CODE_93;
                mp["BM_CODE_128"]=BarcodeMode::BM_CODE_128;
                mp["BM_CODABAR"]=BarcodeMode::BM_CODABAR;
                mp["BM_IATA_2_OF_5"]=BarcodeMode::BM_IATA_2_OF_5;
                mp["BM_INTERLEAVED_2_OF_5"]=BarcodeMode::BM_INTERLEAVED_2_OF_5;
                mp["BM_INDUSTRIAL_2_OF_5"]=BarcodeMode::BM_INDUSTRIAL_2_OF_5;
                mp["BM_MATRIX_2_OF_5"]=BarcodeMode::BM_MATRIX_2_OF_5;
                mp["BM_UCC_128"]=BarcodeMode::BM_UCC_128;
                mp["BM_UPC_A"]=BarcodeMode::BM_UPC_A;
                mp["BM_UPC_E"]=BarcodeMode::BM_UPC_E;
                mp["BM_PATCH"]=BarcodeMode::BM_PATCH;
                mp["BM_POSTNET"]=BarcodeMode::BM_POSTNET;
                mp["BM_AZTEC"]=BarcodeMode::BM_AZTEC;
                mp["BM_DATAMATRIX"]=BarcodeMode::BM_DATAMATRIX;
                mp["BM_MAXICODE"]=BarcodeMode::BM_MAXICODE;
                mp["BM_PDF417"]=BarcodeMode::BM_PDF417;
                mp["BM_QRCODE"]=BarcodeMode::BM_QRCODE;
                mp["BM_EAN_8"]=BarcodeMode::BM_EAN_8;
                mp["BM_EAN_13"]=BarcodeMode::BM_EAN_13;
                mp["BM_MAXIMUM_VALUE"]=BarcodeMode::BM_MAXIMUM_VALUE;

                target_BarcodeMode = argv[i + 1];
                //Merge multiple parameters. (Is there a ',' in the string?)
                if (target_BarcodeMode.find(",") != -1) {
                    for (b_Mode = 0; target_BarcodeMode.find(",", b_Mode+1) != -1;)
                    {
                        int size=target_BarcodeMode.find(",", b_Mode+1);
                        printf("%s(0x%x), ",target_BarcodeMode.substr(b_Mode, size-b_Mode).c_str(), mp[target_BarcodeMode.substr(b_Mode, size-b_Mode).c_str()]);

                        if (mp[target_BarcodeMode.substr(b_Mode, size-b_Mode).c_str()] == 0)
                        {
                            PrintHelpBarcodeParameter(__LINE__);
                            return 1;
                        }

                        barcode_mode |= mp[target_BarcodeMode.substr(b_Mode, size-b_Mode).c_str()];
                        b_Mode=size+1;

                    }
                }

                if (mp[target_BarcodeMode.substr(b_Mode).c_str()] == 0)
                {
                    PrintHelpBarcodeParameter(__LINE__);
                    return 1;
                }

                barcode_mode |= mp[target_BarcodeMode.substr(b_Mode).c_str()];
                printf("%s(0x%x) ",target_BarcodeMode.substr(b_Mode).c_str(), mp[target_BarcodeMode.substr(b_Mode).c_str()]);
                printf(" barcode_mode = 0x%0x\n", barcode_mode);
                if (barcode_mode == 0)
                {
                    PrintHelpBarcodeParameter(__LINE__);
                    return 1;
                }
			}
			i++;
		}
		//MemMode
		if (strcmp(argv[i], "-memory") == 0) {
            printf("%s ", argv[i]);
			output_memory = true;
		}


		//Layout mode
		if (strcmp(argv[i], "-layout") == 0) {
            printf("%s ", argv[i]);
			layout_charater_coordinate = true;
		}
		//Deskew function off
		if (strcmp(argv[i], "-nodeskew") == 0) {
            printf("%s ", argv[i]);
			deskew_func = false;
		}
		if (strcmp(argv[i], "-ImageBanding") == 0) {
            printf("%s ", argv[i]);
			ImageBanding = true;
		}
		//Memory Log output
		if (strcmp(argv[i], "-memLogOut") == 0) {
            printf("%s ", argv[i]);
			mem_Log = true;
		}
		//Original mode
		if (strcmp(argv[i], "-textphoto") == 0) {
            printf("%s ", argv[i]);
			originalMode = PHOcrInputOriginalMode::IOM_TEXT_PHOTO_MODE;
		}
		if (strcmp(argv[i], "-photo") == 0) {
            printf("%s ", argv[i]);
			originalMode = PHOcrInputOriginalMode::IOM_PHOTO_MODE;
		}
		//Color mode
		if (strcmp(argv[i], "-Mono") == 0) {
            printf("%s ", argv[i]);
			colorMode = PHOcrInputColorMode::ICM_BLACK_MODE;
		}
		if (strcmp(argv[i], "-Color") == 0) {
            printf("%s ", argv[i]);
			colorMode = PHOcrInputColorMode::ICM_FULL_COLOR_MODE;
		}
		if (strcmp(argv[i], "-Gray") == 0) {
            printf("%s ", argv[i]);
			colorMode = PHOcrInputColorMode::ICM_GRAY_SCALE_MODE;
		}
        //PaperSize
        if (strcmp(argv[i], "-PSMode") == 0) {
            printf("%s ", argv[i]);
            PSMode = true;
        }
        //PaperSize
        if (strcmp(argv[i], "-PaperSize") == 0) {
            printf("%s ", argv[i]);
            if (i + 1 < argc) {
                target_paper_size = std::string(argv[i + 1]);
                export_paper_size = (PHOcrStandardPaperName)atoi(target_paper_size.c_str());
                printf("export_paper_size = %d\n", export_paper_size);
                i++;
            }
        }
        //Output resolution
        if (strcmp(argv[i], "-res") == 0) {
            if (i + 1 < argc) {
                printf("resolution = %s\n", argv[i + 1]);
                resolution = atoi(argv[i + 1]);
                if (resolution < 100 || resolution > 600) {
                    resolution = 0;
                }
                i++;
            }
        }
        //Image Export Mode
        if (strcmp(argv[i], "-iem") == 0) {
            if (i + 1 < argc) {
                unsigned int iem_tmp=atoi(argv[i + 1]);
                if (iem_tmp <= 3) {
					imageExportMode = (PHOcrImageExportMode)iem_tmp;
                    printf("IEM = %d\n", iem_tmp);
                }
                i++;
            }
        }

        //OutputFileName
        if (strcmp(argv[i], "-OutFile") == 0) {
            printf("%s", argv[i]);
            if (i + 1 < argc) {
                out_file_name = std::string(argv[i + 1]);
                printf("Name = %s\n", out_file_name.c_str());
                i++;
            }
        }


	}
    printf("\n");


	// Check condition of program parameters
	if (!export_pdf && !export_pdfa && !export_txt && !export_xml && !export_word && !export_excel && !export_powerpoint && !get_string_in_zone && !get_barcode_in_zone && !get_barcode && !output_memory) {
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
	if (out_file_name != "") {
        outputname = out_file_name;
    }
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
	phocrSettings.SetPdfImageExportMode(imageExportMode);
	phocrSettings.SetPdfExportMode(PHOcrPDFExportMode::PEM_SEARCHABLE_PDF);
	phocrSettings.SetExportInOneSheet(excel_1sheet);
	phocrSettings.SetUsingImageBandingMechanism(ImageBanding);
	// Export bounding box file
//	phocrSettings.SetExportBoundingBoxFile(layout_charater_coordinate);
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

    //PaperSizeSetting
    phocrSettings.SetTargetPaperSize(export_paper_size);

    //Resolution
    if (resolution != 0) {
        phocrSettings.SetPdfOutputDpi(resolution);
        printf("set resolution=%dDPI\n",phocrSettings.GetPdfOutputDpi());
    }

	// Configure for document
	document->PHOcrSetSettings(phocrSettings);
	// set cancel decision callback
	document->PHOcrSetCancelDecisionMethod((PHOcrCancelDecisionMethod)CancelDecisionMethod);
	printf("%s PHOcr Processing start!!\n", GetTime(tmp));


	/**************/
	/* Processing */
	/**************/
	try {
		/********************/
		/* Text OCR process */
		/********************/
		if(export_pdf || export_pdfa || export_txt || export_xml || export_word || export_excel || export_powerpoint || output_memory) {


            std::vector<PHOcrPagePtr> pages;
            std::vector<std::wstring> list;
            int listcount=0;

			while(0 != fgets( inputFileName, MAX_PATH, filelist )) {
				int len = strlen( inputFileName );
				//fgets returns additional symbols( \n or \r\n )
				//--------------remove \r\n ...
                if (PSMode) {
                    printf("  PSMode Size -----> ");
                    scanf("%d", &export_paper_size);
                    printf("export_paper_size = %d\n", export_paper_size);
                    //PaperSizeSetting
                    phocrSettings.SetTargetPaperSize((PHOcrStandardPaperName)export_paper_size);
				}
				if( inputFileName[len-1] < ' ' ) {
					inputFileName[len-1] = 0;
					if( inputFileName[len-2] < ' ' ) {
					  inputFileName[len-2] = 0;
					}
				}
				filename = ConvertToWString(inputFileName);
				list.push_back(filename);
				listcount++;
			}
			int cnt;
			for (cnt = 0; cnt < phocrexportSettings.size();cnt++) {
				if (1 == listcount) {
	                phocrexportSettings[cnt].setExportFileName(filename);
	            }
	            else {
	                phocrexportSettings[cnt].setExportFileName(outputname_w);
	            }
	        }


#if 0
				try {
                    i1ProcStartTime = get_dtime();
					PHOcrPageMaker::CreatePage(page, filename);
					page->PHOcrSetSettings(phocrSettings);
					page->PHOcrSetLogLevel(PHOcrLogLevel::LL_DIAGNOSTIC);
					document->PHOcrAppendPage(page);
					document->PHOcrSetSettings(phocrSettings);
					document->PHOcrProcess(PHOcrProcessType::PT_PREPROCESS_SEGMENTATION_BARCODE_OCR);
//					printf("PageNo %d:",document->PHOcrGetNumberOfPages());
					printMemoryStatus();
                    i1ProcEndTime = get_dtime();
                    printf("OCR_Running_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);
				} catch (...) {
					PrintHelp(__LINE__);
					return 1;
				}
#else

            if (!output_memory) {
                document->PHOcrConfigureForExporting(phocrexportSettings);
                document->PHOcrBeginExporting();
            }

            for (int i = 0; i < listcount; i++){
                printf("InputFile=%ls\n", list[i].c_str());
                try {
                    i1ProcStartTime = get_dtime();
                    printf("%d=PHOcrPageMaker::CreatePage(page, list[i])\n", PHOcrPageMaker::CreatePage(page, list[i]));
                    page->PHOcrSetSettings(phocrSettings);
                    printMemoryStatus();
                    pages.push_back(page);
                    // Write part of export data (Example: <page> tag of xml) to disk (not cache data)
                    printf("%d=document->PHOcrAppendPages({page}\n", document->PHOcrAppendPages({page}));
					document->PHOcrSetSettings(phocrSettings);
                    i1ProcEndTime = get_dtime();
                    printf("OCR_Running_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);
                } catch (...) {
                    PrintHelp(__LINE__);
                    return 1;
                }

#endif
			}

		}
		/********************************/
		/* Barcode recoginition process */
		/********************************/
		if (get_barcode) {
            int mapcnt = 0;
			// add page from filelist
			while(0 != fgets( inputFileName, MAX_PATH, filelist )) {
				printf("Barcode_InputFile=%s", inputFileName);
				mp2[mapcnt] = inputFileName;
                i1ProcStartTime = get_dtime();
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
					//document->PHOcrAppendPage(page);
    				mapcnt ++;
				} catch (...) {
					PrintHelp(__LINE__);
					return 1;
				}
			}
			numberPages = document->PHOcrGetNumberOfPages();    /* Total page number */
			//Decode Barcode and print
			for (pagenum=0;pagenum < numberPages;pagenum++) {
				//std::cout << "Barcode PageNo:" << pagenum+1 << std::endl;
				page=document->PHOcrGetPage(pagenum);
				//ToDo:Why  does not page object inherit document object settings?
				phocrSettings.SetBarcodeMode(barcode_mode);
				page->PHOcrSetSettings(phocrSettings);
				printf("%d = page->PHOcrGetAllBarcodes(barcodes)\n", page->PHOcrGetAllBarcodes(barcodes));
                i1ProcEndTime = get_dtime();
                printf("OCR_Running_Process_Time_Barcode(%dPage) %.3f\n", pagenum+1, i1ProcEndTime-i1ProcStartTime);

#if 0
				//Print string representation of barcodes found in page.
//  				if(barcodes.size() == 0)
//					std::cout << "\tNone!\n";
//				else
//				{
//                    DocData = document->PHOcrGetDocumentStructData();
//
  //                  PagesData = DocData->GetPages();
    //                Barcodedata = PagesData[0]->GetBarcodes();
//
//					for(size_t i = 0; i < barcodes.size() ; i++)
//					{
//                        std::cout << "\tBarcode_" << i << "\t[" << Barcodedata[i]->GetBarcodeFormat() << "]\t" << Barcodedata[i]->GetResult() << std::endl;
//					}
//				}
#endif
			}
		}
		printf("%s PHOcr Processing end!!\n", GetTime(tmp));
		if (document->PHOcrGetNumberOfPages() == 1) {
			outputname_w = filename;
		}
		/******************/
		/* Export process */
		/******************/
		// Output memory
		if (output_memory) {
			int page_cnt,carea_cnt,paragraph_cnt,line_cnt,word_cnt,char_cnt,charstr_cnt;
			i1ProcStartTime = get_dtime();
			ocr_result = document->PHOcrGetDocumentStructData(DocData);
			//Process All pages in document
			PagesData = DocData->GetPages();
			for (page_cnt = 0; page_cnt < PagesData.size(); page_cnt++) {
                printf("\t<ocr_page id='%d' x='%d' y='%d' w='%d' h='%d'>\n",
                    PagesData[page_cnt]->GetId(), PagesData[page_cnt]->GetX(),
                    PagesData[page_cnt]->GetY(), PagesData[page_cnt]->GetW(), PagesData[page_cnt]->GetH());
				//Process All Carea in page
				CareaData = PagesData[page_cnt]->GetCareas();
				for (carea_cnt = 0; carea_cnt < CareaData.size(); carea_cnt++) {
                    printf("\t  <ocr_carea id='%d' x='%d' y='%d' w='%d' h='%d'>\n",
                        CareaData[carea_cnt]->GetId(), CareaData[carea_cnt]->GetX(),
                        CareaData[carea_cnt]->GetY(), CareaData[carea_cnt]->GetW(), CareaData[carea_cnt]->GetH());
					//Process All paragraph in carea
					ParagraphData = CareaData[carea_cnt]->GetParagraph();
					for (paragraph_cnt = 0; paragraph_cnt < ParagraphData.size(); paragraph_cnt++) {
                        printf("\t    <ocr_par id='%d' x='%d' y='%d' w='%d' h='%d'>\n",
                            ParagraphData[paragraph_cnt]->GetId(), ParagraphData[paragraph_cnt]->GetX(),
                            ParagraphData[paragraph_cnt]->GetY(), ParagraphData[paragraph_cnt]->GetW(), ParagraphData[paragraph_cnt]->GetH());
						//Process All line in paragraph
						LineData = ParagraphData[paragraph_cnt]->GetLines();
						for (line_cnt = 0; line_cnt < LineData.size(); line_cnt++) {
                            printf("\t      <ocr_line id='%d' x='%d' y='%d' w='%d' h='%d'>\n",
                                LineData[line_cnt]->GetId(), LineData[line_cnt]->GetX(),
                                LineData[line_cnt]->GetY(), LineData[line_cnt]->GetW(), LineData[line_cnt]->GetH());
							//Process All word in line
							WordData = LineData[line_cnt]->GetWords();
							for (word_cnt = 0; word_cnt < WordData.size(); word_cnt++) {
                                printf("\t        <ocr_word id='%d' x='%d' y='%d' w='%d' h='%d'>\n",
                                    WordData[word_cnt]->GetId(), WordData[word_cnt]->GetX(),
                                    WordData[word_cnt]->GetY(), WordData[word_cnt]->GetW(), WordData[word_cnt]->GetH());
								//Process All character in word
								CharData = WordData[word_cnt]->GetCharacters();
								for (char_cnt = 0; char_cnt < CharData.size(); char_cnt++) {
                                    printf("\t          <ocr_character id='%d' x='%d' y='%d' w='%d' h='%d' confidence='%f' value='%s'>\n",
                                        CharData[char_cnt]->GetId(), CharData[char_cnt]->GetX(),
                                        CharData[char_cnt]->GetY(), CharData[char_cnt]->GetW(), CharData[char_cnt]->GetH(), CharData[char_cnt]->GetConfidence(), CharData[char_cnt]->GetValue().c_str());

								}
							}
						}
					}

				}
			}
			i1ProcEndTime = get_dtime();
			printf("Result_put_for_Memory_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);
		}
        // Output memory (Barcode)
        if (get_barcode) {
            i1ProcStartTime = get_dtime();
            printf("Output memory (Barcode) Start\n");
            //Print string representation of barcodes found in page.
            numberPages = document->PHOcrGetNumberOfPages();    /* Total page number */
            //Decode Barcode and print
            for (pagenum=0;pagenum < numberPages;pagenum++) {
                std::cout << "Barcode PageNo:" << pagenum+1 <<  std::endl;
                if(barcodes.size() == 0) {
                    std::cout << "\tNone!\n";
                }
                else
                {
                    //DocData = document->PHOcrGetDocumentStructData();
                    document->PHOcrGetDocumentStructData(DocData);
                    PagesData = DocData->GetPages();
                    Barcodedata = PagesData[pagenum]->GetBarcodes();
                    for(size_t i = 0; i < barcodes.size() ; i++)
                    {
                        std::cout
                        << "\tx=" << Barcodedata[i]->GetX() << " y=" << Barcodedata[i]->GetY() << " w=" << Barcodedata[i]->GetW() << " h=" << Barcodedata[i]->GetH()
                        << "\tBarcode_" << i << "\t[" << Barcodedata[i]->GetBarcodeFormat() << "]\t" << Barcodedata[i]->GetResult() << std::endl;
                    }
                }
            }
            i1ProcEndTime = get_dtime();
            printf("Result_put_for_Memory(Barcode)_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);

        }
#if 0
		// Export TXT format
		if (export_txt) {
            i1ProcStartTime = get_dtime();
			document->PHOcrExport(outputname_w, PHOcrExportFormat::EF_TXT);
            i1ProcEndTime = get_dtime();
            printf("Export_Txt_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);
		}
		// Export XML format
		if (export_xml) {
            i1ProcStartTime = get_dtime();
			document->PHOcrExport(outputname_w, PHOcrExportFormat::EF_XML);
            i1ProcEndTime = get_dtime();
            printf("Export_XML_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);
		}
		// Exporting PDF format
		if (export_pdf) {
            i1ProcStartTime = get_dtime();
			document->PHOcrExport(outputname_w, PHOcrExportFormat::EF_PDF);
            i1ProcEndTime = get_dtime();
            printf("Export_PDF_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);
		}
		// Exporting PDF format
		if (export_pdfa) {
            i1ProcStartTime = get_dtime();
			document->PHOcrExport(outputname_w, PHOcrExportFormat::EF_PDFA);
            i1ProcEndTime = get_dtime();
            printf("Export_PDFA_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);
		}
		// Exporting Word format
		if (export_word) {
            i1ProcStartTime = get_dtime();
			document->PHOcrExport(outputname_w, PHOcrExportFormat::EF_DOCX);
            i1ProcEndTime = get_dtime();
            printf("Export_Word_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);
		}
		// Exporting Excel format
		if (export_excel) {
            i1ProcStartTime = get_dtime();
			clock_t start_s = 0;
			document->PHOcrExport(outputname_w, PHOcrExportFormat::EF_XLSX);
            i1ProcEndTime = get_dtime();
            printf("Export_Excel_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);
		}
		// Exporting PPT format
		if (export_powerpoint) {
            i1ProcStartTime = get_dtime();
			clock_t start_s = 0;
			document->PHOcrExport(outputname_w, PHOcrExportFormat::EF_PPTX);
            i1ProcEndTime = get_dtime();
            printf("Export_PPTX_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);
		}
#else
        // End the exporting by end process of all pages
        if (!output_memory) {

            i1ProcStartTime = get_dtime();
            document->PHOcrEndExporting();
            i1ProcEndTime = get_dtime();
            printf("Export_Process_Time %.3f\n", i1ProcEndTime-i1ProcStartTime);
        }
#endif
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

    printf("Total_Process_Time %.3f\n", iProcessEndTime-iProcessStartTime);

	return 0;
}
