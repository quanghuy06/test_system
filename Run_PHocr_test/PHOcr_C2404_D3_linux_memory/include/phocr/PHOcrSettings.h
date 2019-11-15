/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrSettings.h
 * @brief   Interface of PHOcrSettings module
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    2018-12-19
 *****************************************************************************/

#pragma once

#include <string>
#include <memory>
#include "PHOcrDefines.h"
#include "PHOcrStatus.h"
#include "PHOcrEnum.h"

namespace phocr {
/**
 * Forward Declaration of PHOcrSettings detail implementation class
 * and shared ptr declaration.
 */
class PHOcrSettingsImpl;
typedef std::shared_ptr<PHOcrSettingsImpl> PHOcrSettingsImplPtr;

// Forward declaration of Accessor
class PHOcrSettingsAccessor;

/**
 * PHOcrSettings Class Definition.
 *
 * This class specifies all the settings
 * for the PHOcr Document Processing Library.
 */
class PHOCR_API PHOcrSettings {
 private:
  // Accessor is internal data
  friend class PHOcrSettingsAccessor;

  // Internal declarations.
  PHOcrSettingsImplPtr m_Handler;

  // Internal Function.
  PHOcrSettingsImplPtr GetHandler();

 public:
  /**
   * Empty constructor.
   */
  PHOcrSettings(void);

  /**
   * Destructor.
   */
  ~PHOcrSettings(void);

  /**
   * Copy constructor
   */
  PHOcrSettings(const PHOcrSettings &setting);

  /**
   * Assignment operator
   */
  PHOcrSettings& operator=(const PHOcrSettings &setting);

  /**
   * Get Recognition Language for OCR Engine.
   *
   * @return Current Language Setting.
   * @default L"english"
   */
  std::wstring GetOCRLanguage() const;

  /**
   * Set Recognition Language for OCR Engine. The input is case
   * insensitive
   *
   * Language can be:
   *    + single i.e. "English"
   *    + multiple i.e. "English,Japanese"
   *
   * List of supported languages:
   *    // EFIGS languages
   *    english, french, italian, german, spanish
   *
   *    // CJKA languages
   *    japanese, chinesesimplified, chinesetraditional,
   *    korean, arabic
   *
   *    // European languages
   *    danish, dutch, finnish, greek-ancient, greek-modern, norwegian
   *    polish, portuguese, russian, swedish, turkish
   *
   * @param[in] language Language Setting for OCR Engine.
   * @return Status of calling
   */
  PHOcrStatus SetOCRLanguage(const std::wstring& language);

  /**
   * Get Barcode Detection/Decoding Mode Setting.
   *
   * @return Current Barcode Mode Setting.
   */
  unsigned int GetBarcodeMode() const;

  /**
   * Set Barcode Detection/Decoding Mode Setting.
   *
   * @param[in] barcodeType Decoding Mode setting.
   * @return void.
   */
  PHOcrStatus SetBarcodeMode(unsigned int barcodeMode);

  /**
   * Set mode for checking supplemental code of EAN-13, EAN-8, UPC-E, UPC-A.
   * @default PHOcrBarcodeSupplementalCodelMode::SCM_AUTOMATIC_DETECTION
   * @param [in] mode Supplemental Code Mode Setting
   */
  PHOcrStatus SetSupplementalCodeMode(PHOcrBarcodeSupplementalCode mode);

  /**
   * Get flag which setting for supplemental code
   * @return [out] setting of supplemental code
   */
  PHOcrBarcodeSupplementalCode GetSupplementalCodeMode() const;

  /**
   * Check if with outputting start/stop code for Code39.
   *
   * @return Current value setting.
   */
  bool IsWithStartStopCodeForCode39() const;

