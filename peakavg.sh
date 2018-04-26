#!/bin/sh
# Usage: ./peakavg.sh -d  "../ZCust/Lothian/2015_04/pButtonsOnlyAll/APP1" -m -v
# Beware spaces in file path
# 

# 3 Sigma Peak Peak is where top ~1% are dropped as outliers
# Set for 99.7% (3 sigma)
CutOff=".997"
# Set for 09: start (mgstat - measured during Peak activity)
TimeStart="09:"
# Set for 10:59 Stop 
TimeEnd="11:"


Usage="Usage: $0 [-v] [-m] [-a] [-x] -d directory ... \n\tselect one or more of -d directory_to_work_on -[v]mstat -ai[x] -[m]gstat -[a]ll times"

while getopts d:vmax o
do	case "$o" in
	d)  InputFolder="$OPTARG" ;;
	v)	vmstat="Y";;
	m)	mgstat="Y";;
	a)  allTimes="Y";;
	x)  aix="Y";;
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
	echo $InputFolder is not a known directory
	echo $Usage
	exit 1
fi

if [ ! -z $vmstat ] && [ ! -z $aix ] ;
then
	echo "Hey - you can't be Linux and AIX! Pick -x or -v"
	echo $Usage
	exit 1
fi
	

# Where are we now folder
CurrentFolder=`pwd`
cd $InputFolder

myname=`basename "${InputFolder}"`
foldername=`dirname "${InputFolder}"`
foldername=`basename "${foldername}"`

echo "Foldername: ${foldername}"
echo "My Name: ${myname}"


# if mgstat to be processed
#   1     2     3        4         5         6       7        8        9         10       11         12       13      14         15      16      17        18       19       20    ...[30]
# Date, Time, Glorefs, RemGrefs, GRratio,  PhyRds, Rdratio, Gloupds, RemGupds, Rourefs, RemRrefs,  RouLaS, RemRLaS,  PhyWrs,   WDQsz,  WDtmpq, WDphase,  WIJwri,  RouCMs, Jrnwrts, ...[IOPS], ...ActECP,  Addblk, PrgBufL, PrgSrvR,  BytSnt,  BytRcd,  WDpass,  IJUcnt, IJULock

