# os methods for manipulating paths
import os
import argparse

import sys
import bokeh
import csv

import sqlite3

from yape.parsepbuttons import parsepbuttons
from yape.plotpbuttons import mgstat,vmstat,iostat,perfmon

def fileout(db,filename,fileprefix,section):
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

def fileout_splitcols(db,filename,fileprefix,section,split_on):
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
    parser.add_argument("--permon",dest='graphperfmon',help="plot perfmon data",action="store_true")
    parser.add_argument("--timeframe",dest='timeframe',help="specify a timeframe for the plots, i.e. --timeframe \"2018-05-16 00:01:16,2018-05-16 17:04:15\"")
    parser.add_argument("--prefix",dest='prefix',help="specify output file prfeix")
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

        if args.csv:
            ensure_dir(basefilename+os.sep)
            fileout(db,basefilename,fileprefix,"mgstat")
            fileout(db,basefilename,fileprefix,"vmstat")
            fileout_splitcols(db,basefilename,fileprefix,plotDisks,"iostat","Device")
            fileout_splitcols(db,basefilename,fileprefix,"sar-d","DEV")
            fileout(db,basefilename,fileprefix,"perfmon")
            fileout(db,basefilename,fileprefix,"sar-u")

        if args.graphmgstat or args.all:
            ensure_dir(basefilename+os.sep)
            mgstat(db,basefilename,fileprefix,args.timeframe)

        if args.graphvmstat or args.all:
            ensure_dir(basefilename+os.sep)
            vmstat(db,basefilename,fileprefix,args.timeframe)

        if args.graphiostat or args.all:
            ensure_dir(basefilename+os.sep)
            iostat(db,basefilename,fileprefix,plotDisks,args.timeframe)
            
        if args.graphperfmon or args.all:
            ensure_dir(basefilename+os.sep)
            perfmon(db,basefilename,fileprefix,args.timeframe)


    except OSError as e:
        print('Could not process pButtons file because: {}'.format(str(e)))