  /**
   * Add option to with/without outputting start/stop code for Code39
   * Yes: For the barcode with the start/stop code
   * No: For the barcode without the start/stop code,
   *     or when outputting start/stop in the barcode data
   * Example of a barcode image has Code39 with start/stop code as below:
   * 1. Input image attach start/stop code (Asterisk): *1234567*
   * Set to "With":    1234567   (DO NOT output start/stop code)
   * Set to "Without": *1234567* (WILL output start/stop code)
   * 2. Input image no attach start/stop code (Asterisk): 1234567
   * Set to "With":    None
   * Set to "Without": 1234567
   * @default true (Yes)
   * @param[in] value true or false.
   * @return void.
   */
  PHOcrStatus WithStartStopCodeForCode39(bool value);

  /**
   * Check if enable check digit for 1D barcode.
   *
   * @return Current value setting.
   */
  bool IsEnableCheckDigitForOneDBarcode() const;

  /**
   * Enable/Disable to use check digit for 1D barcode.
   *
   * For EAN-8, EAN-13, UPC-A, UPC-E => ALWAYS use check digit calculation
   * - If equal with the final digit, the data of the check digit should be outputted as the bar code data.
   * - If not equal, the bar code data cannot be outputted since it is judged as wrong.
   *
   * For Code 93, Code 128, UCC 128, Postnet => ALWAYS use check digit calculation
   * - If equal with the final digit, the data of the check digit should not be outputted as the bar code data.
   * - If not equal, the bar code data cannot be outputted since it is judged as wrong.
   *
   * For Industrial 2 of 5, IATA 2 of 5, PATCH:
   * - Do not use check digit calculation
   * - The data of all digit should be outputed as the bar code data.
   *
   * For Code 39, Codabar, Interleaved 2 of 5, Matrix 2 of 5
   * - If enable check digit => use check digit calculation
   *   + If equal with the final digit, the data of the check digit should not be outputted as the bar code data.
   *   + If not equal, the bar code data cannot be outputted since it is judged as wrong.
   * - If disable check digit:
   *   + Do not use check digit calculation.
   *   + The data of all digit should be outputed as the bar code data.
   *
   * @param[in] value true or false.
   * @return void.
   */
  PHOcrStatus EnableCheckDigitForOneDBarcode(bool value);

  /**
   * Get value of variable for using image banding mechanism to reduce
   * memory consumption.
   *
   * @return The current value of using image banding mechanism.
   * @default false
   */
  bool GetUsingImageBandingMechanism() const;

  /**
   * Set value of variable for using image banding mechanism to reduce
   * memory consumption.
   *
   * @param[in] usingImageBandingMechanism Input setting from user
   * @return void
   */
  PHOcrStatus SetUsingImageBandingMechanism(
      const bool usingImageBandingMechanism);

  /**
   * Get current value of auto deskew setting.
   *
   * Auto deskew is the process in PHOcr for deskew image
   *
   * @return Current value of auto deskew setting.
   * @default true
   */
  bool GetAutoDeskew() const;

  /**
   * Set value of auto deskew settings.
   *
   * @param[in] deskew User input setting
   * @return Status of calling function
   */
  PHOcrStatus SetAutoDeskew(const bool deskew);

  /**
   * Get current value of auto orientation setting.
   *
   * Auto orientation is the process in PHOcr for make orientation
   * with 90, 180, 270 degree to 0 degree
   *
   * @return Current value of auto deskew setting.
   * @default true
   */
  bool GetAutoOrientation() const;

  /**
   * Set value of auto orientation settings.
   *
   * @param[in] orientation User input setting
   * @return Status of calling function
   */
  PHOcrStatus SetAutoOrientation(const bool orientation);

  /**
   * Get current value of input document type setting.
   *
   * Document type setting correct will make the best accuracy and
   * performance. PHOcr will known what process need for each
   * document type.
   *
   * @return Current value of input document type settings.
   * @default PHOcrInputDocumentType::IDT_SCANNED_DOCUMENT
   * @return default value if have exception
   */
  PHOcrInputDocumentType GetInputDocumentType() const;

  /**
   * Set value of input document type setting.
   *
   * @param[in] input_type User input setting
   * @return Status of calling function
   */
  PHOcrStatus SetInputDocumentType(
      const PHOcrInputDocumentType input_type);

