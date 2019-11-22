/*  TOSHIBA-TSDV
*   Author : Phung Dinh Tai
*   Email : tai.phungdinh@toshiba-tsdv.com
*   Date created : 15/10/2019
*   Description: This script is used to define workflow of pipeline job PHOcr-Integration-Test on
*                Jenkins server which is used for Mekong testing (or mini-system). You can copy this
*                script to pipeline configure box of the job. Also whenever you need to change the
*                configure script, please update on this script first and create a change.
*/
import groovy.json.JsonBuilder
import groovy.json.JsonSlurperClassic
import groovy.json.JsonOutput
import groovy.io.FileType

// Read a json file
def load_json(String filePath) {
    def text = readFile file:filePath
    return new JsonSlurperClassic().parseText(text)
}

// Write json object to file
def write_json(String filePath, mapping){
    writeFile file: filePath, text: new JsonBuilder(mapping).toPrettyString()
}

// Jenkins vote to gerrit base on build result
def gerrit_vote(server, account, label, result, message) {
    // Get change number
    def change = binding.getVariable('GERRIT_CHANGE_NUMBER')
    // Get Gerrit Patch Number
    def patch = binding.getVariable('GERRIT_PATCHSET_NUMBER')
    node ('master') {
        sh "ssh -i ~/.ssh/ocr3_auth/id_rsa -p 29418 ${account}@${server} gerrit review ${change},${patch} --label ${label}=${result} -m \\\"[${label}] ${message}. Please check in ${env.BUILD_URL} for more detail!\\\""
    }
}

def archive_artifacts_if_exists(String folder_name) {
    // If it doesn't exist
    if( fileExists(folder_name) ) {
        // Create all folders up-to and including B
        archiveArtifacts(folder_name)
        println "Archive folder ${folder_name} successfully"
    } else {
        println "Folder ${folder_name} does not exists"
    }
}

/* CHECK IF PHOCR-ENGINEERING-TEST RUNNING */
/*
* Currently, we are using the same physical infrastructure for both of Engineering Test and
* Integration Test in mini-system. So we need to check if Engineering Test is running then we notice
* to developer to re-trigger build later.
*/
@NonCPS
def check_system_available() {
    def is_available = true
    def runningBuilds = Jenkins.instance.getView('All').getBuilds().findAll() { it.getResult().equals(null) }
    runningBuilds.each{item ->
        def job_splitted = item.toString().split()
        if (job_splitted.contains("PHOcr-Engineering-Test") || job_splitted.contains("PHOcr-Extreme-Test")) {
            is_available = false
        }
    }
    return is_available
}

// Get which job will be executed: Engineering Test, Integration Test or a Post Process
def is_et = false
def is_extreme_test = false
def label = "Integration-Test"

try {
    is_extreme_test = "${EXTREME_TEST}"
    if (is_extreme_test) {
        label = "Extreme-Test"
    }
} catch (Exception e) {
    println("Normal testing")
}

/* This variable is used to enable or not process jenkins vote to gerrit review */
def vote_gerrit_enable = true

/********************************************************************************/
/* Information about gerrit project and jenkins build number */
def file_parameters = "parameters.json"
def check_commit_message = "Mekong/utilities/validate/validate_commit_message.py"
def manager_script_path = "`pwd`/Mekong/utilities/manager/nodes_manager.py"
def config_it_perf = "`pwd`/Mekong/utilities/configs/default/configure_integration_test_performance.json"
def base_test_cases = "http://vc1.tsdv.com.vn/2019B/phocr/trunk/src/PerformanceTesting/base_test_cases_mini_system.txt"
def performance_script_path = "`pwd`/Mekong/utilities/performance_for_it/run_it_perf.py"
def server = '10.116.41.96'
def account = 'Jenkins'
visualization_tool = "http://${server}:3000/job/${env.JOB_NAME}/build/${env.BUILD_NUMBER}"
def python = 'python2.7'
def project = 'PHOcr'
def hanoi_project = 'HanoiWorkflow'
def mekong = 'Mekong'
def sad = ":/"
def happy = ":D"
def build_good = true


if (!check_system_available()) {
    // If system is not available then notice to developer to re-trigger build later
    def message = "[ ${sad} ] System is not available for now, please re-trigger later because PHOcr-Engineering-Test or PHOcr-Extreme-Test is running!"
    println(message)
    gerrit_vote(server, account, label, -1, message)
    currentBuild.result = hudson.model.Result.FAILURE
    return
}

