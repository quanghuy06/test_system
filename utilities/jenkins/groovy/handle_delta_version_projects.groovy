/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines groovy methods to update/extract data information from json file
*              which store current delta version on base line of projects.
*/

/**
* Call to python script to execute updating delta version of projects json file.
*/
def IncrementDeltaVersionProject(String python, String mekong, String project) {
    println("*** INCREMENT DELTA VERSION OF PROJECT ${project} BY 1***")

    // Load helper to get path of scripts in Mekong
    def groovy_scripts_helper = load("${mekong}/utilities/jenkins/groovy/groovy_scripts_helper.groovy")
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Load configuration
    def configuration_helper = load(groovy_scripts_helper.ConfigurationHelperScriptPath(mekong))

    // Path to delta version of projects json file
    def delta_version_file = configuration_helper.DeltaVersionFilePath()

    // Use python script
    def update_delta_version_script = python_scripts_helper.UpdateDeltaVersionProjectsScriptPath(mekong)

    // Call to python script to execute updating data
    def update_good = sh (
        script: "${python} ${update_delta_version_script} -f ${delta_version_file} -p ${project}",
        returnStatus: true
    ) == 0

    // Return status of sending email execution
    return update_good
}

/**
* Get current delta version of a project
*/
def DeltaVersionOfProject(String mekong, String project) {
    // Initial return value by zero
    delta_version = "0"

    // Load helper to get path of scripts in Mekong
    def groovy_scripts_helper = load("${mekong}/utilities/jenkins/groovy/groovy_scripts_helper.groovy")

    // Load configuration
    def configuration_helper = load(groovy_scripts_helper.ConfigurationHelperScriptPath(mekong))

    // Path to delta version of projects json file
    def delta_version_file = configuration_helper.DeltaVersionFilePath()

    // Load json file to object
    def jsonHandler = load(groovy_scripts_helper.HandleJsonScriptPath(mekong))
    def json_object = jsonHandler.LoadJson(delta_version_file)

    // Extract information
    if (json_object != null && json_object.containsKey(project)) {
        delta_version = json_object[project]
    }

    return delta_version
}

/**
* Update delta version of project when a change was merged. Check if the change is existing in
* delta-change mapping first to make sure it's not re-trigger of Post Integration
*/
def UpdateDeltaVersionChangeMerged(String python, String mekong, String project, String change_number) {
    println("*** UPDATE DELTA VERSION OF PROJECTS FILE WHEN CHANGE MERGED ***")

    // Load helper to get path of scripts in Mekong
    def groovy_scripts_helper = load("${mekong}/utilities/jenkins/groovy/groovy_scripts_helper.groovy")
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Load configuration
    def configuration_helper = load(groovy_scripts_helper.ConfigurationHelperScriptPath(mekong))

    // Path to delta version of projects json file
    def delta_version_file = configuration_helper.DeltaVersionFilePath()

    // Use python script
    def update_delta_version_script = python_scripts_helper.UpdateDeltaVersionProjectsScriptPath(mekong)

    // Call to python script to execute sending email to people in Post Integration
    def update_good = sh (
        script: "${python} ${update_delta_version_script} -f ${delta_version_file} -p ${project} -c ${change_number}",
        returnStatus: true
    ) == 0

    // Return status of sending email execution
    return update_good
}

return this
