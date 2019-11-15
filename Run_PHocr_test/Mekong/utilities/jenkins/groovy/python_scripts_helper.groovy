/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 01/10/2019
* Description: This script defines some methods to get path to useful python scripts
*/

/**
* Relative path to library folder which includes python scripts. Root path should be Mekong
* directory.
*/
def PythonLibR() {
    return "utilities/jenkins"
}

/**
* Relative path to library folder which includes python scripts for making reports
*/
def PythonReportLibR() {
    return "utilities/report"
}

/**
* Relative path to library folder which includes python scripts work with SVN
*/
def PythonSvnLibR() {
    return "utilities/svn_manager"
}

/**
* Relative path to library folder which includes python scripts for system management
*/
def PythonManagerLibR() {
    return "utilities/manager"
}

/**
* Name of python script which help updating delta version of projects file
*/
def UpdateDeltaVersionProjectsScriptName() {
    return "update_delta_version_projects.py"
}

/**
* Relative path to script which help updating delta version of projects file
*/
def UpdateDeltaVersionProjectsScriptR() {
    return "${PythonLibR()}/${UpdateDeltaVersionProjectsScriptName()}"
}

/**
* Get path to script which help updating delta version of projects file
*/
def UpdateDeltaVersionProjectsScriptPath(String mekong) {
    return "${mekong}/${UpdateDeltaVersionProjectsScriptR()}"
}

/**
* Name of python script which help updating delta-change mapping file
*/
def UpdateDeltaChangeMappingScriptName() {
    return "update_delta_change_mapping.py"
}

/**
* Relative path to python script which help updating delta-change mapping file
*/
def UpdateDeltaChangeMappingScriptR() {
    return "${PythonLibR()}/${UpdateDeltaChangeMappingScriptName()}"
}

/**
* Get full path to python script which help updating delta-change mapping file base on root path to
* Mekong known.
*/
def UpdateDeltaChangeMappingScriptPath(String mekong) {
    return "${mekong}/${UpdateDeltaChangeMappingScriptR()}"
}

/**
* Name of python script which help updating change-build mapping file
*/
def UpdateChangeBuildMappingScriptName() {
    return "update_change_build_mapping.py"
}

/**
* Relative path to python script which help updating change-build mapping file
*/
def UpdateChangeBuildMappingScriptR() {
    return "${PythonLibR()}/${UpdateChangeBuildMappingScriptName()}"
}

/**
* Get full path to python script which help updating change-build mapping file base on path to
* Mekong directory passed.
*/
def UpdateChangeBuildMappingScriptPath(String mekong) {
    return "${mekong}/${UpdateChangeBuildMappingScriptR()}"
}

/**
* Name of python script which help removing all old results when a change was merged into base line
* project.
*/
def DeleteOldResultsPostIntegrationScriptName() {
    return "delete_old_test_result.py"
}

/**
* Relative path to python script which help removing all old results when a change was merged
* into base line project.
*/
def DeleteOldResultsPostIntegrationScriptR() {
    return "${PythonLibR()}/${DeleteOldResultsPostIntegrationScriptName()}"
}

/**
* Get full path to python script which help removing all old results when a change was merged into
* base line project base on path to Mekong directory passed.
*/
def DeleteOldResultsPostIntegrationScriptPath(String mekong) {
    return "${mekong}/${DeleteOldResultsPostIntegrationScriptR()}"
}

/**
* Name of python script which help making accuracy report for delta version when a change is merged
* into base line.
*/
def MakeDeltaAccuracyReportScriptName() {
    return "report_delta_accuracy.py"
}

/**
* Relative path to python script which help making accuracy report for delta version when a change
* is merged into base line.
*/
def MakeDeltaAccuracyReportScriptR() {
    return "${PythonReportLibR()}/${MakeDeltaAccuracyReportScriptName()}"
}

/**
* Get full path to python script which help making accuracy report for delta version when a change
is merged into base line base on path to Mekong directory passed.
*/
def MakeDeltaAccuracyReportScriptPath(String mekong) {
    return "${mekong}/${MakeDeltaAccuracyReportScriptR()}"
}

/**
* Name of python script which help making performance report for delta version when a change is
* merged into base line of project.
*/
def MakeDeltaPerformanceReportScriptName() {
    return "report_delta_performance.py"
}

/**
* Relative path to python script which help making performance report for delta version when a
* change is merged into base line of project.
*/
def MakeDeltaPerformanceReportScriptR() {
    return "${PythonReportLibR()}/${MakeDeltaPerformanceReportScriptName()}"
}

