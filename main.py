# Pandas for data management
import pandas as pd

# os methods for manipulating paths
from os.path import dirname, join
import argparse

#holoview
import holoviews as hv
import holoviews.operation.datashader as hd
import sys
import bokeh

print("python:", sys.version)
print("bokeh:", bokeh.__version__)
print("holoviews:", hv.__version__)
# Bokeh basics
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs


import sqlite3

# Each tab is drawn by one script
from scripts.mgstat_tab import mgstat_tab
from scripts.generic_tab import generic_tab
from scripts.cstat_tab import cstat_tab
from scripts.ss_tab import ss_tab
from scripts.pselfy_tab import pselfy_tab
from scripts.vmstat_tab import vmstat_tab
from scripts.iostat_tab import iostat_tab

from scripts.parsepbuttons import parsepbuttons


parser = argparse.ArgumentParser(description='Provide an interactive visualization to pButtons')
parser.add_argument("pButtons_file_name", help="Path and pButtons to use")
args = parser.parse_args()

try:
    db=sqlite3.connect(":memory:")
    parsepbuttons(args.pButtons_file_name,db)

    # Create each of the tabs
    mgstat_tab = mgstat_tab(db)
    license_tab = generic_tab(db,"license")
    cpffile_tab = generic_tab(db,"cpffile")
    cstat_tab = cstat_tab(db)
    ss_tab = ss_tab(db)
    pselfy_tab = pselfy_tab(db)
    vmstat_tab = vmstat_tab(db)
    iostat_tab = iostat_tab(db)
    windowsinfo_tab = generic_tab(db,"windowsinfo")
    # Put all the tabs into one application
    ts=[mgstat_tab,vmstat_tab,iostat_tab,windowsinfo_tab,license_tab,cpffile_tab,cstat_tab,ss_tab,pselfy_tab]
    tabs = Tabs(tabs = list(filter(None.__ne__, ts)))
    #tabs = Tabs(tabs=[cstat_tab])

    # Put the tabs in the current document for display
    curdoc().add_root(tabs)
except OSError as e:
    print('Could not process pButtons file because: {}'.format(str(e)))
