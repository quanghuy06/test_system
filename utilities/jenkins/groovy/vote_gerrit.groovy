/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines groovy function to checkout Mekong project for automation test
*              system. Currently, we using gerrit server on 10.116.41.96.
*/

/**
* Vote for a change on gerrit for status of build/test
*/
def VoteGerrit(String mekong, String auth_key, String change_number, String patch_set, String label,
               int result, String message, String build_url) {
    // Load helper to get path of scripts in Mekong
    def groovy_scripts_helper = load("${mekong}/utilities/jenkins/groovy/groovy_scripts_helper.groovy")

    // Get configuration helper to extract gerrit server configuration
    def configuration_helper = load(groovy_scripts_helper.ConfigurationHelperScriptPath(mekong))

    def server = configuration_helper.GerritServerIp()
    def account = configuration_helper.GerritAccountForJenkins()

    // Generate command line to execute vote
    cmd = "ssh ${auth_key} -p 29418 ${account}@${server} gerrit review ${change_number},${patch_set}"
    cmd += " --label ${label}=${result} -m \\\"[${label}] ${message} "
    cmd += "Please check in ${build_url} for more detail!\\\""

    // Execute python script to update change on SVN
    def gerrit_vote_good = sh (
        script: "${cmd}",
        returnStatus: true
    ) == 0

    // Return status of voting execution
    return gerrit_vote_good
}

return this
