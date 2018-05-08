# pandas and numpy for data manipulation
import pandas as pd
import numpy as np
import sqlite3

import holoviews as hv
hv.extension('bokeh')

from bokeh.plotting import Figure
from bokeh.models import (CategoricalColorMapper, HoverTool,
						  ColumnDataSource, Panel,
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
								  Tabs, CheckboxButtonGroup,
								  TableColumn, DataTable, Select,PreText)
from bokeh.layouts import column, row, WidgetBox

import matplotlib.pyplot as plt
import matplotlib.colors as colors

from .generic_tab import generic_tab

def pselfy_tab(db):

	cur=db.cursor()
	cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",["psefly"])
	if len(cur.fetchall())==0:
		return None
	pselfy_1_tab = generic_tab(db,"pselfy1")
	pselfy_2_tab = generic_tab(db,"pselfy2")
	pselfy_3_tab = generic_tab(db,"pselfy3")
	pselfy_4_tab = generic_tab(db,"pselfy4")
	tabs = Tabs(tabs = [pselfy_1_tab,pselfy_2_tab,pselfy_3_tab,pselfy_4_tab])
	tab = Panel(child=tabs, title = "ps -elfy")
	#tab = Panel(child=layout, title = mode)
	return tab
