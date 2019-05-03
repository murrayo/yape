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
    PreText,
)
from bokeh.layouts import column, row, WidgetBox

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import matplotlib.colors as colors

from .generic_tab import generic_tab


def cstat_tab(db):
    cstat1 = generic_tab(db, "cstatc11")
    cstat2 = generic_tab(db, "cstatc12")
    cstat3 = generic_tab(db, "cstatc13")
    cstat4 = generic_tab(db, "cstatc14")
    cstatD1 = generic_tab(db, "cstatD1")
    cstatD2 = generic_tab(db, "cstatD2")
    cstatD3 = generic_tab(db, "cstatD3")
    cstatD4 = generic_tab(db, "cstatD4")
    cstatD5 = generic_tab(db, "cstatD5")
    cstatD6 = generic_tab(db, "cstatD6")
    cstatD7 = generic_tab(db, "cstatD7")
    cstatD8 = generic_tab(db, "cstatD8")
    ts = [
        cstat1,
        cstat2,
        cstat3,
        cstat4,
        cstatD1,
        cstatD2,
        cstatD3,
        cstatD4,
        cstatD5,
        cstatD6,
        cstatD7,
        cstatD8,
    ]
    tabs = Tabs(tabs=list(filter(None.__ne__, ts)))
    tab = Panel(child=tabs, title="cstats")
    # tab = Panel(child=layout, title = mode)
    return tab
