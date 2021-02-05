# Pandas for data management
import pandas as pd

import sqlite3
import logging
import re
import sys
from datetime import date, datetime, timedelta

# splits an array into sub arrays with length size
def split(arr, size):
    arrs = []
    while len(arr) > size:
        piece = arr[:size]
        arrs.append(piece)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def validateDate(date_text):
    try:
        datetime.datetime.strptime(date_text, "%d/%m/%y")
    except ValueError:
        raise ValueError("Incorrect data format, should be mm/dd/yy")


# Are the dates in mm/dd/yy format?
def dateChecker(StartDate, dateStrIN):
    lConvertDates = ""

    # if date IN is yyyy convert test to mm/dd/yyyy
    yyyy = False
    if len(dateStrIN.split()[0]) > 8:
        yyyy = True
        StartDate = datetime.strptime(StartDate, "%m/%d/%y").strftime("%m/%d/%Y")
        logging.debug("Date format yyyy")

    # What did I get? "date" or "date time" or "date time AM"
    if len(dateStrIN.split()) == 1:  # Date only
        if dateStrIN != StartDate:
            # Is this xx/xx/yy or xx/xx/yyyy
            if yyyy:
                lConvertDates = "%d/%m/%Y"
            else:
                lConvertDates = "%d/%m/%y"

    elif len(dateStrIN.split()) == 2:  # date time
        if dateStrIN.split()[0] != StartDate:
            if yyyy:
                lConvertDates = "%d/%m/%Y %H:%M:%S"
            else:
                lConvertDates = "%d/%m/%y %H:%M:%S"

    elif len(dateStrIN.split()) == 3:  # date time AM/PM
        if dateStrIN.split()[0] != StartDate:
            if yyyy:
                lConvertDates = "%d/%m/%Y %I:%M:%S %p"
            else:
                lConvertDates = "%d/%m/%y %I:%M:%S %p"
        else:  # OK, but make 24 hour
            if yyyy:
                lConvertDates = "%m/%d/%Y %I:%M:%S %p"
            else:
                lConvertDates = "%m/%d/%y %I:%M:%S %p"

    logging.info("Date format: " + dateStrIN + " converted from : " + lConvertDates)

    return lConvertDates


# Make all date formats the same mm/dd/yy, especially bad in iostat and sar
def convertDateFormat(dateStrIN, lConvertDates):
    dateOut = dateStrIN

    if len(dateStrIN.split()) == 1:  # Date only
        # logging.debug("Date format: "+dateStrIN+" converted from : "+lConvertDates)
        dateOut = datetime.strptime(dateStrIN, lConvertDates).strftime("%m/%d/%y")

    elif len(dateStrIN.split()) == 2:  # xx/xx/yy hh:mm:ss
        # logging.debug("Date format: "+dateStrIN+" converted from : "+lConvertDates)
        dateOut = datetime.strptime(dateStrIN, lConvertDates).strftime(
            "%m/%d/%y %H:%M:%S"
        )

    if len(dateStrIN.split()) > 2:  # xx/xx/yy hh:mm:ss AM
        dateOut = datetime.strptime(dateStrIN, lConvertDates).strftime(
            "%m/%d/%y %H:%M:%S"
        )

        # logging.info(dateOut)

    return dateOut


