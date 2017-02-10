#!/usr/bin/env python3
"""Graph input file.
    
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

from datetime import datetime
from matplotlib.dates import DateFormatter


def graph_column(CsvFileName, InterestingColumns):

    file_prefix = (os.path.basename(CsvFileName)).split('.')[0]

    data = pd.read_csv(
        CsvFileName, 
        header=0,
        parse_dates=[[0,1]]
       )

    data.info()

    data.columns=data.columns.str.strip()
    data=data.rename(columns={'Date_Time':'DateTime'})

    data.index=data.DateTime
    
    for ColumnName in InterestingColumns:
        print(ColumnName)
        
        for graph_style in ['dots', 'lines']:
    
            plt.figure(num=None, figsize=(10,6), dpi=80, facecolor='w', edgecolor='dimgrey')
            
            if graph_style == 'dots':
                plt.plot(data.DateTime, data[ColumnName], ".", markersize=2, color='dimgrey')
            else:    
                plt.plot(data.DateTime, data[ColumnName], color='dimgrey')
            
            plt.grid()
    
            plt.title(ColumnName + " of %s" %(CsvFileName), fontsize=10)
            plt.ylabel(ColumnName, fontsize=10)
        
            plt.xlabel("Time", fontsize=10)

            ax = plt.gca()
            ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

            #plt.show()
            plt.savefig(file_prefix  + '_' + ColumnName + '_' + graph_style + '.png')
            plt.close('all')

def mainline(CsvFileName, CsvFileType):

    """Chart input file.
    
    Args: 
        CsvFileName = path and name of csv file.
    
    Output: 
        outputs graphs files for specific columns.
    """
    
    if CsvFileType == "mgstat" :
        InterestingColumns = ['Glorefs', 'RemGrefs', 'PhyRds', 'Rdratio', 'Gloupds', 'RouLaS', 'PhyWrs', 'WDQsz', 'WDphase', 'Jrnwrts', 'BytSnt', 'BytRcd', 'WIJwri', 'RouCMs', 'Rourefs', 'WDtmpq']
    elif CsvFileType == "vmstat" :
        InterestingColumns = ['r','b','swpd','free','us','sy','id','wa']
    else:
        pass
    
    graph_column(CsvFileName, InterestingColumns)

    
    # move files somewhere
    os.makedirs('./charts', exist_ok = True)

    files = os.listdir('.')
    for f in files:
        if (f.endswith('.png')):
            shutil.move(f, './charts/' + f)

    

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Graph metrics from pButtons csv files')
    parser.add_argument("csv_file_name", help="Path and csv file name to graph")
    parser.add_argument("csv_file_type", help="File type, e.g. mgstat or vmstat")
    args = parser.parse_args()
 
    try:
        mainline(args.csv_file_name, args.csv_file_type)
    except OSError as e:
        print('Could not process csv file because: {}'.format(str(e)))
    
