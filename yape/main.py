# os methods for manipulating paths
from os.path import dirname, join
import argparse

import sys
import bokeh


import sqlite3

from .parsepbuttons import parsepbuttons


def main():
    parser = argparse.ArgumentParser(description='Provide an interactive visualization to pButtons')
    parser.add_argument("pButtons_file_name", help="Path and pButtons to use")
    parser.add_argument("--filedb",help="will use a file instead of in-memory db, to be able to used afterwards or as standalone datasource")
    args = parser.parse_args()

    try:
        if args.filedb is not None:
            db=sqlite3.connect(args.filedb)
        else:
            db=sqlite3.connect(":memory:")
        parsepbuttons(args.pButtons_file_name,db)


    except OSError as e:
        print('Could not process pButtons file because: {}'.format(str(e)))
