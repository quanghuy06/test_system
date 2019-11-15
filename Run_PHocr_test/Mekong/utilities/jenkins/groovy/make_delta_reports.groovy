/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines some methods to make report on Post Integration of Jenkins
*              pipeline. From jenkins bash script, we can checkout to target version of Mekong then
*              load (using load() function) this file and use defined methods here.
*/

/**
* Call to python script to make report on accuracy of PHOcr base on data on database.
*/
def MakeDeltaAccuracyReport(String python, String mekong) {
    println("*** MAKE ACCURACY REPORT FOR DELTA VERSIONS ***")

    // Load helper to get path of scripts in Mekong
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Use python script
    def delta_accuracy_report_script = python_scripts_helper.MakeDeltaAccuracyReportScriptPath(mekong)

    // Execute python script to report accuracy for delta version
    def report_good = sh (
        script: "${python} ${delta_accuracy_report_script}",
        returnStatus: true
    ) == 0

    // Return status of execution
    return report_good
}

/**
* Call to python script to make report on performance of PHOcr base on data on database
*/
def MakeDeltaPerformanceReport(String python, String mekong) {
    println("*** MAKE PERFORMANCE REPORT FOR DELTA VERSIONS ***")

    // Load helper to get path of scripts in Mekong
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Use python script
    def delta_performance_report_script = python_scripts_helper.MakeDeltaPerformanceReportScriptPath(mekong)

    // Execute python script to report performance for delta version
    def report_good = sh (
        script: "${python} ${delta_performance_report_script}",
        returnStatus: true
    ) == 0

    // Return status of execution
    return report_good
}

/**
* After calling to python script, then reports in excel format with suffix .xlsx, then sometimes we
* need to store these reports somewhere and this method help us to copy all excel files in current
* workspace directory to somewhere else.
*/
def ArchiveAllReports(String archive_folder) {
    println("*** ARCHIVE ALL REPORTS IN EXCEL FORMAT ***")
    println("Target directory: ${archive_folder}")

    // Execute copy
    def archive_good = sh (
        script: "mkdir -p ${archive_folder} && cp *.xlsx ${archive_folder}",
        returnStatus: true
    ) == 0

    // Return status of execution
    return archive_good
}

return this