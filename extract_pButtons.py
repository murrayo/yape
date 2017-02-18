#!/usr/bin/env python3
"""Chop up key sections of pButtons and write to formatted .csv files.
    
Usage:
    
   extract_pButtons.py </pButtons/file/name>  
    
    Example: 
        extract_pButtons.py ./pB_test_24hours_30sec.html
        
    Changes:
        MO - replace / with _ in column headings. eg iostat
"""
import argparse
import sys
import csv
import os
import shutil


def get_section(SearchFileName, outputFileName, startString, endString, os_details):
    """Extracts blocks (eg vmstat). Trusts that pButtons has blocks of output between two key words.
    
    Args:
        SearchFileName: path and file name to search.
        outputFileName: output file name
        startString: tag to start extract
        endString: tag to start extract
        
        
    Output:
        Outputs text file of block of lines with context specific fomating.
    """ 
    with open(SearchFileName, mode='rt', encoding='ISO-8859-1') as infile, \
         open(outputFileName, mode='wt') as outfile:
        # Note: I had to use ISO-8859-1 encoding NOT std utf-8.  
        # I suspect characters from non-english, Thai for example. You can also try utf-8.
        
        copy = False
        for line in infile:
        
            if startString in line:
                copy = True
                
                if startString == 'beg_mgstat':
                    infile.readline() # skip first line of junk
                    
                if startString == 'beg_vmstat': # write header
                    if os_details == 'RH':
                        line = ' '.join(line.split()) + '\n' # strip leading and multiple spaces

                        headerLine = line.split('<pre> ',1)[1] # get right hand part of ugly line            
                        headerLine = ''.join(headerLine) # convert part to a string                              
                        headerLine = headerLine.split(' ') # split to change column headings
                        headerLine[0]='Date'
                        headerLine[1]='Time'
                    
                        outfile.write(' '.join(headerLine))
                    
                    if os_details == 'AIX':
                        line = ' '.join(line.split()) # strip leading and multiple spaces

                        headerLine = line.split('<pre> ',1)[1] # get right hand part of ugly line            
                        headerLine = ''.join(headerLine) # convert part to a string 
                        headerLine = headerLine.replace('sy','sy_call',1) # who thought duplicate column headings is a good idea?
                        headerLine = headerLine.replace('hr mi se','')
                        headerLine = headerLine + 'Time' + '\n'
                        headerLine = headerLine.split(' ')
                        
                        outfile.write(' '.join(headerLine))
    
                    else:
                        # TBD
                        pass
                                              
            elif endString in line:     
                if copy == True:
                    break             # only ever one block (even iostat)
                    # copy = False    # To make more generic with multiple blocks
                
            elif copy: 
                if startString == 'beg_mgstat':
                   line = line.replace(' ', '') # strip spaces
                if startString == 'beg_vmstat' or startString == 'id=iostat' :
                    line = ' '.join(line.split()) + '\n' # strip leading and multiple spaces
                
                outfile.write(line)
    

def csv_converter(infile, outfile):
    """
    Read input text file and write out to new csv file.
    """
    
    in_txt = csv.reader(open(infile, mode='rt'), delimiter = ' ')
    out_csv = csv.writer(open(outfile, mode='wt'))

    out_csv.writerows(in_txt)

    
def split_iostat(inputListFile, inputDataFile):
    """ 
    Split preprocessed iostat into one text file per disk.
    
    Args:
        inputListFile: file containing list of disks (first block of iostat).
        inputDataFile: full iostat file.
        
    Output:
        Writes a csv file for each disk.
    """
    
    csv_converter(inputListFile, 'list_iostat.csv')
    csv_converter(inputDataFile, 'all_iostat.csv')
    
    # For each disk write a separate output file
    with open('list_iostat.csv', mode='rt') as inlistfile:
        disklist = []
        
        for line in inlistfile:
            disklist.append(line.split(','))
        
        for disk in disklist:
            header = False   
            
            with open('all_iostat.csv', mode='rt') as indatafile, \
                 open('iostat_' + disk[0] + '.csv', mode='wt') as outfile:       
                
                for diskline in indatafile: 
                
                    if 'Device:' in diskline and header == False:
                        header = True
                        outfile.write(diskline) 
                               
                    if disk[0] in diskline:
                        outfile.write(diskline) 
    
    
