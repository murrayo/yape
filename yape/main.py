# os methods for manipulating paths
import os
import argparse

import sys
import bokeh
import csv

import sqlite3

from yape.parsepbuttons import parsepbuttons
from yape.plotpbuttons import mgstat

def fileout(db,filename,section):
    c = db.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [section])
    if len(c.fetchall()) == 0:
        return None
    print("exporting "+section+" to "+filename)
    c.execute("select * from \""+section+"\"")
    rows = c.fetchall()
    columns = [i[0] for i in c.description]
    with open(filename, "w") as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(columns)
        csvWriter.writerows(rows)

def yape2():
    parser = argparse.ArgumentParser(description='Yape 2.0')
    parser.add_argument("pButtons_file_name", help="path to pButtons file to use")
    parser.add_argument("--filedb",help="use specific file as DB, useful to be able to used afterwards or as standalone datasource")
    parser.add_argument("-c",dest='csv',help="will output the parsed tables as csv files. useful for further processing",action="store_true")
    parser.add_argument("--mgstat",dest='graphmgstat',help="plot mgstat data",action="store_true")
    parser.add_argument("-a","--all",dest='all',help="graph everything")
    parser.add_argument("-o","--out",dest='out',help="specify base output directory, default to the same directory the pbuttons file is in (graphs are create in a subdirectory)")
    args = parser.parse_args()

    try:
        if args.filedb is not None:
            db=sqlite3.connect(args.filedb)
        else:
            db=sqlite3.connect(":memory:")
        parsepbuttons(args.pButtons_file_name,db)

        if args.csv:
            basefilename=args.pButtons_file_name.split(".")[0]
            fileout(db,basefilename+".mgstat.csv","mgstat")
            fileout(db,basefilename+".vmstat.csv","vmstat")
            fileout(db,basefilename+".iostat.csv","iostat")
            fileout(db,basefilename+".sar-d.csv","sar-d")
            fileout(db,basefilename+".perfmon.csv","perfmon")
            fileout(db,basefilename+".sar-u.csv","sar-u")

        if args.graphmgstat:
            f=os.path.abspath(args.pButtons_file_name)
            basename=f.split(".")[0]
            mgstat(db,basename)


    except OSError as e:
        print('Could not process pButtons file because: {}'.format(str(e)))


if __name__ == "__main__":
    main()
