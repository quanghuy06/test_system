cmake_minimum_required(VERSION 3.5)

project(PHOcrTest VERSION 1.0.0)

# Set link directory
link_directories(
    ${CMAKE_BINARY_DIR}/phocr/
    ${PROJECT_SOURCE_DIR}/../3rdparty/googletest-1.8.1/lib/
)

############################################################
# Create an executable
############################################################
# Add an executable with the above sources
add_executable(phocrtests
    Main.cpp
    TestDataManager.cpp
    TestHelper.cpp
    UnitTestUtility.cpp
    UnitTestBarcodeUtility.cpp
    TestPHOcrDocument_Export.cpp
    TestPHOcrDocument_Constructor.cpp
    TestPHOcrDocument_Process.cpp
    TestPHOcrDocument_GetNumberOfPages.cpp
    TestPHOcrDocument_GetOrSetSettings.cpp
    TestPHOcrDocument_GetPage.cpp
    TestPHOcrDocument_RemovePage.cpp
    TestPHOcrDocument_SetCancelDecisionMethod.cpp
    TestPHOcrDocument_SetAndGetLogLevel.cpp
    TestPHOcrDocument_GetTextResults.cpp
    TestPHOcrPage_GetTextResult.cpp
    TestBarcode_BarcodeMode.cpp
    TestPHOcrDocumentData_GetDocumentContent.cpp
    TestPHOcrPageData_GetPageContent.cpp
    TestPHOcrSetting_OCRMultiPagesInParallel.cpp
    TestPHOcrAPI_ExceptionHandling.cpp
    TestDecompressAndCacheTrainedDataInMeMory_Feature.cpp
    TestPHOcrSetting_SetAndGetIccSourceProfile.cpp
    TestPHOcrSettings_Set_Get_PHOcrWorkingDirectory.cpp
    TestPHOcrSettingsSetGetDPI.cpp
    TestPHOcrExport_MemoryFileContemporary.cpp
    TestPHOcrAPI_BarcodeSupplementalCode.cpp
    TestBarcode_BarcodeSupplementalCode.cpp
    TestPHOcrAPI_BarcodeStartStopCodeOfCode39.cpp
    TestBarcode_BarcodeStartStopCodeOfCode39.cpp
    TestPHOcrAPI_BarcodeCheckDigitForOneD.cpp
    TestBarcode_BarcodeCheckDigitForOneD.cpp
    TestPHOcrAPI_PostnetBarcodeDetection.cpp
    TestBarcode_PostnetBarcodeDetection.cpp
)

target_include_directories(phocrtests PUBLIC
    ${PROJECT_SOURCE_DIR}/../
    ${PROJECT_SOURCE_DIR}/../phocr/api
    ${PROJECT_SOURCE_DIR}/../3rdparty/googletest-1.8.1/include
)

# link the new hello_library target with the phocrtests target
target_link_libraries(phocrtests PUBLIC
    PHOcr
    gtest
    boost_system
    boost_regex
    boost_locale
    boost_filesystem
)

############################################################
# Install
############################################################

set_target_properties(phocrtests PROPERTIES INSTALL_RPATH ${CMAKE_INSTALL_PREFIX}/lib)
install(TARGETS phocrtests DESTINATION bin)

############################################################
# Testing
############################################################

file(REMOVE_RECURSE
    phocrexample
)

install(FILES
    ../phocrexamples/Makefile
    DESTINATION phocrexamples
)
install(DIRECTORY
    ../phocrexamples/memory
    ../phocrexamples/phocrexample
    ../phocrexamples/msm_performance_test
    ../phocrexamples/sample1
    ../phocrexamples/sample2
    ../phocrexamples/cancel_phocr
    ../phocrexamples/msm_sample
    DESTINATION phocrexamples
)
install(DIRECTORY
    ../phocrtests
    DESTINATION phocrexamples
)

install(CODE
"
message(\"Build phocr examples\")
execute_process (
    COMMAND \"make\"
    WORKING_DIRECTORY \${CMAKE_INSTALL_PREFIX}/phocrexamples/
    OUTPUT_VARIABLE _out
    ERROR_VARIABLE _err
    RESULT_VARIABLE _res
)

# Remove object file which created by building in example folder
file(GLOB_RECURSE _object_files \"\${CMAKE_INSTALL_PREFIX}/phocrexamples/**/*.o\")
file(REMOVE_RECURSE \${_object_files})
message(\"Clean up object files: \${_object_files}\")

If (NOT \${_res} EQUAL \"0\")
    message(\"Build fail ==========\")
    message( FATAL_ERROR
        \\\"\\n
        =======phocr-out: \${_out}\\n
        =======phocr-err: \${_err}\\n
        =======phocr-res: \${_res}\\n
        \\\")
else()
    message(\"Build all examples success!\")
endif ()
"

)
