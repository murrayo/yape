#!/bin/sh

# This script loops through multiple subdirectories to create graphs
# Useful for benchmarks especially but also where customer data has multiple servers, also with the option of sorting and displaying top 10 websys.Monitor components based on response time

# Usage:    /Users/moldfiel/zISC/600_Tools/pButtonsTools/yape/benchy.sh -gbw 

# Beware spaces in file path

# 0. Extract mgstat, vmstat, perfmon, iostat from pButtons
# 1. Build graphs
# 2. Build csv of peaks and averages
# 3. Find average of top 10 average response times in websys.Monitor

Usage="Usage: $0 [-g] [-s] [-w] [-p] [-b] [-k] [-i \"disk list\"]... \n\tselect one or more of -[g]raphs -[s]napshots -[w]ebsys.Monitor -[b]enchmark -[k]itchen sink"

while getopts i:gswbk o
do	case "$o" in
	g)	graphs="Y";;
	s)  snapshot="Y";;	
	w)	websys="Y";;
	b)  benchmark="Y";;
	k)  kitchen_sink="Y";;
	i)  intreasting_disks="$OPTARG" ;;
	[?])	echo 
	exit 1;;
	esac
done


# Where are we now folder
CurrentFolder=`pwd`

echo "Current: ${CurrentFolder}"


# Get sub directory names

Filelist=`find . -maxdepth 1 -type d -name [^\.]\* | sed 's:^\./::' | sort`

echo ${Filelist}

Looped="N"

for j in ${Filelist}
do
	
	if [ $j != "hold" ] 
	then	
		cd $j
		ls *.html
		
		# Extract mgstat, vmstat, perfmon, iostat from pButtons
		
		for i in `ls *.html`; do /Users/moldfiel/zISC/600_Tools/pButtonsTools/yape/extract_pButtons.py $i -p ${i}_; done
		

		# Create graphs
				
		if [ ! -z $graphs ];
		then
			if [ ! -z $kitchen_sink ];
			then
				for i in `ls *.html`; do /Users/moldfiel/zISC/600_Tools/pButtonsTools/yape/graph_pButtons.py ./${i}_metrics -p line_${i}_ -s line -t ${i} -k; done
				for i in `ls *.html`; do /Users/moldfiel/zISC/600_Tools/pButtonsTools/yape/graph_pButtons.py ./${i}_metrics -p dot_${i}_ -s dot -t ${i} -k; done
				for i in `ls *.html`; do /Users/moldfiel/zISC/600_Tools/pButtonsTools/yape/graph_pButtons.py ./${i}_metrics -p interactive_${i}_ -s interactive -t ${i} -k; done	
			
			else		
				for i in `ls *.html`; do /Users/moldfiel/zISC/600_Tools/pButtonsTools/yape/graph_pButtons.py ./${i}_metrics -p line_${i}_ -s line -t ${i} -I; done
				for i in `ls *.html`; do /Users/moldfiel/zISC/600_Tools/pButtonsTools/yape/graph_pButtons.py ./${i}_metrics -p dot_${i}_ -s dot -t ${i} -I; done
				for i in `ls *.html`; do /Users/moldfiel/zISC/600_Tools/pButtonsTools/yape/graph_pButtons.py ./${i}_metrics -p interactive_${i}_ -s interactive -t ${i} -I; done	
			fi			
		fi
		
		if [ -n "${intreasting_disks}" ]; then

    		echo "Making list of disks ${intreasting_disks}"
			i_am_now_at=`pwd`

			for l in line dot interactive; do	
						
				mkdir -p ${l}_${i}_charts/intreasting_disks

				cd ${l}_${i}_charts/iostat
				
				for m in ${intreasting_disks}; do
					cp iostat_${m}* ../intreasting_disks
				done
				
				cd ${i_am_now_at}
			done	
				
		fi
		
		
		# Get mgstat and vmstat peaks and averages

		if [ ! -z $benchmark ];
	    then	
	    
	    	if [ ! -z $snapshot ];
	    	then
				for i in `ls *.html`; do echo ${i}_metrics; /Users/moldfiel/zISC/600_Tools/pButtonsTools/yape/peakavg.sh -d ./${i}_metrics -mv; done
			else
				for i in `ls *.html`; do echo ${i}_metrics; /Users/moldfiel/zISC/600_Tools/pButtonsTools/yape/peakavg.sh -d ./${i}_metrics -mva; done
			fi				

			# Find average of top 10 average response times in websys.Monitor, eg 10 'worst performing' components
			if [ ! -z $websys ];
			then

				csvfile=`ls *websysMonitor.csv`
				
				if [ -n "$csvfile" ]; then
		
					ztempname="tmp_$csvfile"			
					csvoutfile="../csvtop10.csv"		
		
					# sort csv file

					sort -g -r -t, -k4 ${csvfile} >$ztempname

					head -10 $ztempname | cut -f4 -d, >${ztempname}_zzzcsvtemp.txt

					awk '{ sum += $1 } END { if (NR > 0) printf "%.4f\n", sum / NR }' ${ztempname}_zzzcsvtemp.txt > ${csvfile}.top10Avg.txt

					printf "${j}," >>"${csvoutfile}"
					awk '{ sum += $1 } END { if (NR > 0) printf "%.4f\n", sum / NR }' ${ztempname}_zzzcsvtemp.txt >>"${csvoutfile}"

					rm -rf ${ztempname} ${ztempname}_zzzcsvtemp.txt
				else
					echo "No websysMonitor.csv"
				fi		
			fi
		fi	

		cd ..	
	else
		echo "Skipping hold dir"
	fi



		
done
	
#cat "${outfile}"
#cat zzzoutfiles/zzzlist.txt

#cat "${csvoutfile}"





