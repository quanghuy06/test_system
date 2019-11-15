#!/bin/sh

while true ; do
    case "$1" in
        -g) grounddata=$2; shift 2;;
				-u) user=$2; shift 2;;
				-p) password=$2; shift 2;;
				--help) printhelp="true"; shift;;
        --force) forceupdate="true"; shift;;
        --) shift; break;;
		*) break;;
    esac
done

if [ -z "$grounddata" ] || [ -z "$user" ] | [ -z "$password" ]; then
		printhelp="true"
fi

if [ "$printhelp" = "true" ]; then
		echo ""
    echo "Update ground truth data by using Mekong"
    echo ""
    echo "Using: $0 -u <db_username> -p <db_password> -g <grounddata> --force"
    exit 1
fi

if ! [ -d "Mekong" ]; then
		echo "You need to get Mekong into current directory!"
		git clone http://10.116.41.96:9090/Mekong
		cd "Mekong"
		git checkout Mekong2
		cd ..
fi

scriptdir="Mekong/utilities/other/update_ground.py"

if [ "$forceupdate" = "true" ]; then
		options="--force"
else
		options=""
fi

# Execute command line
python $scriptdir -g $grounddata -u $user -p $password $options
