/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Email:  tai.phungdinh@toshiba-tsdv.com
* Date created: 15/10/2019
* Description: This script defines pipeline for Make Delta Reports job on Jenkins in Post
*              Integration. You can copy this script into bash script shell in pipeline of the job
*              on Jenkins.
*              This is configuration for PHOcr-Make-Delta-Reports job on Jenkins server of
*              mini-system.
*/
import hudson.model.Cause

def python = 'python2.7'
def mekong = 'Mekong'
def project = 'PHOcr'
def it_job = "PHOcr-Integration-Test"
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
        if ("${DatabaseConfigurationMiniSystemCherryPick}" != "") {
            cmd += "&& ${DatabaseConfigurationMiniSystemCherryPick}"
        } else {
            println("You need to setup cherry pick command to Mekong change which configure database for mini-system of Mekong testing")
            build_good = false
            return
        }
        if ("${SvnResourceConfigurationMiniSystemCherryPick}" != "") {
            cmd += "&& ${SvnResourceConfigurationMiniSystemCherryPick}"
        } else {
            println("You need to setup cherry pick command to Mekong change which configure system svn resource for mini-system of Mekong testing")
            build_good = false
            return
        }
        if ("${EmailConfigurationMiniSystemCherryPick}" != "") {
            cmd += "&& ${EmailConfigurationMiniSystemCherryPick}"
        } else {
            println("You need to setup cherry pick command to Mekong change which configure email sending for mini-system of Mekong testing")
            build_good = false
            return
        }
        if ("${JenkinsFileSystemConfigurationMiniSystemCherryPick}" != "") {
            cmd += "&& ${JenkinsFileSystemConfigurationMiniSystemCherryPick}"
        } else {
            println("You need to setup cherry pick command to Mekong change which configure Jenkins file system for mini-system of Mekong testing")
            build_good = false
            return
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

        // Target directory to store of reports
        def upstream_archive_folder = "${configuration_helper.JenkinsStorageDir()}/${parent_job}/${parent_build_number}/archive"

        // Load methods of making reports and supports
        def reporter = load(groovy_scripts_helper.MakeReportsScriptPath(mekong))

        // <M> Make accuracy report
        def report_accuracy_good = reporter.MakeDeltaAccuracyReport(python, mekong)

        // <M> Make performance report
        def report_performance_good = reporter.MakeDeltaPerformanceReport(python, mekong)

        // <M> Archive all reports to target directory
        def archive_reports_good = reporter.ArchiveAllReports(upstream_archive_folder)

        // Create methods to extract information from delta version file of projects
        def version_data_parser = load(groovy_scripts_helper.HandleDeltaVersionProjectsScriptPath(mekong))

        // Get current delta version of project
        def phocr_version = version_data_parser.DeltaVersionOfProject(mekong, project)

        // Load methods to work with SVN
        def svn_updater = load(groovy_scripts_helper.UpdateSvnScriptPath(mekong))

        // <M> Submit delta accuracy report to SVN
        def submit_reports_svn_good = svn_updater.SubmitDeltaAccuracyReport(python, mekong, project)

        // Load methods for sending email
        def send_email_helper = load(groovy_scripts_helper.SendEmailScriptPath(mekong))

        // <M> Send reports to people by email
        def send_email_good = send_email_helper.SendEmailPostIntegration(python, mekong, project, it_job)

        // Conclude result of processes
        def all_good = report_accuracy_good && report_performance_good && archive_reports_good && submit_reports_svn_good && send_email_good

        if (all_good) {
            println("[ ${happy} ] Good job! All processes run successfully!")
            currentBuild.result = hudson.model.Result.SUCCESS
        } else {
            println("[ ${sad} ] Somethings wrong happens in:")
            if (!report_accuracy_good) {
                println("- Report delta accuracy report")
            }
            if (!report_performance_good) {
                println("- Report delta performance report")
            }
            if (!archive_reports_good) {
                println("- Archive reports to parent build")
            }
            if (!submit_reports_svn_good) {
                println("- Submit accuracy report to SVN")
            }
            if (!send_email_good) {
                println("- Send email to people for reporting")
            }
            currentBuild.result = hudson.model.Result.FAILURE
        }
    }
}
