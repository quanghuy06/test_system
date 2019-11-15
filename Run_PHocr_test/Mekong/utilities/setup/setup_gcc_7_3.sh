#!/bin/bash

# @Author: Phung Dinh Tai
# Date created: 09/08/2018
# Description: This script to install g++ version 7.3.0

gxx_bin=$(which g++)
if [ ! -z "${gxx_bin}" ]; then
    version=$(g++ --version | grep "7.3.0")
    if [ ! -z "${version}" ]; then
        echo "INFO: g++ 7.3.0 was installed on this machine. Done!"
        exit 0
    fi
fi

SMB_SERVER="//10.116.16.2/ocrpoc"
SMB_DIRECTORY="softwares"
GCC_PACKAGE="gcc-7.3.0.tgz"
GCC_FOLDER="gcc-7.3.0"
DEFAULT_DESTINATION="/tmp/gxx"

if [ "$2" = "" -a ! -f ${GCC_PACKAGE} ]; then
    helprequested="true"
fi

while true ; do
    case "$1" in
        -u) username=$2; shift 2;;
        -p) password=$2; shift 2;;
        -d) destination=$2; shift 2;;
        -h) helprequested="true"; shift;;
        --) shift; break;;
		*) break;;
    esac
done

if [ "${helprequested}" = "true" ]; then
    echo ""
    echo "Setting up new version of gcc-7.3.0"
    echo ""
    echo "Using: $0 -u <username> -p <password> [-d <target directory>]"
    echo ""
    echo "You need to provide right username and password to access samba server //10.116.16.2/ocrpoc."
    echo "This information is needed to download build version of gcc-7.3.0. If you've already had the"
    echo "build ${GCC_PACKAGE}, do not need pass these options."
    echo "Note that provide with the right name!"
    echo ""
    echo "[Optional] target directory: Where you want to extract build of g++ 7.3.0. If has no "
    echo "specific idea, you can do not pass it, default is /tmp/gxx"
    echo ""
    exit 1
fi

echo "> Get build package of gcc 7.3.0"
if [ -f ${GCC_PACKAGE} ]; then
    echo "Find ${GCC_PACKAGE}"
else
    smbclient -U ${username}%${password} ${SMB_SERVER} --directory=${SMB_DIRECTORY} -c "get \"${GCC_PACKAGE}\""
fi

if [ ! -f ${GCC_PACKAGE} ]; then
    echo "FAIL: Can not get build package. Stop!"
    exit 1
else
    echo "SUCCESSFUL"
fi

echo ""
echo "> Extract build package"
if [ -z "${destination}" ]; then
    destination=${DEFAULT_DESTINATION}
fi

GCC_DIR="${destination}/${GCC_FOLDER}"

if [ -d ${GCC_DIR} ]; then
    rm -rf ${GCC_DIR}
fi

if [ ! -d ${destination} ]; then
    mkdir -p ${destination}
fi
tar xzf ${GCC_PACKAGE} -C ${destination}

if [ -d ${GCC_DIR} ]; then
    echo "SUCCESSFUL"
    rm ${GCC_PACKAGE}
else
    echo "FAIL: Can not extract gcc to ${destination}"
    exit 1
fi

echo ""
echo "> Update alternative for new gcc"
# Get absolute path of g++ binary
# Check and install realpath package
strc=$(dpkg -l | grep -i realpath)
if [ -z "${strc}" ]; then
    echo "Install realpath package"
    sudo apt-get -y install realpath > /dev/null
fi

GXX_BIN=$(realpath ${GCC_DIR}/bin/g++)
GXX_LNK=$(which g++)
if [ -z ${GXX_LNK} ]; then
    rm -f /usr/bin/g++
    # Create soft link
    sudo ln -s ${GXX_BIN} /usr/bin/g++
else
    # Update alternative
    echo "Please choose the right option to the path of gcc 7.3.0 then press ENTER"
    sudo update-alternatives --install /usr/g++ g++ ${GXX_BIN} 1
    sudo update-alternatives --config g++
fi

echo ""
echo "> Checking installation"
version=$(g++ --version | grep "7.3.0")
if [ -z "${version}" ]; then
    echo "Installation FAIL. g++ 7.3.0 was not installed on this machine!"
    exit 1
else
    echo "Installation SUCCESSFUL!"
fi
