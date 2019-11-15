/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrDeclaration.h
 * @brief   Declaration in PHOcr interface
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Jan 24, 2019
 *****************************************************************************/
#pragma once

namespace phocr {

// Definition for PHOcr cancel decision method which PHOcr used for
// check whether or not phocr should cancel running
typedef bool (*PHOcrCancelDecisionMethod)();

}  // namespace phocr