  /**
   * Get current value of input original mode setting.
   *
   * Input scan setting for input document. By using that information,
   * PHOcr will known what process need to be done for make the best
   * accuracy and performance
   *
   * @return Current value of input original mode settings.
   * @default PHOcrInputOriginalMode::IOM_TEXT_MODE
   * @return default value if have exception
   */
  PHOcrInputOriginalMode GetInputOriginalMode() const;

  /**
   * Set value of input original mode setting.
   *
   * @param[in] input_mode User input setting
   * @return Status of calling function
   */
  PHOcrStatus SetInputOriginalMode(
      const PHOcrInputOriginalMode input_mode);

  /**
   * Get current value of input color mode setting.
   *
   * Input scan setting for input document. By using that information,
   * PHOcr will known what process need to be done for make the best
   * accuracy and performance
   *
   * @return Current value of input color mode settings.
   * @default PHOcrInputColorMode::ICM_GRAY_SCALE_MODE
   * @return default value if have exception
   */
  PHOcrInputColorMode GetInputColorMode() const;

  /**
   * Set value of input color mode setting.
   * The user will choose "auto colour" when they want to reduce the file size.
   * Therefore, for PHOcr, "-optimize-pdf-file-size" already covers this scenario nicely.
   * If the user has chosen "auto colour",
   * then "-optimize-pdf-file-size" can be used with full colour input,
   * and the result will be "auto colour".
   * @param[in] input_mode User input setting
   * @return Status of calling function
   */
  PHOcrStatus SetInputColorMode(
      const PHOcrInputColorMode input_mode);

  /**
   * Get current value of data mode setting.
   *
   * Data mode setting will decide what content will be calculated
   * during PHOcr processing
   *
   * @return Current value of data mode settings.
   * @default PHOcrDataMode::DM_HIGH_CONTENT
   * @return default value if have exception
   */
  PHOcrDataMode GetDataMode() const;

  /**
   * Set value of data mode setting.
   *
   * @param[in] input_mode User input setting
   * @return Status of calling function
   */
  PHOcrStatus SetDataMode(
      const PHOcrDataMode input_mode);

  /**
   * Get current product setting.
   *
   * @return Current value of settings.
   * @default PHOcrSupportProduct::SP_SING20_PRODUCTNAME
   * @return default value if have exception
   */
  PHOcrSupportProduct GetProductSetting() const;

  /**
   * Set value of product setting.
   *
   * @param[in] input_product User input setting
   * @return Status of calling function
   */
  PHOcrStatus SetProductSetting(
      const PHOcrSupportProduct input_product);

  /**
   * Get setting for export dpi of embedded image inside of PDF
   *
   * @return The current value of output dpi
   * @return default value if have exception
   */
  int GetPdfOutputDpi() const;

  /**
   * Set setting for exporting dpi of embedded image, text inside of PDF
   * document
   *
   * @param[in] output_dpi User input setting
   * @return Status of calling function
   */
  PHOcrStatus SetPdfOutputDpi(const int output_dpi);

  /**
   * Get setting for embedded image inside of PDF
   *
   * @return The current value of export mode
   * default value is PHOcrImageExportMode::IEM_ORIGINAL
   * @return default value if have exception
   */
  PHOcrImageExportMode GetPdfImageExportMode() const;

  /**
   * Set setting for exporting mode of embedded image inside of PDF
   * document
   *
   * @param[in] export_mode User input setting
   * @return Status of calling function
   */
  PHOcrStatus SetPdfImageExportMode(
      const PHOcrImageExportMode image_export_mode);

  /**
   * Get setting for content inside of PDF document
   *
   * @return The current value of setting
   * default value is PHOcrPDFExportMode::PEM_SEARCHABLE_PDF
   * @return default value if have exception
   */
  PHOcrPDFExportMode GetPdfExportMode() const;

