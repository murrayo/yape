#!/usr/bin/env python3
"""Graph input files.

"""
import argparse
import sys
import os
import shutil


import math
import numpy as np
import pandas as pd

from mpl_toolkits.axes_grid1 import host_subplot
import matplotlib.pyplot as plt
import matplotlib.ticker as tick

from datetime import datetime
from matplotlib.dates import DateFormatter, HourLocator

from bokeh.plotting import figure, output_file, show, save
from bokeh.models import NumeralTickFormatter, DatetimeTickFormatter, Range1d, LinearAxis
from bokeh.palettes import magma


def parse_datetimeVM(x):
    """
    Parses datetime from vmstat as:
        `[hour:minute:second]`
    """
    dt = datetime.strptime(x, '%H:%M:%S')
        
    return dt
    
    
def parse_datetimeWin(x):
    """
    Parses datetime from windows perfmon as:
        `[day/month-hour:minute:second.ms]`
        year will be messed up (1900)
    """
    dt = datetime.strptime(x, '%m/%d/%Y%H:%M:%S.%f')
    
    return dt


def parse_datetimeEsx(x):
    """
    Parses datetime from esxtop as:
        `[day/month-hour:minute:second]`
        year will be messed up (1900)
    """
    dt = datetime.strptime(x, '%m/%d/%Y%H:%M:%S')

    return dt


def parse_timeWin(x):
    """
    Parses datetime from windows perfmon as:
        `[day/month-hour:minute:second.ms]`
        year will be messed up (1900)
    """
    dt = datetime.strptime(x, '%H:%M:%S.%f')
    
    return dt    


def parse_windows_perfmon(CsvFullName):

    """
    Lets make our life easier and tidy up windows perfmon file
    Windows is ugly. There seem to be several formats, examples shown, but you may have to 
    adjust for your site.
    """
    
    with open(CsvFullName, mode='rt') as infile, \
            open('temp_perfmon.csv', mode='wt') as outfile:
    
        HeaderLine = False
        for line in infile:
        
            line = line.replace('"', '')  # strip quotes
            line = line.replace(' ', '')  # strip spaces
            
            if not HeaderLine:
                HeaderLine = True
            
                line = line.split(',')  # split to change column headings
                
                # Work out if date time one field or two and any other format diff
                if line[1] != 'Time':
                    # Example:
                    # "(PDH-CSV 4.0) (Eastern Standard Time)(300)","\\SERVER_NAME\Memory\Available MBytes"
                
                    line[0] = 'DateTime'
                    
                    # strip Servername - Single back slash
                    ServerName = line[2]
                    elems = ServerName.split('\\')
                    ServerName = elems[2]
                     
                    line = ','.join(line)  # Comma separate
                    line = line.replace('\\\\' + ServerName + '\\', '') 

                else:
                    # Example:
                    # "Date \\SERVER_NAME (PDH-CSV 4.0) (SE Asia Standard Time)(-420)","Time","\Memory\Available MBytes"
                    line[0] = 'Date'
                
                    # Remove first leading slash
                    line = [cols.replace('\\', '', 1) for cols in line]  # iterable comprehension
                    # No Server name
                    line = ','.join(line)  # Comma separate

                # esxtop
                # "(PDH-CSV 4.0) (UTC)(0)","\\SYDTAVM1\Memory\Memory Overcommit (1 Minute Avg)"
                # "05/15/2017 06:49:37","0.00"


            line = ''.join(line)  # concatenate it all back together
            line = line.replace(',,', ',0,')  # #Blank (space) field blows up matplotlib

            outfile.write(line)


