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

import matplotlib.pyplot as plt
import matplotlib.colors as colors

from .generic_tab import generic_tab


def ss_tab(db):

    ss_1_tab = generic_tab(db, "ss1")
    ss_2_tab = generic_tab(db, "ss2")
    ss_3_tab = generic_tab(db, "ss3")
    ss_4_tab = generic_tab(db, "ss4")
    ts = [ss_1_tab, ss_2_tab, ss_3_tab, ss_4_tab]
    tabs = Tabs(tabs=list(filter(None.__ne__, ts)))
    tab = Panel(child=tabs, title="%SS")
    # tab = Panel(child=layout, title = mode)
    return tab
