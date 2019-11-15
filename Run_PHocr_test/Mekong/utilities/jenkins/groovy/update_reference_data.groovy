/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/10/2019
* Description: This script defines groovy methods to update reference data to database when a change
*              was merged into project base line. Reference data will be the output of the latest
*              success build in Integration Test of the project.
*/

/**
* Call to python script to get test results of latest success build in Integration Test of project
* to be reference updated to Mekong database. This method need to be executed after delta version
* file was updated when a change of projects was integrated.
*/
def UpdateReferenceDataToDatabase(String python, String mekong, String project, String job_name) {
    println("*** UPDATE RESULT OF LATEST SUCCESS BUILD TO DATABASE AS REFERENCE DATA ***")

    // Load helper to get path of scripts in Mekong
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Using a python script
    def update_reference_data_script = python_scripts_helper.UpdateReferenceDataScriptPath(mekong)

    // Execute python script to update reference data
    def update_reference_data_good = sh (
        script: "${python} ${update_reference_data_script} -p ${project} -j ${job_name}",
        returnStatus: true
    ) == 0

    // Return status of execution
    return update_reference_data_good
}

return this