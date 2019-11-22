/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines groovy function to remove old build/test results when a change
*              was merged and Post Integration is triggered. We only keep the latest build/test
*              results in Integration Test to save disk space.
*/

/**
* Call to python script to remove old build/test results when a change was merged into base line.
* Only keep the latest build for referencing.
*/
def DeleteOldResultsPostIntegration(String python, String mekong, String change_number) {
    println("*** DELETE OLD RESULTS FOR A MERGED CHANGE ***")

    // Load helper to get path of scripts in Mekong
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Using a python script
    def delete_old_test_result_script = python_scripts_helper.DeleteOldResultsPostIntegrationScriptPath(mekong)

    // Execute python script to delete ET anf IT old test result of this change
    def delete_old_test_result_good = sh (
        script: "${python} ${delete_old_test_result_script} -g ${change_number}",
        returnStatus: true
    ) == 0

    // Return status of execution
    return delete_old_test_result_good
}

return this
