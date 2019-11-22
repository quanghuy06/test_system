/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines groovy functions to collect data and submit to svn. Actually,
*              we execute a python script to do this thing.
*/

/**
* Call to a python script to submit accuracy report for a delta version to SVN
*/
def SubmitDeltaAccuracyReport(String python, String mekong, String project) {
    println("*** SUBMIT DELTA ACCURACY REPORT TO SVN ***")

    // Load helper to get path of scripts in Mekong
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Use python script
    def add_acc_svn_script = python_scripts_helper.SubmitDeltaAccuracyReportSvnScriptPath(mekong)

    // Execute python script to submit SVN
    def add_acc_svn_good = sh (
        script: "${python} ${add_acc_svn_script} -p ${project}",
        returnStatus: true
    ) == 0

    // Return status of execution
    return add_acc_svn_good
}

/**
* Call to python script to update change log of project on SVN
*/
def UpdateChangeLog(String python, String mekong, String parameters_file, String gerrit_number) {
    println("*** UPDATE CHANGE LOG OF PROJECT ON SVN ***")

    // Load helper to get path of scripts in Mekong
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Use python script
    def update_change_log_svn_script = python_scripts_helper.UpdateChangeLogSvnScriptPath(mekong)

    // Execute python script to update change on SVN
    def update_change_log_good = sh (
        script: "${python} ${update_change_log_svn_script} -p ${parameters_file} -g ${gerrit_number}",
        returnStatus: true
    ) == 0

    // Return status of execution
    return update_change_log_good
}

return this