def detect_pB_os(SearchFileName):
    """
    Detect OS from Caché version string.
    """
    
    with open(SearchFileName, mode='rt', encoding='ISO-8859-1') as infile:

        for line in infile:
        
            if 'Version String:' in line:
                
                if 'AIX' in line:
                    pB_os = 'AIX'
                elif 'Itanium' in line:  
                    pB_os = 'Itanium'
                elif 'AIX' in line:  
                    pB_os = 'AIX'
                elif 'Red Hat Enterprise Linux' in line:  
                    pB_os = 'RH'
                elif 'Windows' in line:
                    pB_os = 'Windows'
                else:            
                    pB_os = 'undefined'    
                    
                break             # bail
    
    return pB_os           
                  

def mainline(SearchFileName):

    """Step through pButtons file gathering blocks of text and processing.
    
    Args: 
        SearchFileName = path and name of pButtons file.
    
    Output: 
        outputs fomatted csv files for available pButtons sections.
    """

    # get os details   
    os_details = detect_pB_os(SearchFileName)
    
    # mgstat
    get_section(SearchFileName, 'mgstat.csv', 'beg_mgstat', 'end_mgstat', os_details)
    

    if os_details == 'RH':
    
        # vmstat - needs to be converted to csv
        get_section(SearchFileName, 'vmstat.txt', 'beg_vmstat', 'end_vmstat', os_details)
        csv_converter('vmstat.txt', 'vmstat.csv')
    
        # iostat is messy, strip down and separate by disk in several steps
        get_section(SearchFileName, 'iostat_tmp.txt', 'id=iostat', '#Topofpage', os_details)
        get_section('iostat_tmp.txt', 'iostat_list.txt', 'Device:', ':', os_details)   
        split_iostat('iostat_list.txt','iostat_tmp.txt')
    
        # sar is also messy, strip down and separate by disk in several steps
        get_section(SearchFileName, 'sar_tmp.txt', 'id=sar-d', 'Average:', os_details) 
        #To Do - homework ;)            
    
        # tidy up, comment for debugging
        os.remove('vmstat.txt')
        os.remove('iostat_list.txt')
        os.remove('iostat_tmp.txt')
        os.remove('sar_tmp.txt')
        os.remove('list_iostat.csv')    
    
    elif os_details == 'Windows':
        get_section(SearchFileName, 'win_perfmon.csv', 'beg_win_perfmon', 'end_win_perfmon', os_details)
    
    elif os_details == 'AIX':
        get_section(SearchFileName, 'vmstat.txt', 'beg_vmstat', 'end_vmstat', os_details)
        csv_converter('vmstat.txt', 'vmstat.csv')
        
        # AIX iostat is very messy, strip down and comma separate only
        get_section(SearchFileName, 'iostat_tmp.txt', 'id=iostat', '#Topofpage', os_details)
        csv_converter('iostat_tmp.txt', 'iostat_AIX.txt')
        os.remove('iostat_tmp.txt')
        
    
    else:
        # Still work to do on other OS's.
        print('Only mgstat supported on ' + os_details)
          
    
    # move csv files somewhere
    os.makedirs('./' + FILEPREFIX + 'metrics', exist_ok = True)

    for checkFile in ['vmstat.csv', 'mgstat.csv', 'win_perfmon.csv', 'iostat_AIX.txt']:
        if os.path.isfile(checkFile):
            os.rename(checkFile, './' + FILEPREFIX + 'metrics/' + checkFile)

    if os.path.isfile('all_iostat.csv'):
        os.remove('all_iostat.csv')
        
        files = os.listdir('.')
        for f in files:
            if (f.startswith('iostat_')):
                shutil.move(f, './' + FILEPREFIX + 'metrics/' + f)
    
                
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Extract useful metrics from pButtons to csv files')
    parser.add_argument("pButtons_file_name", help="Path and pButtons file name to extract")
    parser.add_argument("-p", "--prefix", help="add prefix string for output directory")
    args = parser.parse_args()
    
    
    if args.prefix is not None:
        FILEPREFIX = args.prefix
    else:
        FILEPREFIX = ''
 
    try:
        mainline(args.pButtons_file_name)
    except OSError as e:
        print('Could not process pButtons file because: {}'.format(str(e)))
    
