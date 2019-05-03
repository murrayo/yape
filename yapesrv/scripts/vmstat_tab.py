# pandas and numpy for data manipulation
import pandas as pd
import numpy as np
import sqlite3

from bokeh.plotting import Figure
from bokeh.models import (
    CategoricalColorMapper,
    HoverTool,
    ColumnDataSource,
    Panel,
    FuncTickFormatter,
    SingleIntervalTicker,
    LinearAxis,
    Legend,
)
from bokeh.models.widgets import (
    CheckboxGroup,
    Slider,
    RangeSlider,
    Tabs,
    CheckboxButtonGroup,
    TableColumn,
    DataTable,
    Select,
)
from bokeh.layouts import column, row, WidgetBox

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.colors as colors


def vmstat_tab(db):
    def make_dataset(vmstat_list):
        newdf = vmstat[vmstat_list]
        # Convert dataframe to column data source
        return ColumnDataSource(newdf)

    def make_plot(src):
        # Blank plot with correct labels
        p = Figure(
            plot_width=1024,
            plot_height=768,
            x_axis_type="datetime",
            title="vmstat",
            output_backend="webgl",
        )
        cm = plt.get_cmap("gist_rainbow")

        numlines = len(vmstat.columns)
        mypal = [cm(1.0 * i / numlines) for i in range(numlines)]
        mypal = list(map(lambda x: colors.rgb2hex(x), mypal))
        col = 0
        legenditems = []
        for key in src.data.keys():
            if key == "datetime":
                continue
            l = key + " "
            col = col + 1
            cline = p.line(
                vmstat.index.values,
                vmstat[key],
                line_width=1,
                alpha=0.8,
                color=mypal[col],
            )
            legenditems += [(key, [cline])]
        p.legend.click_policy = "hide"
        legend = Legend(items=legenditems, location=(0, -30))
        p.add_layout(legend, "right")
        return p

    def update(attr, old, new):
        vmstats_to_plot = [vmstat_selection.labels[i] for i in vmstat_selection.active]
        new_src = make_dataset(vmstats_to_plot)
        plot = make_plot(new_src)
        layout.children[1] = plot

    # get data from DB, setup index
    cur = db.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", ["vmstat"]
    )
    if len(cur.fetchall()) == 0:
        return None
    vmstat = pd.read_sql_query("select * from vmstat", db)
    vmstat.index = pd.to_datetime(vmstat["datetime"])
    vmstat = vmstat.drop(["datetime"], axis=1)
    vmstat.index.name = "datetime"

    vmstat_selection = CheckboxGroup(labels=list(vmstat.columns), active=[0, 5])

    vmstat_list = [vmstat_selection.labels[i] for i in vmstat_selection.active]
    src = make_dataset(vmstat_list)
    vmstat_selection.on_change("active", update)
    plot = make_plot(src)
    controls = WidgetBox(vmstat_selection)
    layout = row(controls, plot)
    tab = Panel(child=layout, title="vmstat")
    return tab