/**
* Get full path to python script which help making performance report for delta version when a
* change is merged into base line of project base on path to Mekong directory passed.
*/
def MakeDeltaPerformanceReportScriptPath(String mekong) {
    return "${mekong}/${MakeDeltaPerformanceReportScriptR()}"
}

/**
* Name of python script which help submit accuracy report of delta versions to SVN in Post
* Integration
*/
def SubmitDeltaAccuracyReportSvnScriptName() {
    return "add_accuracy_to_svn.py"
}

/**
* Relative path to python script which help submit accuracy report of delta versions to SVN in Post
* Integration
*/
def SubmitDeltaAccuracyReportSvnScriptR() {
    return "${PythonSvnLibR()}/${SubmitDeltaAccuracyReportSvnScriptName()}"
}

/**
* Get full path to python script which help submit accuracy report of delta versions to SVN in Post
* Integration base on path to Mekong directory passed.
*/
def SubmitDeltaAccuracyReportSvnScriptPath(String mekong) {
    return "${mekong}/${SubmitDeltaAccuracyReportSvnScriptR()}"
}

/**
* Name of python script which help update change log of project on SVN in Post Integration
*/
def UpdateChangeLogSvnScriptName() {
    return "update_change_log.py"
}

/**
* Relative path to python script which help update change log of project on SVN in Post Integration
*/
def UpdateChangeLogSvnScriptR() {
    return "${PythonSvnLibR()}/${UpdateChangeLogSvnScriptName()}"
}

/**
* Get full path to python script which help update change log of project on SVN in Post Integration
* base on path to Mekong directory passed.
*/
def UpdateChangeLogSvnScriptPath(String mekong) {
    return "${mekong}/${UpdateChangeLogSvnScriptR()}"
}

/**
* Name of python script which help sending email which attaches reports in Post Integration
*/
def SendEmailPostIntegrationScriptName() {
    return "send_email_post_integration.py"
}

/**
* Relative path to python script which help sending email which attaches reports in Post
* Integration
*/
def SendEmailPostIntegrationScriptR() {
    return "utilities/send_email/${SendEmailPostIntegrationScriptName()}"
}

/**
* Get full path to python script which help sending email which attaches reports in Post Integration
* base on path of Mekong directory passed.
*/
def SendEmailPostIntegrationScriptPath(String mekong) {
    return "${mekong}/${SendEmailPostIntegrationScriptR()}"
}

/**
* Name of python script which help updating test results of latest success build in Integration Test
* to database as new reference data when a change was merged.
*/
def UpdateReferenceDataScriptName() {
    return "update_reference_data_post_integration.py"
}

/**
* Relative path to python script which help updating test results of latest success build in
* Integration Test to database as new reference data when a change was merged.
*/
def UpdateReferenceDataScriptR() {
    return "${PythonLibR()}/${UpdateReferenceDataScriptName()}"
}

/**
* Get full path to python script which help updating test results of latest success build in
* Integration Test to database as new reference data when a change was merged base on path to Mekong
* directory passed.
*/
def UpdateReferenceDataScriptPath(String mekong) {
    return "${mekong}/${UpdateReferenceDataScriptR()}"
}

/**
* Name of python script which help updating test cases folder on test nodes of test system to
* update new reference data in Post Integration
*/
def UpdateTestCasesFolderOnNodesScriptName() {
    return "update_test_cases_folder_on_nodes.py"
}

/**
* Relative path to python script which help updating test cases folder on test nodes of test
* system to update new reference data in Post Integration
*/
def UpdateTestCasesFolderOnNodesScriptR() {
    return "${PythonLibR()}/${UpdateTestCasesFolderOnNodesScriptName()}"
}

/**
* Get full path to python script which help updating test cases folder on test nodes of test
* system to update new reference data in Post Integration base on path to mekong directory passed
*/
def UpdateTestCasesFolderOnNodesScriptPath(String mekong) {
    return "${mekong}/${UpdateTestCasesFolderOnNodesScriptR()}"
}

/**
* Name of python script which help preparing build packages for new version of project in Post
* Integration
*/
def PrepareBuildPackagesScriptName() {
    return "prepare_release_build_packages.py"
}

/**
* Relative path to python script which help preparing build packages for new version of project in
* Post Integration
*/
def PrepareBuildPackagesScriptR() {
    return "${PythonLibR()}/${PrepareBuildPackagesScriptName()}"
}

/**
* Get full path to python script which help preparing build packages for new version of project in
* Post Integration base on path to Mekong directory passed.
*/
def PrepareBuildPackagesScriptPath(String mekong) {
    return "${mekong}/${PrepareBuildPackagesScriptR()}"
}

return this
