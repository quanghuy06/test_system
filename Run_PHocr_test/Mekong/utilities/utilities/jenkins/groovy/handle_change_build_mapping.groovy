/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines groovy methods to extract and update information from json
*              mapping file between change number and build number.To update information to
*              change-build mapping file, actually we'll execute python script.
*/

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

/**
* Update change-build mapping file when a build is triggered
*/
def Update(String python, String mekong, String change_number, String patch_set, String job_name, String build_number, String status) {
    // Load helper to get path of scripts in Mekong
    def groovy_scripts_helper = load("${mekong}/utilities/jenkins/groovy/groovy_scripts_helper.groovy")
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Load configuration
    def configuration_helper = load(groovy_scripts_helper.ConfigurationHelperScriptPath(mekong))

    // Path to delta-change mapping json file
    def change_build_mapping_file = configuration_helper.ChangeBuildMappingFilePath(job_name)

    // Path to python script which help update change-build mapping file
    def update_change_build_mapping_script = python_scripts_helper.UpdateChangeBuildMappingScriptPath(mekong)

    // Call to python script to execute updating data
    def update_good = sh (
        script: "${python} ${update_change_build_mapping_script} -c ${change_number} -p ${patch_set} -b ${build_number} -s ${status} -f ${change_build_mapping_file}",
        returnStatus: true
    ) == 0

    // Return status of sending email execution
    return update_good
}

return this
