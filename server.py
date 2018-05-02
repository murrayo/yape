# Hello, Flask!
from flask import Flask, render_template, request
from flask import g

DATABASE = ':memory:'

import pandas as pd

from bokeh.embed import components
from bokeh.models import (CategoricalColorMapper, HoverTool,
						  ColumnDataSource, Panel,
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from bokeh.plotting import Figure

# os methods for manipulating paths
from os.path import dirname, join
import argparse

import sqlite3

from scripts.parsepbuttons import parsepbuttons

parser = argparse.ArgumentParser(description='Provide an interactive visualization to pButtons')
parser.add_argument("pButtons_file_name", help="Path and pButtons to use")
args = parser.parse_args()

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()



# Index page, no args
@app.route('/')
def index():
	name = request.args.get("name")
	if name == None:
		name = "Edward"
	return render_template("index.html", name=args.pButtons_file_name)

@app.route('/mgstat', methods = ['GET', 'POST'])
def mgstat():
    db=get_db()
    parsepbuttons(args.pButtons_file_name,db)
    mgstat=pd.read_sql_query("select * from mgstat",db)
    mgstat.index=pd.to_datetime(mgstat['datetime'])
    mgstat.index.name='datetime'
    mgstat=mgstat.drop(['datetime'],axis=1)
    columns=mgstat.columns.values
    return render_template("mgstat.html",columns=columns)
# With debug=True, Flask server will auto-reload
# when there are code changes
if __name__ == '__main__':
	app.run(port=5000, debug=True)
