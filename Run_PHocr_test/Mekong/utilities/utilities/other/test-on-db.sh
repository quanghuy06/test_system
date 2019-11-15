#!/bin/sh

if [ "$2" = "" ]; then
    echo ""
    echo "Testing by using Mekong on folder"
    echo "      /home/ocrdev/2016A/Mekong"
    echo "      by using bin file in <buildfolder>"
    echo ""
    echo "Using: $0 -b <buildfolder> -q <mekongquery> [--get-all-result]"
    echo ""
    echo "<mekongquery>: example: \"-pro phocr\", \"-id 01_0033\"", "\"-t isetdefault:true\""
    echo ""
    exit 1
fi

mekongquery="undefined"
while true ; do
    case "$1" in
        -b) buildfolder=$2; shift 2;;
        -q) mekongquery=$2; shift 2;;
        --get-all-result) getallresult="true"; shift;;
        --) shift; break;;
		*) break;;
    esac
done

currentdir=`pwd`

command -v realpath >/dev/null 2>&1 || { echo >&2 "I require foo but it's not installed. Installing..."; sudo apt-get install realpath; }
scriptdir=`realpath $0`
mekongfolder=$(dirname $(dirname $(dirname $scriptdir)))

cd $buildfolder
buildfolder=`pwd`
cd -


binfolder="$buildfolder/bin/"
libfolder="$buildfolder/lib/"
sharefolder="$buildfolder/share/"

export LD_LIBRARY_PATH="$libfolder"

if [ -z "$PHOCRDATA_PREFIX" ]; then
    export PHOCRDATA_PREFIX="$sharefolder"
fi

echo "GET TEST CASES"
# Reset test folder and outfile
testfolder=$currentdir/TESTS
if [ "$mekongquery" = "undefined" ]; then
    echo "Skip getting test cases"
else
    if [ -d "$testfolder" ]; then
        rm -rf "$testfolder"
    fi
    mkdir $testfolder
    echo "python $mekongfolder/utilities/tests/get_test_cases.py $mekongquery -o $testfolder"
    python "$mekongfolder/utilities/tests/get_test_cases.py" $mekongquery -o "$testfolder"
fi

# Set outfile name is name of build
outfile=$(basename $buildfolder).xml

echo "EXECUTE TESTING"
# Run test
if [ "$getallresult" = "true" ]; then
    echo "python $mekongfolder/utilities/tests/test_all.py -b $binfolder -t $testfolder --report-bb-accuracy --get-all-result --platform linux"
    python "$mekongfolder/utilities/tests/test_all.py" -b "$binfolder" -t "$testfolder" --report-bb-accuracy --get-all-result --platform linux
else
    echo "python $mekongfolder/utilities/tests/test_all.py -b $binfolder -t $testfolder --report-bb-accuracy --platform linux"
    python "$mekongfolder/utilities/tests/test_all.py" -b "$binfolder" -t "$testfolder" --report-bb-accuracy --platform linux
fi
