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

#need this as utility, since pandas timestamps are not compaitble with sqlite3 timestamps
#there's a possible other solution by using using converters in sqlite, but I haven't explored that yet
def fix_index(df):
    df.index=pd.to_datetime(df['datetime'])
    df=df.drop(['datetime'],axis=1)
    df.index.name='datetime'
    return df

def plot_subset(db,basename,subsetname):
    if not check_data(db,subsetname):
        return None
    data=pd.read_sql_query("select * from \""+subsetname+"\"",db)
    data=fix_index(data)
    for key in data.columns.values:
        file=os.path.join(basename,subsetname+"."+key+".png")
        genericplot(data,key,file)

def check_data(db,name):
    cur = db.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [name])
    if len(cur.fetchall()) == 0:
        print("no data for:"+name)
        return False
    return True

def mgstat(db,basename):
    plot_subset(db,basename,"mgstat")

def vmstat(db,basename):
    plot_subset(db,basename,"vmstat")
