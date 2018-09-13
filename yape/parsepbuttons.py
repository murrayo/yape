# Pandas for data management
import pandas as pd

import sqlite3
import logging


# splits an array into sub arrays with length size
def split(arr, size):
    arrs = []
    while len(arr) > size:
        piece = arr[:size]
        arrs.append(piece)
        arr = arr[size:]
    arrs.append(arr)
    return arrs


def parsepbuttons(file, db):
    pbdtypes = {"tps": "REAL", "rd_sec/s": "REAL", "wr_sec/s": "REAL", "avgrq-sz": "REAL", "avgqu-sz": "REAL", "await": "REAL",
                "svctm": "REAL", "%util": "REAL", "Glorefs": "INTEGER", "RemGrefs": "INTEGER", "GRratio": "INTEGER",  "PhyRds": "INTEGER",
                "Rdratio": "INTEGER", "Gloupds": "INTEGER", "RemGupds": "INTEGER",
                "Rourefs": "INTEGER", "RemRrefs": "INTEGER",  "RouLaS": "INTEGER", "RemRLaS": "INTEGER",  "PhyWrs": "INTEGER",
                "WDQsz": "INTEGER",  "WDtmpq": "INTEGER", "WDphase": "INTEGER",
                "WIJwri": "INTEGER",  "RouCMs": "INTEGER", "Jrnwrts": "INTEGER",  "ActECP": "INTEGER",  "Addblk": "INTEGER",
                "PrgBufL": "INTEGER", "PrgSrvR": "INTEGER",  "BytSnt": "INTEGER",
                "BytRcd": "INTEGER",  "WDpass": "INTEGER",  "IJUcnt": "INTEGER", "IJULock": "INTEGER", "PPGrefs": "INTEGER",
                "PPGupds": "INTEGER", "CPU": "TEXT", "cpu": "TEXT", "%user": "REAL", "%nice": "REAL", "%system": "REAL", "%iowait": "REAL",
                "%steal": "REAL", "%idle": "REAL", "r": "INTEGER", "b": "INTEGER", "swpd": "INTEGER", "free": "INTEGER", "buff": "INTEGER",
                "cache": "INTEGER", "si": "INTEGER", "so": "INTEGER", "bi": "INTEGER", "bo": "INTEGER", "in": "INTEGER", "cs": "INTEGER",
                "us": "INTEGER", "sy": "INTEGER", "id": "INTEGER", "wa": "INTEGER", "st": "INTEGER",
                "Device": "TEXT", "rrqm/s": "REAL", "wrqm/s": "REAL", "r/s": "REAL", "w/s": "REAL",
                "rkB/s": "REAL", "wkB/s": "REAL", "await": "REAL",
                "r_await": "REAL", "w_await": "REAL", "%usr": "INTEGER", "%sys": "INTEGER", "%win": "INTEGER", "%idle": "INTEGER",
                "%busy": "INTEGER", "avque": "REAL", "r+w/s": "INTEGER", "blks/s": "INTEGER", "avwait": "REAL", "avserv": "REAL",
                "w": "INTEGER", "swap": "INTEGER", "re": "INTEGER",  "mf": "INTEGER", "pi": "INTEGER", "po": "INTEGER",
                "fr": "INTEGER", "de": "INTEGER", "sr": "INTEGER", "s3": "INTEGER", "s4": "INTEGER", "sd": "INTEGER",
                "sd": "INTEGER", "GblSz": "INTEGER", "pGblNsz": "INTEGER", "pGblAsz": "INTEGER", "ObjSz": "INTEGER",
                "pObjNsz": "INTEGER", "pObjAsz": "INTEGER", "BDBSz": "INTEGER", "pBDBNsz": "INTEGER", "pBDBAsz": "INTEGER", "avm": "INTEGER", "at": "INTEGER",
                "RouSz":"INTEGER","pRouAsz":"INTEGER","Blk_read/s":"REAL","Blk_wrtn/s":"REAL","Blk_read":"INTEGER","Blk_wrtn":"INTEGER"}
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
    # moving generic items definition out of the loop
    generic_items = ["license", "ifconfig", "sysctl-a", "df-m", "mount", "cpffile", "fdisk-l", "ss1",
                     "ss2", "ss3", "ss4", "linuxinfo", "ipcs", "cpu", "cstatc11", "cstatc12", "cstatc13", "cstatc14",
                     "pselfy1", "pselfy2", "pselfy3", "pselfy4", "cstatD1", "cstatD2", "cstatD3", "cstatD4", "cstatD5",
                     "cstatD6", "cstatD7", "cstatD8", "windowsinfo", "tasklist"]

    cursor.execute("CREATE TABLE IF NOT EXISTS sections (section TEXT)")
    conditions = [
        {"match": "id=license", "mode": "license"},
        {"match": "id=cpffile", "mode": "cpffile"},
        {"match": "id=Windowsinfo", "mode": "windowsinfo"},
        {"match": "id=tasklist", "mode": "tasklist"},
        {"match": "id=\"ss_1\"", "mode": "ss1"},
        {"match": "id=\"ss_2\"", "mode": "ss2"},
        {"match": "id=\"ss_3\"", "mode": "ss3"},
        {"match": "id=\"ss_4\"", "mode": "ss4"},
        {"match": "id=ifconfig", "mode": "ifconfig"},
        {"match": "id=sysctl-a", "mode": "sysctl-a"},
        {"match": "id=linuxinfo", "mode": "linuxinfo"},
        {"match": "id=df-m", "mode": "df-m"},
        {"match": "id=cpu", "mode": "cpu"},
        {"match": "id=mount", "mode": "mount"},
        {"match": "id=fdisk-l", "mode": "fdisk-l"},
        {"match": "id=\"cstat -c1_1\"", "mode": "cstatc11"},
        {"match": "id=\"cstat -c1_2\"", "mode": "cstatc12"},
        {"match": "id=\"cstat -c1_3\"", "mode": "cstatc13"},
        {"match": "id=\"cstat -c1_4\"", "mode": "cstatc14"},
        {"match": "id=\"cstat -D_1\"", "mode": "cstatD1"},
        {"match": "id=\"cstat -D_2\"", "mode": "cstatD2"},
        {"match": "id=\"cstat -D_3\"", "mode": "cstatD3"},
        {"match": "id=\"cstat -D_4\"", "mode": "cstatD4"},
        {"match": "id=\"cstat -D_5\"", "mode": "cstatD5"},
        {"match": "id=\"cstat -D_6\"", "mode": "cstatD6"},
        {"match": "id=\"cstat -D_7\"", "mode": "cstatD7"},
        {"match": "id=\"cstat -D_8\"", "mode": "cstatD8"},
        {"match": "id=\"ps -elfy_1\"", "mode": "pselfy1"},
        {"match": "id=\"ps -elfy_2\"", "mode": "pselfy2"},
        {"match": "id=\"ps -elfy_3\"", "mode": "pselfy3"},
        {"match": "id=\"ps -elfy_4\"", "mode": "pselfy4"},
        {"match": "id=ipcs", "mode": "ipcs"}
    ]

    with open(file, encoding="latin-1") as f:
        insertquery = ""
        skipline = 0
        for line in f:
            if skipline > 0:
                skipline -= 1
                continue
            if not line.strip():
                continue
            if "<pre>\n"==line:
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
            if "end_mgstat" in line:
                logging.debug("end of " + mode)
                query = ""
                count = 0
                insertquery = ""
                mode = ""
            if "end_sar_u" in line:
                logging.debug("end of " + mode)
                query = ""
                count = 0
                insertquery = ""
                mode = ""

            if "An empty file was created." in line:
                logging.debug("empty "+mode+" section")
                continue
            # add better osmode detection

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
            matched = False
            for c in conditions:
                if c["match"] in line:
                    matched = True
                    mode = c["mode"]
                    logging.debug("starting " + mode)
                    query = "CREATE TABLE IF NOT EXISTS \"" + \
                        mode + "\" (line TEXT)"
                    cursor.execute(query)
                    db.commit()
                    continue
            if matched:
                continue
            if "<pre><!-- beg_vmstat -->" == line:
                continue
            if mode == "vmstat" and ("beg_vmstat" in line):
                continue
            if mode == "vmstat" and ("swpd" in line):
                colnames = line.split()[2:]
                numcols = len(colnames) + 2
                added = []
                query = "CREATE TABLE IF NOT EXISTS vmstat(\"datetime\" TEXT,"
                insertquery = "INSERT INTO vmstat VALUES (?,"
                for c in colnames:
                    t = c
                    if c in added:
                        t = c + "_1"
                        added.append(t)
                    else:
                        added.append(c)
                    query += "\"" + t + "\" " + \
                        (pbdtypes.get(c) or "TEXT") + ","
                    insertquery += "?,"
                query = query[:-1]
                insertquery = insertquery[:-1]
                query += ")"
                insertquery += ")"
                cursor.execute(query)
                db.commit()
                continue
            if "id=vmstat>" in line:
                mode = "vmstat"
                count = 0
                logging.debug("starting " + mode)
                if "beg_vmstat" not in line:
                    continue
                if osmode == "sunos" or osmode == "solsparc" or osmode == "hpux":
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
                        query += "\"" + t + "\" " + \
                            (pbdtypes.get(c) or "TEXT") + ","
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                else:
                    # ugh :/
                    logging.debug(line)
                    colnames = line.split("<pre>")[1].split()[2:]
                    numcols = len(colnames) + 2
                    added = []
                    query = "CREATE TABLE IF NOT EXISTS vmstat(\"datetime\" TEXT,"
                    insertquery = "INSERT INTO vmstat VALUES (?,"
                    for c in colnames:
                        t = c
                        if c in added:
                            t = c + "_1"
                            added.append(t)
                        else:
                            added.append(c)
                        query += "\"" + t + "\" " + \
                            (pbdtypes.get(c) or "TEXT") + ","
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                cursor.execute(query)
                db.commit()
                count = 0
                continue
            if "id=sar-u" in line:
                query = ""
                count = 0
                if "SunOS" in line:
                    osmode = "sunos"
                    sardate = line.split()[-1]
                if "HP-UX" in line:
                    sardate = line.split()[-1]
                insertquery = ""
                mode = "sar-u"
                logging.debug("starting " + mode)
                continue
            if "id=iostat" in line:
                query = ""
                count = 0
                insertquery = ""
                mode = "iostat"
                logging.debug("starting " + mode)
                continue
            if "id=sar-d" in line:
                query = ""
                count = 0
                insertquery = ""
                mode = "sar-d"
                logging.debug("starting " + mode)
                continue
            if "beg_mgstat" in line:
                query = ""
                insertquery = ""
                mode = "mgstat"
                logging.debug("starting " + mode)
                continue
            if "id=perfmon" in line:
                query = ""
                insertquery = ""
                mode = "perfmon"
                logging.debug("starting " + mode)
                continue

            if "id=monitor" in line:
                query = ""
                insertquery = ""
                mode = "monitor"
                logging.debug("starting " + mode)
                continue
            # actual parsing things
            if mode == "sar-d":
                if "Linux" in line:
                    cols=line.split()
                    sardate = cols[3]
                    continue
                if "HP-UX" in line:
                    osmode = "hpux"
                    sardate = line.split()[-1]
                    continue
                if "Average" in line:
                    continue
                if "SunOS" in line:
                    osmode = "sunos"
                    sardate = line.split()[-1]
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
                        if 'PM' in cols or 'AM' in cols:
                            skipcols = 2
                    if osmode == "sunos":
                        skipcols = 1
                    if osmode == "hpux":
                        skipcols = 1
                    for c in cols[skipcols:]:
                        query += "\"" + c.replace("DEV", "device") + "\" " + \
                            (pbdtypes.get(c) or "TEXT") + ","
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
                elif ("tps" in line or "device" in line):
                    continue
                cols = line.split()
                if osmode == "sunos" or osmode == "hpux":
                    if len(cols) == numcols:
                        sartime = cols[0]
                        cols = [(sardate + " " + cols[0])] + cols[1:]
                    else:
                        cols = [(sardate + " " + sartime)] + cols
                elif osmode == "linux":
                    if 'PM' in cols or 'AM' in cols:
                        currentdate = sardate + " " + cols[0] + " " + cols[1]
                        cols = [currentdate] + cols[2:]
                    else:
                        currentdate = sardate + " " + cols[0]
                        cols = [currentdate] + cols[1:]
                else:
                    currentdate = cols[0] + " " + cols[1]
                    cols = [currentdate] + cols[2:]
                colcache.append(cols)
                colcachenum += 1
                if colcachenum == 10000:
                    cursor.executemany(insertquery, colcache)
                    colcache = []
                    colcachenum = 0
                count += 1
                if (count % 10000 == 0):
                    db.commit()
                    logging.debug(str(count) + ".")
            if mode == "iostat":
                if "avg-cpu:" in line:
                    skipline=1
                    continue
                if osmode == "hpux":
                    continue
                if len(line.split())==7 and "Linux" in line:
                    currentdate = line.split()[3]
                if "Linux" in line:
                    continue
                if len(line.split()) == 3 or len(line.split()) == 2:
                    currentdate = line.strip()
                    continue
                if "avg-cpu" in line:
                    skipline = 1
                    continue
                if "Device" in line and query == "":
                    cols = list(map(lambda x: x.strip(), line.split()))
                    query = "CREATE TABLE IF NOT EXISTS iostat(\"datetime\" TEXT,"
                    insertquery = "INSERT INTO iostat VALUES (?,"
                    for c in cols:
                        query += "\"" + \
                            c.replace(
                                ":", "") + "\" " + (pbdtypes.get(c.replace(":", "")) or "TEXT") + ","
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
                if (count % 10000 == 0):
                    db.commit()
                    logging.debug(str(count) + ".")
            if mode == "vmstat":
                if "end_vmstat" in line:
                    continue
                cols = line.split()
                if len(cols) != numcols:
                    continue
                if not (osmode == "solsparc" or osmode == "sunos" or osmode == "hpux"):
                    cols = [(cols[0] + " " + cols[1])] + cols[2:]
                cursor.execute(insertquery, cols)
                count += 1
                if (count % 10000 == 0):
                    db.commit()
                    logging.debug(str(count) + ".")
            if mode == "perfmon":
                if "end_win_perfmon" in line:
                    continue
                if query == "":
                    cols = line.split(",")
                    cols = list(map(lambda x: x[1:-1].replace("\"", ""), cols))
                    query = "CREATE TABLE IF NOT EXISTS perfmon(datetime TEXT,"
                    insertquery = "INSERT INTO perfmon VALUES (?,"
                    for c in cols[1:]:
                        query += "\"" + c + "\" REAL,"
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                    cursor.execute(query)
                    db.commit()
                    continue
                cols = list(
                    map(lambda x: x[1:-1].replace("\"", ""), line.split(",")))
                cols = list(map(lambda x: 0.0 if x == " " else x, cols))
                cursor.execute(insertquery, cols)
                count += 1
                if (count % 10000 == 0):
                    db.commit()
                    logging.debug(str(count) + ".")
            if mode == "mgstat":
                if "MGSTAT" in line:
                    continue
                if "No output file was created." in line:
                    logging.warning(
                        "mgstat error in pbuttons: No output file was created.")
                    continue
                if not line.strip():
                    #ignore empty line (some rh mgstat on ~2016.1.x)
                    continue
                if "Date" in line:
                    cols = list(map(lambda x: x.strip(), line.split(",")))
                    query = "CREATE TABLE IF NOT EXISTS mgstat(\"datetime\" TEXT,"
                    insertquery = "INSERT INTO mgstat VALUES (?,"
                    for c in cols[2:]:
                        query += "\"" + c + "\" " + \
                            (pbdtypes.get(c) or "TEXT") + ","
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
                cursor.execute(insertquery, cols)
                count += 1
                if (count % 10000 == 0):
                    db.commit()
                    logging.debug(str(count) + ".")
            if mode == "sar-u":
                if "Linux" in line:
                    sardate = line.split()[3]
                    continue
                if not line.strip():
                    continue
                if "beg_sar_u" in line:
                    continue
                if "Average" in line:
                    continue
                if "%usr" in line and (osmode == "sunos" or osmode == "hpux"):
                    cols = list(map(lambda x: x.strip(), line.split()[1:]))
                    numcols = len(cols) + 1
                    query = "CREATE TABLE IF NOT EXISTS \"sar-u\"(\"datetime\" TEXT,"
                    insertquery = "INSERT INTO \"sar-u\" VALUES (?,"
                    for c in cols:
                        query += "\"" + c + "\" " + \
                            (pbdtypes.get(c) or "TEXT") + ","
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                    cursor.execute(query)
                    db.commit()
                    continue
                if "CPU" in line:
                    cols = list(map(lambda x: x.strip(), line.split()[2:]))
                    query = "CREATE TABLE IF NOT EXISTS \"sar-u\"(\"datetime\" TEXT,"
                    insertquery = "INSERT INTO \"sar-u\" VALUES (?,"
                    for c in cols:
                        query += "\"" + c + "\" " + \
                            (pbdtypes.get(c) or "TEXT") + ","
                        insertquery += "?,"
                    query = query[:-1]
                    insertquery = insertquery[:-1]
                    query += ")"
                    insertquery += ")"
                    cursor.execute(query)
                    db.commit()
                    continue
                cols = list(map(lambda x: x.strip(), line.split()))
                if osmode == "hpux":
                    # hpux sar-u creates one line with all data, split it up chunks of 5
                    # first column of the line is the time
                    for splitcols in split(cols[1:], 5):
                        cols = [(sardate + " " + cols[0])] + splitcols
                        cursor.execute(insertquery, cols)
                        count += 1
                else:
                    if osmode == "sunos":
                        cols = [(sardate + " " + cols[0])] + cols[1:]
                    else:
                        cols = [(sardate + " " + cols[0] +
                                 " " + cols[1])] + cols[2:]
                        cursor.execute(insertquery, cols)
                        count += 1
                if (count % 10000 == 0):
                    db.commit()
                    logging.debug(str(count) + ".")
            if mode == "monitor":
                if "DISK I/O STATISTICS" in line:
                    submode = "disk"
                    query = "CREATE TABLE IF NOT EXISTS \"monitor_disk\"(\"datetime\" TEXT,\"device\" TEXT,\"CUR\" REAL,\"AVE\" REAL,\"MIN\" REAL,\"MAX\" REAL)"
                    insertquery = "INSERT INTO \"monitor_disk\" VALUES (?,?,?,?,?,?)"
                    cursor.execute(query)
                    db.commit()
                    continue
                if "DISTRIBUTED LOCK MANAGEMENT STATISTICS" in line:
                    submode = "dist_lock_stats"
                    continue

                if "PROCESSES" in line:
                    submode = "processes"
                    query = "CREATE TABLE IF NOT EXISTS \"monitor_processes\"(\"datetime\" TEXT,\"PID\" TEXT,\"STATE\" TEXT,\"PRI\" INTEGER,\"NAME\" TEXT,\"PAGES\" TEXT,\"DIOCNT\" INTEGER,\"FAULTS\" INTEGER,\"CPUTIME\" TEXT)"
                    insertquery = "INSERT INTO \"monitor_processes\" VALUES (?,?,?,?,?,?,?,?,?)"
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
                        cols = [(diskdate)] + \
                            [cols[0].replace(":", "")] + cols[3:]
                        cursor.execute(insertquery, cols)
                        count += 1
                        if (count % 10000 == 0):
                            db.commit()
                            logging.debug(str(count) + ".")
                        continue
                    if (":" in line) and (len(cols) == 6):
                        cols = [(diskdate)] + \
                            [cols[0].replace(":", "")] + cols[2:]
                        cursor.execute(insertquery, cols)
                        count += 1
                        if (count % 10000 == 0):
                            db.commit()
                            logging.debug(str(count) + ".")
                        continue

            if mode in generic_items:
                query = "insert into \"" + mode + "\" values(?)"
                cursor.execute(query, [line])
        db.commit()

    return
