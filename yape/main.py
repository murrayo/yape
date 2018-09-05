# os methods for manipulating paths
import os
import argparse

import sys
import bokeh
import csv

import sqlite3

from yape.parsepbuttons import parsepbuttons
from yape.plotpbuttons import mgstat,vmstat,iostat,perfmon,sard,monitor_disk

def fileout(db,basefilename,config,section):
    fileprefix=config["fileprefix"]
    c = db.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [section])
    if len(c.fetchall()) == 0:
        return None
    file=os.path.join(filename,fileprefix+section+".csv")
    print("exporting "+section+" to "+file)
    c.execute("select * from \""+section+"\"")
    columns = [i[0] for i in c.description]

    with open(file, "w") as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(columns)
        csvWriter.writerows(c)

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def fileout_splitcols(db,filename,config,section,split_on):
    fileprefix=config["fileprefix"]
    c = db.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [section])
    if len(c.fetchall()) == 0:
        return None
    c.execute("select distinct "+split_on+" from \""+section+"\"")
    rows=c.fetchall()
    for column in rows:
        c.execute("select * from \""+section+"\" where "+split_on+"=?",[column[0]])
        file=os.path.join(filename,fileprefix+section+"."+column[0]+".csv")
        print("exporting "+section+"-"+column[0]+" to "+file)
        columns = [i[0] for i in c.description]
        with open(file, "w") as f:
            csvWriter = csv.writer(f)
            csvWriter.writerow(columns)
            csvWriter.writerows(c)

def yape2():
    parser = argparse.ArgumentParser(description='Yape 2.0')
    parser.add_argument("pButtons_file_name", help="path to pButtons file to use")
    parser.add_argument("--filedb",help="use specific file as DB, useful to be able to used afterwards or as standalone datasource.")
    parser.add_argument("--skip-parse",dest="skipparse",help="disable parsing; requires filedb to be specified to supply data",action="store_true")
    parser.add_argument("-c",dest='csv',help="will output the parsed tables as csv files. useful for further processing. will currently create: mgstat, vmstat, sar-u. sar-d and iostat will be output per device",action="store_true")
    parser.add_argument("--mgstat",dest='graphmgstat',help="plot mgstat data",action="store_true")
    parser.add_argument("--vmstat",dest='graphvmstat',help="plot vmstat data",action="store_true")
    parser.add_argument("--iostat",dest='graphiostat',help="plot iostat data",action="store_true")
    parser.add_argument("--sard",dest='graphsard',help="plot sar-d data",action="store_true")
    parser.add_argument("--monitor_disk",dest='monitor_disk',help="plot disk data from monitor (vms)",action="store_true")
    parser.add_argument("--perfmon",dest='graphperfmon',help="plot perfmon data",action="store_true")
    parser.add_argument("--timeframe",dest='timeframe',help="specify a timeframe for the plots, i.e. --timeframe \"2018-05-16 00:01:16,2018-05-16 17:04:15\"")
    parser.add_argument("--prefix",dest='prefix',help="specify output file prefix (this is for the filename itself, to specify a directory, use -o)")
    parser.add_argument("--plotDisks",dest='plotDisks',help="restrict list of disks to plot")

    parser.add_argument("-a","--all",dest='all',help="graph everything",action="store_true")
    parser.add_argument("-o","--out",dest='out',help="specify base output directory, defaulting to <pbuttons_name>/")
    args = parser.parse_args()

    try:
        if args.skipparse:
            if args.filedb is None:
                print("filedb required with skip-parse set")
                return -1
        if args.filedb is not None:
            db=sqlite3.connect(args.filedb)
        else:
            db=sqlite3.connect(":memory:")
            db.execute('pragma journal_mode=wal')
            db.execute('pragma synchronous=0')
        if not args.skipparse:
            parsepbuttons(args.pButtons_file_name,db)

        if args.out is not None:
            basefilename=args.out
        else:
            basefilename=args.pButtons_file_name.split(".")[0]

        if args.prefix is not None:
            fileprefix=args.prefix
        else:
            fileprefix=""

        if args.plotDisks is not None:
            plotDisks=args.plotDisks
        else:
            plotDisks=""

        if args.timeframe is not None:
            TIMEFRAMEMODE=True
            print("timeframe on "+args.timeframe)
        else:
            TIMEFRAMEMODE=False


        # a place to hold global configurations/settings
        # makes it easier to extend functionality to carry
        # command line parameters to subfunctions...
        config={}
        config["fileprefix"]=fileprefix
        config["plotdisks"]=plotDisks
        config["timeframe"]=args.timeframe
        config["basefilename"]=basefilename

        if args.csv:
            ensure_dir(basefilename+os.sep)
            fileout(db,basefilename,config,"mgstat")
            fileout(db,basefilename,config,"vmstat")
            fileout_splitcols(db,basefilename,config,"iostat","Device")
            fileout_splitcols(db,basefilename,config,"sar-d","DEV")
            fileout(db,basefilename,config,"perfmon")
            fileout(db,basefilename,config,"sar-u")


        #plotting
        if args.graphsard or args.all:
            ensure_dir(basefilename+os.sep)
            sard(db,config)

        if args.graphmgstat or args.all:
            ensure_dir(basefilename+os.sep)
            mgstat(db,config)

        if args.graphvmstat or args.all:
            ensure_dir(basefilename+os.sep)
            vmstat(db,config)

        if args.monitor_disk or args.all:
            ensure_dir(basefilename+os.sep)
            monitor_disk(db,config)

        if args.graphiostat or args.all:
            ensure_dir(basefilename+os.sep)
            iostat(db,config)

        if args.graphperfmon or args.all:
            ensure_dir(basefilename+os.sep)
            perfmon(db,config)


    except OSError as e:
        print('Could not process pButtons file because: {}'.format(str(e)))
