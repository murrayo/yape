import pandas as pd
import numpy
import sqlite3
import matplotlib.colors as colors
import matplotlib.dates as mdates
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, IndexDateFormatter
import pytz
import re
import os
import mpl_toolkits.mplot3d
import matplotlib.pyplot as plt
from datetime import datetime

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def genericplot(df,column,outfile):
    fig,ax=plt.subplots(figsize=(24,16))
    plt.title(column)
    ax.xaxis.set_minor_locator(mdates.HourLocator())
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.grid(True,which="minor",linestyle="-")
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("\n\n %Y-%m-%d"))
    ax.yaxis.grid()
    df[column].plot(ax=ax)
    plt.savefig(outfile, bbox_inches='tight')
    print("created: "+outfile)
    plt.close()

def mgstat(db,basename):
    mgstat=pd.read_sql_query("select * from mgstat",db)
    mgstat.index=pd.to_datetime(mgstat['datetime'])
    mgstat=mgstat.drop(['datetime'],axis=1)
    mgstat.index.name='datetime'
    numlines = len(mgstat.columns)
    ensure_dir(basename+os.sep)
    for key in mgstat.columns.values:
        file=os.path.join(basename,"mgstat."+key+".png")
        genericplot(mgstat,key,file)
