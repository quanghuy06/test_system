# Toshiba - TSDV
# Team:         PHOcr
# Author:       Phung Dinh Tai
# Date create:  20/03/2017
# Last update:  29/06/2017
# Updated by:   Phung Dinh Tai
# Description:  This script can be use to download additional librabies of PHOcr.
#               These libraries lie on folder phocrlib on samba share
#               smb://10.116.41.96/Share/phocrlib

import sys_path
sys_path.insert_sys_path()

import argparse
import os
from manager.lib_manager.samba_base import SambaManager
from configs.samba import SmbConfig
from configs.projects.phocr import PhocrProject

def main():
    parser = argparse.ArgumentParser(description='Copy dynamic library to PHOcr build')
    parser.add_argument("-b", "--build-folder", required = True,
                        help="Path to PHOcr build folder")
    args = parser.parse_args()

    # Copy dynamic library to lib folder
    print "Packaging PHOcr build package"
    smb_manager = SambaManager(SmbConfig.SERVER, SmbConfig.USERNAME, SmbConfig.PASSWORD,
                               SmbConfig.RELEASE_DISK)
    print "Get PHOcr dynamic library from samba share"
    lib_path = os.path.join(args.build_folder, PhocrProject.build.LIB)
    print "SUCCESSFULLY!"

if __name__ == "__main__":
    main()
