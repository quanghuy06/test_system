#!/bin/bash

USERS='binhnk thuyttp namld huanlv phuchm taipd namnb datvt'
REMOTE_SERVER="10.116.41.96"
USER_REMOTE="ocr3"
SRC_REMOTE="/media/ocr3/data/Samba"
DEST_LOCAL="/media/ocr5/backup/workspace"
DATE=$(date +"%d")
MONTH=$(date +"%m")
YEAR=$(date +"%Y")
DAY=$(date +"%w") # 0..6 in which 0 is Sunday

_sync_remote()
{
	for user in $USERS
	do
		if ! [ -d "${DEST_LOCAL}/new/${user}" ]; then
			mkdir -p "${DEST_LOCAL}/new/${user}"
		fi
		rsync -a ${USER_REMOTE}@${REMOTE_SERVER}:${SRC_REMOTE}/${user}/ "${DEST_LOCAL}/new/${user}/" --delete
	done
}

_sync_store()
{
	for user in $USERS
	do
		if ! [ -d "${DEST_LOCAL}/new/${user}" ]; then
			mkdir -p "${DEST_LOCAL}/new/${user}"
		fi
		if ! [ -d "${DEST_LOCAL}/old/${user}" ]; then
			mkdir -p "${DEST_LOCAL}/old/${user}"
		fi
		rsync -a "${DEST_LOCAL}/new/${user}/" "${DEST_LOCAL}/old/${user}/" --delete
	done
}

_store_weekly_backup()
{
	for user in $USERS
	do
		tar czf ${DEST_LOCAL}/${WEEK_FOLDER}/files/${user}.tar.gz ${DEST_LOCAL}/old/${user}
	done
}

_create_patch()
{
	for user in $USERS
	do
		USER_FOLDER="$1/${user}"
		if ! [ -d ${USER_FOLDER} ]; then
			mkdir -p "${USER_FOLDER}"
		fi
		diff -ruN ${DEST_LOCAL}/old/${user}/ ${DEST_LOCAL}/new/${user}/ > $1/${user}/${DATE}_${MONTH}_${YEAR}.patch
	done
}

DATE_START=$(date -d'sunday-7 days' +%d_%m_%Y)
WEEK_FOLDER="Week_${DATE_START}"
DATE_START=$(date -d'sunday-42 days' +%d_%m_%Y)
WEEK_DELETE="Week_${DATE_START}"
_sync_store
_sync_remote

if [ $DAY = 0 ]; then
# Weekly backup on Sunday
	WEEK_FOLDER="${DATE}_${MONTH}_${YEAR}"
	if ! [ -d ${PATCHES_FOLDER} ]; then
		mkdir -p "${DEST_LOCAL}/${WEEK_FOLDER}/files"
	fi
	_store_weekly_backup
	if [ -d "${DEST_LOCAL}/${WEEK_DELETE}" ]; then
		rm -rf "${DEST_LOCAL}/${WEEK_DELETE}"
	fi
else
# Daily backup
	PATCHES_FOLDER="${DEST_LOCAL}/${WEEK_FOLDER}/patches"
	if ! [ -d $PATCHES_FOLDER ]; then
		mkdir -p "${PATCHES_FOLDER}"
	fi
	_create_patch "${PATCHES_FOLDER}"
fi

# Backup to company's samba server
MOUNT_POINT="/tmp/backup_workspace_/"
rsync -a "${DEST_LOCAL}/" "${MOUNT_POINT}" --delete