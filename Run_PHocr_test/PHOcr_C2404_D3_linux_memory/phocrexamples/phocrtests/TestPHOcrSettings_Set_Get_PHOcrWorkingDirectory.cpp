/*****************************************************************************
 * Copyright 2017 TOSHIBA TEC Corporation
 * @file    TestPHOcrSettingsSetGetPHOcrWorkingDirectory.cpp
 * @brief   This module is used to
 * @author  Trong Nguyen Van<trong.nguyenvan@toshiba-tsdv.com>
 * @date    Aug 30, 2019
 *****************************************************************************/

#include "TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory.h"
#include <sys/stat.h>
#include <unistd.h>
#include <vector>
#include <thread>
#include <stdexcept>
#include <boost/filesystem.hpp>
#include "UnitTestUtility.h"
#include "TestDataManager.h"
#include "phocr/api/PHOcrDocument.h"
#include "phocr/api/PHOcrSettings.h"
#include "phocr/api/PHOcrDocumentMaker.h"
#include "phocr/api/PHOcrExportSetting.h"
#include "phocr/api/PHOcrEnum.h"
#include "phocr/api/PHOcrStatus.h"
#include "phocr/api/PHOcrStringHelper.h"

// Namespace that I will use
using phocr::PHOcrDocumentPtr;
using phocr::PHOcrSettings;
using phocr::PHOcrDocumentMaker;
using phocr::PHOcrExportSetting;
using phocr::PHOcrExportFormat;
using phocr::PHOcrStatus;
using phocr::TestDataManager;
using phocr::ConvertToWString;
using phocr::ConvertToString;

namespace fs = boost::filesystem;

TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory::TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory()
    : result_name_(L"result"),
      phocr_working_dir_("phocr_working_dir"),
      permission_denied_dir_("permission_denied_dir") {
  image_path_ = ConvertToWString(phocr::TestDataManager::Instance()->GetPath("01_0033.jpg"));
}

TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory::~TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory() {
  UnitTestUtility::DeletePossiblePHOcrOutputFile();
}

bool TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory::IsPHOcrDirectoryWorked(
    std::atomic<bool>& is_done) {
  const std::string kTXTFile = ".txt";
  const std::string kXMLFile = ".xml";
  const std::string kXLSXFile = ".xlsx";
  const std::string kDOCXFile = ".docx";
  const std::string kPPTXFile = ".pptx";
  const std::string kPDFFile = ".pdf";
  bool have_txt_file(false);
  bool have_xml_file(false);
  bool have_pdf_file(false);
  bool have_docx_file(false);
  bool have_xlsx_file(false);
  bool have_pptx_file(false);

  // Processing there
  while (is_done.load() == false) {
    for (fs::directory_iterator itr(phocr_working_dir_); itr != fs::directory_iterator(); ++itr) {
      std::string file_extension = fs::extension(itr->path());
      if (!have_txt_file && file_extension == kTXTFile) {
        have_txt_file = true;
      } else if (!have_xml_file && file_extension == kXMLFile) {
        have_xml_file = true;
      } else if (!have_xlsx_file && file_extension == kXLSXFile) {
        have_xlsx_file = true;
      } else if (!have_docx_file && file_extension == kDOCXFile) {
        have_docx_file = true;
      } else if (!have_pptx_file && file_extension == kPPTXFile) {
        have_pptx_file = true;
      } else if (!have_pdf_file && file_extension == kPDFFile) {
        have_pdf_file = true;
      }

      // Early break
      if (have_txt_file && have_xml_file && have_pdf_file && have_docx_file
          && have_xlsx_file && have_pptx_file) {
        return true;
      }
    }
  }
  return false;
}

void TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory::DoPHOcrExport(
    PHOcrDocumentPtr document,
    PHOcrSettings setting,
    std::vector<PHOcrExportSetting> export_setting,
    std::atomic<bool>& is_done) {
  auto export_status = document->PHOcrExport(export_setting);
  is_done = true;
  ASSERT_EQ(export_status, PHOcrStatus::PHOCR_OK);
}

// In this fixture, user doesn't set the working directory for PHOcr. I must
// ensure that PHOcr data is stored in current running directory.
TEST_F(TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory, user_do_not_set_PHOcr_working_directory) {
  PHOcrSettings settings;
  settings.SetOCRLanguage(L"English");
  PHOcrDocumentPtr document;
  PHOcrDocumentMaker::CreateDocument(document, image_path_, settings);
  std::vector<PHOcrExportSetting> export_setting = {
      {
          result_name_, PHOcrExportFormat::EF_TXT
      },
      {
          result_name_, PHOcrExportFormat::EF_XML
      },
      {
          result_name_, PHOcrExportFormat::EF_DOCX
      },
      {
          result_name_, PHOcrExportFormat::EF_PDF
      }
  };
  auto export_status = document->PHOcrExport(export_setting);
  ASSERT_EQ(export_status, PHOcrStatus::PHOCR_OK);

  // Check result file existance
  std::string result_file_prefix = ConvertToString(result_name_);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".txt") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".xml") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".docx") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".pdf") > 0);
}

