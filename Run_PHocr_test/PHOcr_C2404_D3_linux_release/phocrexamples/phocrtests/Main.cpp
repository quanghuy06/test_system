/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    main.cpp
 * @brief   main phocr testing file
 * @author  PHOcr team<ocrpoc@toshiba-tsdv.com>
 * @date    Mar 13, 2019
 *****************************************************************************/

#define CATCH_CONFIG_RUNNER
#include <csignal>
#include <algorithm>
#include <boost/filesystem.hpp>
#include "gtest/gtest.h"

#include "phocrtests/TestDataManager.h"

using phocr::TestDataManager;
namespace fs = boost::filesystem;

bool SetupTest(int argc, char* argv[],
               std::vector<int>& abandon_indexes) {
  std::string phocr_data_path = "";
  for (int i = 0; i < argc; ++i) {
    if ((std::string(argv[i]) == "--test-data-path") &&
        (i < argc - 1)) {
      phocr_data_path = argv[i + 1];
      abandon_indexes.push_back(i);
      abandon_indexes.push_back(i + 1);
    }
  }
  if (phocr_data_path == "") {
    return false;
  }

  // Create test data manager on phocr data path
  if (!fs::exists(phocr_data_path)) {
    fprintf(stderr, "PHOcr data path: '%s' not exists on system\n",
            phocr_data_path.c_str());
    return false;
  }

  TestDataManager::Instance(phocr_data_path);
  return true;
}

void PrintHelp(int argc, char* argv[]) {
  fprintf(stderr, "Usage: %s --test-data-path <phocr_data_path>\n", argv[0]);
  fprintf(stderr, "Usage: %s --test-data-path <phocr_data_path> "
      "--gtest_filter=ClassTest.*\n", argv[0]);
}

int main(int argc, char* argv[]) {
  // Global setup...
  std::vector<int> abandon_indexes;
  if (!SetupTest(argc, argv, abandon_indexes)) {
    PrintHelp(argc, argv);
    return 1;
  }

  int parameters_count = argc - abandon_indexes.size();
  char** parameters = new char*[parameters_count];
  int catch_parameters_index = 0;
  for (int i = 0; i < argc; ++i) {
    auto i_position_in_abandon_list =
        std::find(abandon_indexes.begin(), abandon_indexes.end(), i);
    if (i_position_in_abandon_list == abandon_indexes.end()) {
      parameters[catch_parameters_index++] = argv[i];
    }
  }

  testing::InitGoogleTest(&parameters_count, parameters);

  /**
   * deallocated memory before exit program to pass memcheck
   */
  int result_status = RUN_ALL_TESTS();
  delete[] parameters;
  return result_status;
}
