/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    OutputFileType.h
 * @brief
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    May 20, 2019
 *****************************************************************************/
#ifndef PHOCRTESTS_OUTPUTFILETYPE_H_
#define PHOCRTESTS_OUTPUTFILETYPE_H_

// Define output file type of PHOcr
enum class OutputFileType {
  OCR_TEXT,
  BB_TEXT,
  PDFA,
  PDF,
  NO_OCR_PDF,
  XML,
  DOCX,
  PPTX,
  XLSX,
};

#endif  // PHOCRTESTS_OUTPUTFILETYPE_H_ //
