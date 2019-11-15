/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrMemoryDataFilter.h
 * @brief   This module is used to
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Sep 13, 2019
 *****************************************************************************/

#ifndef PHOCR_API_PHOCRMEMORYDATAFILTER_H_
#define PHOCR_API_PHOCRMEMORYDATAFILTER_H_

#include <string>
#include <vector>
#include <boost/property_tree/ptree.hpp>
#include "phocr/api/PHOcrDocumentData.h"
#include "phocr/api/PHOcrPageData.h"
#include "phocr/include/TypeConverter.h"
#include "phocr/api/PHOcrDocumentTextResult.h"


namespace phocr {
namespace pt = boost::property_tree;
/**
 * This class is used filter PHOcr data in memory structure, then dump that
 * data to json file, ...
 */
PHOCR_API class PHOcrMemoryDataFilter {
  /**
   * Build ptree of page information
   * @param page_info Page info in memory structure
   * @param json A property tree to store all data
   */
  void BuildPageInformation(PHOcrPageInfoDataPtr page_info, pt::ptree& json);

  /**
   * Build ptree of barcodes
   * @param barcodes Barcodes info in memory structure
   * @param json A property tree to store all data
   */
  void BuildBarcodes(
      std::vector<PHOcrBarcodeDataPtr> barcodes, pt::ptree& json);

  /**
   * Build ptree of content areas
   * @param careas Content areas information in memory structure
   * @param json A property tree to store all data
   */
  void BuildContentAreas(
      std::vector<PHOcrCareaDataPtr> careas, pt::ptree& json);

  /**
   * Build ptree of tables
   * @param tables Tables data in memory structure
   * @param json A property tree to store all data
   */
  void BuildTables(std::vector<PHOcrTableDataPtr> tables, pt::ptree& json);

  /**
   * Build ptree of photos
   * @param photos Photos information in memory structure
   * @param json A property tree to store all data
   */
  void BuildPhotos(std::vector<PHOcrPhotoDataPtr> photos, pt::ptree& json);

  /**
   * Build the ptree of one PHOcrElementData
   * @param element_data Input PHOcrElementData
   * @param json_element A corresponding ptree to input element
   */
  void BuildJsonElement(
      PHOcrElementDataPtr element_data, pt::ptree& json_element);

  /**
   * Build the ptree from one PHOcrLineDataPtr or PHOcrParagraphPtr
   * @param element
   * @param json_list_info
   */
  template<typename T>
  inline void BuildJsonListInfo(T element, pt::ptree& json_list_info) {
    PHOcrListInfo list_info = element->GetListInfo();
    json_list_info.put("is list", list_info.isList());
    json_list_info.put(
        "type",
        Convert<PHOcrListType, std::string>(list_info.getListType()));
    json_list_info.put("name", list_info.getListName());
    json_list_info.put("level", list_info.getListLevel());
    json_list_info.put("start value", list_info.getStartValue());
  }

  /**
   * Detect the path to output file
   * @param json_path
   * @param working_directory
   * @return
   */
  static std::string DetectOutputPath(
      const std::string json_path, const char* working_directory);

 public:
  PHOcrMemoryDataFilter();

  /**
   * API to dump data of a PHOcr document in memory to json file
   * @param document_data A PHOcrDocumentData in memory structure
   * @param json_path Path to json file, default will be writed to working dir
   * @return
   */
  bool DumpJsonFile(
      PHOcrDocumentData* document_data, const std::string& json_path = "");

  /**
   * API to dump data of a PHOcr page in memory to json file
   * @param page_data A PHOcrPageData in memory structure
   * @param json_path Path to json file, default will be writed to working dir
   * @return
   */
  bool DumpJsonFile(
      PHOcrPageData* page_data, const std::string& json_path = "");

  /**
   * API to dump data of PHOcrDocumentTextResult to file
   * @param document_text
   * @param text_path
   * @return
   */
  void DumpTextFile(
      PHOcrDocumentTextResult* document_text,
      const std::string& text_path = "");

  /**
   * Build a ptree from PHOcrPageData
   * @param page_data
   * @param json_page
   * @return
   */
  bool BuildJsonPageData(PHOcrPageData* page_data, pt::ptree& json_page);

  ~PHOcrMemoryDataFilter();
};

}  // namespace phocr

#endif  // PHOCR_API_PHOCRMEMORYDATAFILTER_H_ //
