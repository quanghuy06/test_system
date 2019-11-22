# TOSHIBA - TSDV
# Team:             PHOcr
# Author:           Phung Dinh Tai
# Email:            tai.phungdinh@toshiba-tsdv.com
# Date create:      30/08/2018
# Description:      This script define some usage of virtual box manager, which control virtual
#                   machines used in Mekong Automated Test System


class VirtualManagerConf(object):

    # Command lines
    CMD_LIST_RUNNING_VMS = \
        "vboxmanage list runningvms"
    CMD_START_VM = \
        "vboxmanage startvm {0} --type headless"
    CMD_STOP_VM = \
        "vboxmanage controlvm {0} poweroff"
    CMD_RESTORE_SNAPSHOT = \
        "vboxmanage snapshot {0} restore {1}"
    CMD_ADD_SHARE_FOLDER_VM = \
        'vboxmanage sharedfolder add {0} --name {1} --hostpath {2} --transient'
    # Command list all snapshot of a virtual machine
    CMD_SNAPSHOT_LIST = "vboxmanage snapshot {vm} list"
    # Command rename a snapshot of virtual machine
    CMD_SNAPSHOT_RENAME = "vboxmanage snapshot {vm} edit {old_name} --name {new_name}"
    # Command delete a snapshot of virtual machine
    CMD_SNAPSHOT_DELETE = "vboxmanage snapshot {vm} delete {snapshot}"
    # Command take a snapshot of virtual machine
    CMD_SNAPSHOT_TAKE = "vboxmanage snapshot {vm} take {snapshot}"

    # Expect of standard output. This will check if action is done successfully or not
    EXPECT_START = "successfully started"
    EXPECT_RESTORE = "100%"
    EXPECT_STOP = "100%"
