# Author: 			TaiPD
# Email: 			tai.phungdinh@toshiba-tsdv.compile
# Date create: 		August, 17th 2016
# Last update: 		19/8/2106
# Usage: 			python <script> -u <username> -w <workspace>
# Description: 		This script will be called automatically by request when execute create_worksp_client.py
import optparse
import os
import pexpect

# Parse options
parser = optparse.OptionParser()
# Fetch username
parser.add_option('-u', '--user',
		  dest="username",
		  help="username ",
		  )
# Fetch workspace
parser.add_option('-w', '--workspace', 
                  dest="workspace",
	          help="name of workspace",
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

# Check if not enough arguments, then warning and do nothing
if not (options.username and options.workspace) :
	print ("Usage: <script> -u <username> -w <workspace>")
else :	# If enough parameters
	child = pexpect.spawn("members smbgrp")
	userSamba = False
	while True:
	    try:	# Check if user is added to samba server then break while() and continue
			child.expect(options.username)
			userSamba = True
			break;
	    except pexpect.EOF: # If not then warning and exit script
			break
	if not userSamba :
		print ("User doesn't have an acount on samba server!")
		print ("Error!")
	else :
		# Create workspace follow structure
		ws_path = "/samba/" + options.username + "/" + options.workspace
		if os.path.exists(ws_path) :
			print("Worksapce has already existed!")
		else :
			pexpect.run("sudo mkdir " + ws_path)
			pexpect.run("sudo chown " + options.username + ":smbgrp " + ws_path) 
			# Create SRC folder
			src_path = ws_path + "/SRC"
			pexpect.run("sudo mkdir " + src_path)
			pexpect.run("sudo chown " + options.username + ":smbgrp " + src_path) 
			# Create TESTS folder
			test_path = ws_path + "/TESTS"
			pexpect.run("sudo mkdir " + test_path)
			pexpect.run("sudo chown " + options.username + ":smbgrp " + test_path) 
			# Create UTILITIES folder
			ut_path = ws_path + "/UTILITIES" 
			pexpect.run("sudo mkdir " + ut_path)
			pexpect.run("sudo chown " + options.username + ":smbgrp " + ut_path) 
			# Create REVIEW folder
			review_path = ws_path + "/REVIEW"
			pexpect.run("sudo mkdir " + review_path)
			pexpect.run("sudo chown " + options.username + ":smbgrp " + review_path)

			# Git source code and utilities
			# Git clone source code from vc1.tsdv.com.vn/git
			# repo = "http://vc1.tsdv.com.vn/git/2016A/ocr/HanoiWorkflow.git"
			# pexpect.run("sudo git clone " + repo + " " + src_path)
			# Git clone utilities
			# repo = ""
			# pexpect.run("sudo git clone " + repo + " " + ut_path)
			print ("Successful!")
	