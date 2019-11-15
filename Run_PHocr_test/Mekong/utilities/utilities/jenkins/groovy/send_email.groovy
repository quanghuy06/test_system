/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines groovy function to send email to people for reports by calling to
*              python script.
*/

/**
* Call to python script to execute send email for people in Post Integration for accuracy and
* performance reports.
*/
def SendEmailPostIntegration(String python, String mekong, String project, String job) {
    println("*** SEND EMAIL FOR REPORTING IN POST INTEGRATION ***")

    // Load helper to get path of scripts in Mekong
    def python_scripts_helper = load("${mekong}/utilities/jenkins/groovy/python_scripts_helper.groovy")

    // Python
    def send_email_script = python_scripts_helper.SendEmailPostIntegrationScriptPath(mekong)

    // Call to python script to execute sending email to people in Post Integration
    def send_email_good = sh (
            script: "${python} ${send_email_script} -p ${project} -j ${job}",
            returnStatus: true
    ) == 0

    // Return status of sending email execution
    return send_email_good
}

return this
