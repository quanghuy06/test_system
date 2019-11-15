/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrDefines.h
 * @brief   Export and import macros for dynamic library
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    2018-12-19
 *****************************************************************************/

#pragma once

#if defined(_WIN32) || defined(__CYGWIN__)
    #if defined(PHOCR_EXPORTS)
       #define PHOCR_API __declspec(dllexport)
    #elif defined(PHOCR_IMPORTS)
       #define PHOCR_API __declspec(dllimport)
    #else
       #define PHOCR_API
    #endif
    #define PHOCR_LOCAL
#else
    #if __GNUC__ >= 4
      #if defined(PHOCR_EXPORTS) || defined(PHOCR_IMPORTS)
          #define PHOCR_API  __attribute__ ((visibility ("default")))
          #define PHOCR_LOCAL  __attribute__ ((visibility ("hidden")))
      #else
          #define PHOCR_API
          #define PHOCR_LOCAL
      #endif
    #else
      #define PHOCR_API
      #define PHOCR_LOCAL
    #endif
#endif
