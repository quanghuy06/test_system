# Author: TaiPD
# Email: tai.phungdinh@toshiba-tsdv.com 
# Date create: August, 19th 2016
# Last update: 25/8/2016

				Create workspace on samba server
-----------
Content: 
1. Overview
2. Develope Enviroment
3. Detail setup
4. Script usage
[Tip 1] Set Path enviroment variable
[Tip 2] Useful command line linux to manage user and group
------------

1. Overview
- User at remote machine will run a python script create_worksp_client.py to require server create workspace and share on samba server
- To do this action, user need a valid account that create by administrator user on server. On server side, administrator can manage samba users:
create an user account samba by using python script create_samba_user.py and delete an user by using delete_samba_user.py
- Each samba user have a home directory and only them have permission -rwx on this directory. Other members of samba group (smbgrp) only have permission -rx.
- For client:
	+ URL to folder of user's NFS share: \\<server>\<username>
	+ URL to workspace: \\<server>\<username>\<workspace>
- Directory store user's data on server
	+ Directory for each user's data: /samba/<username>
	+ Directory for workspace: /samba/<username>/<workspace>

2. Develope Enviroment
 2.1 Client
- OS: Windows 10, Ubuntu 14.04
- Packages need:
  + python version 2.7 or later
  + pip
  + python modules: paramiko (SSH)
 2.2 Server
- OS: Ubuntu 14.04 LTS
- Packages need:
 + samba
 + git
 + members
 + python-pip
 + python modules: pexpect (interactive password)
 
3. Detail setup
 3.1 Client Windows, Ubuntu 14.04
  3.1.1 Install python 2.6.6	(Not check)
  - Download Windows Installer Packages (MSI) python-2.6.6: https://www.python.org/download/releases/2.6.6/
  - Run .msi file --> As default python is installed in C:\Python26
  - Add python directory C:\Python26 to Path environment variable so we can use python in command prompt --> see How to in [Tip 1]
  3.1.2 Install pip
  - Download get-pip.py : https://bootstrap.pypa.io/get-pip.py
  - Open command prompt, change current directory to where store get-pip.py
  - Run command: python get-pip.py
  - As default, pip is installed in C:\Python26\Scripts\
  - Add this directory to Path environment variable so we can use pip in command prompt --> see How to in [Tip 1]
  3.1.2 Install python modules
  - Use git bash
  - Install paramiko: pip install paramiko
 3.2 Server
  3.2.1 Install samba server
  - sudo apt-get install samba
  3.2.2 Install git
  - sudo apt-get install git
  3.2.3 Install members
  - sudo apt-get install members
  3.2.3 Install python 2.7 (In ubuntu 14.04, python 2.7 is a built-in package)
  3.2.4 Install pip
  - sudo apt-get install python-pip
  3.2.5 Install python modules
  - Set proxy 
  - pip install pexpect
  3.2.6 Other
  - Add samba group: sudo groupadd smbgrp
  - Add user administrator:
   sudo useradd -m -d /home/administrator -G sudo,smbgrp administrator
   sudo passwd administrator --> Type password: admin
  - Copy script file to /home/administrator/Scripts
  - Configure for administrator user to run sudo command without entering password
   sudo visudo
   Add this line to end of file: administrator ALL=(ALL) NOPASSWD:ALL
   Save it and log out to execute
  - Create folder /samba to store all data will be share in samba group
   + sudo mkdir /samba
   + sudo chmod 755 /samba
   + sudo chown administrator:smbgrp /samba
4. Scripts usage
 4.1 Client
 - Usage: python create_worksp_client.py -u <username> -p <password> -s <server> -w <workspace>
 - Process:
  + SSH by username and password to check if user is valid
  + If user is valid, SSH by administrator to call script create_worksp_server.py on server.
 - Output: Print url to NFS samba on screen such as \\<server>\<username>\<workspace> . Check by paste this url to windows explorer
 4.2 Server
  4.2.1 Create workspace
   - Usage: python create_worksp_server.py -u <username> -w <workspace>
   - Process:
    + Check if user has an samba account: If not --> Error
    + Create workspace follow structure, workspace has path /samba/<username>/<workspace> and it contains 4 child folder: SRC, TESTS, UTILITIES, REVIEW
    + Change permission and owner for these directories to user. --> Because this script is execute by administrator.
    + Git clone data for SRC and UTILITIES
   - Output: Workspace has been created follow structure and share for user on samba server
  4.2.2 Create account to samba group
   - Usage: python create_samba_user.py -u <username> -p <password>
   - This script will be called automatically by request when execute create_worksp_client.py on client
   - Process:
    + Check if directory /samba is existed --> If not then create
    + Add user to samba server, set home directory is /samba/<username>
    + Configure /etc/samba/smb.conf to make folder share for user
    + Restart samba service to apply changes
   - Output: Create samba account and folder share for user. URL for NFS folder is \\<server>\<username>, require permission to access from remote machine
  4.2.3 Delete an user of samba group
   - Usage: delete_samba_user -u <username>
   - Process:
    + Delete user
    + Delete directory /samba/<username>
    + Edit samba config file /etc/samba/smb.conf
    + Restart samba service to apply changes
    
[Tip 1] Set Path enviroment variable
- In Search on Taskbar, search by enviroment --> click on Edit the system environment variables
- In box System Properties --> click on button Environment Variables... at bottom
- In the second table on Environment Variables windows, choose Path then click on button Edit...
- In Edit Enviroment Variables windows --> click on New --> Type directory --> OK

[Tip 2] Useful command line linux to manage user and group
- List all groups on system: cut -d: -f1 /etc/group
- List all users of group: members <group>
- Disable list users on login screen ubuntu: 
	+ sudo mkdir -p /etc/lightdm/lightdm.conf.d
	+ sudo gedit /etc/lightdm/lightdm.conf.d/10-ubuntu.conf
	+ Add these line to file
		[SeatDefaults]
		user-session=ubuntu
		greeter-show-manual-login=true    
		greeter-hide-users=true    
		allow-guest=false
	+ Save file and restart lightdm service: sudo service lightdm restart

[Tip 3] Set proxy for environment
	export http_proxy=http://<username>:<password>@<server>:<port>
	export https_proxy=http://<username>:<password>@<server>:<port>