def parsepbuttons(file, db):

    logger = logging.getLogger(__name__)

    # Files are parsed by reading the input pButtons file line by line.
    #
    # When a new section we care about is encountered, eg. "beg_mgstat" for mgstat;
    # An sqlite table is created using the column names in the OS command output
    # Each row is populated until the end of the section is encountered, eg. "end_mgstat".
    # Simple?
    #
    # Well the problem is different OS, and OS versions *may* output the same command in different ways.
    # Different column headings, or wildly different structure.
    # For example sar -u may be different in Red Hat and AIX. iostat is a terrible output to work with.
    # Some commands dont even have a time stamp! Date strings, espeially in windows performn can be a real pia.
    #
    # Over time exceptions are added to a section for the different operting systems and formats.
    # The version string determines can be used a filter, for example;
    # "Product Version String: Cache for UNIX (IBM AIX for System Power System-64) 2017.2.1 (Build 801) Wed Dec 6 2017 09:23:33 EST"
    # You now know its AIX at least.
    #
    # The basic steps are;
    # Set up a list of table columns and data types
    # Filter the sections based on whether they are able to be charted

    # Table columns and data types

    pbdtypes = {
        "tps": "REAL",
        "rd_sec/s": "REAL",
        "wr_sec/s": "REAL",
        "avgrq-sz": "REAL",
        "avgqu-sz": "REAL",
        "svctm": "REAL",
        "%util": "REAL",
        "Glorefs": "INTEGER",
        "RemGrefs": "INTEGER",
        "GRratio": "INTEGER",
        "PhyRds": "INTEGER",
        "Rdratio": "INTEGER",
        "Gloupds": "INTEGER",
        "RemGupds": "INTEGER",
        "Rourefs": "INTEGER",
        "RemRrefs": "INTEGER",
        "RouLaS": "INTEGER",
        "RemRLaS": "INTEGER",
        "PhyWrs": "INTEGER",
        "WDQsz": "INTEGER",
        "WDtmpq": "INTEGER",
        "WDphase": "INTEGER",
        "WIJwri": "INTEGER",
        "RouCMs": "INTEGER",
        "Jrnwrts": "INTEGER",
        "ActECP": "INTEGER",
        "Addblk": "INTEGER",
        "PrgBufL": "INTEGER",
        "PrgSrvR": "INTEGER",
        "BytSnt": "INTEGER",
        "BytRcd": "INTEGER",
        "WDpass": "INTEGER",
        "IJUcnt": "INTEGER",
        "IJULock": "INTEGER",
        "PPGrefs": "INTEGER",
        "PPGupds": "INTEGER",
        "CPU": "TEXT",
        "cpu": "TEXT",
        "%user": "REAL",
        "%nice": "REAL",
        "%system": "REAL",
        "%iowait": "REAL",
        "%steal": "REAL",
        "%idle": "REAL",
        "physc": "REAL",
        "%entc": "REAL",
        "r": "INTEGER",
        "b": "INTEGER",
        "swpd": "INTEGER",
        "free": "INTEGER",
        "buff": "INTEGER",
        "cache": "INTEGER",
        "si": "INTEGER",
        "so": "INTEGER",
        "bi": "INTEGER",
        "bo": "INTEGER",
        "in": "INTEGER",
        "cs": "INTEGER",
        "us": "INTEGER",
        "sy": "INTEGER",
        "id": "INTEGER",
        "wa": "INTEGER",
        "st": "INTEGER",
        "Device": "TEXT",
        "rrqm/s": "REAL",
        "wrqm/s": "REAL",
        "r/s": "REAL",
        "w/s": "REAL",
        "rkB/s": "REAL",
        "wkB/s": "REAL",
        "await": "REAL",
        "r_await": "REAL",
        "w_await": "REAL",
        "%usr": "INTEGER",
        "%sys": "INTEGER",
        "%win": "INTEGER",
        "%wio": "INTEGER",
        "%busy": "INTEGER",
        "avque": "REAL",
        "r+w/s": "INTEGER",
        "blks/s": "INTEGER",
        "avwait": "REAL",
        "avserv": "REAL",
        "w": "INTEGER",
        "swap": "INTEGER",
        "re": "INTEGER",
        "mf": "INTEGER",
        "pi": "INTEGER",
        "po": "INTEGER",
        "fr": "INTEGER",
        "de": "INTEGER",
        "sr": "INTEGER",
        "s3": "INTEGER",
        "s4": "INTEGER",
        "sd": "INTEGER",
        "GblSz": "INTEGER",
        "pGblNsz": "INTEGER",
        "pGblAsz": "INTEGER",
        "ObjSz": "INTEGER",
        "pObjNsz": "INTEGER",
        "pObjAsz": "INTEGER",
        "BDBSz": "INTEGER",
        "pBDBNsz": "INTEGER",
        "pBDBAsz": "INTEGER",
        "avm": "INTEGER",
        "at": "INTEGER",
        "RouSz": "INTEGER",
        "pRouAsz": "INTEGER",
        "Blk_read/s": "REAL",
        "Blk_wrtn/s": "REAL",
        "Blk_read": "INTEGER",
        "Blk_wrtn": "INTEGER",
        "rsec/s": "REAL",
        "wsec/s": "REAL",
        # AIX vmstat
        "fre": "INTEGER",
        "cy": "INTEGER",
        "pc": "REAL",
        "ec": "REAL",
    }

    # Some other useful variables

    mode = ""  # hold current parsing mode
    submode = ""  # further status var for ugly vms monitor data parsing
    cursor = db.cursor()
    count = 0
    sardate = ""
    sartime = ""
    osmode = ""
    colcache = []
    colcachenum = 0
    numcols = 0
    mgstatdate = ""
    started_before_midnight = False

    # Move generic items out of the loop we will not chart these

    generic_items = [
        "license",
        "ifconfig",
        "sysctl-a",
        "df-m",
        "mount",
        "cpffile",
        "fdisk-l",
        "ss1",
        "ss2",
        "ss3",
        "ss4",
        "linuxinfo",
        "ipcs",
        "cpu",
        "cstatc11",
        "cstatc12",
        "cstatc13",
        "cstatc14",
        "pselfy1",
        "pselfy2",
        "pselfy3",
        "pselfy4",
        "cstatD1",
        "cstatD2",
        "cstatD3",
        "cstatD4",
        "cstatD5",
        "cstatD6",
        "cstatD7",
        "cstatD8",
        "windowsinfo",
        "tasklist",
    ]

    cursor.execute("CREATE TABLE IF NOT EXISTS sections (section TEXT)")
    conditions = [
        {"match": "id=license", "mode": "license"},
        {"match": "id=cpffile", "mode": "cpffile"},
        {"match": "id=Windowsinfo", "mode": "windowsinfo"},
        {"match": "id=tasklist", "mode": "tasklist"},
        {"match": 'id="ss_1"', "mode": "ss1"},
        {"match": 'id="ss_2"', "mode": "ss2"},
        {"match": 'id="ss_3"', "mode": "ss3"},
        {"match": 'id="ss_4"', "mode": "ss4"},
        {"match": "id=ifconfig", "mode": "ifconfig"},
        {"match": "id=sysctl-a", "mode": "sysctl-a"},
        {"match": "id=linuxinfo", "mode": "linuxinfo"},
        {"match": "id=df-m", "mode": "df-m"},
        {"match": "id=cpu", "mode": "cpu"},
        {"match": "id=mount", "mode": "mount"},
        {"match": "id=fdisk-l", "mode": "fdisk-l"},
        {"match": 'id="cstat -c1_1"', "mode": "cstatc11"},
        {"match": 'id="cstat -c1_2"', "mode": "cstatc12"},
        {"match": 'id="cstat -c1_3"', "mode": "cstatc13"},
        {"match": 'id="cstat -c1_4"', "mode": "cstatc14"},
        {"match": 'id="cstat -D_1"', "mode": "cstatD1"},
        {"match": 'id="cstat -D_2"', "mode": "cstatD2"},
        {"match": 'id="cstat -D_3"', "mode": "cstatD3"},
        {"match": 'id="cstat -D_4"', "mode": "cstatD4"},
        {"match": 'id="cstat -D_5"', "mode": "cstatD5"},
        {"match": 'id="cstat -D_6"', "mode": "cstatD6"},
        {"match": 'id="cstat -D_7"', "mode": "cstatD7"},
        {"match": 'id="cstat -D_8"', "mode": "cstatD8"},
        {"match": 'id="ps -elfy_1"', "mode": "pselfy1"},
        {"match": 'id="ps -elfy_2"', "mode": "pselfy2"},
        {"match": 'id="ps -elfy_3"', "mode": "pselfy3"},
        {"match": 'id="ps -elfy_4"', "mode": "pselfy4"},
        {"match": "id=ipcs", "mode": "ipcs"},
    ]

    # Start reading the pButtons file

    with open(file, encoding="latin-1") as f:
        insertquery = ""
        lConvertDates = ""
        skipline = 0
        for line in f:
            if skipline > 0:
                skipline -= 1
                continue
            if not line.strip():
                continue
            if "<pre>\n" == line:
                continue

            # determine parsing states
            if "Topofpage" in line and mode != "":
                logging.debug("end of " + mode)
                if colcachenum > 0:
                    cursor.executemany(insertquery, colcache)
                    colcache = []
                    colcachenum = 0
                query = ""
                insertquery = ""
                mode = ""
                lConvertDates = ""
            if "end_mgstat" in line:
                logging.debug("end of " + mode)
                query = ""
                count = 0
                insertquery = ""
                mode = ""
                lConvertDates = ""
            if "end_sar_u" in line:
                logging.debug("end of " + mode)
                query = ""
                count = 0
                insertquery = ""
                mode = ""
                lConvertDates = ""
            if "An empty file was created." in line:
                logging.debug("empty " + mode + " section")
                continue
            # add better osmode detection

            # Get start date and time and use for validating date formats of OS commands
            # Profile run "24Hours_5Sec" started at 00:01:00 on Apr 08 2019.
            # or e.g. HH:MM no SS
            # Profile run "24Hour_5Sec" started at 00:01 on Oct 15 2020.

            if "Profile run" in line:
                line = line.strip()
                logging.info(line)
                timeanddateList = line.split("at ")

                StartTimeStr = timeanddateList[1].split(" on ")[0]
                if len(StartTimeStr) == 8:  # HH:MM:SS
                    pass
                elif len(StartTimeStr) == 5:  # HH:MM
                    StartTimeStr = datetime.strptime(StartTimeStr, "%H:%M").strftime(
                        "%H:%M:%S"
                    )
                else:
                    logging.critical("Profile section time problem: %s", line)
                    sys.exit(1)

                StartDateStr = timeanddateList[1].split(" on ")[1].rstrip(".")
                if len(StartDateStr) == 11:  # 4 digit year
                    StartDateStr = datetime.strptime(StartDateStr, "%b %d %Y").strftime(
                        "%m/%d/%y"
                    )
                elif len(StartDateStr) == 9:  # 2 digit year
                    StartDateStr = datetime.strptime(StartDateStr, "%b %d %y").strftime(
                        "%m/%d/%y"
                    )
                else:
                    logging.critical("Profile section date problem: %s", line)
                    sys.exit(1)

                StartTimeHour = datetime.strptime(StartTimeStr, "%H:%M:%S").time()
                StartTimeCheck = datetime.strptime("23:45:00", "%H:%M:%S").time()

                # Probably meant to start at midnight - results without dates will be fudged to be next day
                if StartTimeHour > StartTimeCheck:
                    logger.info(f"Started before midnight ({str(StartTimeHour)})")
                    started_before_midnight = True

                StartDateStartTimeStr = StartDateStr + " " + StartTimeStr
                logging.info("Start at: " + StartDateStartTimeStr)
                continue

            if "Version String" in line:
                if "HP HP-UX for Itanium" in line:
                    osmode = "hpux"
                    continue
                if "Solaris for SPARC-64" in line:
                    osmode = "solsparc"
                    continue
                if "OpenVMS/IA64" in line:
                    osmode = "openvms"
                if "Linux" in line:
                    osmode = "linux"
                    continue
                if "AIX" in line:
                    osmode = "AIX"
                    continue
                if "Ubuntu Server LTS" in line:
                    osmode = "ubuntu"
                    continue

            # Is this one of the generic sections?
            matched = False
            for c in conditions:
                if c["match"] in line:
                    matched = True
                    mode = c["mode"]
                    logging.debug("starting " + mode)
                    query = 'CREATE TABLE IF NOT EXISTS "' + mode + '" (line TEXT)'
                    cursor.execute(query)
                    db.commit()
                    continue
            if matched:
                continue

            # vmstat
            if "<pre><!-- beg_vmstat -->" == line:
                continue
            if mode == "vmstat" and ("beg_vmstat" in line):
                continue
            if mode == "vmstat" and ("swpd" in line):  # eg Red Hat
                colnames = line.split()[2:]
                numcols = len(colnames) + 2
                added = []
                query = 'CREATE TABLE IF NOT EXISTS vmstat("datetime" TEXT,'
                insertquery = "INSERT INTO vmstat VALUES (?,"
                for c in colnames:
                    t = c
                    if c in added:
                        t = c + "_1"
                        added.append(t)
                    else:
                        added.append(c)
                    query += '"' + t + '" ' + (pbdtypes.get(c) or "TEXT") + ","
                    insertquery += "?,"
                query = query[:-1]
                insertquery = insertquery[:-1]
                query += ")"
                insertquery += ")"
                logging.debug(insertquery)
                cursor.execute(query)
                db.commit()
                continue
            if "id=vmstat>" in line:
                mode = "vmstat"
                count = 0
                logging.info("starting " + mode)
                if "beg_vmstat" not in line:
                    continue
                if (
                    osmode == "sunos"
                    or osmode == "solsparc"
                    or osmode == "hpux"
                    or osmode == "ubuntu"
                ):
                    colnames = line.split("<pre>")[1].split()
                    colnames = list(map(lambda x: x.strip(), colnames))
                    numcols = len(colnames)
                    added = []
                    query = "CREATE TABLE IF NOT EXISTS vmstat("
                    insertquery = "INSERT INTO vmstat VALUES ("
                    for c in colnames:
                        t = c
                        if c in added:
                            t = c + "_1"
                            added.append(t)
                        else:
                            added.append(c)
                        query += '"' + t + '" ' + (pbdtypes.get(c) or "TEXT") + ","
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                elif osmode == "AIX":
                    colnames = line.split("<pre>")[1].split()
                    colnames = list(map(lambda x: x.strip(), colnames))[
                        0:-3
                    ]  # time (hr mi se) will moved from end to datetime
                    numcols = len(colnames) + 1
                    added = []
                    query = 'CREATE TABLE IF NOT EXISTS vmstat("datetime" TEXT,'
                    insertquery = "INSERT INTO vmstat VALUES (?,"
                    for c in colnames:
                        t = c
                        if c in added:
                            t = c + "_1"
                            added.append(t)
                        else:
                            added.append(c)
                        query += '"' + t + '" ' + (pbdtypes.get(c) or "TEXT") + ","
                        insertquery += "?,"
                    logging.debug(query)
                    logging.debug(insertquery)
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                else:
                    # ugh :/
                    colnames = line.split("<pre>")[1].split()[2:]
                    numcols = len(colnames) + 2
                    added = []
                    query = 'CREATE TABLE IF NOT EXISTS vmstat("datetime" TEXT,'
                    insertquery = "INSERT INTO vmstat VALUES (?,"
                    for c in colnames:
                        t = c
                        if c in added:
                            t = c + "_1"
                            added.append(t)
                        else:
                            added.append(c)
                        query += '"' + t + '" ' + (pbdtypes.get(c) or "TEXT") + ","
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                    logging.debug(query)
                    logging.debug(insertquery)

                cursor.execute(query)
                db.commit()
                count = 0
                continue

            if "id=sar-u" in line:
                query = ""
                lConvertDates = ""
                count = 0
                if "SunOS" in line:
                    osmode = "sunos"
                    sardate = line.split()[-1]
                if "HP-UX" in line:
                    sardate = line.split()[-1]
                insertquery = ""
                mode = "sar-u"
                logging.info("starting " + mode + " osmode " + osmode + ".")
                continue
            if "id=iostat" in line:
                query = ""
                count = 0
                insertquery = ""
                mode = "iostat"
                lConvertDates = ""
                logging.info("starting " + mode)
                continue
            if "id=sar-d" in line:
                query = ""
                count = 0
                insertquery = ""
                mode = "sar-d"
                lConvertDates = ""
                logging.info("starting " + mode)
                continue
            if "beg_mgstat" in line:
                query = ""
                insertquery = ""
                mode = "mgstat"
                lConvertDates = ""
                logging.info("starting " + mode)
                continue
            if "id=perfmon" in line:
                query = ""
                insertquery = ""
                mode = "perfmon"
                logging.info("starting " + mode)
                lConvertDates = ""
                perfmon_time_separate = False
                continue
            if "id=monitor" in line:
                query = ""
                insertquery = ""
                mode = "monitor"
                lConvertDates = ""
                logging.info("starting " + mode)
                continue

            # actual parsing things
            if mode == "sar-d":
                if osmode == "AIX":  # Bail, TBD
                    continue
                if "Linux" in line:
                    cols = line.split()
                    sardate = cols[3]
                    if query == "":  # First time in check start date
                        lConvertDates = dateChecker(StartDateStr, sardate)
                    if lConvertDates != "":
                        sardate = convertDateFormat(sardate, lConvertDates)
                    # Increment date if most of the activity is the next day
                    if started_before_midnight:
                        logger.info(f"sardate is {sardate}")
                        early_date = datetime.strptime(sardate, "%m/%d/%y").date()
                        early_date += timedelta(days=1)
                        sardate = datetime.strftime(early_date, "%m/%d/%y")
                        logger.info(f"new sardate is {sardate}")
                    continue
                if "HP-UX" in line:
                    osmode = "hpux"
                    sardate = line.split()[-1]
                    if query == "":  # First time in check start date
                        lConvertDates = dateChecker(StartDateStr, sardate)
                    if lConvertDates != "":
                        sardate = convertDateFormat(sardate, lConvertDates)
                    # Increment date if most of the activity is the next day
                    if started_before_midnight:
                        logger.info(f"sardate is {sardate}")
                        early_date = datetime.strptime(sardate, "%m/%d/%y").date()
                        early_date += timedelta(days=1)
                        sardate = datetime.strftime(early_date, "%m/%d/%y")
                        logger.info(f"new sardate is {sardate}")
                    continue
                if "Average" in line:
                    continue
                if "SunOS" in line:
                    osmode = "sunos"
                    sardate = line.split()[-1]
                    if query == "":  # First time in check start date
                        lConvertDates = dateChecker(StartDateStr, sardate)
                    if lConvertDates != "":
                        sardate = convertDateFormat(sardate, lConvertDates)
                    continue
                if ("tps" in line or "device" in line) and query == "":
                    logging.debug("osmode:" + osmode)
                    cols = list(map(lambda x: x.strip(), line.split()))
                    numcols = len(cols)
                    query = "CREATE TABLE IF NOT EXISTS sard(datetime TEXT,"
                    insertquery = "INSERT INTO sard VALUES (?,"
                    skipcols = 2
                    if osmode == "linux":
                        skipcols = 1
                        if "PM" in cols or "AM" in cols:
                            skipcols = 2
                    if osmode == "sunos":
                        skipcols = 1
                    if osmode == "hpux":
                        skipcols = 1
                    for c in cols[skipcols:]:
                        query += (
                            '"'
                            + c.replace("DEV", "device")
                            + '" '
                            + (pbdtypes.get(c) or "TEXT")
                            + ","
                        )
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                    logging.debug("create query:" + query)
                    logging.debug("insert query:" + insertquery)
                    cursor.execute(query)
                    db.commit()
                    continue
                elif "tps" in line or "device" in line:
                    continue
                cols = line.split()
                if osmode == "sunos" or osmode == "hpux":
                    if len(cols) == numcols:
                        sartime = cols[0]
                        cols = [(sardate + " " + cols[0])] + cols[1:]
                    else:
                        cols = [(sardate + " " + sartime)] + cols
                elif osmode == "linux":
                    if "PM" in cols or "AM" in cols:
                        currentdate = sardate + " " + cols[0] + " " + cols[1]
                        cols = [currentdate] + cols[2:]
                    else:
                        currentdate = sardate + " " + cols[0]
                        cols = [currentdate] + cols[1:]
                else:
                    currentdate = cols[0] + " " + cols[1]
                    cols = [currentdate] + cols[2:]
                # deal with data not being logged on hp-ux sometimes with high load
                if len(cols) == insertquery.count("?"):
                    colcache.append(cols)
                else:
                    logging.debug("invalid column found in sar-d" + str(line))
                colcachenum += 1
                if colcachenum == 10000:
                    cursor.executemany(insertquery, colcache)
                    colcache = []
                    colcachenum = 0
                count += 1
                if count % 10000 == 0:
                    db.commit()
                    logging.debug(str(count) + ".")

            if mode == "iostat":  # Build table column names
                if "avg-cpu:" in line:
                    skipline = 1
                    continue
                if osmode == "hpux":  # Bail, TBD
                    continue
                if osmode == "AIX":  # Bail, TBD
                    continue
                # Linux 3.10.0-229.el7.x86_64 (BPH-PRODTRAK.bdms.co.th) 	06/14/2019 	_x86_64_	(12 CPU)
                # Linux 3.0.101-0.47.52-default (TRAKDBPROD01) 	10/28/2019 	_x86_64_
                if len(line.split()) in (5, 6, 7) and "Linux" in line:
                    currentdate = line.split()[3]
                    if query == "":  # First time in check start date
                        lConvertDates = dateChecker(StartDateStr, currentdate)
                    if lConvertDates != "":
                        currentdate = convertDateFormat(currentdate, lConvertDates)
                    continue
                if "Linux" in line:
                    continue
                if len(line.split()) == 2:  # date and time
                    currentdate = line.strip()
                    if query == "":  # First time in check start date
                        lConvertDates = dateChecker(StartDateStr, currentdate)
                    if lConvertDates != "":
                        currentdate = convertDateFormat(currentdate, lConvertDates)
                    continue
                if len(line.split()) == 3:  # date time AM
                    currentdate = line.strip()
                    if query == "":  # First time in check start date
                        lConvertDates = dateChecker(StartDateStr, currentdate)
                    if lConvertDates != "":
                        currentdate = convertDateFormat(currentdate, lConvertDates)
                    continue
                if "avg-cpu" in line:
                    skipline = 1
                    continue
                if "Device" in line and query == "":
                    cols = list(map(lambda x: x.strip(), line.split()))
                    query = 'CREATE TABLE IF NOT EXISTS iostat("datetime" TEXT,'
                    insertquery = "INSERT INTO iostat VALUES (?,"
                    for c in cols:
                        query += (
                            '"'
                            + c.replace(":", "")
                            + '" '
                            + (pbdtypes.get(c.replace(":", "")) or "TEXT")
                            + ","
                        )
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                    cursor.execute(query)
                    db.commit()
                    continue
                elif "Device" in line:
                    continue
                cols = line.split()
                cols = [currentdate.strip()] + cols
                db.execute(insertquery, cols)
                count += 1
                if count % 10000 == 0:
                    db.commit()
                    logging.debug(str(count) + ".")

            if mode == "vmstat":
                if "end_vmstat" in line:
                    continue
                cols = line.split()

                if osmode == "AIX":
                    cols = [(mgstatdate + " " + cols[-1])] + cols[0:-1]
                    # logging.debug(cols)

                if len(cols) != numcols:
                    logging.debug(str(len(cols)) + "." + str(numcols))
                    continue

                if not (
                    osmode == "solsparc"
                    or osmode == "sunos"
                    or osmode == "hpux"
                    or osmode == "ubuntu"
                    or osmode == "AIX"
                ):
                    cols = [(cols[0] + " " + cols[1])] + cols[2:]

                cursor.execute(insertquery, cols)
                count += 1
                if count % 10000 == 0:
                    db.commit()
                    logging.debug(str(count) + ".")

            if mode == "perfmon":
                if "end_win_perfmon" in line:
                    continue
                if query == "":

                    # Use a regular expression to find any (column names) within quotes and substitue
                    # e.g. get rid of  commas  in  column names
                    for quoted_part in re.findall(r"\"(.+?)\"", line):
                        line = line.replace(
                            quoted_part, quoted_part.replace(",", "ken")
                        )

                    # Could combine with above, but keeping in spirit of original structure
                    cols = line.split(",")

                    cols = list(map(lambda x: x[1:].replace('"', ""), cols))
                    cols = list(map(lambda x: x[1:].replace("(", "_"), cols))
                    cols = list(map(lambda x: x[1:].replace(")", "_"), cols))

                    # logger.info(list(map(lambda x: f"{x}", cols)))

                    if cols[1] == "Time":
                        perfmon_time_separate = True

                    query = "CREATE TABLE IF NOT EXISTS perfmon(datetime TEXT,"
                    insertquery = "INSERT INTO perfmon VALUES (?,"
                    for c in cols[1:]:
                        query += '"' + c + '" REAL,'
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                    cursor.execute(query)
                    db.commit()
                    continue
                cols = list(map(lambda x: x[1:-1].replace('"', ""), line.split(",")))
                cols = list(map(lambda x: 0.0 if x == " " else x, cols))

                if perfmon_time_separate == True:
                    cols[0] = cols[0] + " " + cols[1]

                cursor.execute(insertquery, cols)
                count += 1
                if count % 10000 == 0:
                    db.commit()
                    logging.debug(str(count) + ".")

            if mode == "mgstat":
                if "MGSTAT" in line:
                    continue
                if "No output file was created." in line:
                    logging.warning(
                        "mgstat error in pbuttons: No output file was created."
                    )
                    continue
                if not line.strip():
                    # ignore empty line (some rh mgstat on ~2016.1.x)
                    continue
                if "Date" in line:
                    cols = list(map(lambda x: x.strip(), line.split(",")))
                    query = 'CREATE TABLE IF NOT EXISTS mgstat("datetime" TEXT,'
                    insertquery = "INSERT INTO mgstat VALUES (?,"
                    for c in cols[2:]:
                        query += '"' + c + '" ' + (pbdtypes.get(c) or "TEXT") + ","
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                    cursor.execute(query)
                    db.commit()
                    continue

                cols = list(map(lambda x: x.strip(), line.split(",")))
                cols = [(cols[0] + " " + cols[1])] + cols[2:]
                if (
                    mgstatdate == ""
                ):  # Get start date for metrics that dont keep date like AIX vmstat
                    mgstatdate = cols[0].split()[0]

                try:
                    cursor.execute(insertquery, cols)
                except sqlite3.Error as e:
                    logging.error("Data insert error")
                    logging.error("tried to add:")
                    logging.error(line)
                    logging.error("last good:")
                    logging.error(lastgood)
                    logging.error("into query:")
                    logging.error(insertquery)
                    logging.error(e)
                    sys.exit(1)
                count += 1
                lastgood = line
                if count % 10000 == 0:
                    db.commit()
                    logging.debug(str(count) + ".")

            if mode == "sar-u":
                if "Linux" in line:
                    sardate = line.split()[3]
                    if query == "":  # First time in check start date
                        lConvertDates = dateChecker(StartDateStr, sardate)
                    if lConvertDates != "":
                        sardate = convertDateFormat(sardate, lConvertDates)
                    # Increment date if most of the activity is the next day
                    if started_before_midnight:
                        logger.info(f"sardate is {sardate}")
                        early_date = datetime.strptime(sardate, "%m/%d/%y").date()
                        early_date += timedelta(days=1)
                        sardate = datetime.strftime(early_date, "%m/%d/%y")
                        logger.info(f"new sardate is {sardate}")
                    continue
                if "AIX" in line:  # 5 May 2019. AIX7.2 + Cache 2017.2
                    sardate = line.split()[5]
                    if query == "":  # First time in check start date
                        lConvertDates = dateChecker(StartDateStr, sardate)
                    if lConvertDates != "":
                        sardate = convertDateFormat(sardate, lConvertDates)
                    continue
                    # Increment date if most of the activity is the next day
                    if started_before_midnight:
                        logger.info(f"sardate is {sardate}")
                        early_date = datetime.strptime(sardate, "%m/%d/%y").date()
                        early_date += timedelta(days=1)
                        sardate = datetime.strftime(early_date, "%m/%d/%y")
                        logger.info(f"new sardate is {sardate}")
                if (
                    "System" in line
                ):  # 5 May 2019. AIX7.2 + Cache 2017.2, extra line in sar-u
                    continue
                if not line.strip():  # Empty line
                    continue
                if "beg_sar_u" in line:
                    continue
                if "Average" in line:
                    continue
                if "%usr" in line and (osmode == "sunos" or osmode == "hpux"):
                    cols = list(map(lambda x: x.strip(), line.split()[1:]))
                    numcols = len(cols) + 1
                    query = 'CREATE TABLE IF NOT EXISTS "sar-u"("datetime" TEXT,'
                    insertquery = 'INSERT INTO "sar-u" VALUES (?,'
                    for c in cols:
                        query += '"' + c + '" ' + (pbdtypes.get(c) or "TEXT") + ","
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                    cursor.execute(query)
                    db.commit()
                    continue
                if "CPU" in line:
                    cols = list(map(lambda x: x.strip(), line.split()[1:]))
                    query = 'CREATE TABLE IF NOT EXISTS "sar-u"("datetime" TEXT,'
                    insertquery = 'INSERT INTO "sar-u" VALUES (?,'
                    for c in cols:
                        query += '"' + c + '" ' + (pbdtypes.get(c) or "TEXT") + ","
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                    logging.debug(query)
                    cursor.execute(query)
                    db.commit()
                    continue
                if "%entc" in line:  # 5 May 2019. AIX7.2 + Cache 2017.2
                    cols = list(map(lambda x: x.strip(), line.split()[1:]))
                    query = 'CREATE TABLE IF NOT EXISTS "sar-u"("datetime" TEXT,'
                    insertquery = 'INSERT INTO "sar-u" VALUES (?,'
                    for c in cols:
                        query += '"' + c + '" ' + (pbdtypes.get(c) or "TEXT") + ","
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                    logging.debug(query)
                    cursor.execute(query)
                    db.commit()
                    continue

                cols = list(map(lambda x: x.strip(), line.split()))
                if osmode == "hpux":
                    # hpux sar-u creates one line with all data, split it up chunks of 5
                    # first column of the line is the time
                    timecol = [sardate + " " + cols[0]]
                    for splitcols in split(cols[1:], 5):
                        cols = timecol + splitcols
                        # cursor.execute(insertquery, cols)
                        count += 1
                else:
                    if osmode == "sunos":
                        cols = [(sardate + " " + cols[0])] + cols[1:]
                    elif osmode == "AIX":  # 5 May 2019. AIX7.2 + Cache 2017.2
                        cols = [(sardate + " " + cols[0])] + cols[1:]
                        cursor.execute(insertquery, cols)
                        count += 1
                    else:
                        if cols[1] == "AM" or cols[1] == "PM":
                            cols[0] = datetime.strptime(
                                cols[0] + " " + cols[1], "%I:%M:%S %p"
                            ).strftime("%H:%M:%S")
                        cols = [(sardate + " " + cols[0])] + cols[1:]
                        cursor.execute(insertquery, cols)
                        count += 1

                if count % 10000 == 0:
                    # logging.debug(insertquery)
                    # logging.debug(cols)
                    db.commit()
                    logging.debug(str(count) + ".")

            if mode == "monitor":
                if "DISK I/O STATISTICS" in line:
                    submode = "disk"
                    query = 'CREATE TABLE IF NOT EXISTS "monitor_disk"("datetime" TEXT,"device" TEXT,"CUR" REAL,"AVE" REAL,"MIN" REAL,"MAX" REAL)'
                    insertquery = 'INSERT INTO "monitor_disk" VALUES (?,?,?,?,?,?)'
                    cursor.execute(query)
                    db.commit()
                    continue
                if "DISTRIBUTED LOCK MANAGEMENT STATISTICS" in line:
                    submode = "dist_lock_stats"
                    continue

                if "PROCESSES" in line:
                    submode = "processes"
                    query = 'CREATE TABLE IF NOT EXISTS "monitor_processes"("datetime" TEXT,"PID" TEXT,"STATE" TEXT,"PRI" INTEGER,"NAME" TEXT,"PAGES" TEXT,"DIOCNT" INTEGER,"FAULTS" INTEGER,"CPUTIME" TEXT)'
                    insertquery = (
                        'INSERT INTO "monitor_processes" VALUES (?,?,?,?,?,?,?,?,?)'
                    )
                    cursor.execute(query)
                    db.commit()
                    continue
                if "PAGE MANAGEMENT STATISTICS" in line:
                    submode = "page_stats"
                    continue
                if "I/O SYSTEM STATISTICS" in line:
                    submode = "system_io"
                    continue
                if "FILE PRIMITIVE STATISTICS" in line:
                    submode = "file_prim_stats"
                    continue
                if "LOCK MANAGEMENT STATISTICS" in line:
                    submode = "lock_stats"
                    continue
                if "DECNET STATISTICS" in line:
                    submode = "decnet"
                    continue
                if "FILE SYSTEM CACHING STATISTICS" in line:
                    submode = "caching_stats"
                    continue
                if "SCS STATISTICS" in line:
                    submode = "scs_stats"
                    continue
                if "MSCP SERVER STATISTICS" in line:
                    submode = "mscp_stats"
                    continue
                if "DISTRIBUTED TRANSACTION STATISTICS" in line:
                    submode = "dist_transaction_stats"
                    continue
                if "TIMER STATISTICS" in line:
                    submode = "timer_stats"
                    continue
                if "DYNAMIC LOCK REMASTERING STATISTICS" in line:
                    submode = "dynamic_lock_stats"
                    continue
                if "ALIGNMENT FAULT STATISTICS" in line:
                    submode = "align_fault"
                    continue

                if submode == "disk":
                    cols = list(map(lambda x: x.strip(), line.split()))
                    if len(cols) == 2:
                        diskdate = cols[0] + " " + cols[1]
                        continue
                    if (":" in line) and (len(cols) == 7):
                        cols = [(diskdate)] + [cols[0].replace(":", "")] + cols[3:]
                        cursor.execute(insertquery, cols)
                        count += 1
                        if count % 10000 == 0:
                            db.commit()
                            logging.debug(str(count) + ".")
                        continue
                    if (":" in line) and (len(cols) == 6):
                        cols = [(diskdate)] + [cols[0].replace(":", "")] + cols[2:]
                        cursor.execute(insertquery, cols)
                        count += 1
                        if count % 10000 == 0:
                            db.commit()
                            logging.debug(str(count) + ".")
                        continue

            if mode in generic_items:
                query = 'insert into "' + mode + '" values(?)'
                cursor.execute(query, [line])
        logging.debug("Saftey Commit")
        db.commit()

    return
