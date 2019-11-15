/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines groovy methods to extract and update information from json
*              mapping file between delta version and change number.To update information to
*              delta-change mapping file, we'll execute python script.
*/

/**
* Update delta-change mapping file when a change was merged by executing python script
*/
def Update(String python, String mekong, String project, String delta_version, String change_number) {
    println("*** UPDATE DELTA-CHANGE MAPPING FILE ***")

    // Load helper to get path of scripts in Mekong
    def groovy_scripts_helper = load("${mekong}/utilities/jenkins/groovy/groovy_scripts_helper.groovy")
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Load configuration
    def configuration_helper = load(groovy_scripts_helper.ConfigurationHelperScriptPath(mekong))

    // Path to delta change mapping json file
    def delta_change_mapping_file = configuration_helper.DeltaChangeMappingFilePath(project)

    // Use python script
    def update_delta_change_mapping_script = python_scripts_helper.UpdateDeltaChangeMappingScriptPath(mekong)

    // Execute python script to update mapping file
    def update_good = sh (
        script: "${python} ${update_delta_change_mapping_script} -f ${delta_change_mapping_file} -d ${delta_version} -c ${change_number}",
        returnStatus: true
    ) == 0

    // Return status of execution
    return update_good
}

/**
* Get change number of a delta version. If there is no data for the delta version the zero is
* returned.
*/
def GetChangeNumber(String mekong, String project, String delta_version) {
    change_number = "0"

    // Load helper to get path of scripts in Mekong
    def groovy_scripts_helper = load("${mekong}/utilities/jenkins/groovy/groovy_scripts_helper.groovy")

    // Load configuration
    def configuration_helper = load(groovy_scripts_helper.ConfigurationHelperScriptPath(mekong))

    // Path to delta-change mapping json file
    def delta_change_mapping_file = configuration_helper.DeltaChangeMappingFilePath(project)

    // Load json file to object
    def jsonHandler = load(groovy_scripts_helper.HandleJsonScriptPath(mekong))
    def json_object = jsonHandler.LoadJson(delta_change_mapping_file)

    // Extract information
    if (json_object != null && json_object.containsKey(delta_version)) {
        change_number = json_object[delta_version]
    }

    return change_number
}

return this
