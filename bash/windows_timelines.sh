#!/bin/bash

trap "exit 1" TERM
export TOP_PID=$$

RIP='perl /home/jasa/work/development/RegRipper3.0/rip.pl'

function tln2csv {
	egrep '^[0-9]+\|' | awk -F '|' '{OFS="|";print 0,$5,0,0,0,0,0,-1,$1,-1,-1}' |mactime2 -b - -d -t "$TIMEZONE"
}

function usage {
    echo "Usage: $0 [options] [<windows_mount_dir>}"
		echo ""
		echo "Options:"
		echo "    -t <timezone>    convert timestamps from UTC to the given timezone"
		echo "    -l               list availabel timezones"
		echo "    -h               show this help information"
}

POSITIONAL_ARGS=()
TIMEZONE=UTC

while [[ $# -gt 0 ]]; do
	case $1 in 
	-t)
		TIMEZONE="$2"
		shift
		shift
	;;
	-l)
		mactime2 -t list
		exit 0
	;;
	-h)
		usage
		exit 0
	;;
	*)
		POSITIONAL_ARGS+=("$1")
		shift
	;;
	esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

if [ $# -ne "1" ]; then
    usage
    exit 1
fi

###########################################################
#
# Check required tools
#
#if ! command -v "${RIP}" &>/dev/null; then
#    echo "missing RegRipper; please install RegRipper to ${RIP}" >&2
#    exit 1
#fi

if ! command -v "mactime2" &>/dev/null; then
    echo "missing mactime2; please run `cargo install mactime2`" >&2
    exit 1
fi

if ! command -v "regdump" &>/dev/null; then
    echo "missing regdump; please run `cargo install nt_hive2`" >&2
    exit 1
fi
###########################################################


###########################################################
#
# Checks if a file exists and is readable. If it is, this
# function prints the name of the file.
# If <fail_if_missing> evaluates to true, the functions
# aborts this script if the file does not exist or 
# if it is not readable
# 
# Usage: 
#
# check_file <filename> <fail_if_missing>
#
function check_file {
    local FILE=$1
    local FAIL_IF_MISSING=$2

    if [ -r "$FILE" ]; then
        echo "[+] found '$FILE'" >&2
        echo "$FILE"
        exit
    fi

    if $FAIL_IF_MISSING; then
        echo "[-] missing '$FILE', aborting..." >&2
        kill -s TERM $TOP_PID
    fi

    echo ""
}
###########################################################

###########################################################
#
# Usage:
#
# do_timeline <registry hive file> [<destination>]
#
# If you do not specify a destination, it will default to the
# basename of the registry hive file.
# In every case, destination will be prefixed by 'tln_' and
# suffixed by '.csv', so the remaining file will have the name
#   tln_${destination}.csv
#
function do_timeline {
    local FILE=$1
    if [ "x$2" == "x" ]; then 
        BASENAME=$(basename "$FILE")
    else
        BASENAME=$2
    fi
    
    echo "[+] creating timeline for '$BASENAME'" >&2
    
    $RIP -r "$FILE" -aT 2>/dev/null | egrep '^[0-9]+\|' >tln_$BASENAME.txt
    cat tln_$BASENAME.txt | tln2csv >"tln_$BASENAME.csv"
    BASENAME=
}
###########################################################

###########################################################
#
# Usage:
#
# host_info <path of SYSTEM hive> <path of SOFTWARE hive>
#
function host_info {
    SYSTEM="$1"
    SOFTWARE="$2"
    ${RIP} -r "$SYSTEM" -p compname > compname.txt
    ${RIP} -r "$SYSTEM" -p timezone > timezone.txt

    ${RIP} -r "$SOFTWARE" -p msis > installed_software.txt
    ${RIP} -r "$SOFTWARE" -p winver > winver.txt

    ${RIP} -r "$SYSTEM" -p usbstor > usbstor.txt
    ${RIP} -r "$SYSTEM" -p mountdev2 > mounted_devices.txt
}
###########################################################

###########################################################
#
# Usage:
#
# user_info <username> <path of ntuser.dat>
#
function user_info {
    USER="$1"
    NTUSER_DAT="$2"

    ${RIP} -r "$NTUSER_DAT" -p run > "${USER}_run.txt"
    ${RIP} -r "$NTUSER_DAT" -p cmdproc > "${USER}_cmdproc.txt"
}
###########################################################

###########################################################
#
# Usage:
#
# copy_user_file <username> <profiledir> <source_file_name>
#
function copy_user_file {
	USER="$1"
	PROFILEDIR="$2"
	SRCFILE="$3"
	BASE=$(echo "$SRCFILE" | cut -d . -f 1)
	EXT=$(echo "$SRCFILE" | cut -d . -f 2)
	CNT=1
	for F in `find "$PROFILEDIR" -type f -iname "$SRCFILE"`; do 
		DSTFILE="${BASE}_${USER}_${CNT}.${EXT}"

		if [ -r "$F" ]; then
			echo "[+] exfiltrating '$F' from user $USER" >&2
			cp "$F" "$DSTFILE"
		else
			echo "[-] file '$F' not found" >&2
		fi
		CNT=$(($CNT+1))
	done
}
###########################################################


###########################################################
#
# Usage:
#
# registry_timeline <hive_file>
#
function registry_timeline {
	FILE="$1"
	HIVE=$(basename "$FILE")
	if [ -r "$FILE" ]; then
		echo "[+] creating a timeline of '$HIVE'" >&2
		regdump -b "$FILE" | mactime2 -b - -d -t "$TIMEZONE" > "regtln_${HIVE}.csv"
	else
		echo "[-] file '$FILE' not found" >&2
	fi
}
###########################################################

###########################################################
#
# Usage:
#
# evtx_timeline <logs_path>
#
function evtx_timeline {
	LOGS_PATH="$1"
  echo "[+] creating windows evtx timeline" >&2
  evtx2bodyfile "$LOGS_PATH/"*.evtx | mactime2 -d | gzip -c - >evtx.csv.gz
}
###########################################################


WIN_MOUNT=`realpath "$1"`

if [ ! -d "$WIN_MOUNT" ]; then 
    echo "'$WIN_MOUNT' is not a directory" >&2
    exit 1
fi

SYSTEM="$(check_file "$WIN_MOUNT/Windows/System32/config/SYSTEM" true)"
SOFTWARE="$(check_file "$WIN_MOUNT/Windows/System32/config/SOFTWARE" true)"
SECURITY="$(check_file "$WIN_MOUNT/Windows/System32/config/SECURITY" true)"
#SYSCACHE="$(check_file "$WIN_MOUNT/Windows/System32/config/Syscache.hve" true)"
AMCACHE="$(check_file "$WIN_MOUNT/Windows/appcompat/Programs/Amcache.hve" false)"
if [ "x$AMCACHE" == "x" ]; then
    AMCACHE="$(check_file "$WIN_MOUNT/Windows/AppCompat/Programs/Amcache.hve" false)"
fi

host_info "$SYSTEM" "$SOFTWARE"

for F in "$SYSTEM" "$SOFTWARE" "$SECURITY"; do
    do_timeline "$F"
	registry_timeline "$F"
done

if [ "x$AMCACHE" != "x" ]; then
    do_timeline "$AMCACHE"
fi

if [ ! -d "$WIN_MOUNT/Users" ]; then
    echo "[-] no Users directory found" >&2
    exit 1
fi

while IFS= read -r D; do 
    USER=$(basename $D)
    USER_DIR=$(realpath "$D")
    echo "[+] found user '$USER'"

    NTUSER_DAT=$(check_file "$USER_DIR/NTUSER.DAT" false)
    USRCLASS_DAT=$(check_file "$USER_DIR/AppData/Local/Microsoft/Windows/UsrClass.dat" false)
    if [ "x$NTUSER_DAT" != "x" ]; then
        do_timeline "$NTUSER_DAT" "${USER}_ntuser"
		else
				echo "[-] missing file $NTUSER_DAT"
    fi
    if [ "x$USRCLASS_DAT" != "x" ]; then
        do_timeline "$USRCLASS_DAT" "${USER}_usrclass"
		else
		echo "[-] missing file $USRCLASS_DAT"
    fi

	copy_user_file "$USER" "$USER_DIR" "ConsoleHost_history.txt"

done < <(find "$WIN_MOUNT/Users" -maxdepth 1 -mindepth 1 -type d)

evtx_timeline "$WIN_MOUNT/Windows/System32/winevt/Logs"
