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
def it_job_name = "PHOcr-Integration-Test"
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

        // Load configuration helper of jenkins
        def configuration_helper = load(groovy_scripts_helper.ConfigurationHelperScriptPath(mekong))

        // Load methods to prepare build packages
        def packages_helper = load(groovy_scripts_helper.PrepareBuildPackagesScriptPath(mekong))

        // Get archive folder of parent build on Post Integration to store build packages
        def upstream_archive_folder = "${configuration_helper.JenkinsStorageDir()}/${parent_job}/${parent_build_number}/archive"

        // <M> Run processes to archive release build packages
        def prepare_good = packages_helper.PrepareBuildPackages(python, mekong, project, it_job_name, upstream_archive_folder)

        // Conclude result of processes
        def all_good = prepare_good

        if (all_good) {
            println("[ ${happy} ] Good job! All processes run successfully!")
            currentBuild.result = hudson.model.Result.SUCCESS
        } else {
            println("[ ${sad} ] Somethings wrong happens in:")
            if (!prepare_good) {
                println("- Prepare build packages for release new delta version")
            }
            currentBuild.result = hudson.model.Result.FAILURE
        }
    }
}