  /**
   * Set setting for content inside of PDF document
   *
   * @param[in] export_mode User input setting
   * @return Status of calling function
   */
  PHOcrStatus SetPdfExportMode(
      const PHOcrPDFExportMode export_mode);

  /**
   * Check if the setting of document is export excel in the same sheet
   * @return default value (false) if have exception
   */
  bool IsExportInOneSheet() const;

  /**
   * Setting to export excel in one sheet
   * @param export_same_sheet
   */
  PHOcrStatus SetExportInOneSheet(bool export_same_sheet);

  /**
   * Main API to set target paper size setting for PHOcr
   * @param target_paper_size Name of target paper size that you want at output
   * document, list of supported size is listed at PHOcrStandardPaperName enum
   */
  PHOcrStatus SetTargetPaperSize(PHOcrStandardPaperName target_paper_size);

  /**
   * Get out the target paper size
   * @return Target paper size
   */
  PHOcrStandardPaperName GetTargetPaperSize() const;

  /**
   * Set flag to enable PDF output file size optimization
   */
  PHOcrStatus SetOptimizeFileSizePDFOutput(bool value);

  /**
   * Get flag to optimize file size of PDF output
   */
  bool GetOptimizeFileSizePDFOutput() const;

  /**
   * Set minimum area for macro segment regions to generate hybrid segmentation
   * data.
   */
  PHOcrStatus SetMinimumHybridSegmentRegion(int minimum_area);

  /**
   * Get minimum area of hybrid segment region
   */
  int GetMinimumAreaHybridSegmentRegion();

  /**
   * Enable parallel OCR multipage scan with two page OCR in the same time
   * If this flag are false, parallel will only inside of each page processing.
   * @default PHOcrParallelType::PARALLEL_AUTO_SELECT
   * @param [in] is_parallel_pages
   */
  PHOcrStatus SetOCRMultiPagesInParallel(PHOcrParallelType is_parallel_pages);

  /**
   * Get flag which setting parallel OCR multipage scan with two page OCR in the same time
   * If this flag are false, parallel will only inside of each page processing.
   * @return [out] setting of parallel pages
   */
  PHOcrParallelType GetOCRMultiPagesInParallel();

  /**
   * Set information for ICC profile when export to PDF
   * Please make sure that the source profile is compressed by using the FlateDecode algorithm
   */
  PHOcrStatus SetIccSourceProfile(const std::wstring& source_profile);

  /**
   * Set information for ICC profile when export to PDF
   * Please make sure that the data is read from source profile
   * which is compressed by using the FlateDecode algorithm
   */
  PHOcrStatus SetIccSourceProfile(const char* icc_source_profile, size_t icc_size);

  /**
   * Get data of icc profile
   */
  char* GetIccSourceProfile() const;

  /**
   * Get length of data of icc profile
   */
  size_t GetIccSourceProfileSize() const;

  /**
   * Set flag to use icc source profile or not
   */
  PHOcrStatus UseIccSourceProfile(bool value);

  /**
   * Check if can use icc source profile
   */
  bool CanUseIccSourceProfile() const;

  /**
   * Set the working directory for PHOcr
   * @param working_directory New working directory
   * @return Status of action
   */
  PHOcrStatus SetPHOcrWorkingDirectory(const char* working_directory);

  /**
   * Get out PHOcr working directory
   * @return The working directory of PHOcr
   */
  const char* GetPHOcrWorkingDirectory() const;

  /**
   * Set the DPI for PHOcr from outside (for example: FAX document).
   * DPI contains horizontal and vertical resolution.
   * @param horizontal_res The horizontal resolution
   * @param vertical_res The vertical resolution
   * @return
   */
  PHOcrStatus SetDPI(unsigned int horizontal_res, unsigned int vertical_res);

  /**
   * Get the DPI out
   * @param[out] horizontal_res
   * @param[out] vertical_res
   * @return Status of the action get fax DPI
   */
  PHOcrStatus GetDPI(
      unsigned int& horizontal_res,
      unsigned int& vertical_res) const;
};

}  // namespace phocr
