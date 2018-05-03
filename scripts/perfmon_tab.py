# pandas and numpy for data manipulation
import pandas as pd
import numpy as np
import sqlite3

from bokeh.plotting import Figure
from bokeh.models import (CategoricalColorMapper, HoverTool,
						  ColumnDataSource, Panel,
						  FuncTickFormatter, SingleIntervalTicker, LinearAxis)
from bokeh.models import Legend
from bokeh.models.widgets import (CheckboxGroup, Slider, RangeSlider,
								  Tabs, CheckboxButtonGroup,
								  TableColumn, DataTable, Select)
from bokeh.layouts import column, row, WidgetBox

import matplotlib.pyplot as plt
import matplotlib.colors as colors

def perfmon_tab(db):
    def make_dataset(perfmon_list):
        newdf=perfmon[perfmon_list]
        # Convert dataframe to column data source
        return ColumnDataSource(newdf)
    def make_plot(src):
        # Blank plot with correct labels
        p = Figure(plot_width = 1024, plot_height = 768,x_axis_type="datetime",
                  title = 'perfmon')
        cm = plt.get_cmap('gist_rainbow')

        numlines = len(perfmon.columns)
        mypal=[cm(1.*i/numlines) for i in range(numlines)]
        mypal=list(map(lambda x: colors.rgb2hex(x), mypal))
        col=0
        legenditems=[]
        for key in src.data.keys():
            if key=='datetime':
                continue
            l=key+" "
            col=col+1
            cline=p.line(perfmon.index.values,perfmon[key],line_width=1,alpha=0.8,color=mypal[col])
            legenditems+=[(key,[cline])]
        p.legend.click_policy="hide"
        legend = Legend(items=legenditems, location=(0, -30))
        p.add_layout(legend, 'below')
        return p

    def update(attr, old, new):
        perfmons_to_plot = [perfmon_selection.labels[i] for i in perfmon_selection.active]
        new_src = make_dataset(perfmons_to_plot)
        plot=make_plot(new_src)
        #TODO:crude hack in lack of a better solution so far
        layout.children[1]=plot

    #get data from DB, setup index
    cur=db.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",["perfmon"])
    if len(cur.fetchall())==0:
        return None
    perfmon=pd.read_sql_query("select * from perfmon",db)
    perfmon.index=pd.to_datetime(perfmon['datetime'])
    perfmon=perfmon.drop(['datetime'],axis=1)
    perfmon.index.name='datetime'

    perfmon_selection = CheckboxGroup(labels=list(perfmon.columns),
                                      active = [0,5],width=300,height=1000)

    perfmon_list=[perfmon_selection.labels[i] for i in perfmon_selection.active]
    src=make_dataset(perfmon_list)

    plot = make_plot(src)
    perfmon_selection.on_change('active', update)
    controls=WidgetBox(perfmon_selection,width=300,height=1000)

    layout = row(controls,plot)
    tab = Panel(child=layout, title = 'perfmon')
    return tab
