/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines pipeline for Post Integration. Currently, these are processes
*              which are required to be finished before other change to be tested when a change
*              was merged:
*              - Update new reference data to database using test results of latest success build in
*              Integration Test
*              - Update test cases folder on node master (where install jenkins)
*              - Synchronize test cases on node master with all other test nodes in system
*              => Step 2 and 3 are combined into 1 in synchronization of test cases.
*/

def python = 'python2.7'
def mekong = 'Mekong'
def project = 'PHOcr'
def it_job = 'PHOcr-Integration-Test'
def sad = ":/"
def happy = ":D"
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

        // Change number to be integrated
        def change_number = "${GERRIT_CHANGE_NUMBER}"

        // Load methods to handle delta version of projects file
        def version_handler = load(groovy_scripts_helper.HandleDeltaVersionProjectsScriptPath(mekong))

        // <M> Check and update new version of the project
        def update_version_good = version_handler.UpdateDeltaVersionChangeMerged(python, mekong, project, change_number)

        // Load methods to handle delta-change mapping file of the project
        def delta_change_mapping_handler = load(groovy_scripts_helper.HandleDeltaChangeMappingScriptPath(mekong))

        // Get current delta version of the project
        def current_delta_version = version_handler.DeltaVersionOfProject(mekong, project)

        // <M> Update delta-change mapping for new change
        def update_delta_change_mapping_good = delta_change_mapping_handler.Update(python, mekong, project, current_delta_version, change_number)

        // Load methods to update reference data
        def reference_data_updater = load(groovy_scripts_helper.UpdateReferenceDataScriptPath(mekong))

        // <M> Update reference data to Mekong database
        def update_reference_good = reference_data_updater.UpdateReferenceDataToDatabase(python, mekong, project, it_job)

        // Load methods to synchronize test cases folder on test nodes in system
        def synchronize_helper = load(groovy_scripts_helper.SynchronizeTestCasesFolderOnNodesScriptPath(mekong))

        // <M> Synchronize test cases on test nodes
        def synchronize_good = synchronize_helper.SynchronizeOnNodes(python, mekong)

        // Conclude result of processes
        def all_good = update_version_good && update_delta_change_mapping_good && update_reference_good && synchronize_good

        // Generate message for voting to the change on gerrit
        def gerrit_message = ""

        // Result of build
        def status = 0

        if (all_good) {
            println("[ ${happy} ] Good job! All processes run successfully!")
            currentBuild.result = hudson.model.Result.SUCCESS
            gerrit_message = "SUCCESS: All processes successfully!"
            status = 1
        } else {
            println("[ ${sad} ] Somethings wrong happens in:")
            if (!update_version_good) {
                println("- Update delta version of projects")
            }
            if (!update_delta_change_mapping_good) {
                println("- Update delta-change mapping file of project")
            }
            if (!update_reference_good) {
                println("- Update reference data")
            }
            if (!synchronize_good) {
                println("- Synchronize test cases folder on test nodes")
            }
            currentBuild.result = hudson.model.Result.FAILURE
            gerrit_message = "FAILED: Something wrong happens!"
            status = -1
        }

        // Load methods to vote gerrit
        def gerrit_voter = load(groovy_scripts_helper.VoteGerritScriptPath(mekong))

        // Patch set for voting
        def patch_set_number = "${GERRIT_PATCHSET_NUMBER}"

        // Label for current job
        def label = "${env.JOB_NAME}"

        // URL to current build
        def build_url = "${env.BUILD_URL}"


        // Authority key to pass Gerrit server.
        // Currently Gerrit server and Jenkins server are the same machine so we don't need
        // authority key
        def auth_key = ""

        // <M> Vote message to change one gerrit for summary status of processes
        def vote_gerrit_good = gerrit_voter.VoteGerrit(mekong, auth_key, change_number, patch_set_number, label, status, gerrit_message, build_url)

        // Check if voting is failed
        if (!vote_gerrit_good) {
            println("WARN: Failed to vote to gerrit server for the change!")
        }
    }
}
