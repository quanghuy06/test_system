/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 01/10/2019
* Description: This script defines some configuration of automation test system such as path to
*              static data file, static jenkins directory,...
*/

/**
* Ip of Gerrit server
*/
def GerritServerIp() {
    return "10.116.41.96"
}

/**
* Account of jenkins on Gerrit
*/
def GerritAccountForJenkins() {
    return "Jenkins"
}

/**
* Path to directory where jenkins store data of builds from archive artifacts. This is where we can
* find build/test results after testing finish. This is global location for jenkins. There are
* specific folders for each job.
*/
def JenkinsStorageDir() {
    return "/media/ocr3/data/Jenkins"
}

/**
* Path to directory which is default place to store static data of jenkins. We'll use this location
* to configuration file.
*/
def JenkinsConfigurationDir() {
    return "${env.JENKINS_HOME}/jobs"
}

/**
* Name of json mapping file between change number and list of build for that change. Also we have
* status of each build.
*/
def ChangeBuildMappingFileName() {
    return "change_build_mapping.json"
}

/**
* Path to json mapping file between change number and list of build for that change. Also we have
* status of each build.
*/
def ChangeBuildMappingFilePath(String job_name) {
    return "${JenkinsConfigurationDir()}/${job_name}/${ChangeBuildMappingFileName()}"
}

/**
* Name of json mapping file between delta version with the change number
*/
def DeltaChangeMappingFileName() {
    return "delta_change_mapping.json"
}

/**
* Get path to json file which includes mapping between delta version and change number of a project
*/
def DeltaChangeMappingFilePath(String project) {
    return "${JenkinsConfigurationDir()}/gerrit-projects/${project}/${DeltaChangeMappingFileName()}"
}

/**
* Name of json file which includes current delta version on base line of all projects
*/
def DeltaVersionFileName() {
    return "delta_version_projects.json"
}

/**
* Get path to json file which include current delta version of gerrit projects
*/
def DeltaVersionFilePath() {
    return "${JenkinsConfigurationDir()}/gerrit-projects/${DeltaVersionFileName()}"
}

return this
