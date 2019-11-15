# Author: 			TaiPD
# Email: 			tai.phungdinh@toshiba-tsdv.compile
# Date create: 		August, 19th 2016
# Last update: 		19/8/2106
# Usage: 			python <script> -u <user> 
# Description: 		This script is used by administrator to delete an user account on samba server

import optparse
import pexpect

# Parse options
parser = optparse.OptionParser()
# Fetch username
parser.add_option('-u', '--user',
		  dest="username",
		  help="username ",
		  )
# Fetch options 
options, remaining = parser.parse_args()

if not options.username :
	print ("Usage: python create_samba_user.py -u <username>")
else :
	# Check if user is a Samba user
	child = pexpect.spawn("members smbgrp")
	userSamba = False
	while True:
	    	try:
			child.expect(options.username)
			userSamba = True
			break
	    	except pexpect.EOF:
			break
	if not userSamba :
		print (options.username + " is not a Samba user!")
	else :
		# Delete user
		pexpect.run("sudo userdel " + options.username)
		# Delete user's share folder
		pexpect.run("sudo rm -rf /samba/" + options.username)
		# Edit samba config file /etc/samba/smb.conf
		pexpect.run("cp /etc/samba/smb.conf smb.conf.tmp")
		# Open file and read file into data list
		with open("smb.conf.tmp", "r") as myfile :
			data = myfile.readlines()
		index = data.index("[" + options.username + "]\n")
		# Remove line in data list that used to configure for user
		for count in range(11) :
			data.pop(index - 1)
		# Apply edit to file
		with open("smb.conf.tmp", "w") as myfile :
			myfile.writelines(data)
		pexpect.run("sudo mv smb.conf.tmp /etc/samba/smb.conf")
		# Restart samba service to apply changes
		pexpect.run("sudo service smbd restart")
