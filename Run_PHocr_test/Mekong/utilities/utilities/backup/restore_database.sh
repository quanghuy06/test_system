#!/bin/bash

DEST_LOCAL="/media/ocr5/backup/mekongdb"
REL_DEST="media/ocr5/backup/mekongdb"

echo "Get back up of yesterday"
DATE_START=$(date -d'sunday-7 days' +%d_%m_%Y)
WEEK_FOLDER="Week_${DATE_START}"
YESTERDAY=$(date -d'-1 days' +%d_%m_%Y)

# Remove MekongDB folder
rm -rf "MekongDB"

# Create temporary working directory
CURR_WD=`pwd`
TMP_WD="backup_database_hh12491042509"
mkdir "${TMP_WD}"
cd "${TMP_WD}"

# Copy package and patch file to working directory
# Copy backup package
PACKAGE="mekongdb.tar.gz"
PACKAGE_PATH="${DEST_LOCAL}/${DATE_START}/${PACKAGE}"
cp "${PACKAGE_PATH}" .
# Extract package
tar xzf "${PACKAGE}"
# Remove compress package
rm "${PACKAGE}"
if [ "${YESTERDAY}" != "${DATE_START}" ]; then
	# If yesterday is normal day, patch data
	# Copy patch file to working directory
	PATCH="${DEST_LOCAL}/${WEEK_FOLDER}/patches/${YESTERDAY}.patch"
	cp "${PATCH}" .
	patch -s -p0 < "${YESTERDAY}.patch"
fi

# Copy data
cp -r "${REL_DEST}/old" "${CURR_WD}/MekongDB"

# Remove temporary working directory
cd "${CURR_WD}"
rm -rf "${TMP_WD}"
echo "Finish! Backup folder is MekongDB"

