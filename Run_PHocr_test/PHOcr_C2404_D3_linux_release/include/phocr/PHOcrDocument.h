/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrDocument.h
 * @brief   Interface of PHOcrDocument
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    2018-12-19
 *****************************************************************************/

#pragma once

#include <memory>
#include <vector>

#include "PHOcrPage.h"
#include "PHOcrSettings.h"
#include "PHOcrDefines.h"
#include "PHOcrStatus.h"
#include "PHOcrDeclaration.h"
#include "PHOcrDocumentData.h"
#include "PHOcrExportSetting.h"

namespace phocr {

/**
 * Forward Declaration of PHOcrDocument Detailed Implementation
 * and shared ptr declaration.
 */
class PHOcrDocumentImpl;
typedef std::shared_ptr<PHOcrDocumentImpl> PHOcrDocumentImplPtr;

/**
 * Forward Declaration of PHOcrDocument APIs and shared ptr
 * declaration
 */
class PHOcrDocument;
typedef std::shared_ptr<PHOcrDocument> PHOcrDocumentPtr;

// Forward declaration of Accessor
class PHOcrDocumentAccessor;

/**
 * PHOcrDocument Class Definition.
 *
 * This is the main class for the PHOcr Document Processing Library
 * and provides the top level OCR and Export capability with page
 * handling.
 */
class PHOCR_API PHOcrDocument {
 private:
  // Accessor is internal data
  friend class PHOcrDocumentAccessor;

  // Internal Declaration.
  PHOcrDocumentImplPtr m_Handler;

  // Internal Function.
  PHOcrDocumentImplPtr GetHandler();

  /**
   * Internal use constructors, you need to call PHOcrDocumentMaker
   * for create PHOcrDocument instead of call directly below
   * constructors
   */
  PHOcrDocument();
  explicit PHOcrDocument(
      const std::wstring& filePath);
  explicit PHOcrDocument(
      const std::wstring& filePath, PHOcrSettings settings);
  explicit PHOcrDocument(
      const unsigned char *fileData, int length);
  explicit PHOcrDocument(
      const unsigned char *fileData, int length,
      PHOcrSettings settings);

 public:
  /**
   * Destructor
   */
  ~PHOcrDocument();

  /**
   * Export to multiple files using export setting list
   * @param[in] export_setting list of setting
   * @return Status of calling function
   */
  PHOcrStatus PHOcrExport(
          const std::vector<phocr::PHOcrExportSetting>& export_setting);

  /**
   * Get text result of all pages in the document
   * @param[out] text_results that will contain document text result
   * @return Status of calling function
   */
  PHOcrStatus PHOcrGetTextResults(std::string& text_results);

  /**
   * Get number of pages in the document.
   *
   * @return number of pages in document.
   * @return 0 if have exception
   */
  long PHOcrGetNumberOfPages() const;

  /**
   * Set document settings
   *
   * @param[in] phocrSettings Input settings for document
   * @return Status of calling function
   */
  PHOcrStatus PHOcrSetSettings(PHOcrSettings phocrSettings);

  /**
   * Get copy of current document processing settings.
   *
   * @return Copy of current PHOcrSettings object.
   * if have exception, return default contractor of PHOcrSettings
   */
  PHOcrSettings PHOcrGetSettings();

  /**
   * Append page list into document
   *
   * @param[in] pages Page list to append to document
   * @return Status of calling function
   */
  PHOcrStatus PHOcrAppendPages(std::vector<PHOcrPagePtr> pages);

  /**
   * Insert page into document at specific position
   *
   * @param[in] page Page object to insert to page list of document
   * @param[in] position Position in page list which input page will
   *                     be insert at that position
   * @return Status of calling function
   */
  PHOcrStatus PHOcrInsertPage(PHOcrPagePtr page,
                              unsigned int position);

  /**
   * Remove page at position
   *
   * @param[in] position Position of page will be removed in page list
   * @return Status of calling function
   */
  PHOcrStatus PHOcrRemovePage(unsigned int position);

  /**
   * Get a pointer to a specified page.
   *
   * @param[in] pageNumber Specifies page number of PHOcrPage to
   *                       retrieve.
   * @return If page number inside of number of page range, return the
   * PHOcrPage instance, if pageNumber not inside page range, nullptr
   * are returned.
   * @return NULL if have exception
   */
  PHOcrPagePtr PHOcrGetPage(long pageNumber);

  /**
   * During running, PHOcr will check that should PHOcr are cancel.
   * This API will set the decision method which PHOcr will call for
   * get the decision.
   *
   * @param[in] decision_method Method for making decision
   * @return Status of calling function
   */
  PHOcrStatus PHOcrSetCancelDecisionMethod(
      PHOcrCancelDecisionMethod decision_method);

  /**
   * Set logging level for processing
   *
   * @param[in] log_level Input log level
   * @return Status of function call
   */
  PHOcrStatus PHOcrSetLogLevel(const PHOcrLogLevel log_level);

  /**
   * Get current log level of page
   *
   * @return Current log level
   * @return default value LL_OFF if have exception
   */
  PHOcrLogLevel PHOcrGetLogLevel() const;

  /**
   * Get data structure of one PHOcrDocument
   * @param[out] document_data Store the document data
   * @return Status of this action
   */
  PHOcrStatus PHOcrGetDocumentStructData(PHOcrDocumentDataPtr& document_data);

  /**
   * API to set the size of TrainedDataCache in MB unit. This is the maximum
   * size that the cache will reach to. If the allocated memory is greater than
   * this value, part of old data in the cache will be deleted.
   * Note: 100 MB is the cache size by default. If you want to use another size,
   * please call this function only 1 time, before start any job by PHOcr. Or
   * you can ReleaseTrainedDataCacheMemory before using.
   * @param cache_memory
   * @return The status of the method
   */
  PHOcrStatus SetTrainedDataCacheMemory(float cache_memory);

  /**
   * API to release all memory hold by the TrainedDataCache to the OS. Must call
   * after all job is done to prevent memory leak
   */
  void ReleaseTrainedDataCacheMemory();

  /**
   * API to query the allocated memory inside the TrainedDataCache
   * @return The memory that is allocated in the TrainedDataCache
   */
  float QueryAllocatedTrainedDataMemory();

  /**
   * API to disable the TrainedDataCache. If the cache is disable, then PHOcr
   * will load directly from file on disk. If the cache is already run, then
   * call to this method will return error.
   * @param disable
   * @return Status of this method
   */
  PHOcrStatus DisableTrainedDataCache(bool disable);

  /**
   * Configure for exporting with list of export settings
   * Note: this function will return error if call it two
   *       times before call end exporting
   * @param export_setting - list of export setting
   * @return Status of this method
   */
  PHOcrStatus PHOcrConfigureForExporting(
    const std::vector<phocr::PHOcrExportSetting>& export_setting);

  /**
   * Processing all page inside document and export to temporary data
   * Whenever, end exporting are called, document will finish export
   * @return Status of this method
   */
  PHOcrStatus PHOcrBeginExporting();

  /**
   * Finalize exporting, all pages will be export to
   * expected output in export settings
   * @return Status of this method
   */
  PHOcrStatus PHOcrEndExporting();
};
}  // namespace phocr
