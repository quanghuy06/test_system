/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrStatus.h
 * @brief   Define the error code
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Jan 21, 2019
 *****************************************************************************/
#pragma once

namespace phocr {

enum class PHOcrStatus {
  // Notify that everything are running in normal
  PHOCR_OK = 0,
  // Notify that phocr are interrupted by cancel functionality
  // which provided by function PHOcrSetCancelDecisionMethod in
  // PHOcrPage and PHOcrDocument
  PHOCR_INTERRUPT_BY_CANCEL,
  // Notify that internal error occurs inside of PHOcr
  PHOCR_INTERNAL_ERROR,
  // Notify that disk space are not enough for PHOcr running
  PHOCR_FULL_DISK_ERROR,
  // Notify that phocr are working with memory more than expect
  PHOCR_OUT_OF_MEMORY_ERROR,
  // Notify that invalid argument of APIs function call
  PHOCR_INVALID_ARGUMENT_ERROR,

  ////////////////////////////// Error for document exporting in begin/end mode
  // Not yet configure for export before call begin export
  PHOCR_ERROR_NOT_YET_CONFIG_FOR_EXPORT,
  // Not yet call begin export
  PHOCR_ERROR_NOT_YET_CALL_BEGIN_EXPORT,
  // Configure for export after begin function already called
  PHOCR_ERROR_CONFIG_FOR_EXPORT_AFTER_BEGIN,
  // Call PHOcrExport during Begin/End mode
  PHOCR_ERROR_CALL_EXPORT_DURING_BEGIN_END_MODE
};

}  // namespace phocr
