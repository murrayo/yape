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


def iostat_tab(db):
    def make_dataset(iostat_list):
        newdf = iostat[iostat_list]
        # Convert dataframe to column data source
        return ColumnDataSource(newdf)

    def make_plot(src):
        # Blank plot with correct labels
        p = Figure(
            plot_width=1024,
            plot_height=768,
            x_axis_type="datetime",
            title="iostat",
            output_backend="webgl",
        )
        cm = plt.get_cmap("gist_rainbow")

        numlines = len(iostat.columns)
        mypal = [cm(1.0 * i / numlines) for i in range(numlines)]
        mypal = list(map(lambda x: colors.rgb2hex(x), mypal))
        col = 0
        legenditems = []
        for key in src.data.keys():
            if key == "datetime":
                continue
            l = key + " "
            col = col + 1
            p.line(
                iostat.index.values,
                iostat[key],
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
        iostats_to_plot = [iostat_selection.labels[i] for i in iostat_selection.active]
        new_src = make_dataset(iostats_to_plot)
        plot = make_plot(new_src)
        # TODO:crude hack in lack of a better solution so far
        layout.children[1] = plot

    # get data from DB, setup index
    cur = db.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", ["iostat"]
    )
    if len(cur.fetchall()) == 0:
        return None
    iostat = pd.read_sql_query("select * from iostat", db)
    iostat.index = pd.to_datetime(iostat["datetime"])
    iostat = iostat.drop(["datetime"], axis=1)
    iostat.index.name = "datetime"
    iostat_selection = CheckboxGroup(labels=list(iostat.columns), active=[0, 5])

    iostat_list = [iostat_selection.labels[i] for i in iostat_selection.active]
    src = make_dataset(iostat_list)

    plot = make_plot(src)

    iostat_selection.on_change("active", update)
    controls = WidgetBox(iostat_selection)

    layout = row(controls, plot)
    tab = Panel(child=layout, title="iostat")
    return tab
