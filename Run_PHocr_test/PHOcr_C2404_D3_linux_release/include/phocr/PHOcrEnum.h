/******************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrEnum.h
 * @brief   Public enumeration for PHOcr APIs
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Jan 24, 2019
 *****************************************************************************/
#pragma once

#include "PHOcrDefines.h"

namespace phocr {

/**
 * PHOcr Export Format Settings.
 *
 * Specifies format of export data which provided by Export function
 * of PHOcrDocument or PHOcrPage
 */
enum class PHOcrExportFormat {
  // Export to TXT format
  EF_TXT,
  // Export to Microsoft Word format
  EF_DOCX,
  // Export to Microsoft Excel format
  EF_XLSX,
  // Export to Microsoft Power Point format
  EF_PPTX,
  // Export to XML format
  EF_XML,
  // Export to PDF format
  EF_PDF,
  // Export to PDFA format
  EF_PDFA,
  // Export to bounding box format (using for internal testing)
  EF_BB,
  // Export only text inside memory
  EF_MEMORY_TXT,
  // Export complete data inside memory
  EF_MEMORY_COMPLETE,
  // Doesn't export any thing
  EF_NONE
};

/**
 * Define the input document type
 */
enum class PHOcrInputDocumentType {
  // Document generated from scanner
  IDT_SCANNED_DOCUMENT,
  // Document generated from fax
  IDT_FAX_DOCUMENT
};

/**
 * Define the original mode of scanner
 */
enum class PHOcrInputOriginalMode {
  // Text mode
  IOM_TEXT_MODE,
  // Photo mode
  IOM_PHOTO_MODE,
  // Text/Photo mode
  IOM_TEXT_PHOTO_MODE
};

/**
 * Color mode of scan
 */
enum class PHOcrInputColorMode {
  // Corresponding BLACK mode of MFP
  ICM_BLACK_MODE,
  // Corresponding GRAY_SCALE mode of MFP
  ICM_GRAY_SCALE_MODE,
  // Corresponding FULL_COLOR mode of MFP
  ICM_FULL_COLOR_MODE,
  // Corresponding AUTO_COLOR mode of MFP
  ICM_AUTO_COLOR_MODE,
};

/**
 * Data mode for PHOcr processing
 */
enum class PHOcrDataMode {
  // Perform OCRing for text data, other data type will not be
  // calculated, this enum suitable for export EF_TXT
  DM_LOW_CONTENT,
  // Take more time than low content however other data type information
  // i.e. table, photo, ... will be calculated, this enum suitable for
  // export format EF_DOCX, EF_XLSX, EF_PPTX and EF_XML
  DM_HIGH_CONTENT,
};

/**
 * MFP Product, need confirm for product we will support
 */
enum class PHOcrSupportProduct {
  SP_SING20_PRODUCTNAME,
};

/**
 * PHOcr log level enum which used for setting log level of
 * PHOcrDocument or PHOcrPage
 */
enum class PHOcrLogLevel {
  // Turn off logging
  LL_OFF,
  // Logging information for diagnostic
  LL_DIAGNOSTIC,
};

enum class PHOcrPDFExportMode {
  // Export PDF without OCR
  PEM_ONLY_IMAGE,
  // Export PDF with embedded text components
  PEM_SEARCHABLE_PDF
};

/**
 * Image mode when exporting
 */
enum class PHOcrImageExportMode {
  // Export rich format with original embedded image
  IEM_ORIGINAL,
  // Export rich format with binarized embedded image
  IEM_BINARY,
  // Export rich format with halftone embedded image
  IEM_HALFTONE,
  // Export rich format with halftoning photo region in embedded image
  IEM_HALFTONE_PHOTO
};

/**
 * Define all types of standard paper size that PHOcr can support. PHOcr can
 * support these type of paper size, with portrait and landscape orientation.
 * In future development, this enum may be expanded
 */
enum class PHOcrStandardPaperName {
  SP_FIRST_PAGE_SIZE = 0,         // Every page will be the paper size which is set in 1st page
  SP_ORIGINAL,                    // Keep the original size as the input image
  SP_LETTER_PORTRAIT,             // Letter portrait
  SP_LETTER_LANDSCAPE,            // Letter landscape
  SP_LEDGER_PORTRAIT,             // Ledger portrait
  SP_LEDGER_LANDSCAPE,            // Ledger landscape
  SP_LEGAL_PORTRAIT,              // Legal portrait
  SP_LEGAL_LANDSCAPE,             // Legal landscape
  SP_STATEMENT_PORTRAIT,          // Statement portrait
  SP_STATEMENT_LANDSCAPE,         // Statement landscape
  SP_A3_PORTRAIT,                 // A3 portrait
  SP_A3_LANDSCAPE,                // A3 landscape
  SP_A4_PORTRAIT,                 // A4 portrait
  SP_A4_LANDSCAPE,                // A4 landscape
  SP_A5_PORTRAIT,                 // A5 portrait
  SP_A5_LANDSCAPE,                // A5 landscape
  SP_A6_PORTRAIT,                 // A6 portrait
  SP_A6_LANDSCAPE,                // A6 landscape
  SP_B4_PORTRAIT,                 // B4 portrait
  SP_B4_LANDSCAPE,                // B4 landscape
  SP_B5_PORTRAIT,                 // B5 portrait
  SP_B5_LANDSCAPE,                // B5 landscape
  SP_LG_13_PORTRAIT,              // 13\" LG portrait
  SP_LG_13_LANDSCAPE,             // 13\" LG landscape
  SP_J_POST_CARD_PORTRAIT,        // J Post Card portrait
  SP_J_POST_CARD_LANDSCAPE,       // J Post Card landscape
  SP_FOLIO_PORTRAIT,              // Folio portrait
  SP_FOLIO_LANDSCAPE,             // Folio landscape
  SP_COMPUTER_PORTRAIT,           // Computer portrait
  SP_COMPUTER_LANDSCAPE,          // Computer landscape
  SP_SQ_85_PORTRAIT,              // 8.5\" SQ portrait
  SP_SQ_85_LANDSCAPE,             // 8.5\" SQ landscape
  SP_K16_PORTRAIT,                // 16K portrait
  SP_K16_LANDSCAPE,               // 16K landscape
  SP_K8_PORTRAIT,                 // 8K portrait
  SP_K8_LANDSCAPE,                // 8K landscape
};

enum class PHOcrPageDirection {
  HORIZONTAL = 0,
  VERTICAL = 2
};

enum class PHOcrLineDirection {
  LEFT_TO_RIGHT = 0,
  RIGHT_TO_LEFT = 1,
  TOP_TO_BOTTOM = 2
};

enum class PHOcrTextAlignment {
  NONE,                // Can't analysis alignment of text
  ALIGN_LEFT,          // All lines but first line align left
                       // If text have < 3 line --> NONE
  ALIGN_RIGHT,         // All lines align right
                       // If text have < 2 line --> NONE
  ALIGN_CENTER,        // All lines align center
                       // If text have < 2 line --> NONE
  ALIGN_JUSTIFY,       // Justify all line except last line
  ALIGN_JUSTIFY_FULL,  // Justify all line NOT except last line
};


enum class PHOcrListType {
  NUMBERING,
  BULLET,
  NONE
};

enum class PHOcrNumberingName {
  ARABIC_NON_SUFFIX,
  ARABIC_PERIOD,
  ARABIC_PAREN_R,
  ALPHA_LC_PERIOD,
  ALPHA_UC_PERIOD,
  ALPHA_LC_PAREN_R,
  ROMAN_LC_PERIOD,
  ROMAN_UC_PERIOD
};

enum class PHOcrBulletName {
  HOLLOW_ROUND,
  FILLED_ROUND
};

/**
 *  +------------------+  Orientation Example:
 *  | 1 Aaaa Aaaa Aaaa |  ====================
 *  | Aaa aa aaa aa    |  To left is a diagram of some (1) English and
 *  | aaaaaa A aa aaa. |  (2) Chinese text and a (3) photo credit.
 *  |                2 |
 *  |   #######  c c C |  Upright Latin characters are represented as A and a.
 *  |   #######  c c c |  '<' represents a latin character rotated
 *  | < #######  c c c |      anti-clockwise 90 degrees.
 *  | < #######  c   c |
 *  | < #######  .   c |  Upright Chinese characters are represented C and c.
 *  | 3 #######      c |
 *  +------------------+  NOTA BENE: enum values here should match goodoc.proto

 * If you orient your head so that "up" aligns with Orientation,
 * then the characters will appear "right side up" and readable.
 *
 * In the example above, both the English and Chinese paragraphs are oriented
 * so their "up" is the top of the page (page up).  The photo credit is read
 * with one's head turned leftward ("up" is to page left).
 *
 * The values of this enum match the convention of Tesseract's osdetect.h
*/
enum class PHOcrOrientation {
  ORIENTATION_ERROR      = -1,
  ORIENTATION_PAGE_UP    = 0,
  ORIENTATION_PAGE_RIGHT = 1,
  ORIENTATION_PAGE_DOWN  = 2,
  ORIENTATION_PAGE_LEFT  = 3,
};

/**
 * The grapheme clusters within a line of text are laid out logically
 * in this direction, judged when looking at the text line rotated so that
 * its Orientation is "page up".
 *
 * For English text, the writing direction is left-to-right.  For the
 * Chinese text in the above example, the writing direction is top-to-bottom.
*/
enum class PHOcrWritingDirection {
  WRITING_DIRECTION_ERROR         = -1,
  WRITING_DIRECTION_LEFT_TO_RIGHT = 0,
  WRITING_DIRECTION_RIGHT_TO_LEFT = 1,
  WRITING_DIRECTION_TOP_TO_BOTTOM = 2,
};

/**
 * The text lines are read in the given sequence.
 *
 * In English, the order is top-to-bottom.
 * In Chinese, vertical text lines are read right-to-left.  Mongolian is
 * written in vertical columns top to bottom like Chinese, but the lines
 * order left-to right.
 *
 * Note that only some combinations make sense.  For example,
 * WRITING_DIRECTION_LEFT_TO_RIGHT implies TEXTLINE_ORDER_TOP_TO_BOTTOM
*/
enum class PHOcrTextlineOrder {
  TEXTLINE_ORDER_LEFT_TO_RIGHT = 0,
  TEXTLINE_ORDER_RIGHT_TO_LEFT = 1,
  TEXTLINE_ORDER_TOP_TO_BOTTOM = 2,
};

/**
 * Type of parallel inside of PHOcr
 */
enum class PHOcrParallelType {
  PARALLEL_INSIDE_ONE_PAGE_PROCESSING = 0,  // Parallel inside each page processing
  PARALLEL_TWO_PAGES_IN_SAME_TIME     = 1,  // Parallel two pages in the same time and disable parallel inside each page
  PARALLEL_AUTO_SELECT                = 2   // Auto selection base on input scan type
};

/**
 * Type of barcode supplemental code that PHOcr support to detect
 */
enum class PHOcrBarcodeSupplementalCode {
  BSC_AUTOMATIC_DETECTION          = 0,  // Automatic detection
  BSC_WITHOUT_AUTOMATIC_DETECTION  = 1,  // Without automatic detection
  BSC_WITH_AUTO_DETECTION          = 2,  // With auto detection (No. of digit is automatically detected)
  BSC_WITH_AUTO_DETECTION_2_DIGITS = 3,  // With auto detection (2 digits)
  BSC_WITH_AUTO_DETECTION_5_DIGITS = 4   // With auto detection (5 digits)
};

}  // namespace phocr
