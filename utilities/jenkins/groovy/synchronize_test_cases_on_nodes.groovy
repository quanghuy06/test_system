/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 03/10/2019
* Description: This script defines groovy methods to synchronize test cases folder on nodes to get
*              updated reference data from database in Post Integration when a change war merged
*              into base line of project.
*/

/**
* Call to python script to execute synchronization on all test nodes of system to update test cases
*/
def SynchronizeOnNodes(String python, String mekong) {
    println("*** SYNCHRONIZE TEST CASES FOLDER ON NODE FOR GETTING UPDATED REFERENCE DATA ***")

    // Load helper to get path of scripts in Mekong
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Using a python script
    def synchronize_test_cases_script = python_scripts_helper.SynchronizeTestCasesFolderOnNodeScriptPath(mekong)

    // Execute python script to update reference data
    def synchronize_good = sh (
        script: "${python} ${synchronize_test_cases_script}",
        returnStatus: true
    ) == 0

    // Return status of execution
    return synchronize_good
}

return this