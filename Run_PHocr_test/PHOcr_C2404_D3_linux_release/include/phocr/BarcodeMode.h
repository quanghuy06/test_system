/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    BarcodeMode.h
 * @brief
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    May 15, 2019
 *****************************************************************************/
#ifndef PHOCR_API_BARCODEMODE_H_
#define PHOCR_API_BARCODEMODE_H_

namespace phocr {
/**
 * Types of barcode that PHOcr support to detect
 */
class BarcodeMode {
 public:
  BarcodeMode() = delete;
  virtual ~BarcodeMode() = delete;

  static const unsigned int BM_AUTO;
  static const unsigned int BM_1D_BARCODE;
  static const unsigned int BM_2D_BARCODE;
  static const unsigned int BM_CODE_39;
  static const unsigned int BM_CODE_93;
  static const unsigned int BM_CODE_128;
  static const unsigned int BM_CODABAR;
  static const unsigned int BM_IATA_2_OF_5;
  static const unsigned int BM_INTERLEAVED_2_OF_5;
  static const unsigned int BM_INDUSTRIAL_2_OF_5;
  static const unsigned int BM_MATRIX_2_OF_5;
  static const unsigned int BM_UCC_128;
  static const unsigned int BM_UPC_A;
  static const unsigned int BM_UPC_E;
  static const unsigned int BM_PATCH;
  static const unsigned int BM_POSTNET;
  static const unsigned int BM_AZTEC;
  static const unsigned int BM_DATAMATRIX;
  static const unsigned int BM_MAXICODE;
  static const unsigned int BM_PDF417;
  static const unsigned int BM_QRCODE;
  static const unsigned int BM_EAN_8;
  static const unsigned int BM_EAN_13;

  // Define the maximum value of barcode mode
  static const unsigned int BM_MAXIMUM_VALUE;
};

}  // namespace phocr

#endif  // PHOCR_API_BARCODEMODE_H_ //
