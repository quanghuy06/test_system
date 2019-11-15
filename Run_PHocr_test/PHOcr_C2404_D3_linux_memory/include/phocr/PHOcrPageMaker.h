/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrPageMaker.h
 * @brief   Maker of PHOcrPage
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Jan 22, 2019
 *****************************************************************************/
#pragma once

#include "PHOcrPage.h"
#include "PHOcrStatus.h"

namespace phocr {

/**
 * Maker for PHOcrPage
 */
class PHOcrPageMaker {
 public:
  PHOcrPageMaker() = delete;
  virtual ~PHOcrPageMaker() = delete;

  /**
   * Construct from file path
   *
   * @param[out] page Created page
   * @param[in] filePath Path to target file for processing.
   * @return Status of creating page
   */
  static PHOcrStatus CreatePage(
      PHOcrPagePtr& page,
      const std::wstring& filePath);

  /**
   * Construct from image file data stream. File data is image in
   * compressed state. The page settings will be keep as default.
   * If input image is multipages, the first page will be used to
   * create PHOcrPage.
   *
   * @param[out] page Created page
   * @param[in] fileData File stream data of target file for processing.
   * @param[in] length   Length of the file stream.
   * @return Status of creating page
   */
  static PHOcrStatus CreatePage(
      PHOcrPagePtr& page,
      const unsigned char * fileData, int length);
};

}  // namespace phocr
