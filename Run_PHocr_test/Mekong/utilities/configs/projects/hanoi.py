# Toshiba - TSDV
# Team:                 PHOcr
# Author:               Phung Dinh Tai
# Email:                tai.phungdinh@gmail.com
# Date created:         23/06/2017
# Last updated:         30/06/2017
# Updated by:           Phung Dinh Tai
# Description:  This script defines all information for HanoiWorkflow project. The following
#               configuration will be used in whole project. Please give correct information
#               to ensure all work fine.

class HanoiProject:

    NAME = "HanoiWorkflow"
    PRODUCT = "hanoi"
    RELEASE_PREFIX = "Hanoi_installer"
    RELEASE_SUFFIX = "run"
    RELEASE_DIRECTORY = "HanoiWorkflowReleases"
    DELTA = "hanoi_delta"
    LIBS = ["lib.*\.so.*"]
    CONFIG_SUFFIX = "wpr"

    class build:
        WORKING_DIR = "HanoiWorkflow/install/HanoiInstallerLinux"
        CMD = "./GenerateHanoiTesseractInstaller.sh"
        RESULT = "Hanoi_installer.run"

    class components:
        DEFAULT = "HanoiWorkflow"

    class branches:
        MASTER = "master"

    class Windows:
        VM_HANOI_TEMP_DIR = "Hanoi"          # Directory store Hanoi installer file on VM
        RELEASE_PREFIX = "HanoiInstaller"
        RELEASE_SUFFIX = "exe"
        INSTALL_DIR = r'C:/Program\ Files/Hanoi/'

    @staticmethod
    def is_hanoi_installer(file_name):
        """
        Check input file name is Hanoi Installer's name or not.

        Parameters
        ----------
        file_name: str
            Input file name.

        Returns
        -------
        bool
            True if input file name is match with Hanoi Installer name
            False if input file name is not match
        """
        import re
        if re.search(HanoiProject.RELEASE_PREFIX, file_name, re.I) \
                or re.search(HanoiProject.Windows.RELEASE_PREFIX,
                             file_name,
                             re.I):
            return True
        else:
            return False
