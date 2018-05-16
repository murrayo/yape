# os methods for manipulating paths
import os
import argparse

import sys
import bokeh
import csv

import sqlite3

from yape.parsepbuttons import parsepbuttons
from yape.plotpbuttons import mgstat,vmstat,iostat

def fileout(db,filename,section):
    c = db.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [section])
    if len(c.fetchall()) == 0:
        return None
    file=os.path.join(filename,section+".csv")
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

def fileout_splitcols(db,filename,section,split_on):
    c = db.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [section])
    if len(c.fetchall()) == 0:
        return None
    c.execute("select distinct "+split_on+" from \""+section+"\"")
    rows=c.fetchall()
    for column in rows:
        c.execute("select * from \""+section+"\" where "+split_on+"=?",[column[0]])
        file=os.path.join(filename,section+"."+column[0]+".csv")
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

        if args.csv:
            ensure_dir(basefilename+os.sep)
            fileout(db,basefilename,"mgstat")
            fileout(db,basefilename,"vmstat")
            fileout_splitcols(db,basefilename,"iostat","Device")
            fileout_splitcols(db,basefilename,"sar-d","DEV")
            fileout(db,basefilename,"perfmon")
            fileout(db,basefilename,"sar-u")

        if args.graphmgstat or args.all:
            ensure_dir(basefilename+os.sep)
            mgstat(db,basefilename)

        if args.graphvmstat or args.all:
            ensure_dir(basefilename+os.sep)
            vmstat(db,basefilename)

        if args.graphiostat or args.all:
            ensure_dir(basefilename+os.sep)
            iostat(db,basefilename)

    except OSError as e:
        print('Could not process pButtons file because: {}'.format(str(e)))
