#!/bin/bash

REMOTE_SERVER="10.116.41.96"
USER_REMOTE="ocr3"
SRC_REMOTE="/home/ocr3/.jenkins/"
DEST_LOCAL="/media/ocr4/backup/jenkins"
DATE=$(date +"%d")
MONTH=$(date +"%m")
YEAR=$(date +"%Y")
DAY=$(date +"%w") # 0..6 in which 0 is Sunday
DATE_START=$(date -d'sunday-7 days' +%d_%m_%Y)
WEEK_FOLDER="Week_${DATE_START}"
DATE_START=$(date -d'sunday-42 days' +%d_%m_%Y)
WEEK_DELETE="Week_${DATE_START}"
if ! [ -d "${DEST_LOCAL}/new" ]; then
	mkdir -p "${DEST_LOCAL}/new"
fi
if ! [ -d "${DEST_LOCAL}/old" ]; then
	mkdir -p "${DEST_LOCAL}/old"
fi
rsync -a "${DEST_LOCAL}/new/" "${DEST_LOCAL}/old/" --delete --copy-links
rsync -a ${USER_REMOTE}@${REMOTE_SERVER}:${SRC_REMOTE} "${DEST_LOCAL}/new/" --delete --copy-links

if [ $DAY = 0 ]; then
# Weekly backup on Sunday
	WEEK_FOLDER="${DATE}_${MONTH}_${YEAR}"
	WEEK_PATH="${DEST_LOCAL}/${WEEK_FOLDER}"
	if ! [ -d ${WEEK_PATH} ]; then
		mkdir -p "${WEEK_PATH}}"
	fi
	tar czf "${WEEK_PATH}/jenkins.tar.gz" "${DEST_LOCAL}/old/"
	if [ -d "${DEST_LOCAL}/${WEEK_DELETE}" ]; then
		rm -rf "${DEST_LOCAL}/${WEEK_DELETE}"
	fi
else
# Daily backup
	PATCHES_FOLDER="${DEST_LOCAL}/${WEEK_FOLDER}/patches"
	if ! [ -d $PATCHES_FOLDER ]; then
		mkdir -p "${PATCHES_FOLDER}"
	fi
	diff -ruN "${DEST_LOCAL}/old/" "${DEST_LOCAL}/new/" > "${PATCHES_FOLDER}/${DATE}_${MONTH}_${YEAR}.patch"
fi

# Backup to company's samba server
MOUNT_POINT="/tmp/backup_jenkins_/"
rsync -a "${DEST_LOCAL}/" "${MOUNT_POINT}" --delete --copy-links