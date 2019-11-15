/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrExportSetting.h
 * @brief   Setting structure for exporting
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Jul 31, 2019
 *****************************************************************************/
#ifndef PHOCR_API_PHOCREXPORTSETTING_H_
#define PHOCR_API_PHOCREXPORTSETTING_H_

#include <string>
#include "PHOcrEnum.h"
#include "PHOcrDocumentResult.h"

namespace phocr {
/**
 * Export setting for PHOcr. It maybe file export (construct from file_path
 * and PHOcrExportFormat) or memory export (construct from PHOcrDocumentResult and
 * PHOcrExportFormat)
 */
class PHOcrExportSetting {
  std::wstring export_file_name_;
  PHOcrExportFormat export_format_;
  PHOcrDocumentResult* result_;

 public:
  PHOcrExportSetting();

  PHOcrExportSetting(
      const std::wstring& export_file_name, PHOcrExportFormat export_format);

  PHOcrExportSetting(
      PHOcrDocumentResult* result, PHOcrExportFormat export_format);

  PHOcrExportSetting(const PHOcrExportSetting& src);

  const PHOcrExportSetting& operator=(const PHOcrExportSetting& src);

  const std::wstring& getExportFileName() const;

  void setExportFileName(const std::wstring& export_file_name);

  PHOcrExportFormat getExportFormat() const;

  void setExportFormat(PHOcrExportFormat export_format);

  PHOcrDocumentResult* getDocumentResult() const;

  void setDocumentResult(PHOcrDocumentResult* result);

  bool IsExportingFile() const;

  bool IsExportingMemory() const;

  unsigned int IsValidExportSetting() const;

  std::string DecodeValidExportSettingCode(unsigned int valid_code) const;
};

}  // namespace phocr


#endif  // PHOCR_API_PHOCREXPORTSETTING_H_ //
