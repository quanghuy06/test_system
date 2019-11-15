/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrPage.h
 * @brief   Interface for PHOcrPage
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    2018-12-19
 *****************************************************************************/

#pragma once

#include <string>
#include <vector>
#include <memory>

#include "PHOcrRectangle.h"
#include "PHOcrSettings.h"
#include "PHOcrExportSetting.h"
#include "PHOcrDefines.h"
#include "PHOcrDeclaration.h"
#include "PHOcrPageData.h"

namespace phocr {

/**
 * Forward Declaration of PHOcrPage detail implementation class
 * and shared ptr declaration.
 */
class PHOcrPageImpl;
typedef std::shared_ptr<PHOcrPageImpl> PHOcrPageImplPtr;

/**
 * Forward Declaration of PHOcrPage and shared ptr declaration
 */
class PHOcrPage;
typedef std::shared_ptr<PHOcrPage> PHOcrPagePtr;

// Forward declaration of Accessor
class PHOcrSettingsAccessor;

/**
 * PHOcrPage Class Definition.
 *
 * This class provides more fine grained capability on the page
 * level, including Zonal OCR, Barcode Detection.
 */
class PHOCR_API PHOcrPage {
 private:
  // Accessor is internal data
  friend class PHOcrPageAccessor;

  // Internal declarations.
  PHOcrPageImplPtr m_Handler;

  // Internal Function.
  PHOcrPageImplPtr GetHandler();

  /**
   * Internal use constructors, you need to call PHOcrPageMaker for
   * create PHOcrPage instead of call directly below constructors
   */
  PHOcrPage() = delete;
  explicit PHOcrPage(PHOcrPageImplPtr handle, int pageNumber);
  explicit PHOcrPage(const std::wstring& filePath);
  explicit PHOcrPage(const unsigned char * fileData, int length);

 public:
  /**
   * Destructor
   */
  ~PHOcrPage();

  /**
   * Get x resolution in DPI (dots/inch)
   *
   * @return x resolution value
   * @return 0 if have exception
   */
  long PHOcrGetXResolution();

  /**
   * Get y resolution in DPI (dots/inch)
   *
   * @return y resolution value.
   * @return 0 if have exception
   */
  long PHOcrGetYResolution();

  /**
   * Get x resolution in mm
   *
   * @return x resolution in mm.
   * @return 0 if have exception
   */
  double PHOcrGetXResolutionInMM();

  /**
   * Get y resolution in mm
   *
   * @return y resolution in mm.
   * @return 0 if have exception
   */
  double PHOcrGetYResolutionInMM();

  /**
   * Set page processing settings.
   *
   * @param[in] phocrSettings Setting for page
   * @return void.
   */
  PHOcrStatus PHOcrSetSettings(const PHOcrSettings& phocrSettings);

  /**
   * Find string in a zone within page.
   *
   * @param[out] string_in_zone String in zone and match with regex
   * @param[in] x      X position of target zone.
   * @param[in] y      Y position of target zone.
   * @param[in] width  Width of target zone.
   * @param[in] height Height of target zone.
   * @param[in] regex  Regular Expression search pattern to
   *                   condition string found in zone.
   *
   * @return Status of function call
   */
  PHOcrStatus PHOcrGetStringInAZone(
      std::wstring& string_in_zone,
      int x, int y,
      int width, int height,
      const std::wstring& regex = L"");

  /**
   * Find string in a zone within page.
   *
   * @param[out] string_in_zone String in zone and match with regex
   * @param[in] zone  Definition of target zone
   * @param[in] regex Regular Expression search pattern to
   *                  condition string found in zone.
   *
   * @return Status of function call
   */
  PHOcrStatus PHOcrGetStringInAZone(
      std::wstring& string_in_zone,
      const PHOcrRectangle<long>& zone,
      const std::wstring& regex = L"");

  /**
   * Find barcode in a zone within page.
   *
   * @param[out] barcode_content Barcode in zone and match with regex
   * @param[in] x      X position of target zone.
   * @param[in] y      Y position of target zone.
   * @param[in] width  Width of target zone.
   * @param[in] height Height of target zone.
   * @param[in] regex  Regular Expression search pattern to
   *                   condition barcode found in zone.
   *
   * @return Barcode content found in zone which matched
   * regular expression.
   */
  PHOcrStatus PHOcrGetBarcodeInAZone(
      std::wstring& barcode_content,
      int x, int y,
      int width, int height,
      const std::wstring& regex = L"");

  /**
   * Find barcode in a zone within page.
   *
   * @param[in] zone  Definition of target zone
   * @param[in] regex Regular Expression search pattern to
   *                  condition barcode found in zone.
   *
   * @return Barcode content found in zone which matched
   * regular expression.
   */
  PHOcrStatus PHOcrGetBarcodeInAZone(
      std::wstring& barcode_content,
      const PHOcrRectangle<long>& zone,
      const std::wstring& regex = L"");

  /**
   * Get all barcodes within page.
   *
   * @return Vector of string which contain all Barcode content found
   * in page.
   */
  PHOcrStatus PHOcrGetAllBarcodes(
      std::vector<std::wstring>& barcodes);

  /**
   * Export to file using specified export format.
   * Will append output format suffix onto the filePath provided.
   *
   * @param[in] filePath Path to output file
   * @param[in] format   Export format type
   * @return Status of calling function
   */
  PHOcrStatus PHOcrExport(
      const std::vector<phocr::PHOcrExportSetting>& export_setting);

  /**
   * Get text from ocr results in all the page
   * @param text_result variable that contain page text result
   * @return Status of calling function
   */
  PHOcrStatus PHOcrGetTextResult(std::string& text_result);

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
   * @return default value if have exception
   */
  PHOcrLogLevel PHOcrGetLogLevel() const;

  /**
   * Get page data struct after ocr processing
   * @param[out] Data of page
   * @return Status of action
   */
  PHOcrStatus PHOcrGetPageDataStruct(PHOcrPageDataPtr& page_data);
};

}  // namespace phocr