if [ ! -z $mgstat ];
then

	# Output
	outfile="../../3_Sigma_PeakPeak_mgstat.csv"
	if [ ! -f $outfile ]
	then
		printf "Directory,Range,File name,3 Sigma Peak  Glorefs,3 Sigma Peak RemGrefs,3 Sigma Peak PhyRds,3 Sigma Rdratio,3 Sigma Peak GloUpds,3 Sigma Rourefs,3 Sigma Peak WIJwri,3 Sigma Peak Jrnwrts,3 Sigma Peak PhyWrs,3 Sigma Peak IOPS (est)" > $outfile
		printf ",ABS PEAK-->,Peak  Glorefs,Peak RemGrefs,Peak PhyRds,Peak Rdratio,Peak GloUpds,Peak Rourefs,Peak WIJwri,Peak Jrnwrts,Peak PhyWrs,Peak IOPS (est)" >> $outfile
		printf ",AVERAGE-->,Average  Glorefs,Average RemGrefs,Average PhyRds,Average Rdratio,Average GloUpds,Average Rourefs,Average WIJwri,Average Jrnwrts,Average PhyWrs (>0 only),Average IOPS (est)" >> $outfile
		printf "\r\n" >>$outfile
	else
		echo "Appending to end of existing $outfile"
	fi
		
	for infile in `ls mgstat.csv`
	do 

		# Print original file name
		echo "--------------------------------------"
		echo "$infile"
		iopsName="$infile"_iops.csv
		
	    printf "${myname}," >>$outfile
		
		if [ ! -z $allTimes ];
		then
			printf "All Times," >>$outfile					
			cp $infile temp.txt
		else		
			# Select only Peak hours 09:00-10:59
			printf "${TimeStart} to ${TimeEnd}," >>$outfile	
			sed -n -e '/, '${TimeStart}'/,/, '${TimeEnd}'/p' $infile >temp.txt
		fi

	    printf "${infile}" >>$outfile

		infile="temp.txt"
		
		# Add Total ESTIMATED IOPS as last field
		# Caché IOPS is estimated = PhyRds 6 + PhyWrs 14 + WIJWri 18 + (Jrnwrts 20 * 2)
		
		awk -F"," 'BEGIN { OFS = "," } {$30=$6+$14+$18+$20+$20; print}' temp.txt > $iopsName; cp $iopsName temp.txt
		
		# How many lines in mgstat now
		totalLines=1
		totalLines=`wc -l < ${infile}`
		
		# Remove last line (11:00:nn)
		head -n $((totalLines-1)) temp.txt > temp1.txt; mv temp1.txt temp.txt
		totalLines=`wc -l < ${infile}`
		echo "mgstat total lines: " $totalLines 

		
		# Where is the 3 sigma cut off? Need to get maximum from top and bottom
		SigmaCnt=1
		SigmaCnt=`printf "%.0f" $(echo "scale=2;($totalLines-($totalLines*${CutOff}))" | bc)`
		echo "mgstat take off n: " $SigmaCnt
		
		# How many without 3 sigma
		Remainder=$(($totalLines-$SigmaCnt))
		echo "Remainder lines : " $Remainder
		
		# How many off top and bottom
		takeOff=$((SigmaCnt/2))
		echo "Take off top and take off bottom: " $takeOff
		
		#--- Sort and print 3 Sigma Peak Peak
		for fieldNo in 3 4 6 7 8 10 18 20 14 30 
		do 
			# Create temp file containing only data between Sigma
			printf "," >>$outfile
			theCell=`sort -g -r -t, -k${fieldNo} ${infile} | head -$(($totalLines-$takeOff)) | tail -$(((totalLines-$takeOff)-$takeOff)) | head -1 | cut -f${fieldNo} -d,`
			printf "$theCell" >>$outfile
		done
		
		printf "," >>$outfile
		#--- Sort and print true Peak
		for fieldNo in 3 4 6 7 8 10 18 20 14 30
		do 
			printf "," >>$outfile
			theCell=`sort -g -r -t, -k${fieldNo} ${infile} | head -1 | cut -f${fieldNo} -d,`
			printf "$theCell" >>$outfile			
		done
		

		printf "," >>$outfile	
		# Now for Average - need to loose top and bottom for 3 sigma again
		for fieldNo in 3 4 6 7 8 10 18 20
		do 
			printf "," >>$outfile
			printf "`sort -g -r -t, -k${fieldNo} ${infile} | head -$(($totalLines-$takeOff)) | tail -$(((totalLines-$takeOff)-$takeOff))`" >ztempa.csv
			theCell=`awk -F ',' '{ total += $'$fieldNo'; count++ } END { printf "%d", total/count }' ztempa.csv`
			printf "$theCell" >>$outfile
		done

		# PhyWrs, 14 is special - Only want non-zero lines
		for fieldNo in 14
		do 
			printf "," >>$outfile
			printf "`sort -g -r -t, -k${fieldNo} ${infile} | head -$(($totalLines-$takeOff)) | tail -$(((totalLines-$takeOff)-$takeOff))`" >ztempw.csv
			theCell=`awk -F ',' ' $'$fieldNo' { total += $'$fieldNo'; count++ } END { printf "%d", total/count }' ztempw.csv`
			printf "$theCell" >>$outfile			
		done

		for fieldNo in 30
		do 
			printf "," >>$outfile
			printf "`sort -g -r -t, -k${fieldNo} ${infile} | head -$(($totalLines-$takeOff)) | tail -$(((totalLines-$takeOff)-$takeOff))`" >ztempa.csv
			theCell=`awk -F ',' '{ total += $'$fieldNo'; count++ } END { printf "%d", total/count }' ztempa.csv`
			printf "$theCell" >>$outfile
		done

		printf "\r\n" >>$outfile
		
	done	
	
	echo $outfile " ready"

	rm temp.txt
    rm ztempa.csv
    rm ztempw.csv


fi


# if vmstat to be processed

#     1        2     3  4     5     6       7     8      9   10    11    12   13   14 15 16 17 18 19 [20]
# 03/30/15 00:01:00  r  b   swpd   free   buff  cache   si   so    bi    bo   in   cs us sy id wa st [Ttl CPU]

