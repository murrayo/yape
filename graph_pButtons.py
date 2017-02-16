#!/usr/bin/env python3
"""Graph input files.
    
Usage:
    
    graph_pButtons.py </input/file/name.csv> <file_type> 
    
    Example: 
        graph_pButtons.py ./metrics/mgstat.csv mgstat
"""
import argparse
import sys
import os
import shutil


import math
import pandas as pd

import mpl_toolkits.axisartist as AA
from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

from datetime import datetime
from matplotlib.dates import DateFormatter


def parse_datetimeVM(x):
    '''
    Parses datetime from vmstat as:
        `[hour:minute:second]`
    '''
    dt = datetime.strptime(x, '%H:%M:%S')
        
    return dt
    
    
def parse_datetimeWin(x):
    '''
    Parses datetime from windows perfmon as:
        `[day/month-hour:minute:second.ms]`
        year will be messed up (1900)
    '''
    dt = datetime.strptime(x, '%m/%d/%Y%H:%M:%S.%f')
    
    return dt    
    
def parse_timeWin(x):
    '''
    Parses datetime from windows perfmon as:
        `[day/month-hour:minute:second.ms]`
        year will be messed up (1900)
    '''
    dt = datetime.strptime(x, '%H:%M:%S.%f')
    
    return dt    

def parse_windows_perfmon(CsvFullName):

    '''
    Lets make our life easier and tidy up windows perfmon file
    Windows is ugly. There seem to be several formats
    '''
    
    with open(CsvFullName, mode='rt') as infile, \
         open('temp_perfmon.csv', mode='wt') as outfile:
    
        HeaderLine = False
        for line in infile:
        
            line = line.replace('"', '') # strip quotes    
            line = line.replace(' ', '') # strip spaces 
            
            if HeaderLine == False:
                HeaderLine = True
            
                line = line.split(',') # split to change column headings
                
                # Work out if date time one field or two and any other format diff
                if line[1] != 'Time':
                
                    line[0]='DateTime'
                    
                    # strip Servername - Single back slash
                    ServerName=line[2]
                    elems = ServerName.split('\\')
                    ServerName =elems[2]
                     
                    line = ','.join(line)
                    line = line.replace('\\\\' + ServerName + '\\', '') 

                else:
                    line[0] ='Date'    
                
                    # Remove first leading slash
                    line = [cols.replace('\\', '',1) for cols in line]
                    # No Server name
                    line = ','.join(line)

            strLine = ''.join(line)
            strLine = line.replace(',,', ',0,') # #Blank field blows up matplotlib
                                                # Find better way
            
            outfile.write(strLine)


def plot_it(CsvFullName, CsvFileType, InterestingColumns, DateTimeIndexed, IndexColumn, data):
    ''' 
    Generic plotter
    '''
    
    for ColumnName in InterestingColumns:
    
        for graph_style in ['dots', 'lines']:

            plt.figure(num=None, figsize=(10,6), dpi=80, facecolor='w', edgecolor='dimgrey')
        
            if DateTimeIndexed == 'NoIndex':
                if graph_style == 'dots':
                    plt.plot(data[ColumnName], ".", markersize=2, color='dimgrey')
                else:    
                    plt.plot(data[ColumnName], color='dimgrey')
                    
            elif DateTimeIndexed == 'DateTimeIndexed' or DateTimeIndexed == 'WinDateTimeIndexed':
            
                if graph_style == 'dots':
                    plt.plot(data.DateTime, data[ColumnName], ".", markersize=2, color='dimgrey')
                else:    
                    plt.plot(data.DateTime, data[ColumnName], color='dimgrey')
 
            elif DateTimeIndexed == 'TimeIndexed' or DateTimeIndexed == 'WinTimeIndexed':
            
                if graph_style == 'dots':
                    plt.plot(data.Time, data[ColumnName], ".", markersize=2, color='dimgrey')
                else:    
                    plt.plot(data.Time, data[ColumnName], color='dimgrey')
 
 
            plt.grid()

            plt.title(ColumnName, fontsize=10)
            plt.xlabel("Time", fontsize=10)
            plt.tick_params(labelsize=8)
            #plt.title(ColumnName + " of %s" %(CsvFullName), fontsize=10)
            #plt.ylabel(ColumnName, fontsize=10)


            ax = plt.gca()
            ax.set_ylim(ymin=0) # Always zero start

            if '%' in ColumnName:
                ax.set_ylim(ymax=100)
            elif CsvFileType == 'vmstat' and ColumnName in 'us sy wa id':
                ax.set_ylim(ymax=100)
    
            ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

            plt.savefig(CsvFileType  + '_' + ColumnName.replace('/', '_') + '_' + graph_style + '.png')
            plt.close('all')
            
    