// In this fixture, user set the working directory as current running directory
TEST_F(TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory, user_set_working_directory_same_with_current_running_directory) {
  PHOcrSettings settings;
  settings.SetOCRLanguage(L"English");
  PHOcrStatus setup_status = settings.SetPHOcrWorkingDirectory(".");
  ASSERT_EQ(setup_status, PHOcrStatus::PHOCR_OK);
  PHOcrDocumentPtr document;
  PHOcrDocumentMaker::CreateDocument(document, image_path_, settings);
  std::vector<PHOcrExportSetting> export_setting = {
      {
          result_name_, PHOcrExportFormat::EF_TXT
      },
      {
          result_name_, PHOcrExportFormat::EF_XML
      },
      {
          result_name_, PHOcrExportFormat::EF_DOCX
      },
      {
          result_name_, PHOcrExportFormat::EF_PDF
      }
  };
  auto export_status = document->PHOcrExport(export_setting);
  ASSERT_EQ(export_status, PHOcrStatus::PHOCR_OK);

  // Check result file existance
  std::string result_file_prefix = ConvertToString(result_name_);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".txt") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".xml") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".docx") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".pdf") > 0);
}

// In this fixture, user sets the wrong value for working directory
TEST_F(TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory, user_set_wrong_PHOcr_working_directory) {
  PHOcrSettings settings;

  // Null value
  const char* working_dir(nullptr);
  PHOcrStatus status = settings.SetPHOcrWorkingDirectory(working_dir);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);

  // Empty value
  working_dir = "";
  status = settings.SetPHOcrWorkingDirectory(working_dir);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);

  // Invalid working directory
  working_dir = "/invalid/path";
  status = settings.SetPHOcrWorkingDirectory(working_dir);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_INVALID_ARGUMENT_ERROR);
}

// In this fixture, user set the right value for working directory
TEST_F(TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory, user_set_right_PHOcr_working_directory) {
  PHOcrSettings settings;
  settings.SetOCRLanguage(L"English");

  // Set the right working directory
  // Create new directory on current running folder and set it as the PHOcr
  // working directory
  UnitTestUtility::CreateNewDirectory(phocr_working_dir_);
  PHOcrStatus status = settings.SetPHOcrWorkingDirectory(phocr_working_dir_.c_str());
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);

  PHOcrDocumentPtr document;
  PHOcrDocumentMaker::CreateDocument(document, image_path_, settings);
  std::vector<PHOcrExportSetting> export_setting = {
      {
          result_name_, PHOcrExportFormat::EF_TXT
      },
      {
          result_name_, PHOcrExportFormat::EF_BB
      },
      {
          result_name_, PHOcrExportFormat::EF_XML
      },
      {
          result_name_, PHOcrExportFormat::EF_DOCX
      },
      {
          result_name_, PHOcrExportFormat::EF_XLSX
      },
      {
          result_name_, PHOcrExportFormat::EF_PPTX
      },
      {
          result_name_, PHOcrExportFormat::EF_PDF
      },
  };

  // To ensure PHOcr is working well in the setup directory. I create new
  // thread to run PHOcrExport
  // I must ensure that some time this folder must have the
  std::atomic<bool> is_done(false);
  std::thread check_working_directory(
      &TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory::DoPHOcrExport,
      this,
      document,
      settings,
      export_setting,
      std::ref(is_done));
  bool is_working_dir_work_well = IsPHOcrDirectoryWorked(is_done);
  check_working_directory.join();
  EXPECT_EQ(is_working_dir_work_well, true);
}

// In this fixture, user gets the working directory of PHOcr. I must ensure that
// this action is in well define behavior
TEST_F(TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory, user_get_PHOcr_working_directory) {
  // When working directory is't setup. I ensure that running dir and PHOcr
  // running dir is the same
  PHOcrSettings settings;
  std::string running_path = UnitTestUtility::GetCurrentPath();
  std::string phocr_working_directory = settings.GetPHOcrWorkingDirectory();
  ASSERT_EQ(phocr_working_directory, running_path);

  UnitTestUtility::CreateNewDirectory(phocr_working_dir_);
  // Set PHOcr working dir
  PHOcrStatus status = settings.SetPHOcrWorkingDirectory(phocr_working_dir_.c_str());
  phocr_working_directory = settings.GetPHOcrWorkingDirectory();
  ASSERT_EQ(phocr_working_directory, phocr_working_dir_);
  UnitTestUtility::DeleteDirectoryRecursive(phocr_working_dir_);
}

