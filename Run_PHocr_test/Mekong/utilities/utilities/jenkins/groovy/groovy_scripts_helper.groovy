/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 01/10/2019
* Description: This script defines some methods to get path to useful groovy scripts
*/

/**
* Relative path to library folder which include groovy scripts. Root path is Mekong directory.
*/
def GroovyLibR() {
    return "utilities/jenkins/groovy"
}

/**
* Name of the groovy script which includes methods to help execute removing old build/test results
* of a change when it was merged into base line of project
*/
def DeleteOldResultsPostIntegrationScriptName() {
    return "delete_old_results.groovy"
}

/**
* Relative path to groovy script includes methods to help remove old results when a change was
* merged where we only keep the latest build success data to save disk space
*/
def DeleteOldResultsPostIntegrationScriptR() {
    return "${GroovyLibR()}/${DeleteOldResultsPostIntegrationScriptName()}"
}

/**
* Path to groovy script includes methods to help remove old results when a change was merged and we
* only keep results of latest success build on Integration Test to save disk space.
*/
def DeleteOldResultsPostIntegrationScriptPath(String mekong) {
    return "${mekong}/${DeleteOldResultsPostIntegrationScriptR()}"
}

/**
* Name of the groovy script which includes custom configuration of jenkins file system which is
* useful information for executing jobs.
*/
def ConfigurationHelperScriptName() {
    return "configuration_helper.groovy"
}

/**
* Relative path of configuration helper groovy script
*/
def ConfigurationHelperScriptR() {
    return "${GroovyLibR()}/${ConfigurationHelperScriptName()}"
}

/**
* Path to groovy script which includes custom configuration of jenkins which is necessary
* information for executing jobs.
*/
def ConfigurationHelperScriptPath(String mekong) {
    return "${mekong}/${ConfigurationHelperScriptR()}"
}

/**
* Name of groovy script which help handling json data file
*/
def HandleJsonScriptName() {
    return "handle_json.groovy"
}

/**
* Relative path script which has methods to handle json data file
*/
def HandleJsonScriptR() {
    return "${GroovyLibR()}/${HandleJsonScriptName()}"
}

/**
* Path to script includes methods to handle json data file
*/
def HandleJsonScriptPath(String mekong) {
    return "${mekong}/${HandleJsonScriptR()}"
}

/**
* Name of groovy script which help handling json file which includes current delta version of
* projects
*/
def HandleDeltaVersionProjectsScriptName() {
    return "handle_delta_version_projects.groovy"
}

/**
* Relative path to groovy script which help handling json file includes current delta version of
* gerrit projects.
*/
def HandleDeltaVersionProjectsScriptR() {
    return "${GroovyLibR()}/${HandleDeltaVersionProjectsScriptName()}"
}

/**
* Get full path to groovy script which help handling json file includes current delta version of
* gerrit projects base on path to Mekong directory passed.
*/
def HandleDeltaVersionProjectsScriptPath(String mekong) {
    return "${mekong}/${HandleDeltaVersionProjectsScriptR()}"
}

/**
* Name of groovy script which help handling json file maps between delta version with change number
* of a project
*/
def HandleDeltaChangeMappingScriptName() {
    return "handle_delta_change_mapping.groovy"
}

/**
* Relative path to groovy script which help handling json file maps between delta version with
* change number of a project
*/
def HandleDeltaChangeMappingScriptR() {
    return "${GroovyLibR()}/${HandleDeltaChangeMappingScriptName()}"
}

/**
* Get full path to  groovy script which help handling json file maps between delta version with
* change number of a project base on path to Mekong directory passed.
*/
def HandleDeltaChangeMappingScriptPath(String mekong) {
    return "${mekong}/${HandleDeltaChangeMappingScriptR()}"
}

/**
* Name of groovy script which help handling json file maps between change number of project and list
* of build numbers which test for it.
*/
def HandleChangeBuildMappingScriptName() {
    return "handle_change_build_mapping.groovy"
}

/**
* Relative path to groovy script which help handling json file maps between change number of
* project and list of build numbers which test for it.
*/
def HandleChangeBuildMappingScriptR() {
    return "${GroovyLibR()}/${HandleChangeBuildMappingScriptName()}"
}

/**
* Get full path to groovy script which help handling json file maps between change number of project
* and list of build numbers which test for it base on path to Mekong directory passed.
*/
def HandleChangeBuildMappingScriptPath(String mekong) {
    return "${mekong}/${HandleChangeBuildMappingScriptR()}"
}

