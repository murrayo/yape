# pandas and numpy for data manipulation
import pandas as pd
import numpy as np
import sqlite3

from bokeh.plotting import Figure
from bokeh.models import (CategoricalColorMapper, HoverTool,
						  ColumnDataSource, Panel,
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
								  Tabs, CheckboxButtonGroup,
								  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox

import matplotlib.pyplot as plt
import matplotlib.colors as colors

def iostat_tab(db):
    def make_dataset(iostat_list):
        newdf=iostat[iostat_list]
        # Convert dataframe to column data source
        return ColumnDataSource(newdf)
    def make_plot(src):
        # Blank plot with correct labels
        p = Figure(plot_width = 1024, plot_height = 768,x_axis_type="datetime",
                  title = 'iostat')
        cm = plt.get_cmap('gist_rainbow')

        numlines = len(iostat.columns)
        mypal=[cm(1.*i/numlines) for i in range(numlines)]
        mypal=list(map(lambda x: colors.rgb2hex(x), mypal))
        col=0
        for key in src.data.keys():
            if key=='datetime':
                continue
            l=key+" "
            col=col+1
            p.line(iostat.index.values,iostat[key],line_width=1,alpha=0.8,name=key,legend=key,color=mypal[col])
        p.legend.click_policy="hide"
        return p

    #get data from DB, setup index
    iostat=pd.read_sql_query("select * from iostat",db)
    iostat.index=pd.to_datetime(iostat['datetime'])
    iostat.index.name='datetime'

    src=make_dataset(iostat.columns.values)
    plot = make_plot(src)

    layout = row(plot)
    tab = Panel(child=layout, title = 'iostat')
    return tab