def graph_column(CsvFullName, CsvFileType, InterestingColumns, DateTimeIndexed, IndexColumn):
               
    if DateTimeIndexed == 'DateTimeIndexed':

        data = pd.read_csv(
            CsvFullName, 
            header=0,
            parse_dates=[[0,1]] # Combine columns 0 and 1 and parse as a single date column.
           )

        # data.info() # Debug
        data.columns=data.columns.str.strip()
        data=data.rename(columns={'Date_Time':'DateTime'})
        data.index=data.DateTime

    elif CsvFileType == 'win_perfmon' and DateTimeIndexed == 'WinDateTimeIndexed':
    
        data = pd.read_csv(
            CsvFullName, 
            header=0,
            converters={0: parse_datetimeWin}
           )
        
        data.columns=data.columns.str.strip()
        data.index=data.DateTime

    elif CsvFileType == 'win_perfmon' and DateTimeIndexed == 'WinTimeIndexed' :

        data = pd.read_csv(
            CsvFullName, 
            header=0,
            converters={1: parse_timeWin}
           )
        
        data.columns=data.columns.str.strip()
        data.index=data.Time
    
        
    elif DateTimeIndexed == 'TimeIndexed':

        data = pd.read_csv(
            CsvFullName, 
            header=0,
            converters={IndexColumn: parse_datetimeVM}
           )

        # data.info()
        data.columns=data.columns.str.strip()
        data.index=data.Time
        
    else:
    
        data = pd.read_csv(
            CsvFullName, 
            header=0
           )

        data.columns=data.columns.str.strip()
        
    plot_it(CsvFullName, CsvFileType, InterestingColumns, DateTimeIndexed, IndexColumn, data)
            
            
def GetColumnHeadings(CsvDirName, CsvFileType):
    ''' 
        Build the header column list and work out where the indexes are.
    '''

    DateTimeIndexed = 'NoIndex'
    IndexColumn = 0
    
    with open(CsvDirName, mode='rt') as infile:
        
        for line in infile:
            InterestingColumns = line.split(',')     
            break
            
    InterestingColumns[-1] = InterestingColumns[-1].strip()   # Remove new line   

    if  CsvFileType == 'win_perfmon' and InterestingColumns[0] == 'DateTime':
        DateTimeIndexed = 'WinDateTimeIndexed'
        IndexColumn = 0 
        InterestingColumns.remove('DateTime') 

    elif CsvFileType == 'win_perfmon' and InterestingColumns[0] == 'Date':
        DateTimeIndexed = 'WinTimeIndexed'
        IndexColumn = 0 
        InterestingColumns.remove('Date')
        InterestingColumns.remove('Time')
        
    elif 'Date' in InterestingColumns[0] and 'Time' in InterestingColumns[1]:
        DateTimeIndexed = 'DateTimeIndexed'
        IndexColumn = 0
        InterestingColumns.remove('Date')
        InterestingColumns.remove('Time')

    elif 'Time' in InterestingColumns:      # No date but time is somewhere, eg. vmstat
        DateTimeIndexed = 'TimeIndexed'
        IndexColumn = InterestingColumns.index('Time')
        InterestingColumns.remove('Time')
        
    if 'Device:' in line :                  # eg. iostat
        InterestingColumns.remove('Device:')
 
    return InterestingColumns, DateTimeIndexed, IndexColumn


