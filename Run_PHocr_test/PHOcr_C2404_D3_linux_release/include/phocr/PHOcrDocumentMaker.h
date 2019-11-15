/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrDocumentMaker.h
 * @brief   Header file of class PHOcrDocumentMaker
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Jan 22, 2019
 *****************************************************************************/
#pragma once

#include "PHOcrStatus.h"
#include "PHOcrDocument.h"

namespace phocr {

/**
 * Maker for PHOcrDocument
 */
class PHOcrDocumentMaker {
 public:
  PHOcrDocumentMaker() = delete;
  virtual ~PHOcrDocumentMaker() = delete;

  /**
   * Create document with empty page list, settings for
   * PHOcr Document variable will be keep as default value
   *
   * @param[out] document Created document
   * @return Status of creating document
   */
  static PHOcrStatus CreateDocument(
      PHOcrDocumentPtr& document);

  /**
   * Construct document from image path. Settings for document will
   * be keep as default value (like when PHOcrSettings initialized)
   *
   * @param[out] document Created document
   * @param[in] filePath Path to target image file for processing.
   * @return Status of creating document
   */
  static PHOcrStatus CreateDocument(
      PHOcrDocumentPtr& document,
      const std::wstring& filePath);

  /**
   * Construct from file path and a custom settings.
   *
   * @param[out] document Created document
   * @param[in] filePath Path to target file for processing.
   * @param[in] settings Custom settings for document
   * @return Status of creating document
   */
  static PHOcrStatus CreateDocument(
      PHOcrDocumentPtr& document,
      const std::wstring& filePath,
      PHOcrSettings settings);

  /**
   * Construct from image file data stream. File data is image in
   * compressed state. This APIs will create page list inside document
   * by using fileData. The document settings will be keep as default
   *
   * If have any exception, document will be NULL
   *
   * @param[out] document Created document
   * @param[in] fileData File stream data of target file for processing.
   * @param[in] length Length of the file stream.
   * @return Status of creating document
   */
  static PHOcrStatus CreateDocument(
      PHOcrDocumentPtr& document,
      const unsigned char *fileData,
      int length);

  /**
    * Construct from image file data stream and a custom settings.
    * File data is image in compressed state. This APIs will create
    * page list inside document by using fileData. The document
    * settings will be set as input custom settings
    *
    * @param[out] document Created document
    * @param[in] fileData File stream data of target file for processing.
    * @param[in] length Length of the file stream.
    * @param[in] settings Custom settings for document
    * @return Status of creating document
    */
  static PHOcrStatus CreateDocument(
      PHOcrDocumentPtr& document,
      const unsigned char *fileData,
      int length,
      PHOcrSettings settings);
};

}  // namespace phocr
