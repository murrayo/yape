import pandas as pd
import numpy
import sqlite3
import matplotlib

matplotlib.use("Agg")
import matplotlib.colors as colors
import matplotlib.dates as mdates
from matplotlib.dates import (
    DayLocator,
    HourLocator,
    MinuteLocator,
    SecondLocator,
    DateFormatter,
    drange,
    IndexDateFormatter,
    MO,
    TU,
    WE,
    TH,
    FR,
    SA,
    SU,
)
from matplotlib.ticker import FormatStrFormatter
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import AutoMinorLocator
import pytz
import re
import os
import mpl_toolkits.mplot3d
import matplotlib.pyplot as plt
from datetime import datetime
import logging


def dispatch_plot(df, column, outfile, config, device_name):
    genericplot(df, column, outfile, config, device_name)


def parse_tuple(string):
    try:
        s = eval(string)
        if type(s) == tuple:
            return s
        return
    except:
        return


def genericplot(df, column, outfile, config, device_name):
    timeframe = config["timeframe"]
    outfile = outfile.replace(":", ".")
    logging.info("creating " + outfile)

    dim = (16, 6)
    markersize = 1
    style = "-"
    marker = ""

    colormapName = "Set1"
    plt.style.use("seaborn-whitegrid")
    palette = plt.get_cmap(colormapName)
    colour = palette(1)

    # Is this a numeric column?
    try:
        column_type = str(df[column].dtype)
    except AttributeError:
        column_type = "unknown"

    if column_type == "float64" or column_type == "int64":
        logging.debug(column_type)
    else:
        return

    try:
        dim = parse_tuple("(" + config["plotting"]["dim"] + ")")
    except KeyError:
        pass
    try:
        markersize = float(config["plotting"]["markersize"])
    except KeyError:
        pass
    try:
        style = config["plotting"]["style"]
    except KeyError:
        pass

    if style == "":
        marker = "o"

    # Defaults or override with config file

    fig, ax = plt.subplots(figsize=dim, dpi=80, facecolor="w", edgecolor="dimgrey")

    if timeframe is not None:
        ax.plot(
            df[column][timeframe.split(",")[0] : timeframe.split(",")[1]],
            alpha=0.7,
            color=colour,
            linestyle=style,
            markersize=markersize,
            marker=marker
        )
    else:
        ax.plot(
            df[column],
            alpha=0.7,
            color=colour,
            linestyle=style,
            markersize=markersize,
            marker=marker
        )

    plt.grid(which="both", axis="both", linestyle="--")

    # vmstat make chart top "100"
    if column == "us" or column == "sy" or column == "wa" or column == "Total CPU":
        ax.set_ylim(ymax=100)

    # y axis
    ax.get_yaxis().set_major_formatter(
        plt.FuncFormatter(lambda x, loc: "{:,}".format(float(x)))
    )

    ax.set_ylim(ymin=0)  # Always zero start

    if df[column].max() > 10:
        ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("{x:,.0f}"))
    else:
        ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("{x:,.3f}"))

    # if df[column].max() > 999:
    #    ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter("{x:,.0f}"))
    # else:
    #    ax.yaxis.set_major_formatter(ScalarFormatter(useOffset=None))
    #    ax.get_yaxis().get_major_formatter().set_scientific(False)

    # Try to be smarter with the x axis. more to come
    if timeframe is not None and timeframe != "":
        StartTime = datetime.strptime(timeframe.split(",")[0], "%Y-%m-%d %H:%M:%S")
        EndTime = datetime.strptime(timeframe.split(",")[-1], "%Y-%m-%d %H:%M:%S")

        TotalMinutes = (EndTime - StartTime).total_seconds() / 60
        logging.debug("TF Minutes: " + str(TotalMinutes))
    else:
        StartTime = df.index[0]
        EndTime = df.index[-1]

        # logging.debug("Sart Date: "+str(StartTime))
        # logging.debug("End  Date: "+str(EndTime))

        TotalMinutes = (df.index[-1] - df.index[0]).total_seconds() / 60
        logging.debug("All Minutes: " + str(TotalMinutes))

    if TotalMinutes <= 15:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
        ax.xaxis.set_major_locator(
            mdates.SecondLocator(interval=int((TotalMinutes * 60) / 10))
        )
    elif TotalMinutes <= 180:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        ax.xaxis.set_major_locator(
            mdates.MinuteLocator(interval=int(TotalMinutes / 10))
        )
    elif TotalMinutes <= 1500:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
        ax.xaxis.set_major_locator(mdates.HourLocator())
    elif TotalMinutes <= 3000:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d-%H:%M"))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %m/%d - %H:%M"))

    StartTimeStr = datetime.strftime(StartTime, "%a %Y-%m-%d %H:%M:%S")
    EndTimeStr = datetime.strftime(EndTime, "%a %Y-%m-%d %H:%M:%S")
    
    if device_name == "":
        plt.title(
            column + " between " + StartTimeStr + " and " + EndTimeStr, fontsize=12
        )
    else:
        plt.title(
            device_name
            + " : "
            + column
            + " between "
            + StartTimeStr
            + " and "
            + EndTimeStr,
            fontsize=12,
        )
    # plt.xlabel("Time", fontsize=10)
    plt.tick_params(labelsize=10)

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(outfile, bbox_inches="tight")

    plt.close()