// This fixture test the case that user set the working directory that don't
// have enough permisson
TEST_F(TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory, user_set_PHOcr_working_directory_with_permission_denied_directory) {
  std::string permission_denied_directory =
      (fs::current_path() / fs::path(permission_denied_dir_)).string();

  // Create a directory at permission_denied_directory with
  int dir_err = mkdir(permission_denied_directory.c_str(), S_IRUSR);
  if (dir_err == 0) {
    PHOcrSettings settings;
    PHOcrStatus status = settings.SetPHOcrWorkingDirectory(permission_denied_directory.c_str());
    EXPECT_NE(status, PHOcrStatus::PHOCR_OK);
    UnitTestUtility::DeleteDirectoryRecursive(permission_denied_directory);
  } else {
    std::cerr << "Error when try to create folder " + permission_denied_directory << std::endl;
  }
}

// In this fixture, developer set working directory but still write data to
// running directory => PHOcr will show error in this case
TEST_F(TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory, user_write_any_data_on_running_directory) {
  // Create a directory without writing permisson
  const char* running_dir = "running_dir";
  const char* output_dir = "output_dir";
  const char* working_dir = "working_dir";
  fs::path current_path = fs::current_path();
  fs::path running_path = current_path / fs::path(running_dir);
  fs::path output_path = current_path / fs::path(output_dir);
  fs::path working_path = current_path / fs::path(working_dir);
  running_dir = running_path.c_str();
  output_dir = output_path.c_str();
  working_dir = working_path.c_str();

  if (fs::exists(running_dir)) {
    fs::remove_all(running_dir);
  }
  // Create running directory have owner and group excutable, read permisson
  int mkdir_status = mkdir(running_dir, S_IXUSR | S_IXGRP | S_IXOTH | S_IRUSR | S_IRGRP | S_IROTH);
  if (mkdir_status == -1) {
    std::cerr << "Error when try to create folder " + std::string(running_dir) << std::endl;
    return;
  }

  if (fs::exists(working_dir)) {
    fs::remove_all(working_dir);
  }
  // Create working directory have full permission
  mkdir_status = mkdir(working_dir, S_IRWXU | S_IRWXG | S_IRWXO);
  if (mkdir_status == -1) {
    std::cerr << "Error when try to create folder " + std::string(working_dir) << std::endl;
    return;
  }

  if (fs::exists(output_dir)) {
    fs::remove_all(output_dir);
  }
  // Create output directory have full permisson
  mkdir_status = mkdir(output_dir, S_IRWXU | S_IRWXG | S_IRWXO);
  if (mkdir_status == -1) {
    std::cerr << "Error when try to create folder " + std::string(output_dir) << std::endl;
    return;
  }

  // Before changing directory, we must save the absolute path to image
  fs::path image_path(image_path_);
  image_path = fs::absolute(image_path);

  // Change runnig dir to a directory with excutable permission only
  int chdir_status = chdir(running_dir);
  if (chdir_status == -1) {
    std::cerr << "Error when changing directory to " + std::string(running_dir) << std::endl;
    return;
  }

  // Start export document now
  PHOcrSettings settings;
  PHOcrStatus setup_status = settings.SetPHOcrWorkingDirectory(working_dir);
  ASSERT_EQ(setup_status, PHOcrStatus::PHOCR_OK);
  PHOcrDocumentPtr document;
  PHOcrDocumentMaker::CreateDocument(document, image_path.wstring(), settings);
  std::wstring output_file_path = ConvertToWString(output_dir) + L"/" + result_name_;
  std::vector<PHOcrExportSetting> export_setting = {
      {
          output_file_path, PHOcrExportFormat::EF_BB
      },
      {
          output_file_path, PHOcrExportFormat::EF_TXT
      },
      {
          output_file_path, PHOcrExportFormat::EF_XML
      },
      {
          output_file_path, PHOcrExportFormat::EF_DOCX
      },
      {
          output_file_path, PHOcrExportFormat::EF_PPTX
      },
      {
          output_file_path, PHOcrExportFormat::EF_XLSX
      },
      {
          output_file_path, PHOcrExportFormat::EF_PDF
      },
  };

  // Because PHOcrExport catch any kind of exception. So that we must ensure
  // that the status is always success
  PHOcrStatus status = document->PHOcrExport(export_setting);
  ASSERT_EQ(status, PHOcrStatus::PHOCR_OK);

  // Check result file existance
  std::string result_file_prefix = ConvertToString(output_file_path);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + "_0.txt") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".txt") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".xml") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".docx") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".pptx") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".xlsx") > 0);
  ASSERT_TRUE(UnitTestUtility::GetFileSize(result_file_prefix + ".pptx") > 0);

  // Re assign old directory before delete
  chdir_status = chdir(current_path.c_str());
  if (chdir_status == -1) {
    std::cerr << "Error when changing directory to " + current_path.string() << std::endl;
    return;
  }

  UnitTestUtility::DeleteDirectoryRecursive(running_dir);
  UnitTestUtility::DeleteDirectoryRecursive(working_dir);
  UnitTestUtility::DeleteDirectoryRecursive(output_dir);
}
