#!/bin/bash

ROOTDIR=~/jenkins/workspace/

if [ -z $1 ]; then
	echo "Empty argument! Nothing to do!"
	exit
fi
WSDIR="${ROOTDIR}$1"

if [ ! -d $WSDIR ]; then
	echo "Create workspace directory"
	mkdir -p $WSDIR
else
	echo "Clean workspace"
	rm -rf $WSDIR/*
fi