/********************** GET MEKONG UTILITIES TO MASTER **************************/
stage('Checkout utilities') {
    echo "--------------------------------- CHECKOUT MEKONG UTILITIES STAGE -------------------------------------"
    try {
        node("master") {
            // Clean master workspace
            sh "rm -rf *"
            // Checkout Mekong utilities
            cmd = "git clone ssh://taipd@10.116.41.96:29418/Mekong && cd Mekong && git checkout MekongTestAfterWindowSupport "
            if ("${MekongBranch}" != "") {
                cmd += "&& ${MekongBranch}"
            }
            if ("${SystemConfigurationMiniSystemCherryPick}" != "") {
                cmd += "&& ${SystemConfigurationMiniSystemCherryPick}"
            } else {
                println("You need to setup cherry pick command to Mekong change which configure system infrastructure for mini-system of Mekong testing")
                return
            }
            if ("${DatabaseConfigurationMiniSystemCherryPick}" != "") {
                cmd += "&& ${DatabaseConfigurationMiniSystemCherryPick}"
            } else {
                println("You need to setup cherry pick command to Mekong change which configure database for mini-system of Mekong testing")
                return
            }
            if ("${BuildConfigurationMiniSystemCherryPick}" != "") {
                cmd += "&& ${BuildConfigurationMiniSystemCherryPick}"
            } else {
                println("You need to setup cherry pick command to Mekong change which configure build release option to avoid conflict ICC license for mini-system of Mekong testing")
                return
            }
            if ("${PerformanceTestConfigurationMiniSystemCherryPick}" != "") {
                cmd += "&& ${PerformanceTestConfigurationMiniSystemCherryPick}"
            } else {
                println("You need to setup cherry pick command to Mekong change which configure resource for performance testing for mini-system of Mekong testing")
            }
            if ("${SynchronizationConfigurationMiniSystemCherryPick}" != "") {
                cmd += "&& ${SynchronizationConfigurationMiniSystemCherryPick}"
            } else {
                println("You need to setup cherry pick command to Mekong change which configure resource of synchronization for mini-system of Mekong testing")
            }
            if ("${TimeoutIntegrationTestConfigurationCherryPick}" != "") {
                cmd += "&& ${TimeoutIntegrationTestConfigurationCherryPick}"
            } else {
                println("You need to setup cherry pick command to Mekong change which configure timeout of Integration Test for mini-system of Mekong testing")
            }
            sh cmd
            sh "rm -rf Mekong/.git"
        }
    } catch(Exception e) {
        println e
        println e.printStackTrace()
        if (vote_gerrit_enable) {
            def message = "[ ${sad} ] Something wrong happened, please contact Test Team for support!"
            gerrit_vote(server, account, label, -1, message)
        }
        build_good = false
        return
    }
    /******************** CREATE PARAMETERS JSON FILE ***********************/
    try{
        node("master") {
            // Load helper to get path of scripts in Mekong
            def groovy_scripts_helper = load("${mekong}/utilities/jenkins/groovy/groovy_scripts_helper.groovy")

            // Load methods to work with delta version of projects file
            delta_version_handler = load(groovy_scripts_helper.HandleDeltaVersionProjectsScriptPath(mekong))

            def parameters_map = [:]
            // parameters_map["profile_path"] = "Mekong/utilities/tests/profile.json"
            parameters_map["job_name"] = "${env.JOB_NAME}"
            parameters_map["project"] = "${GERRIT_PROJECT}"
            parameters_map["refspec"] = "${GERRIT_REFSPEC}"
            parameters_map["email"] = "${GERRIT_CHANGE_OWNER_EMAIL}"
            parameters_map["is_et"] = is_et
            parameters_map["is_extreme_test"] = is_extreme_test
            parameters_map["build_number"] = "${env.BUILD_NUMBER}"
            parameters_map["branch"] = "${GERRIT_BRANCH}"
            parameters_map["phocr_delta"] = delta_version_handler.DeltaVersionOfProject(mekong, project)
            parameters_map["hanoi_delta"] = delta_version_handler.DeltaVersionOfProject(mekong, hanoi_project)
            parameters_map["reviewer"] = "${GERRIT_EVENT_ACCOUNT_NAME}"
            def gerrit = [:]
            gerrit["commit_message"] = "${GERRIT_CHANGE_COMMIT_MESSAGE}"
            gerrit["comment"] = ""
            parameters_map["gerrit"] = gerrit
            // Write parameters json file
            def builder = new JsonBuilder(parameters_map)
            writeFile file: file_parameters, text: builder.toPrettyString()
        }
    } catch(Exception e){
        println e
        println e.printStackTrace()
        if (vote_gerrit_enable) {
            def message = "[ ${sad} ] Sorry, something wrong happened, please contact Test Team for support!"
            gerrit_vote(server, account, label, -1, message)
        }
        build_good = false
        return
    } finally {
        echo "--------------------------------- CHECKOUT UTILITIES END -------------------------------------"
    }

    /******************** CHECK COMMIT MESSAGE ***********************/
    try{
        node("master"){
            /* Check commit message */
            build_good = sh (
                script: "${python} ${check_commit_message} -p ${file_parameters}",
                returnStatus: true
            ) == 0
            /* Check build flag*/
            if (!build_good) {
                // Commit message is incorrect
                if (vote_gerrit_enable) {
                    def message = "[ ${sad} ] Commit message is incorrect. Please inspect log for more detail!"
                    gerrit_vote(server, account, label, -1, message)
                }
                build_good = false
                return
            }
        }
    } catch(Exception e){
        println e
        println e.printStackTrace()
        if (vote_gerrit_enable) {
            def message = "[ ${sad} ] Sorry, something wrong happened, please contact Test Team for support!"
            gerrit_vote(server, account, label, -1, message)
        }
        build_good = false
        return
    }
}

