#!/bin/bash

REMOTE_SERVER="10.116.41.96"
USER_REMOTE="ocr3"
SRC_REMOTE="/media/ocr3/data/MekongDB"
DEST_LOCAL="/media/ocr5/backup/mekongdb"
DATE=$(date +"%d")
MONTH=$(date +"%m")
YEAR=$(date +"%Y")
DAY=$(date +"%w") # 0..6 in which 0 is Sunday

_sync_remote()
{
	if ! [ -d "${DEST_LOCAL}/new/${user}" ]; then
		mkdir -p "${DEST_LOCAL}/new/${user}"
	fi
	rsync -a ${USER_REMOTE}@${REMOTE_SERVER}:${SRC_REMOTE}/${user}/ "${DEST_LOCAL}/new/${user}/" --delete
}

_sync_store()
{
	if ! [ -d "${DEST_LOCAL}/new" ]; then
		mkdir -p "${DEST_LOCAL}/new"
	fi
	if ! [ -d "${DEST_LOCAL}/old" ]; then
		mkdir -p "${DEST_LOCAL}/old"
	fi
	rsync -a "${DEST_LOCAL}/new/" "${DEST_LOCAL}/old/" --delete
}

_store_weekly_backup()
{
	tar czf "${DEST_LOCAL}/${WEEK_FOLDER}/mekongdb.tar.gz" "${DEST_LOCAL}/old/"
}

_create_patch()
{
	diff -ruN "${DEST_LOCAL}/old/" "${DEST_LOCAL}/new/" > "$1/${DATE}_${MONTH}_${YEAR}.patch"
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
	WEEK_BACKUP_FOLDER="${DEST_LOCAL}/${WEEK_FOLDER}"
	if ! [ -d $WEEK_BACKUP_FOLDER ]; then
		mkdir -p "${WEEK_BACKUP_FOLDER}"
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
MOUNT_POINT="/tmp/backup_database_/"
rsync -a "${DEST_LOCAL}/" "${MOUNT_POINT}" --delete