def graph_column(CsvFullName, CsvFileType, InterestingColumns, DateTimeIndexed, IndexColumn):

    graph_style = args.style
    Number_Days=0

    # Depending on file type read in data and set indexes
    if DateTimeIndexed == 'DateTimeIndexed':

        data = pd.read_csv(
            CsvFullName, 
            header=0,
            parse_dates=[[0, 1]]  # Combine columns 0 and 1 and parse as a single date column.
           )

        # data.info() # Debug
        data.columns = data.columns.str.strip()
        data = data.rename(columns={'Date_Time': 'DateTime'})
        data.index = data.DateTime
        
        Number_Days = (data.DateTime.max() - data.DateTime.min()).days
        #print('Days: ', Number_Days)

    elif CsvFileType == 'esxtop' and DateTimeIndexed == 'WinDateTimeIndexed':

        data = pd.read_csv(
            CsvFullName,
            header=0,
            converters={0: parse_datetimeEsx}
        )

        data.columns = data.columns.str.strip()
        data.index = data.DateTime

        Number_Days = (data.DateTime.max() - data.DateTime.min()).days
        # print('Days; ', Number_Days)

    elif CsvFileType == 'win_perfmon' and DateTimeIndexed == 'WinDateTimeIndexed':
    
        data = pd.read_csv(
            CsvFullName, 
            header=0,
            converters={0: parse_datetimeWin}
           )
        
        data.columns = data.columns.str.strip()
        data.index = data.DateTime

        Number_Days = (data.DateTime.max() - data.DateTime.min()).days
        #print('Days; ', Number_Days)

    elif CsvFileType == 'win_perfmon' and DateTimeIndexed == 'WinTimeIndexed':

        data = pd.read_csv(
            CsvFullName, 
            header=0,
            converters={1: parse_timeWin}
           )
        
        data.columns = data.columns.str.strip()
        data.index = data.Time
        
    elif DateTimeIndexed == 'TimeIndexed':

        data = pd.read_csv(
            CsvFullName, 
            header=0,
            converters={IndexColumn: parse_datetimeVM}
           )

        # data.info()
        data.columns = data.columns.str.strip()
        data.index = data.Time
        
    else:
    
        data = pd.read_csv(
            CsvFullName, 
            header=0
           )
        data.columns = data.columns.str.strip()

    if CsvFileType == 'vmstat':
        data['Total CPU'] = 100-data.id

    # Just trying some things here

    if CsvFileType == 'mgstat':
        # Create an average for charting benchmark results
        # Note the window of 100 -- if there are less than 100 data points will blow up script at plt.savefig
        # If less than 100 data points divide by 10 and/or round up to even integer
        if len(data.index) <= 100:
            rolling_index=math.ceil((len(data.index)/10) / 2.) * 2
        else:
            rolling_index=100     

        data['Average Glorefs'] = data['Glorefs'].rolling(window=rolling_index, center=False).mean()

        # Get rid of outliers for indicative graphs and stats collection
        # data['Smoothed reads'] = data[np.abs(data['PhyRds'] - data['PhyRds'].mean()) <= (3 * data['PhyRds'].std())]
        # print(data[np.abs(data['PhyRds'] - data['PhyRds'].mean()) <= (3 * data['PhyRds'].std())])

    # Now plot each column
    for ColumnName in InterestingColumns:

        if graph_style == 'interactive':

            if 'iostat' not in CsvFileType:
                BokehChart = figure(x_axis_type='datetime', title=CsvFileType + ' ' + ColumnName + CHART_TITLE,
                                    width=1024, height=768, x_axis_label='time')
            else:
                BokehChart = figure(x_axis_type='auto', title=CsvFileType + ' ' + ColumnName + CHART_TITLE, width=1024,
                                    height=768, x_axis_label='time ->')

            BokehChart.line(data.index, data[ColumnName], legend=ColumnName, line_width=1)

            if 'Disksec' in ColumnName or 'svctm' in ColumnName or 'await' in ColumnName:  # Outputs in milliseconds
                BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0.000")
            else:
                BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

            if 'iostat' not in CsvFileType:
                BokehChart.xaxis[0].formatter = DatetimeTickFormatter(minutes=['%R'], hours=['%R'], days=['%a %d'])

            ColumnNameOut = ColumnName.replace('/', '_')
            ColumnNameOut = ColumnNameOut.replace('\\', '_')

            output_file(CsvFileType + '_' + ColumnNameOut + '_interactive.html')
            save(BokehChart)

        else:

            plt.figure(num=None, figsize=(10, 6), dpi=80, facecolor='w', edgecolor='dimgrey')

            if DateTimeIndexed == 'NoIndex':
                if graph_style == 'dot':
                    plt.plot(data[ColumnName], ".", markersize=2, color='dimgrey')
                else:
                    plt.plot(data[ColumnName], color='dimgrey')

            elif DateTimeIndexed == 'DateTimeIndexed' or DateTimeIndexed == 'WinDateTimeIndexed':
                
                if graph_style == 'dot':
                    plt.plot(data.DateTime, data[ColumnName], ".", markersize=2, color='dimgrey')
                else:
                    plt.plot(data.DateTime, data[ColumnName], color='dimgrey')

            elif DateTimeIndexed == 'TimeIndexed' or DateTimeIndexed == 'WinTimeIndexed':

                if graph_style == 'dot':
                    plt.plot(data.Time, data[ColumnName], ".", markersize=2, color='dimgrey')
                else:
                    plt.plot(data.Time, data[ColumnName], color='dimgrey')

            plt.grid()

            plt.title(CsvFileType + ' ' + ColumnName + CHART_TITLE, fontsize=10)

            plt.xlabel("Time", fontsize=10)
            plt.tick_params(labelsize=8)

            ax = plt.gca()

            if DateTimeIndexed != 'NoIndex':
            
                if Number_Days > 1:
                    ax.xaxis.set_major_formatter(DateFormatter("%a %H:%M"))
                else:
                    ax.xaxis.set_major_formatter(DateFormatter("%H:%M"))
                    
                ax.xaxis.set_minor_locator(HourLocator())

            ax.set_ylim(ymin=0)  # Always zero start

            if '%' in ColumnName:
                ax.set_ylim(ymax=100)
            elif CsvFileType == 'vmstat' and ColumnName in 'us sy wa id Total CPU':
                ax.set_ylim(ymax=100)

            if 'Disksec' in ColumnName or 'svctm' in ColumnName or 'await' in ColumnName:  # Outputs in milliseconds
                ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(float(x))))
            else:
                ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(int(x))))

            #print(CsvFileType + '_' + ColumnName.replace('/', '_') + '_' + graph_style + '.png')    
            plt.savefig(CsvFileType + '_' + ColumnName.replace('/', '_') + '_' + graph_style + '.png')

            plt.close('all')

    # Now create a few combined plots. Useful but also a guide to creating your own.
    colors = magma(7)

    if graph_style == 'interactive' and CsvFileType == 'vmstat':

        BokehChart = figure(x_axis_type='datetime', title=CsvFileType + ' vmstat' + CHART_TITLE, width=1024,
                            height=768, x_axis_label='time', toolbar_location="above")

        myWrite_Legend = 'CPU max ' + str(max(data['Total CPU']))
        BokehChart.line(data.index, data['Total CPU'], legend=myWrite_Legend, line_width=1, alpha=0.8,  line_color=colors[4])
        BokehChart.yaxis.axis_label = "Total CPU"

        myRead_Legend='b max ' + str(max(data['b']))
        BokehChart.extra_y_ranges = {"b_y": Range1d(start=0, end=100)}
        BokehChart.add_layout(LinearAxis(y_range_name="b_y", axis_label="b", formatter=NumeralTickFormatter(format="0,0")), 'right')
        BokehChart.line(data.index, data['b'], legend=myRead_Legend, line_width=1, line_color=colors[0], y_range_name="b_y")

        # BokehChart.x_range = Range1d(0,data.index.max())
        BokehChart.y_range = Range1d(0,100)

        BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
        BokehChart.xaxis[0].formatter = DatetimeTickFormatter(minutes=['%R'], hours=['%R'], days=['%a %d'])

        output_file(CsvFileType + '_CPU_vs_Blocked_interactive.html')
        save(BokehChart)

    if graph_style == 'interactive' and CsvFileType == 'mgstat':
        BokehChart = figure(x_axis_type='datetime', title=CsvFileType + ' Reads and Writes' + CHART_TITLE,
                                width=1024,
                                height=768, x_axis_label='time', toolbar_location="above")

        myWrite_Legend = 'PhyWrs max ' + str(max(data['PhyWrs']))
        BokehChart.line(data.index, data['PhyWrs'], legend=myWrite_Legend, line_width=1, alpha=0.8,
                            line_color=colors[4])
        BokehChart.yaxis.axis_label = "PhyWrs"

        myRead_Legend = 'Reads max ' + str(max(data['PhyRds']))
        BokehChart.extra_y_ranges = {"PhyRds_y": Range1d(start=0, end=max(data['PhyRds']))}
        BokehChart.add_layout(
                LinearAxis(y_range_name="PhyRds_y", axis_label="PhyRds", formatter=NumeralTickFormatter(format="0,0")),
                'right')
        BokehChart.line(data.index, data['PhyRds'], legend=myRead_Legend, line_width=1, line_color=colors[0],
                            y_range_name="PhyRds_y")

        # BokehChart.x_range = Range1d(0,data.index.max())
        BokehChart.y_range = Range1d(0, max(data['PhyWrs']))

        BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
        BokehChart.xaxis[0].formatter = DatetimeTickFormatter(minutes=['%R'], hours=['%R'], days=['%a %d'])

        output_file(CsvFileType + '_Reads_and_Writes_interactive.html')
        save(BokehChart)

        BokehChart = figure(x_axis_type='datetime', title=CsvFileType + ' Glorefs and Writes' + CHART_TITLE, width=1024,
                            height=768, x_axis_label='time', toolbar_location="above")

        myWrite_Legend = 'Glorefs max ' + str(max(data['Glorefs']))
        BokehChart.line(data.index, data['Glorefs'], legend=myWrite_Legend, line_width=1, alpha=0.8,
                        line_color=colors[4])
        BokehChart.yaxis.axis_label = "Glorefs"

        myRead_Legend = 'PhyWrs max ' + str(max(data['PhyWrs']))
        BokehChart.extra_y_ranges = {"PhyWrs_y": Range1d(start=0, end=max(data['PhyWrs']))}
        BokehChart.add_layout(
            LinearAxis(y_range_name="PhyWrs_y", axis_label="PhyWrs", formatter=NumeralTickFormatter(format="0,0")),
            'right')
        BokehChart.line(data.index, data['PhyWrs'], legend=myRead_Legend, line_width=1, line_color=colors[0],
                        y_range_name="PhyWrs_y")

        # BokehChart.x_range = Range1d(0,data.index.max())
        BokehChart.y_range = Range1d(0, max(data['Glorefs']))

        BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
        BokehChart.xaxis[0].formatter = DatetimeTickFormatter(minutes=['%R'], hours=['%R'], days=['%a %d'])

        output_file(CsvFileType + '_Glorefs_and_Writes_interactive.html')
        save(BokehChart)


        BokehChart = figure(x_axis_type='datetime', title=CsvFileType + ' Glorefs and WIJ Writes' + CHART_TITLE, width=1024,
                            height=768, x_axis_label='time', toolbar_location="above")

        myWrite_Legend = 'Glorefs max ' + str(max(data['Glorefs']))
        BokehChart.line(data.index, data['Glorefs'], legend=myWrite_Legend, line_width=1, alpha=0.8,
                        line_color=colors[4])
        BokehChart.yaxis.axis_label = "Glorefs"

        myRead_Legend = 'WIJwri max ' + str(max(data['WIJwri']))
        BokehChart.extra_y_ranges = {"WIJwri_y": Range1d(start=0, end=max(data['WIJwri']))}
        BokehChart.add_layout(
            LinearAxis(y_range_name="WIJwri_y", axis_label="WIJwri", formatter=NumeralTickFormatter(format="0,0")),
            'right')
        BokehChart.line(data.index, data['WIJwri'], legend=myRead_Legend, line_width=1, line_color=colors[0],
                        y_range_name="WIJwri_y")

        # BokehChart.x_range = Range1d(0,data.index.max())
        BokehChart.y_range = Range1d(0, max(data['Glorefs']))

        BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
        BokehChart.xaxis[0].formatter = DatetimeTickFormatter(minutes=['%R'], hours=['%R'], days=['%a %d'])

        output_file(CsvFileType + '_Glorefs_and_WIJ_Writes_interactive.html')
        save(BokehChart)


        BokehChart = figure(x_axis_type='datetime', title=CsvFileType + ' Glorefs and Journal Writes' + CHART_TITLE,
                            width=1024,
                            height=768, x_axis_label='time', toolbar_location="above")

        myWrite_Legend = 'Glorefs max ' + str(max(data['Glorefs']))
        BokehChart.line(data.index, data['Glorefs'], legend=myWrite_Legend, line_width=1, alpha=0.8,
                        line_color=colors[4])
        BokehChart.yaxis.axis_label = "Glorefs"

        myRead_Legend = 'Jrnwrts max ' + str(max(data['Jrnwrts']))
        BokehChart.extra_y_ranges = {"Jrnwrts_y": Range1d(start=0, end=max(data['Jrnwrts']))}
        BokehChart.add_layout(
            LinearAxis(y_range_name="Jrnwrts_y", axis_label="Jrnwrts", formatter=NumeralTickFormatter(format="0,0")),
            'right')
        BokehChart.line(data.index, data['Jrnwrts'], legend=myRead_Legend, line_width=1, line_color=colors[0],
                        y_range_name="Jrnwrts_y")

        # BokehChart.x_range = Range1d(0,data.index.max())
        BokehChart.y_range = Range1d(0, max(data['Glorefs']))

        BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
        BokehChart.xaxis[0].formatter = DatetimeTickFormatter(minutes=['%R'], hours=['%R'], days=['%a %d'])

        output_file(CsvFileType + '_Glorefs_and_Journal_Writes_interactive.html')
        save(BokehChart)


        # Plot all writes

        BokehChart = figure(x_axis_type='datetime', title=CsvFileType + ' Glorefs and all Writes' + CHART_TITLE,
                            width=1024,
                            height=768, x_axis_label='time', toolbar_location="above")

        myWrite_Legend = 'Glorefs max ' + str(max(data['Glorefs']))
        BokehChart.line(data.index, data['Glorefs'], legend=myWrite_Legend, line_width=2, alpha=0.8,
                        line_color=colors[4])
        BokehChart.yaxis.axis_label = "Glorefs"

        BokehChart.extra_y_ranges={}
        BokehChart.extra_y_ranges = {"allwrts_y": Range1d(start=0, end=max(max(data['Jrnwrts']),max(data['WIJwri'])))}
        #BokehChart.extra_y_ranges = {"allwrts_y2": Range1d(start=0, end=max(data['PhyWrs']))}

        BokehChart.add_layout(LinearAxis(y_range_name="allwrts_y", axis_label="Journal,WIJ and DB writes", formatter=NumeralTickFormatter(format="0,0")),'right')
        #BokehChart.add_layout(LinearAxis(y_range_name="allwrts_y2", axis_label="DB writes", formatter=NumeralTickFormatter(format="0,0")),'left')


        myRead_Legend = 'Jrnwrts max ' + str(max(data['Jrnwrts']))
        BokehChart.line(data.index, data['Jrnwrts'], legend=myRead_Legend, line_width=2, line_color=colors[0],
                        y_range_name="allwrts_y")

        myWIJ_Legend = 'WIJ Writes per second max ' + str(max(data['WIJwri']))
        BokehChart.line(data.index, data['WIJwri'], legend=myWIJ_Legend, line_width=2, line_color=colors[5],
                        y_range_name="allwrts_y")

        myWrite_Legend = 'PhyWrs max ' + str(max(data['PhyWrs']))
        BokehChart.line(data.index, data['PhyWrs'], legend=myWrite_Legend, line_width=2, line_color=colors[3],y_range_name="allwrts_y")


        # BokehChart.x_range = Range1d(0,data.index.max())
        BokehChart.y_range = Range1d(0, max(data['Glorefs']))

        BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
        BokehChart.xaxis[0].formatter = DatetimeTickFormatter(minutes=['%R'], hours=['%R'], days=['%a %d'])

        output_file(CsvFileType + '_Glorefs_and_all_Writes_interactive.html')
        save(BokehChart)

    if graph_style == 'interactive' and 'iostat' in CsvFileType:

        BokehChart = figure(x_axis_type='auto', title=CsvFileType + ' Reads and Writes' + CHART_TITLE, width=1024,
                            height=768, x_axis_label='time ->', toolbar_location="above")

        myWrite_Legend = 'Writes per second max ' + str(max(data['w/s']))
        BokehChart.line(data.index, data['w/s'], legend=myWrite_Legend, line_width=1, alpha=0.8,  line_color=colors[4])
        BokehChart.yaxis.axis_label = "w/s"

        myRead_Legend='Reads per second max ' + str(max(data['r/s']))
        BokehChart.extra_y_ranges = {"Reads": Range1d(start=0, end=max(data['r/s']))}
        BokehChart.add_layout(LinearAxis(y_range_name="Reads", axis_label="r/s", formatter=NumeralTickFormatter(format="0,0")), 'right')
        BokehChart.line(data.index, data['r/s'], legend=myRead_Legend, line_width=1, line_color=colors[0], y_range_name="Reads")

        BokehChart.x_range = Range1d(0,max(data.index))
        BokehChart.y_range = Range1d(0,max(data['w/s']))
        BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

        output_file(CsvFileType + '_Reads_and_Writes_interactive.html')
        save(BokehChart)


        BokehChart = figure(x_axis_type='auto', title=CsvFileType + ' svctm and await' + CHART_TITLE, width=1024,
                            height=768, x_axis_label='time ->', toolbar_location="above")

        mysvctm_Legend = 'svctm max ' + str(max(data['svctm']))
        BokehChart.line(data.index, data['svctm'], legend=mysvctm_Legend, line_width=1, alpha=0.8,  line_color=colors[4])
        BokehChart.yaxis.axis_label = "svctm and await"

        myawait_Legend='await max ' + str(max(data['await']))
        #BokehChart.extra_y_ranges = {"await": Range1d(start=0, end=max(data['await']))}
        #BokehChart.add_layout(LinearAxis(y_range_name="await", axis_label="await", formatter=NumeralTickFormatter(format="0,0.000")), 'right')
        #BokehChart.line(data.index, data['await'], legend=myawait_Legend, line_width=1, line_color=colors[0], y_range_name="await")
        BokehChart.line(data.index, data['await'], legend=myawait_Legend, line_width=1, line_color=colors[0])

        BokehChart.x_range = Range1d(0,max(data.index))
        BokehChart.y_range = Range1d(0,max(max(data['svctm']),max(data['await'])))
        BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0.000")

        output_file(CsvFileType + '_svctm_and_await_interactive.html')
        save(BokehChart)


        BokehChart = figure(x_axis_type='auto', title=CsvFileType + ' Writes and w_await' + CHART_TITLE, width=1024,
                            height=768, x_axis_label='time ->', toolbar_location="above")

        myWrite_Legend = 'Writes per second max ' + str(max(data['w/s']))
        BokehChart.line(data.index, data['w/s'], legend=myWrite_Legend, line_width=1, alpha=0.8,  line_color=colors[4])
        BokehChart.yaxis.axis_label = "w/s"

        myRead_Legend='w_await max ' + str(max(data['w_await']))
        BokehChart.extra_y_ranges = {"w_Await": Range1d(start=0, end=max(data['w_await']))}
        BokehChart.add_layout(LinearAxis(y_range_name="w_Await", axis_label="w_await", formatter=NumeralTickFormatter(format="0,0.000")), 'right')
        BokehChart.line(data.index, data['w_await'], legend=myRead_Legend, line_width=1, line_color=colors[0], y_range_name="w_Await")

        BokehChart.x_range = Range1d(0,max(data.index))
        BokehChart.y_range = Range1d(0,max(data['w/s']))
        BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

        output_file(CsvFileType + '_Writes_and_w_await_interactive.html')
        save(BokehChart)


        BokehChart = figure(x_axis_type='auto', title=CsvFileType + ' Reads and r_await' + CHART_TITLE, width=1024,
                            height=768, x_axis_label='time ->', toolbar_location="above")

        myWrite_Legend = 'Reads per second max ' + str(max(data['r/s']))
        BokehChart.line(data.index, data['r/s'], legend=myWrite_Legend, line_width=1, alpha=0.8,  line_color=colors[4])
        BokehChart.yaxis.axis_label = "r/s"

        myRead_Legend='r_await max ' + str(max(data['r_await']))
        BokehChart.extra_y_ranges = {"r_Await": Range1d(start=0, end=max(data['r_await']))}
        BokehChart.add_layout(LinearAxis(y_range_name="r_Await", axis_label="r_await", formatter=NumeralTickFormatter(format="0,0.000")), 'right')
        BokehChart.line(data.index, data['r_await'], legend=myRead_Legend, line_width=1, line_color=colors[0], y_range_name="r_Await")

        BokehChart.x_range = Range1d(0,max(data.index))
        BokehChart.y_range = Range1d(0,max(data['r/s']))
        BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")

        output_file(CsvFileType + '_Reads_and_r_await_interactive.html')
        save(BokehChart)

        # BokehChart = figure(x_axis_type='auto', title=CsvFileType + ' Writes and Write kB/s' + CHART_TITLE, width=1024,
        #                     height=768, x_axis_label='time ->', toolbar_location="above")
        #
        # myWrite_Legend = 'Writes per second max ' + str(max(data['w/s']))
        # BokehChart.line(data.index, data['w/s'], legend=myWrite_Legend, line_width=1, alpha=0.8,  line_color=colors[4])
        # BokehChart.yaxis.axis_label = "w/s"
        #
        # myRead_Legend='Write kB/s max ' + str(max(data['wkB/s']))
        # BokehChart.extra_y_ranges = {"Right_y": Range1d(start=0, end=max(data['wkB/s']))}
        # BokehChart.add_layout(LinearAxis(y_range_name="Right_y", axis_label="wkB/s", formatter=NumeralTickFormatter(format="0,0")), 'right')
        # BokehChart.line(data.index, data['wkB/s'], legend=myRead_Legend, line_width=1, line_color=colors[0], y_range_name="Right_y")
        #
        # BokehChart.x_range = Range1d(0,max(data.index))
        # BokehChart.y_range = Range1d(0,max(data['w/s']))
        # BokehChart.yaxis[0].formatter = NumeralTickFormatter(format="0,0")
        #
        # output_file(CsvFileType + '_w_s_and_wkB_s_interactive.html')
        # save(BokehChart)