/**
* Name of groovy script which help making reports in post integration test
*/
def MakeReportsScriptName() {
    return "make_delta_reports.groovy"
}

/**
* Relative path to groovy script which help making reports in post integration test
*/
def MakeReportsScriptR() {
    return "${GroovyLibR()}/${MakeReportsScriptName()}"
}

/**
* Get full path to groovy script which help making reports in post integration test base on path to
* Mekong directory passed.
*/
def MakeReportsScriptPath(String mekong) {
    return "${mekong}/${MakeReportsScriptR()}"
}

/**
* Name of groovy script which help sending email
*/
def SendEmailScriptName() {
    return "send_email.groovy"
}

/**
* Relative path to groovy script which help sending email
*/
def SendEmailScriptR() {
    return "${GroovyLibR()}/${SendEmailScriptName()}"
}

/**
* Get full path to groovy script which help sending email base on path to Mekong directory passed
*/
def SendEmailScriptPath(String mekong) {
    return "${mekong}/${SendEmailScriptR()}"
}

/**
* Name of groovy script which help working with SVN
*/
def UpdateSvnScriptName() {
    return "update_svn.groovy"
}

/**
* Relative path to groovy script which help working with SVN
*/
def UpdateSvnScriptR() {
    return "${GroovyLibR()}/${UpdateSvnScriptName()}"
}

/**
* Get full path to groovy script which help working with SVN base on path to Mekong directory passed
*/
def UpdateSvnScriptPath(String mekong) {
    return "${mekong}/${UpdateSvnScriptR()}"
}

/**
* Name of groovy script which has methods to update reference data to database when a change was
* merged into base line of a project
*/
def UpdateReferenceDataScriptName() {
    return "update_reference_data.groovy"
}

/**
* Relative path to groovy script which has methods to update reference data to database when a
* change was merged into base line of a project
*/
def UpdateReferenceDataScriptR() {
    return "${GroovyLibR()}/${UpdateReferenceDataScriptName()}"
}

/**
* Get full path to groovy script which has methods to update reference data to database when a
* change was merged into base line of a project base on path to Mekong directory passed.
*/
def UpdateReferenceDataScriptPath(String mekong) {
    return "${mekong}/${UpdateReferenceDataScriptR()}"
}

/**
* Name of groovy script which has methods to update test cases folder on test nodes to update
* new reference data in Post Integration
*/
def UpdateTestCasesFolderOnNodesScriptName() {
    return "update_test_cases_folder_on_nodes.groovy"
}

/**
* Relative path to groovy script which has methods to update test cases folder on test nodes to
* update new reference data in Post Integration
*/
def UpdateTestCasesFolderOnNodesScriptR() {
    return "${GroovyLibR()}/${UpdateTestCasesFolderOnNodesScriptName()}"
}

/**
* Get full path to groovy script which has methods to update test cases folder on test nodes to
* update new reference data in Post Integration base on path to Mekong directory passed.
*/
def UpdateTestCasesFolderOnNodesScriptPath(String mekong) {
    return "${mekong}/${UpdateTestCasesFolderOnNodesScriptR()}"
}

/**
* Name of groovy script which has methods to vote for a change to gerrit base on test results
*/
def VoteGerritScriptName() {
    return "vote_gerrit.groovy"
}

/**
* Relative path to groovy script which has methods to vote for a change to gerrit base on test
* results
*/
def VoteGerritScriptR() {
    return "${GroovyLibR()}/${VoteGerritScriptName()}"
}

/**
* Get full path to groovy script which has methods to vote for a change to gerrit base on test
* results base on path to Mekong directory passed.
*/
def VoteGerritScriptPath(String mekong) {
    return "${mekong}/${VoteGerritScriptR()}"
}

/**
* Name of groovy script which has methods to prepare build packages in Post Integration for new
* delta version of project.
*/
def PrepareBuildPackagesScriptName() {
    return "prepare_build_package_release.groovy"
}

/**
* Relative path to groovy script which has methods to prepare build packages in Post Integration for
* new delta version of project.
*/
def PrepareBuildPackagesScriptR() {
    return "${GroovyLibR()}/${PrepareBuildPackagesScriptName()}"
}

/**
* Get full path to groovy script which has methods to prepare build packages in Post Integration
* for new delta version of project base on path to Mekong directory passed.
*/
def PrepareBuildPackagesScriptPath(String mekong) {
    return "${mekong}/${PrepareBuildPackagesScriptR()}"
}

return this
