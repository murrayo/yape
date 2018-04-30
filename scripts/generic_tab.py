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

def generic_tab(db,mode):
	c=db.cursor()
	c.execute("select * from \""+mode+"\"")
	text=""
	for r in c:
		l=r[0]
		text+=l
	content=PreText(text=text)
	layout = WidgetBox(content,sizing_mode="scale_both")
	tab = Panel(child=layout, title = mode)
	return tab