if [ ! -z $vmstat ];
then

	# Output
	outfile="../../3_Sigma_PeakPeak_vmstat.csv"
	
	if [ ! -f $outfile ]
	then
		printf "Directory,Range,File name,3 Sigma Peak r,3 Sigma Peak b,3 Sigma Peak us,3 Sigma Peak sy,3 Sigma Peak id,3 Sigma Peak wa,3 Sigma Peak Ttl CPU" > $outfile
		printf ",ABS PEAK-->,Peak r,Peak b,Peak us,Peak sy,Peak id,Peak wa,Peak Ttl CPU" >> $outfile
		printf ",AVERAGE-->,Average r,Average b,Average us,Average sy,Average id,Average wa,Average Ttl CPU" >> $outfile
		printf "\r\n" >>$outfile
	else
		echo "Appending to end of existing $outfile"
	fi

	for infile in `ls vmstat.csv`
	do 
		
		# Print original file name
		echo "--------------------------------------"
		echo "$infile"
		cpuName="$infile"_cpu.csv
				
	    printf "${myname}," >>$outfile
		
		if [ ! -z $allTimes ];
		then
			printf "All Times," >>$outfile					
			cp $infile temp.txt
		else		
			# Select only Peak hours 09:00-10:59
			printf "${TimeStart} to ${TimeEnd}," >>$outfile	
			sed -n -e '/,'${TimeStart}'/,/,'${TimeEnd}'/p' $infile >temp.txt
		fi

	    printf "${infile}" >>$outfile

		infile="temp.txt"
		
		# Add Total CPU as last field
		awk -F"," 'BEGIN { OFS = "," } {$20=100-$17; print}' temp.txt > $cpuName; cp $cpuName temp.txt

						
		# How many lines in vmstat now
		totalLines=1
		totalLines=`wc -l < ${infile}`
		
		# Remove last line (11:00:nn)
		head -n $((totalLines-1)) temp.txt > temp1.txt; mv temp1.txt temp.txt
		totalLines=`wc -l < ${infile}`
		echo "vmstat total lines: " $totalLines 

		
		# Where is the 3 sigma cut off? Need to get maximum from top and bottom
		SigmaCnt=1
		SigmaCnt=`printf "%.0f" $(echo "scale=2;($totalLines-($totalLines*${CutOff}))" | bc)`
		echo "vmstat take off n: " $SigmaCnt
		
		# How many without 3 sigma
		Remainder=$(($totalLines-$SigmaCnt))
		echo "Remainder lines : " $Remainder
		
		# How many off top and bottom
		takeOff=$((SigmaCnt/2))
		echo "Take off top and take off bottom: " $takeOff
		

		#--- Sort and print 3 Sigma Peak Peak
		for fieldNo in 3 4 15 16 17 18 20
		do 
			# Create temp file containing only data between Sigma
			printf "," >>$outfile
			printf "`sort -g -r -t, -k${fieldNo} ${infile} | head -$(($totalLines-$takeOff)) | tail -$(((totalLines-$takeOff)-$takeOff)) | head -1 | cut -f${fieldNo} -d,`" >>$outfile
		done

	    printf "," >>$outfile
		#--- Sort and print true Peak
		for fieldNo in 3 4 15 16 17 18 20
		do 
			printf "," >>$outfile
			printf "`sort -g -r -t, -k${fieldNo} ${infile} | head -1 | cut -f${fieldNo} -d,`" >>$outfile
		done

		printf "," >>$outfile
		# Now for Average - need to loose top and bottom for 3 sigma again
		for fieldNo in 3 4 15 16 17 18 20
		do 
			printf "," >>$outfile
			printf "`sort -g -r -t, -k${fieldNo} ${infile} | head -$(($totalLines-$takeOff)) | tail -$(((totalLines-$takeOff)-$takeOff))`" >ztempa.csv
			awk -F ',' '{ total += $'$fieldNo'; count++ } END { printf "%d", total/count }' ztempa.csv >>$outfile
		done

		printf "\r\n" >>$outfile
		
	done	
	
	echo $outfile " ready"

	rm temp.txt
    rm ztempa.csv

fi

# if AIX vmstat to be processed

#  1  2    3      4     5  6  7  8  9   10  11   12    13    14 15 16 17 18 19 20 [21]
#  r  b   avm    fre    re pi po fr sr  cy  in   sy    cs    us sy id wa hr mi se [Ttl CPU]
#  1, 0,11070002,478444,0, 0, 0, 0, 0,  0,  4635,47237,15682,6, 2, 88,5, 00:01:16


