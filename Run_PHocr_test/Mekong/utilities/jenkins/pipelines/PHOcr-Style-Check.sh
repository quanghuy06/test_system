#!/bin/bash

################################## CLEAN STAGE ##################################
git clean -fdx
git fetch ssh://namld@10.116.41.96:29418/PHOcr $GERRIT_REFSPEC && git checkout FETCH_HEAD

################################## CPPLINT ##################################
TMP_FOLDER=/tmp/check-style
if [ ! -d "$TMP_FOLDER" ]; then
    mkdir $TMP_FOLDER
fi
curr_folder="$PWD"
cd $TMP_FOLDER
rm -rf check-style
git clone ssh://namld@10.116.41.96:29418/check-style && scp -p -P 29418 namld@10.116.41.96:hooks/commit-msg check-style/.git/hooks/
cd check-style
git fetch ssh://namld@10.116.41.96:29418/check-style refs/changes/17/1917/1 && git checkout FETCH_HEAD
cd "$curr_folder"

python3 $TMP_FOLDER/check-style/check_style.py --root-folder $PWD

################################## CPPCHECK & PYLINT ##################################
# Setting for pylint
export PYTHONPATH=$PWD/phocroffice/:$PYTHONPATH
echo "[MASTER]" > pylintrc
echo "init-hook='from phocr_shared.phocr_python_path import load_path; load_path()'" >> pylintrc
PYLINT_RCFILE="$PWD/pylintrc"

analysis() {
    log_file="$1"
    echo "Start cppcheck"
    cpp_folders="phocr/ barcode/ macroregion/ preprocess/ leptonica/ utility/ ocrengine/"
    cpp_flags="-DOCRENGINE -DMACROREGION -DPREPROCESS -DBARCODE -DPHOCR_TESSERACT -DTESS_EDITED -DNOT_RELEASE -D__GXX_EXPERIMENTAL_CXX0X__ -D__cplusplus=201103L -D__MMX__ -D__SSE__ -D__SSE2__ -D__SSE3__ -D__SSSE3__ -D__POPCNT__"
    cpp_flags="$cpp_flags -DPHOCR_EXPORTS -DPREPROCESSOR_EXPORTS -DBARCODE_EXPORTS -DMACROREGION_EXPORTS"
    cpp_flags="$cpp_flags -DUTILITY_EXPORTS -DPHOCR_EXPORTS -DTESS_EXPORTS -DLIBLEPT_EXPORTS"
    #cppcheck $cpp_flags --enable=all --inconclusive --xml --xml-version=2 $cpp_folders 2> cppcheck_${log_file}.xml > cppcheck_log.txt
    echo "Finish cppcheck"

    python_package="phocroffice"
    echo "Start pylint"
    echo "We are in $PWD"
    pylint --rcfile $PYLINT_RCFILE --dummy-variables-rgx=^_.* --disable=R0201,W0232,R0913 --max-attributes=25 --max-public-methods=80 --max-args=8 \
        --good-names=x,y,w,h,i,j,k,ex,Run,_ $python_package -f html > pylint_${log_file}.html || true
    echo "Finish pylint"
}

echo "Process static checking"
analysis "after"
header_after=`git log --pretty=oneline --abbrev-commit -n 1 | cat`
git reset --hard HEAD~1
header_before=`git log --pretty=oneline --abbrev-commit -n 1 | cat`
analysis "before"

if [ -d "scripts" ]; then
    rm -rf "scripts"
fi
message_diff="<h3 style=\"color: orange; line-height: 2; text-align: left;\">Before: $header_before</h3><h3 style=\"color: orange; line-height: 2; text-align: left;\">After: $header_after</h3>"

cp -r /home/ocr3/.jenkins/scripts .
python3 scripts/compare_style.py -o pylint_out.html -t TOOL_PYLINT -b pylint_before.html -a pylint_after.html --diff-header "$message_diff"
#python3 scripts/compare_style.py -o cppcheck_out.html -t TOOL_CPPCHECK -b cppcheck_before.xml -a cppcheck_after.xml --diff-header "$message_diff"

server="10.116.41.96"
account="Jenkins"
change="$GERRIT_CHANGE_NUMBER"
patch="$GERRIT_PATCHSET_NUMBER"
label="StyleChecker"
message="Style report"
result="0"
ssh -p 29418 ${account}@${server} gerrit review ${change},${patch} --label ${label}=${result} -m \"[${label}] ${message} ${BUILD_URL}\"