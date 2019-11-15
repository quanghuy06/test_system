/**
* TSDV - PHOcr team
* Author: Tai Phung Dinh
* Date created: 30/09/2019
* Description: This script defines groovy function to checkout Mekong project for automation test
*              system. Currently, we using gerrit server on 10.116.41.96.
*/

/**
* Checkout to a specific change of Mekong
*/
def CheckoutMekong(String mekong_branch_checkout) {
    println("*** CHECKOUT MEKONG UTILITIES ***")
    // Checkout Mekong project
    cmd = "git clone ssh://taipd@10.116.41.96:29418/Mekong"
    // Checkout to branch MekongTestAfterWindowSupport for automation test system
    cmd = " && cd Mekong && git checkout MekongTestAfterWindowSupport"
    // Checkout to a specific change of Mekong if required
    if ("${MekongBranch}" != "") {
        cmd += " && ${mekong_branch_checkout}"
    }

    // Execute command to checkout source code
    def checkout_good = sh (
        script: "${cmd}",
        returnStatus: true
    ) == 0

    // Return status of execution
    return checkout_good
}

return this
