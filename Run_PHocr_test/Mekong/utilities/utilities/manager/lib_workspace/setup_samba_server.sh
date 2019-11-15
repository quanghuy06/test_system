#!/bin/bash
# TOSHIBA-TSDV
# Author:       Tai Phung Dinh
# Email:        tai.phungdinh@toshiba-tsdv.com
# Date create:  August 20th, 2016
# Last update:  22/9/2016
# Description:  This bash script is used for set up environment for
#               creating samba server of automation test system

ERROR_PACKS=""      # Packages install with error
# Function for check package is install or not. If not, install it.
check_package() {
  echo -e "\n$1: "
  ISINSTALLED=`dpkg-query -l $1 | grep ii`
  # ISINSTALLED should be empty if package hasn't been installed
  if [ -z "$ISINSTALLED" ]; then
    # Package hasn't been installed
    echo -e "Not installed!\nInstall..."
    if sudo apt-get -y install $1; then
      # Install successfully
      echo "Successfully installed $1"
    else
      # Fail to install --> add to list error packages
      ERROR_PACKS="$ERROR_PACKS $1"
      echo "Error installing $1"
    fi
  else
    # Package has been installed
    echo "Installed!"
  fi
}

check_python_module() {
  echo -e "\nPython module $1 :"
  ISINSTALLED=`pip freeze | grep "$1"`
  if [ -z "$ISINSTALLED" ]; then
     echo "Install..."
     sudo -E pip install $1
     ISINSTALLED=`pip freeze | grep "$1"`
     if [ -z "$ISINSTALLED" ]; then
        echo "Error install python module $1"
        ERROR_PACKS="$ERROR_PACKS $1"
     else
        echo "Install Successfully!"
     fi
  else
     echo "Installed!"
  fi
}
# Check for samba server
echo "Check for samba server package..."
check_package samba
# Check for members --> use to check user is valid or not
echo "Check for members package..."
check_package members
# Check for pip
echo "Check for pip..."
ISINSTALLED=`pip --version | grep "pip"`
# ISINSTALLED should be empty if pip haven't been installed
if [ -z "$ISINSTALLED" ]; then
  # pip haven't been installed
  echo -e "\nNot installed!\nInstall..."
  wget https://bootstrap.pypa.io/get-pip.py
  sudo -E python get-pip.py
  rm get-pip.py
  # Check if pip is installed successfully
  ISINSTALLED=`pip --version | grep "pip"`
  if [ -z "$ISINSTALLED" ]; then
    # Fail to install pip
    ERROR_PACKS="$ERROR_PACKS pip"
    echo "Error installing pip"
  else
    # Install successfully
    echo "Installed successfully!"
    # Install python module pexpect
    check_python_module pexpect
  fi
else
  # pip have been installed
  echo "Installed!"
  # Check for python module pexpect
  check_python_module pexpect
fi

# Setup user and group for samba. Create group smbgrp for users using
# samba on linux. User wants to use samba need to be an user on linux
# server.
GROUP="smbgrp"
echo "Check for samba group $GROUP..."
if grep -q $GROUP /etc/group; then
   # Group existed
   echo "Group $GROUP has already existed!"
else
   # Group does not exist
   echo -e "Not exists!\nAdd group..."
   sudo groupadd $GROUP
   echo "Added"
fi

# Create groups for admins of samba server
ADMINGROUP="admin_samba"
echo "Check for samba group $ADMINGROUP..."
if grep -q $ADMINGROUP /etc/group; then
   # Group existed
   echo "Group $GROUP has already existed!"
else
   # Group does not exist
   echo -e "Not exists!\nAdd group..."
   sudo groupadd $ADMINGROUP
   echo "Added"
fi

# Create an admin user for samba group
ADMIN="administrator"
echo "Check for user $ADMIN..."
ISEXIST=`id $ADMIN | grep "$ADMIN"`
# ISEXIST should be empty if admin user does not exist
if [ ! -z "$ISEXIST" ]; then
   # ISEXIST is not empty --> admin user existed
   echo "User $ADMIN has already existed!"
else
   # admin user does not exist --> Add
   echo -e "Not exists!\nAdd user..."
   sudo useradd -m -G sudo,$GROUP,$ADMINGROUP $ADMIN
   echo "Please type \"admin\" for all password required!"
   sudo passwd $ADMIN
   sudo smbpasswd -a $ADMIN
   # Allow ADMIN can run sudo without enter a password
   # ******** Do not change this **********
   ISEXIST=`id $ADMIN | grep "$ADMIN"`
   # ISEXIST should be empty if admin user fail to add
   if [ ! -z "$ISEXIST" ]; then
      # Admin user added successfully
      sudo cp /etc/sudoers .
      echo "$ADMIN ALL=(ALL) NOPASSWD:ALL" | sudo tee --append sudoers
      sudo mv sudoers /etc/sudoers
   else
      echo "Add user $ADMIN failed!"
   fi
   # **************************************
fi

# Create folder for all samba's folders
SAMBA_DIR="/samba"
echo "Create folder /samba"
if [ -d "$SAMBA_DIR" ]; then
   echo "Folder $SAMBA_DIR has already existed!"
else
   # Folder does not exist --> Create
   sudo mkdir $SAMBA_DIR
   sudo chmod 775 $SAMBA_DIR
   sudo chown $ADMIN:$ADMINGROUP $SAMBA_DIR
fi

# Create folder Scripts that contain scripts that is requested from
# client
echo "Create folder Scripts"
SCRIPTS_DIR="/home/administrator/Scripts/"
if [ -d "$SCRIPTS_DIR" ]; then
   echo "Folder $SCRIPTS_DIR has already existed!"
   if [ ! -f "$SCRIPTS_DIR/create_workspace_server.py" ]; then
      sudo cp create_workspace_server.py $SCRIPTS_DIR
      sudo chown $ADMIN $SCRIPTS_DIR/create_workspace_server.py
   fi
else
   # Create folder SCRIPTS and copy script create_workspace_server.py into it
   sudo mkdir $SCRIPTS_DIR
   sudo cp create_workspace_server.py $SCRIPTS_DIR
   sudo chmod 775 $ADMIN
   sudo chown -R $ADMIN:$ADMINGROUP $SCRIPTS_DIR
fi

# Print all packages fail to install on screen
if [ ! -z "$ERROR_PACKS" ]; then
  echo "Error while install packages: $ERROR_PACKS"
else
  echo "All packages are installed successfully!"
fi
