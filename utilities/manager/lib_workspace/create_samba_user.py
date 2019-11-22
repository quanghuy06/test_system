# Author: 			TaiPD
# Email: 			tai.phungdinh@toshiba-tsdv.compile
# Date create: 		August, 17th 2016
# Last update: 		19/8/2106
# Usage: 			python <script> -u <user> -p <password>
# Description: 		This script is used by administrator to create an user account on samba server
import optparse
import pexpect
import os

# Parse options
parser = optparse.OptionParser()
# Fetch username
parser.add_option('-u', '--user',
		  dest="username",
		  help="username ",
		  )
# Fetch passwork
parser.add_option('-p', '--passwd', 
                  dest="password",
		  help="password",
                  )
parser.add_option('-v', '--verbose',
                  dest="verbose",
                  default=False,
                  action="store_true",
                  )
parser.add_option('--version',
                  dest="version",
                  default=0.1,
                  type="float",
                  )
# Fetch options 
options, remaining = parser.parse_args()

# Check if options are enough
if not (options.username and options.password) :
	print ("Usage: python create_samba_user.py -u <username> -p <password>")
else :
	# Check if user account have already existed
	child = pexpect.spawn("members smbgrp")
	while True:
	    try:
		child.expect(options.username)
		print("User already existed!")
		os._exit(1)
	    except pexpect.EOF:
		break
	# Add user
	useradd = "sudo useradd " + options.username + " -G smbgrp"		# Add user to group smbgrp
	pexpect.run(useradd)
	# Set password for linux
	passwd = "sudo passwd " + options.username
	setpasswd = pexpect.spawn(passwd)
	setpasswd.expect("Enter new UNIX password: ")
	setpasswd.sendline(options.password)
	setpasswd.expect("Retype new UNIX password: ")
	setpasswd.sendline(options.password)
	#Set password for samba
	smbpasswd = "sudo smbpasswd -a " + options.username
	setsmbpasswd = pexpect.spawn(smbpasswd)
	setsmbpasswd.expect("New SMB password:")
	setsmbpasswd.sendline(options.password)
	setsmbpasswd.expect("Retype new SMB password:")
	setsmbpasswd.sendline(options.password)
	# Create folder share for user
	if not os.path.exists("/samba") :
		pexpect.run('sudo mkdir /samba')
	pexpect.run('sudo chown administrator:smbgrp /samba')			# Change owner of /samba from root to administrator
	folder = "/samba/" + options.username
	pexpect.run("sudo mkdir " + folder)
	pexpect.run("sudo chmod -R 0771 " + folder)
	pexpect.run("sudo chown " + options.username + ":smbgrp " + folder)	# Change owner of /samba/user from root to user
	# Configure folder samba share
	pexpect.run("cp /etc/samba/smb.conf smb.conf.tmp")		# need to edit samba config file at /etc/samba/smb.conf
	configure = "\n[" + options.username + "]\n"			# name will show when access url \\<server>
	configure += "path = /samba/" + options.username + "\n"	# set path to share
	configure += "browsable = yes\nwritable = yes\nread only = no\nguest ok = no\ncreate mask = 0771\n"  	# Set some attributes
	configure += "write list = " + options.username + "\n"	# Only owner can write to this folder 
	configure += "read list = @smbgrp\n"					# Other members in group smbgrp can read
	configure += "valid users = @smbgrp\n"					# This share folder can access by members of group smbgrp
	with open("smb.conf.tmp", "a") as myfile:
	    myfile.write(configure)
	pexpect.run("sudo mv smb.conf.tmp /etc/samba/smb.conf")
	pexpect.run("sudo service smbd restart")				# Restart smbd service to apply changes