if [ ! -z $aix ];
then

	# Output
	outfile="../../3_Sigma_PeakPeak_vmstat_aix.csv"
	
	if [ ! -f $outfile ]
	then
		printf "Directory,Range,File name,3 Sigma Peak r,3 Sigma Peak b,3 Sigma Peak us,3 Sigma Peak sy,3 Sigma Peak id,3 Sigma Peak wa,3 Sigma Peak Ttl CPU" > $outfile
		printf ",ABS PEAK-->,Peak r,Peak b,Peak us,Peak sy,Peak id,Peak wa,Peak Ttl CPU" >> $outfile
		printf ",AVERAGE-->,Average r,Average b,Average us,Average sy,Average id,Average wa,Average Ttl CPU" >> $outfile
		printf "\r\n" >>$outfile
	else
		echo "Appending to end of existing $outfile"
	fi

	for infile in `ls vmstat.csv`
	do 
	
		# Print original file name
		echo "--------------------------------------"
		echo "$infile"
		echo "All time? ${allTimes}"
		echo "--------------------------------------"
		
		cpuName="$infile"_cpu_aix.csv
				
	    printf "${myname}," >>$outfile
		
		if [ ! -z $allTimes ];
		then
			printf "All Times," >>$outfile					
			cp $infile temp.txt
		else		
			# Select only Peak hours 09:00-10:59
			printf "${TimeStart} to ${TimeEnd}," >>$outfile	
			sed -n -e '/,'${TimeStart}'/,/,'${TimeEnd}'/p' $infile >temp.txt
		fi
		
	    printf "${infile}" >>$outfile

		infile="temp.txt"
		
		# Add Total CPU as last field
		awk -F"," 'BEGIN { OFS = "," } {$21=100-$16; print}' temp.txt > $cpuName; cp $cpuName temp.txt

						
		# How many lines in vmstat now
		totalLines=1
		totalLines=`wc -l < ${infile}`
		
		# Remove last line (11:00:nn)
		head -n $((totalLines-1)) temp.txt > temp1.txt; mv temp1.txt temp.txt
		totalLines=`wc -l < ${infile}`
		echo "vmstat total lines: " $totalLines 

		
		# Where is the 3 sigma cut off? Need to get maximum from top and bottom
		SigmaCnt=1
		SigmaCnt=`printf "%.0f" $(echo "scale=2;($totalLines-($totalLines*${CutOff}))" | bc)`
		echo "vmstat take off n: " $SigmaCnt
		
		# How many without 3 sigma
		Remainder=$(($totalLines-$SigmaCnt))
		echo "Remainder lines : " $Remainder
		
		# How many off top and bottom
		takeOff=$((SigmaCnt/2))
		echo "Take off top and take off bottom: " $takeOff
		

		#--- Sort and print 3 Sigma Peak Peak
		for fieldNo in 1 2 14 15 16 17 21
		do 
			# Create temp file containing only data between Sigma
			printf "," >>$outfile
			printf "`sort -g -r -t, -k${fieldNo} ${infile} | head -$(($totalLines-$takeOff)) | tail -$(((totalLines-$takeOff)-$takeOff)) | head -1 | cut -f${fieldNo} -d,`" >>$outfile
		done

	    printf "," >>$outfile
		#--- Sort and print true Peak
		for fieldNo in 1 2 14 15 16 17 21
		do 
			printf "," >>$outfile
			printf "`sort -g -r -t, -k${fieldNo} ${infile} | head -1 | cut -f${fieldNo} -d,`" >>$outfile
		done

		printf "," >>$outfile
		# Now for Average - need to loose top and bottom for 3 sigma again
		for fieldNo in 1 2 14 15 16 17 21
		do 
			printf "," >>$outfile
			printf "`sort -g -r -t, -k${fieldNo} ${infile} | head -$(($totalLines-$takeOff)) | tail -$(((totalLines-$takeOff)-$takeOff))`" >ztempa.csv
			awk -F ',' '{ total += $'$fieldNo'; count++ } END { printf "%d", total/count }' ztempa.csv >>$outfile
		done

		printf "\r\n" >>$outfile
		
	done	
	
	echo $outfile " ready"

	rm temp.txt
    rm ztempa.csv

fi

cd "$CurrentFolder"

	
		









