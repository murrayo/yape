#!/bin/sh

# This script loops through multiple pButtons html files (eg a weeks worth) to create a single graph

# Usage:    ./yape_week.sh -d ../ZCust/201705/pButtons/xyz_server -I -v

# Beware spaces in file path


YAPE_PATH="/Users/moldfiel/zISC/600_Tools/pButtonsTools/yape"

line=""
dot=""
interactive=""
kitchen=""

Usage="Usage: $0 [-g] [-a] [-s] [-w] [-v] [-p] [-b] -d directory ... \n\t -d directory_to_work_on -[L]ine -[D]ot -[I]interactive -[v]mstat -[p]erfmon -[i]ostats -[k]itchen\n"

while getopts d:LDIvpik o
do	case "$o" in
	d)  InputFolder="$OPTARG" ;;
	L)	line="line";;
	D)  dot="dot";;
	I)  interactive="interactive";;	
	p)  perfmon="Y";;
	v)  vmstat="Y";;
	i)  iostats="Y";;
	k)  kitchen=" -k ";;
	[?])	echo 
	exit 1;;
	esac
done

# Basic validation

if [ -z $InputFolder ];
then
	echo $Usage
	exit 1
fi
	
if [ ! -d $InputFolder ];
then
	echo "\n${InputFolder} is not a known directory\n"
	echo $Usage
	exit 1
fi

CHART_TYPES="${line}${dot}${interactive}"
if [ "${CHART_TYPES}" == "" ];
then
	echo "\nEnter at least one chart type\n"
	echo $Usage
	exit 1    
else
    CHART_TYPES="${line} ${dot} ${interactive}"
    echo "Charting: ${CHART_TYPES}"
fi

# Where are we now folder
CurrentFolder=`pwd`


# Change to input directory and extract metrics for each pButtons file

cd "${InputFolder}"
for i in `ls *.html`; do ${YAPE_PATH}/extract_pButtons.py $i -p ${i}_; done

LAST_FILE=$i

# Create a consolidated metrics .csv file

mkdir all_days

>all_days/all_mg_inc_headers.txt
>all_days/mgstat.csv

for i in `find . -name mgstat.csv`; do cat $i >>all_days/all_mg_inc_headers.txt; done
sed '2,${/^Date/d;}' all_days/all_mg_inc_headers.txt >all_days/mgstat.csv


if [ "${vmstat}" == "Y" ];
then
    >all_days/all_vm_inc_headers.txt
    >all_days/vmstat.csv
    
    for i in `find . -name vmstat.csv`; do cat $i >>all_days/all_vm_inc_headers.txt; done
    sed '2,${/^Date/d;}' all_days/all_vm_inc_headers.txt >all_days/vmstat.csv
    
    # AIX will not display a week because it has no dates, need to somehow add dates
    #sed -i '/^$/d' all_days/all_vm_inc_headers.txt
    #sed '2,${/^r/d;}' all_days/all_vm_inc_headers.txt >all_days/vmstat.csv

    
fi

if [ "${perfmon}" == "Y" ];
then
    >all_days/all_wp_inc_headers.txt
    >all_days/win_perfmon.csv
    
    for i in `find . -name win_perfmon.csv`; do cat $i >>all_days/all_wp_inc_headers.txt; done
    sed '2,${/Memory/d;}' all_days/all_wp_inc_headers.txt >all_days/win_perfmon.csv
fi


if [ "${iostats}" == "Y" ];
then
    echo "\n\t --iostat not supported yet \n"
fi

    for j in ${CHART_TYPES}; do ${YAPE_PATH}/graph_pButtons.py all_days -p ${j}_ -s ${j} -t "Last_Day_${LAST_FILE}" -I ${kitchen}; done


cd "${CurrentFolder}"


