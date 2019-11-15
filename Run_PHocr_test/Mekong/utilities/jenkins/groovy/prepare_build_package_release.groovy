/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines groovy methods to prepare build packages for release in Post
* Integration when a change was merged
*/

/**
* Call to python script to prepare build packages for Post Integration. Get build packages from
* latest success build, rename and copy to archive folder of Post Integration
* @param it_job_name Name of Integration Test job of the project
* @param archive_folder Destination for build packages
*/
def PrepareBuildPackages(String python, String mekong, String project, String it_job_name, String destination) {
    println("*** PREPARE BUILD PACKAGES FOR NEW DELTA VERSION ***")

    // Load helper to get path of scripts in Mekong
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Using a python script
    def prepare_build_packages_script = python_scripts_helper.PrepareBuildPackagesScriptPath(mekong)

    // Execute python script to delete ET anf IT old test result of this change
    def prepare_good = sh (
        script: "${python} ${prepare_build_packages_script} -p ${project} -i ${it_job_name} -d ${destination}",
        returnStatus: true
    ) == 0

    // Return status of execution
    return prepare_good
}

return this
