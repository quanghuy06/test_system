/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Email:  tai.phungdinh@toshiba-tsdv.com
* Date created: 30/09/2019
* Description: This script defines pipeline for Delete Old Results job on Jenkins in Post
*              Integration. You can copy this script into bash script shell in pipeline of the job
*              on Jenkins. For this job, we remove all build/test results of the change which was
*              merged into base line except the latest success build result for reference later.
*              Results to be removed from both of Engineering and Integration Test.
*/
import hudson.model.Cause

def python = 'python2.7'
def mekong = 'Mekong'
def project = 'PHOcr'
def sad = ":/"
def happy = ":D"

class UpstreamInfo implements Serializable {
    String job_name
    int build_number

    UpstreamInfo(name, build) {
        this.job_name = name
        this.build_number = build
    }
}

@NonCPS
def get_upstream() {
    def upstream_job = ""
    def upstream_build = 0
    def causes = currentBuild.rawBuild.getCauses()
    causes.each{item ->
        if (item instanceof Cause.UpstreamCause) {
            upstream_job = item.properties.upstreamProject
            upstream_build = item.properties.upstreamBuild
        }
    }
    return new UpstreamInfo(upstream_job, upstream_build)
}

/* Get information of upstream build which trigger this build */
def upstream_info = get_upstream()
def parent_job = upstream_info.job_name
def parent_build_number = upstream_info.build_number

if (parent_job == "" || parent_build_number == 0) {
    println("[ ${sad} ] Sorry, can not get information from parent job Post Integration!")
    return
}

def build_good = true

stage("Checkout Mekong utilities") {
    node("master") {
        // Clean master workspace
        sh "rm -rf *"
        // Checkout Mekong utilities
        cmd = "git clone ssh://taipd@10.116.41.96:29418/Mekong && cd Mekong && git checkout MekongTestAfterWindowSupport "
        if ("${MekongBranch}" != "") {
            cmd += "&& ${MekongBranch}"
        }
        sh cmd
        sh "rm -rf Mekong/.git"
    }
}

if (!build_good) {
    println("[ ${sad} ] Sorry, failed to checkout Mekong utilities, force to stop!")
    currentBuild.result = hudson.model.Result.FAILURE
    return
}

stage("Execute processes") {
    node("master") {
        // Load helper to get path of scripts in Mekong
        def groovy_scripts_helper = load("${mekong}/utilities/jenkins/groovy/groovy_scripts_helper.groovy")

        // Load methods to extract data from delta version file
        def version_data_handler = load(groovy_scripts_helper.HandleDeltaVersionProjectsScriptPath(mekong))

        // Get current delta version on base line of PHOcr
        def phocr_version = version_data_handler.DeltaVersionOfProject(mekong, project)

        // Load methods to extract data from delta-change mapping file
        def delta_change_mapping_handler = load(groovy_scripts_helper.HandleDeltaChangeMappingScriptPath(mekong))

        // Get change relates to current delta version
        def phocr_change_number = delta_change_mapping_handler.GetChangeNumber(mekong, project,
            phocr_version)

        // Load methods of making reports and supports
        def data_deleter = load(groovy_scripts_helper.DeleteOldResultsPostIntegrationScriptPath(mekong))

        // <M> Delete old results data of the change
        def delete_results_good = data_deleter.DeleteOldResultsPostIntegration(python, mekong, phocr_change_number)

        // Conclude result of processes
        def all_good = delete_results_good

        if (all_good) {
            println("[ ${happy} ] Good job! All processes run successfully!")
            currentBuild.result = hudson.model.Result.SUCCESS
        } else {
            println("[ ${sad} ] Somethings wrong happens in:")
            if (!delete_results_good) {
                println("- Delete old results for change ${phocr_change_number} of project ${project}")
            }
            currentBuild.result = hudson.model.Result.FAILURE
        }
    }
}
