/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrRectangle.h
 * @brief   Header only implementation of PHOcrRectangle class.
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    2018-12-19
 *****************************************************************************/

#pragma once

#include "PHOcrDefines.h"

namespace phocr {

/**
 * PHOcrRectangle Class Definition.
 *
 * This class provides the ability to specify a rectangular region
 * using x,y,w,h notation. This is used for PHOcrPage class functions
 * GetBarcodeInAZone and GetStringInAZone.
 *
 * Only documented with minor comments due to class simplicity.
 */
template <typename T>
class PHOCR_API PHOcrRectangle
{
public:
    T x;
    T y;
    T width;
    T height;

    PHOcrRectangle(void)
    {
    }


    PHOcrRectangle(const PHOcrRectangle& rect)
    {
      this->x = rect.x;
      this->y = rect.y;
      this->width = rect.width;
      this->height = rect.height;
    }


    PHOcrRectangle(T x, T y, T width, T height)
    {
        this->x = x;
        this->y = y;
        this->height = height;
        this->width = width;
    }

    ~PHOcrRectangle(void)
    {
    }

    bool IsOverlap(const PHOcrRectangle& rect)
    {
        if((x + width) < rect.x)
        {
            return false;
        }
        if((rect.x + rect.width) < x)
        {
            return false;
        }
        if((y + height) < rect.y)
        {
            return false;
        }
        if((rect.y + rect.height) < y)
        {
            return false;
        }
        return true;
    }

    /**
     * Validate rectangle (a string zone or a barcode zone)
     */
    bool IsValid() const {
      if (x < 0 || y < 0 || width < 0 || height < 0) {
        return false;
      }
      return true;
    }
};

}  // namespace phocr
