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

def cstat_tab(db):
	cstat1=generic_tab(db,"cstatc11")
	cstat2=generic_tab(db,"cstatc12")
	cstat3=generic_tab(db,"cstatc13")
	cstat4=generic_tab(db,"cstatc14")
	tabs = Tabs(tabs = [cstat1,cstat2,cstat3,cstat4])
	tab = Panel(child=tabs, title = "cstats")
	#tab = Panel(child=layout, title = mode)
	return tab