def GetColumnHeadings(CsvDirName, CsvFileType):
    """ 
        Build the header column list and work out where the indexes are.
    """

    InterestingColumns = []
    line = ''
    DateTimeIndexed = 'NoIndex'
    IndexColumn = 0
    
    with open(CsvDirName, mode='rt') as infile:
        
        for line in infile:
            InterestingColumns = line.split(',')     
            break
            
    InterestingColumns[-1] = InterestingColumns[-1].strip()   # Remove new line   

    if CsvFileType == 'win_perfmon' and InterestingColumns[0] == 'DateTime':
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
        
    if 'Device:' in line:                  # eg. iostat
        InterestingColumns.remove('Device:')
 
    return InterestingColumns, DateTimeIndexed, IndexColumn


def mainline(CsvDirName, Csvkitchen_sink, DoNotIostat):

    """Chart input file.
    
    Args: 
        CsvDirName  = path for csv files.
        Csvkitchen_sink   = if True only print key metrics
        DoNotIostat = do not process iostat
    
    Output: 
        outputs graphs for csv columns
    """
            
    files = os.listdir(CsvDirName)
    
    for csvFilename in files:
    
        if DoNotIostat and 'iostat' in os.path.basename(csvFilename):
            pass
            
        else:
            if os.path.basename(csvFilename).split('.')[1] == 'csv':
                print('Charting: ' + csvFilename + ' - ' + args.style + ' ' + CHART_TITLE)
            
                CsvFileType = os.path.basename(csvFilename).split('.')[0]
                fullName = CsvDirName + '/' + csvFilename

                # Windows needs clean up, override filename to temp file
                if CsvFileType == 'win_perfmon' or CsvFileType == 'esxtop':
                    parse_windows_perfmon(fullName)
                    fullName = 'temp_perfmon.csv'

                # Get column headers and decide if indexed    
                InterestingColumns,  DateTimeIndexed, IndexColumn = GetColumnHeadings(fullName, CsvFileType)

                if not Csvkitchen_sink:                    
                    if CsvFileType == 'mgstat':
                        InterestingColumns = ['Glorefs', 'RemGrefs', 'PhyRds', 'Rdratio', 'Gloupds', 'RouLaS', 'PhyWrs',
                                              'WDQsz', 'WDphase', 'Jrnwrts', 'BytSnt', 'BytRcd', 'WIJwri', 'RouCMs',
                                              'Rourefs', 'WDtmpq', 'Average Glorefs']
                    elif CsvFileType == 'vmstat':
                        InterestingColumns = ['r', 'b', 'us', 'sy', 'id', 'wa', 'Total CPU']
                    elif CsvFileType == 'win_perfmon':
                        InterestingColumns = ['Processor(_Total)\%PrivilegedTime',
                                              'Processor(_Total)\%UserTime',
                                              'Processor(_Total)\%ProcessorTime',
                                              'Processor(_Total)\Interrupts/sec',
                                              'Memory\AvailableMBytes',
                                              'Memory\PageReads/sec',
                                              'Memory\PageWrites/sec',
                                              'PagingFile(_Total)\%Usage',
                                              'PhysicalDisk(_Total)\DiskTransfers/sec',
                                              'System\Processes',
                                              'System\ProcessorQueueLength']
                    elif CsvFileType == 'esxtop':
                        InterestingColumns = ['PhysicalCpu(_Total)\%ProcessorTime',
                                              'PhysicalCpu(_Total)\%UtilTime',
                                              'PhysicalCpu(_Total)\%CoreUtilTime']

                # Chart each column
                graph_column(fullName, CsvFileType, InterestingColumns, DateTimeIndexed, IndexColumn)

                if OUTDIR:
                    TGTDIR=OUTDIR
                else:
                    TGTDIR='./' + FILEPREFIX + 'charts'
                # move files to new home
                os.makedirs(TGTDIR, exist_ok=True)

                iostatMade = False
                mgstatMade = False
                vmstatMade = False
                perfmonMade = False
            
                files = os.listdir('.')
                for pngFilename in files:
                    if (pngFilename.endswith('.png')) or (pngFilename.endswith('_interactive.html')):
                
                        if pngFilename.startswith('iostat_'):
                            if not iostatMade:
                                iostatMade = True
                                os.makedirs(os.path.join(TGTDIR,'iostat'), exist_ok=True)
                            shutil.move(pngFilename, os.path.join(TGTDIR,'iostat',pngFilename) )  
                        elif pngFilename.startswith('mgstat_'):
                            if not mgstatMade:
                                mgstatMade = True
                                os.makedirs(os.path.join(TGTDIR,'mgstat'), exist_ok=True)
                            shutil.move(pngFilename, os.path.join(TGTDIR,'mgstat',pngFilename) )                                
                        elif pngFilename.startswith('vmstat_'):
                            if not vmstatMade:
                                vmstatMade = True
                                os.makedirs(os.path.join(TGTDIR,'vmstat'), exist_ok=True)
                            shutil.move(pngFilename, os.path.join(TGTDIR,'vmstat',pngFilename))        
                        elif pngFilename.startswith('win_perfmon_'):
                            if not perfmonMade:
                                perfmonMade = True
                                os.makedirs(os.path.join(TGTDIR,'win_perfmon'), exist_ok=True)
                            shutil.move(pngFilename, os.path.join(TGTDIR,'win_perfmon',pngFilename))      
                        else:        
                            shutil.move(pngFilename, os.path.join(TGTDIR,pngFilename))
                
                if os.path.isfile('temp_perfmon.csv'):
                    os.remove('temp_perfmon.csv')

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Graph metrics from pButtons csv files')
    parser.add_argument("csv_dir_name", help="Path to directory containing .csv files to chart")
    parser.add_argument("-k", "--kitchen_sink", help="Kitchen sink mode, ALL columns will be charted", action="store_true")
    parser.add_argument("-I", "--Iostat", help="Do NOT process iostat if exists", action="store_true")
    parser.add_argument("-s", "--style", help="Chart style: line (default), dots, interactive html", choices=['line', 'dot', 'interactive'], default='line')
    parser.add_argument("-p", "--prefix", help="add prefix string for output directory")
    parser.add_argument("-t", "--title", help="Title for all charts, eg pass file name")
    parser.add_argument("-o","--out",help="set output directory")
    
    args = parser.parse_args()

    if args.prefix is not None:
        FILEPREFIX = args.prefix
    else:
        FILEPREFIX = ''

    if args.out is not None:
        OUTDIR = args.out
    else:
        OUTDIR = ''

    if args.title is not None:
        CHART_TITLE = ' : ' + args.title
    else:
        CHART_TITLE = ''

    try:
        mainline(args.csv_dir_name, args.kitchen_sink, args.Iostat)
    except OSError as e:
        print('Could not process csv file because: {}'.format(str(e)))