def mainline(CsvDirName, Csvkitchen_sink, DoNotIostat, BokehSample, filePrefix):

    """Chart input file.
    
    Args: 
        CsvDirName  = path for csv files.
        Csvkitchen_sink   = if True only print key metrics
        DoNotIostat = do not process iostat
    
    Output: 
        outputs graphs for csv columns
    """
    
    print('Prefix: ' + filePrefix)
        
    files = os.listdir(CsvDirName)
    
    for csvFilename in files:
    
        if DoNotIostat and 'iostat' in os.path.basename(csvFilename):
            pass
            
        else:
            if os.path.basename(csvFilename).split('.')[1] == 'csv' :
                print('Charting: ' + csvFilename)
            
                CsvFileType = os.path.basename(csvFilename).split('.')[0]
                fullName = CsvDirName + '/' + csvFilename
  
                if CsvFileType == 'win_perfmon' :       # Windows needs clean up
                    parse_windows_perfmon(fullName)
                    fullName = 'temp_perfmon.csv'

                # Get column headers and decide if indexed    
                InterestingColumns,  DateTimeIndexed, IndexColumn = GetColumnHeadings(fullName, CsvFileType)

                # Bokeh experiment
                if BokehSample:  
                    pass
    
                if not Csvkitchen_sink:                    
                    if CsvFileType == 'mgstat' :
                        InterestingColumns = ['Glorefs', 'RemGrefs', 'PhyRds', 'Rdratio', 'Gloupds', 'RouLaS', 'PhyWrs', 'WDQsz', \
                                              'WDphase', 'Jrnwrts', 'BytSnt', 'BytRcd', 'WIJwri', 'RouCMs', 'Rourefs', 'WDtmpq']
                    elif CsvFileType == 'vmstat' :
                        InterestingColumns = ['r','b','us','sy','id','wa']
                    elif CsvFileType == 'win_perfmon' :
                        InterestingColumns = [  'Processor(_Total)\%PrivilegedTime', \
                                                'Processor(_Total)\%UserTime',\
                                                'Processor(_Total)\%ProcessorTime',\
                                                'Processor(_Total)\Interrupts/sec',\
                                                'Memory\AvailableMBytes',\
                                                'Memory\PageReads/sec',\
                                                'Memory\PageWrites/sec',\
                                                'PagingFile(_Total)\%Usage',\
                                                'PhysicalDisk(_Total)\DiskTransfers/sec',\
                                                'System\Processes',\
                                                'System\ProcessorQueueLength']
                                                
                graph_column(fullName, CsvFileType, InterestingColumns, DateTimeIndexed, IndexColumn)


                # move files to new home
                os.makedirs('./charts', exist_ok = True)

                iostatMade  = False
                mgstatMade  = False
                vmstatMade  = False
                perfmonMade = False
            
                files = os.listdir('.')
                for pngFilename in files:
                    if (pngFilename.endswith('.png')):
                
                        if (pngFilename.startswith('iostat_')) :
                            if not iostatMade:
                                iostatMade = True
                                os.makedirs('./charts/iostat', exist_ok = True)
                            shutil.move(pngFilename, './charts/iostat/' + pngFilename)  
                        elif (pngFilename.startswith('mgstat_')) :
                            if not mgstatMade:
                                mgstatMade = True
                                os.makedirs('./charts/mgstat', exist_ok = True)
                            shutil.move(pngFilename, './charts/mgstat/' + pngFilename)                                
                        elif (pngFilename.startswith('vmstat_')) :
                            if not vmstatMade:
                                vmstatMade = True
                                os.makedirs('./charts/vmstat', exist_ok = True)
                            shutil.move(pngFilename, './charts/vmstat/' + pngFilename)        
                        elif (pngFilename.startswith('win_perfmon_')) :
                            if not perfmonMade:
                                perfmonMade = True
                                os.makedirs('./charts/win_perfmon', exist_ok = True)
                            shutil.move(pngFilename, './charts/win_perfmon/' + pngFilename)        
                        else:        
                            shutil.move(pngFilename, './charts/' + pngFilename)
                
                if os.path.isfile('temp_perfmon.csv'):
                    os.remove('temp_perfmon.csv')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Graph metrics from pButtons csv files')
    parser.add_argument("csv_dir_name", help="Path to directory containing .csv files to chart")
    parser.add_argument("-k", "--kitchen_sink", help="Kitchen sink mode, ALL columns will be charted", action="store_true")
    parser.add_argument("-I", "--Iostat", help="Do NOT process iostat if exists", action="store_true")
    parser.add_argument("-B", "--Bokeh", help="Charts interactive using Bokeh", action="store_true")
    args = parser.parse_args()
 
    try:
        mainline(args.csv_dir_name, args.kitchen_sink, args.Iostat, args.Bokeh, args.prefix)
    except OSError as e:
        print('Could not process csv file because: {}'.format(str(e)))
    
