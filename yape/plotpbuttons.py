import pandas as pd
import numpy
import sqlite3
import matplotlib.colors as colors
import matplotlib.dates as mdates
from matplotlib.dates import DayLocator, HourLocator, DateFormatter, drange, IndexDateFormatter
from matplotlib.ticker import AutoMinorLocator
import pytz
import re
import os
import mpl_toolkits.mplot3d
import matplotlib.pyplot as plt
from datetime import datetime

def genericplot(df,column,outfile,timeframe):
    print("creating"+outfile)
    fig,ax=plt.subplots(figsize=(16,6), dpi=80, facecolor='w', edgecolor='dimgrey')

    if timeframe!="":
        ax.xaxis.set_minor_locator(AutoMinorLocator(n=10))
    else:
        ax.xaxis.set_minor_locator(mdates.HourLocator())
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M:%S'))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("\n\n %Y-%m-%d"))

    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "{:,}".format(float(x))))
    if timeframe is not None:
        df[column][timeframe.split(",")[0]:timeframe.split(",")[1]].plot(ax=ax)
    else:
        df[column].plot(ax=ax)

    ax.set_ylim(ymin=0)  # Always zero start

    plt.grid(which='both', axis='both')
    plt.title(column, fontsize=10)
    plt.xlabel("Time", fontsize=10)
    plt.tick_params(labelsize=8)

    plt.savefig(outfile, bbox_inches='tight')

    plt.close()

#need this as utility, since pandas timestamps are not compaitble with sqlite3 timestamps
#there's a possible other solution by using using converters in sqlite, but I haven't explored that yet
def fix_index(df):
    df.index=pd.to_datetime(df['datetime'])
    df=df.drop(['datetime'],axis=1)
    df.index.name='datetime'
    return df

def plot_subset_split(db,basename,subsetname,split_on,timeframe):
    if not check_data(db,subsetname):
        return None
    c=db.cursor()
    c.execute("select distinct "+split_on+" from \""+subsetname+"\"")
    rows=c.fetchall()
    for column in rows:
        c.execute("select * from \""+subsetname+"\" where "+split_on+"=?",[column[0]])
        data=pd.read_sql_query("select * from \""+subsetname+"\" where "+split_on+"=\""+column[0]+"\"",db)
        data=fix_index(data)
        data=data.drop([split_on],axis=1)
        for key in data.columns.values:
            if timeframe!="":
                file=os.path.join(basename,subsetname+"."+column[0]+"."+key.replace("/","_")+"."+timeframe+".png")
            else:
                file=os.path.join(basename,subsetname+"."+column[0]+"."+key.replace("/","_")+".png")
            genericplot(data,key,file,timeframe)

def plot_subset(db,basename,subsetname,timeframe):
    if not check_data(db,subsetname):
        return None
    data=pd.read_sql_query("select * from \""+subsetname+"\"",db)
    if 'datetime' not in data.columns.values:
        #one of those evil OS without datetime in vmstat
        #evil hack: take index from mgstat (we should have that in every pbuttons) and map that
        #is going to horribly fail when the number of rows doesn't add up ---> TODO for later
        dcolumn=pd.read_sql_query("select datetime from mgstat",db)
        data.index=pd.to_datetime(dcolumn['datetime'])
        data.index.name='datetime'
    else:
        data=fix_index(data)
    for key in data.columns.values:

        if timeframe is not None:
            file=os.path.join(basename,subsetname+"."+key.replace("\\","_").replace("/","_")+"."+timeframe+".png".replace("%","_"))
        else:
            file=os.path.join(basename,subsetname+"."+key.replace("\\","_").replace("/","_")+".png".replace("%","_"))
        genericplot(data,key,file,timeframe)

def check_data(db,name):
    cur = db.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [name])
    if len(cur.fetchall()) == 0:
        print("no data for:"+name)
        return False
    return True

def mgstat(db,basename,timeframe=""):
    plot_subset(db,basename,"mgstat",timeframe)
def perfmon(db,basename,timeframe=""):
    plot_subset(db,basename,"perfmon",timeframe)

def vmstat(db,basename,timeframe=""):
    plot_subset(db,basename,"vmstat",timeframe)

def iostat(db,basename,timeframe=""):
    plot_subset_split(db,basename,"iostat","Device",timeframe)