# need this as utility, since pandas timestamps are not compaitble with sqlite3 timestamps
# there's a possible other solution by using using converters in sqlite, but I haven't explored that yet
def fix_index(df):
    df.index = pd.to_datetime(df["datetime"])
    df = df.drop(["datetime"], axis=1)
    df.index.name = "datetime"
    return df


def plot_subset_split(db, config, subsetname, split_on):
    fileprefix = config["fileprefix"]
    timeframe = config["timeframe"]
    basename = config["basefilename"]
    plotDisks = config["plotDisks"]

    if not check_data(db, subsetname):
        return None
    c = db.cursor()
    c.execute("select distinct " + split_on + ' from "' + subsetname + '"')
    rows = c.fetchall()
    for column in rows:
        # If specified only plot selected disks for iostat - saves time and space
        if len(plotDisks) > 0 and subsetname == "iostat" and column[0] not in plotDisks:
            logging.info("Skipping plot subsection: " + column[0])
        else:
            logging.info("Including plot subsection: " + column[0])
            c.execute(
                'select * from "' + subsetname + '" where ' + split_on + "=?",
                [column[0]],
            )
            data = pd.read_sql_query(
                'select * from "'
                + subsetname
                + '" where '
                + split_on
                + '="'
                + column[0]
                + '"',
                db,
            )
            if len(data["datetime"][0].split()) == 1:
                # another evil hack for iostat on some redhats (no complete timestamps)
                # the datetime field only has '09/13/18' instead of '09/13/18 14:39:49'
                # -> take timestamps from mgstat
                data = data.drop("datetime", axis=1)
                size = data.shape[0]
                # one of those evil OS without datetime in vmstat
                # evil hack: take index from mgstat (we should have that in every pbuttons) and map that
                # is going to horribly fail when the number of rows doesn't add up ---> TODO for later
                dcolumn = pd.read_sql_query("select datetime from mgstat", db)
                ##since mgstat has only one entry per timestamp, but iostat has one entry per timestamp per device
                ##we need to duplicate the rows appropriately which is data.shape[0]/dcolumn.shape[0]) times
                # dcolumn=dcolumn.loc[dcolumn.index.repeat(size/dcolumn.shape[0])].reset_index(drop=True)

                data.index = pd.to_datetime(dcolumn["datetime"][:size])
                data.index.name = "datetime"
            else:
                data = fix_index(data)
            data = data.drop([split_on], axis=1)
            for key in data.columns.values:
                if timeframe is not None:
                    file = os.path.join(
                        basename,
                        fileprefix
                        + subsetname
                        + "."
                        + column[0]
                        + "."
                        + key.replace("/", "_")
                        + "."
                        + timeframe
                        + ".png",
                    )
                else:
                    file = os.path.join(
                        basename,
                        fileprefix
                        + subsetname
                        + "."
                        + column[0]
                        + "."
                        + key.replace("/", "_")
                        + ".png",
                    )
                logging.debug(key)
                dispatch_plot(data, key, file, config, column[0])


def plot_subset(db, config, subsetname):
    fileprefix = config["fileprefix"]
    timeframe = config["timeframe"]
    basename = config["basefilename"]
    if not check_data(db, subsetname):
        return None
    data = pd.read_sql_query('select * from "' + subsetname + '"', db)

    if "datetime" not in data.columns.values:
        logging.debug("No datetime")
        size = data.shape[0]
        # one of those evil OS without datetime in vmstat
        # evil hack: take index from mgstat (we should have that in every pbuttons) and map that
        # is going to horribly fail when the number of rows doesn't add up ---> TODO for later
        dcolumn = pd.read_sql_query("select datetime from mgstat", db)
        data.index = pd.to_datetime(dcolumn["datetime"][:size])
        data.index.name = "datetime"

    else:
        data = fix_index(data)

    # if vmstat add an extra column
    #
    if subsetname == "vmstat":
        data["Total CPU"] = 100 - data["id"]

    for key in data.columns.values:  # key is the column name

        if timeframe is not None:
            file = os.path.join(
                basename,
                fileprefix
                + subsetname
                + "."
                + key.replace("\\", "_").replace("/", "_")
                + "."
                + timeframe
                + ".png".replace("%", "_"),
            )
        else:
            file = os.path.join(
                basename,
                fileprefix
                + subsetname
                + "."
                + key.replace("\\", "_").replace("/", "_")
                + ".png".replace("%", "_"),
            )

        dispatch_plot(data, key, file, config, "")


def check_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [name])
    if len(cur.fetchall()) == 0:
        logging.warning("no data for:" + name)
        return False
    return True


def mgstat(db, config):
    logging.debug(config)
    plot_subset(db, config, "mgstat")


def perfmon(db, config):
    plot_subset(db, config, "perfmon")


def vmstat(db, config):
    plot_subset(db, config, "vmstat")


def iostat(db, config):
    plot_subset_split(db, config, "iostat", "Device")


def monitor_disk(db, config):
    plot_subset_split(db, config, "monitor_disk", "device")


def sard(db, config):
    plot_subset_split(db, config, "sard", "device")


def saru(db, config):
    plot_subset_split(db, config, "sar-u", "CPU")
