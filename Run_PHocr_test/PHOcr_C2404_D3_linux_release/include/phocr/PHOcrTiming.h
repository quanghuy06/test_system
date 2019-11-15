/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    PHOcrTiming.h
 * @brief
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Apr 19, 2019
 *****************************************************************************/
#ifndef PHOCR_API_PHOCRTIMING_H_
#define PHOCR_API_PHOCRTIMING_H_

#include <chrono>
#include <string>

namespace ch = std::chrono;
namespace phocr {
/**
 * Manage the timing of PHOcr program
 */
class PHOcrTiming {
  // Start point of time
  static ch::system_clock::time_point start_time_;

  // End point of time
  static ch::system_clock::time_point end_time_;

  /**
   * Check if both start time and end time is set up yet
   * @return
   */
  static bool IsSetUpTimingDone();

 public:
  // Delete constructor
  PHOcrTiming() = delete;

  // Delete destructor
  ~PHOcrTiming() = delete;

  /**
   * Set the start time at the point of time where this function is called
   */
  static void SetStartTimeNow();

  /**
   * Set the end time at the point of time where this function is called
   */
  static void SetEndTimeNow();

  /**
   * Get end time
   * @return
   */
  static ch::system_clock::time_point get_end_time();

  /**
   * Set end time
   * @param end_time
   */
  void set_end_time(ch::system_clock::time_point end_time);

  /**
   * Get start time
   * @return
   */
  static ch::system_clock::time_point get_start_time();

  /**
   * Set start time
   * @param start_time
   */
  void set_start_time(ch::system_clock::time_point start_time);

  /**
   * Measure elapsed time between end time and start time in milliseconds
   * @param slow_factor If you think the target system has worse performance. If
   * target computer's performance is better, then use slow factor as
   * 1/slow_factor
   * @return
   */
  static double MeasureElapsedTime(double slow_factor = 1);

  /**
   * Estimate the approximate time when run on board
   * @return
   */
  static double MeasureElapsedTimeOnBoard();

  /**
   * Print a time_point object to system time format, like this:
   * Mon May  6 16:50:21 ICT 2019
   * @param timepoint
   */
  static void PrintSystemTime(const ch::system_clock::time_point& timepoint);

  /**
   * Print system time_point at now
   */
  static void PrintSystemTimeNow();

  /**
   * Check if start time is set
   * @return
   */
  static bool IsStartTimeSet();

  /**
   * Check if end time is set
   * @return
   */
  static bool IsEndTimeSet();

  /**
   * Create the timestamp based on current time
   */
  static long TimeStamp();

  /**
   * Paste timestamp to the input
   * @param input
   */
  static void PasteTimeStamp(std::string& input);
};

}  // namespace phocr

#endif  // PHOCR_API_PHOCRTIMING_H_ //