if (!build_good) {
    println("[ ${sad} ] Build failed!")
    currentBuild.result = hudson.model.Result.FAILURE
    return
}

stage('Build') {
    echo "--------------------------------- BUILD STAGE -------------------------------------"
    node("master") {
        /* Run Mekong script to manage build on build node*/
        build_good = sh (
            script: "${python} ${manager_script_path} --build -p ${file_parameters}",
            returnStatus: true
        ) == 0
        /* Check build flag*/
        if (!build_good) {
            // Build fail
            archive_artifacts_if_exists("info/")
            def message = "[ ${sad} ] Sorry, failed in build stage. Please inspect log to find out what happened!"
            if (vote_gerrit_enable) {
                gerrit_vote(server, account, label, -1, message)
            }
            println(message)
            return
        }
    }
}

if (!build_good) {
    println("[ :( ] Build failed!")
    currentBuild.result = hudson.model.Result.FAILURE
    return
}

def test_good = true
def test_performance_good = true

stage('Testing') {
    echo "----------------------------------------- TESTING STAGE ------------------------------------------"
    node("master") {
        parallel testingBranch: {
            /* Run Mekong script to manage testing on test nodes*/
            build_good = sh (
                script: "${python} ${manager_script_path} --test -p ${file_parameters}",
                returnStatus: true
            ) == 0
            archive_artifacts_if_exists("info/")
            if (build_good) {
                // Test successfully
                archive_artifacts_if_exists("linux/")
                archive_artifacts_if_exists("windows/")
            } else {
                // Test fail
                def message = "[ ${sad} ] Sorry, fail in test stage. Please inspect log to find out what happened!"
                if (vote_gerrit_enable) {
                    gerrit_vote(server, account, label, -1, message)
                }
                println(message)
                return
            }
        }, performanceBranch: {
            /* Run Mekong script to manage performance testing on boards */
            test_performance_good = sh (
                script: "${python} ${performance_script_path} -b ${base_test_cases} -c ${config_it_perf}",
                returnStatus: true
            ) == 0
            if (test_performance_good) {
                if (vote_gerrit_enable) {
                    archive_artifacts_if_exists( "svn_report_link.txt" )
                    def svn_report_link = readFile( "svn_report_link.txt" )
                    def message = "[ ${happy} ] Performance testing finish!. You can find report on SVN follow: ${svn_report_link}"
                    gerrit_vote(server, account, label, 0, message)
                }
            } else {
                if (vote_gerrit_enable) {
                    def message = "[ ${happy} ] Sorry, fail in test performance. Please contact with Test Team for support!"
                    gerrit_vote(server, account, label, -1, message)
                }
            }
        },
        failFast: true|false
    }
    echo "---------------------------------------- TESTING ENDED -------------------------------------"
}

/* If fail test, then return immediately */
build_good = test_good && test_performance_good
if (!build_good) {
    println("[ :( ] Testing failed!")
    currentBuild.result = hudson.model.Result.FAILURE
    return
}

stage('Post build') {
    echo "------------------------------------------- POST BUILD STAGE -------------------------------------"
    try {
        node("master") {
            /******************* UPDATE CHANGE-BUILD MAPPING JSON FILE *************************/
            // Load helper to get path of scripts in Mekong
            def groovy_scripts_helper = load("${mekong}/utilities/jenkins/groovy/groovy_scripts_helper.groovy")

            // Load methods to work with change-build mapping file of job
            change_build_mapping_helper = load(groovy_scripts_helper.HandleChangeBuildMappingScriptPath(mekong))

            // Get information for update
            def change_number = "${GERRIT_CHANGE_NUMBER}"
            def patch_set = "${GERRIT_PATCHSET_NUMBER}"
            def job_name = "${env.JOB_NAME}"
            def build_number = "${env.BUILD_NUMBER}"
            def status = "success"
            if (!build_good) {
                status = "fail"
            }

            // <M> Run update
            change_build_mapping_helper.Update(python, mekong, change_number, patch_set, job_name, build_number, status)

            // <M> Vote to gerrit when all work finish normally
            def message = "[ ${happy} ] Testing finished! You can use visualization tool ${visualization_tool} to see detail of test cases changes!"
            gerrit_vote(server, account, label, 0, message)
        }
    }
    catch(Exception e) {
        println e
        println e.printStackTrace()
        if (vote_gerrit_enable) {
            def message = "[ ${sad} ] Sorry, something wrong happened, please contact to test team for checking issues!"
            gerrit_vote(server, account, label, -1, message)
        }
        return
    } finally {
        // Conclude all result
        if (build_good) {
            currentBuild.result = hudson.model.Result.SUCCESS
        } else {
            currentBuild.result = hudson.model.Result.FAILURE
        }
        echo "------------------------------------------- ALL ENDED --------------------------------------"
    }
}
