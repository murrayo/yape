# Pandas for data management
import pandas as pd

import sqlite3

def parsepbuttons(file,db):
    pbdtypes={"tps":"REAL","rd_sec/s":"REAL","wr_sec/s":"REAL","avgrq-sz":"REAL","avgqu-sz":"REAL","await":"REAL",
              "svctm":"REAL","%util":"REAL","Glorefs":"INTEGER", "RemGrefs":"INTEGER", "GRratio":"INTEGER",  "PhyRds":"INTEGER",
              "Rdratio":"INTEGER", "Gloupds":"INTEGER", "RemGupds":"INTEGER",
              "Rourefs":"INTEGER", "RemRrefs":"INTEGER",  "RouLaS":"INTEGER", "RemRLaS":"INTEGER",  "PhyWrs":"INTEGER",
              "WDQsz":"INTEGER",  "WDtmpq":"INTEGER", "WDphase":"INTEGER",
              "WIJwri":"INTEGER",  "RouCMs":"INTEGER", "Jrnwrts":"INTEGER",  "ActECP":"INTEGER",  "Addblk":"INTEGER",
              "PrgBufL":"INTEGER", "PrgSrvR":"INTEGER",  "BytSnt":"INTEGER",
              "BytRcd":"INTEGER",  "WDpass":"INTEGER",  "IJUcnt":"INTEGER", "IJULock":"INTEGER", "PPGrefs":"INTEGER",
              "PPGupds":"INTEGER","CPU":"TEXT","%user":"REAL","%nice":"REAL","%system":"REAL","%iowait":"REAL",
              "%steal":"REAL","%idle":"REAL","r":"INTEGER","b":"INTEGER","swpd":"INTEGER","free":"INTEGER","buff":"INTEGER",
              "cache":"INTEGER","si":"INTEGER","so":"INTEGER","bi":"INTEGER","bo":"INTEGER","in":"INTEGER","cs":"INTEGER",
              "us":"INTEGER","sy":"INTEGER","id":"INTEGER","wa":"INTEGER","st":"INTEGER",
              "Device":"TEXT","rrqm/s":"REAL","wrqm/s":"REAL","r/s":"REAL","w/s":"REAL",
              "rkB/s":"REAL","wkB/s":"REAL","await":"REAL",
              "r_await":"REAL","w_await":"REAL","%usr":"INTEGER","%sys":"INTEGER","%win":"INTEGER","%idle":"INTEGER",
              "%busy":"INTEGER","avque":"REAL","r+w/s":"INTEGER","blks/s":"INTEGER","avwait":"REAL","avserv":"REAL",
              "w":"INTEGER","swap":"INTEGER","re":"INTEGER",  "mf":"INTEGER", "pi":"INTEGER", "po":"INTEGER",
               "fr":"INTEGER", "de":"INTEGER", "sr":"INTEGER", "s3":"INTEGER", "s4":"INTEGER", "sd":"INTEGER",
               "sd":"INTEGER","GblSz":"INTEGER","pGblNsz":"INTEGER","pGblAsz":"INTEGER","ObjSz":"INTEGER",
               "pObjNsz":"INTEGER","pObjAsz":"INTEGER","BDBSz":"INTEGER","pBDBNsz":"INTEGER","pBDBAsz":"INTEGER"}
    mode="" #hold current parsing mode
    cursor = db.cursor()
    count=0
    sardate=""
    sartime=""
    osmode=""
    colcache=[]
    colcachenum=0
    numcols=0
    cursor.execute("CREATE TABLE sections (section TEXT)")

    with open(file, encoding="latin-1") as f:
        insertquery=""
        skipline=0
        for line in f:
            if skipline>0:
                skipline-=1
                continue
            #determine parsing states
            if "Topofpage" in line and mode!="":
                print("end of "+mode)
                if colcachenum>0:
                    cursor.executemany(insertquery,colcache)
                    colcache=[]
                    colcachenum=0
                query=""
                insertquery=""
                mode=""
            if "end_mgstat" in line:
                print("end of "+mode)
                query=""
                count=0
                insertquery=""
                mode=""
            if "end_sar_u" in line:
                print("end of "+mode)
                query=""
                count=0
                insertquery=""
                mode=""
            #add better osmode detection
            if "Product Version String" in line:
                if "Solaris for SPARC-64" in line:
                    osmode="solsparc"
                continue
                #no continues in here, because sometimes the topofpage is in the same line as the start of a
                #new section
            if "id=license" in line:
                mode="license"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=cpffile" in line:
                mode="cpffile"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=Windowsinfo" in line:
                mode="windowsinfo"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=tasklist" in line:
                    mode="tasklist"
                    print("starting "+mode)
                    query="CREATE TABLE "+mode+" (line TEXT)"
                    cursor.execute(query)
                    db.commit()
                    continue
            if "id=\"ss_1\"" in line:
                mode="ss1"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (\"line\" TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"ss_2\"" in line:
                mode="ss2"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"ss_3\"" in line:
                mode="ss3"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"ss_4\"" in line:
                mode="ss4"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=ifconfig" in line:
                mode="ifconfig"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=sysctl-a" in line:
                mode="sysctl-a"
                print("starting "+mode)
                query="CREATE TABLE \""+mode+"\" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=linuxinfo" in line:
                mode="linuxinfo"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=df-m" in line:
                mode="df-m"
                print("starting "+mode)
                query="CREATE TABLE \""+mode+"\" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=cpu" in line:
                mode="cpu"
                print("starting "+mode)
                query="CREATE TABLE \""+mode+"\" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=mount" in line:
                mode="mount"
                print("starting "+mode)
                query="CREATE TABLE \""+mode+"\" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=fdisk-l" in line:
                mode="fdisk-l"
                print("starting "+mode)
                query="CREATE TABLE \""+mode+"\" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -c1_1\"" in line:
                mode="cstatc11"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -c1_2\"" in line:
                mode="cstatc12"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -c1_3\"" in line:
                mode="cstatc13"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -c1_4\"" in line:
                mode="cstatc14"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -D_1\"" in line:
                mode="cstatD1"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -D_2\"" in line:
                mode="cstatD2"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -D_3\"" in line:
                mode="cstatD3"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -D_4\"" in line:
                mode="cstatD4"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -D_5\"" in line:
                mode="cstatD5"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -D_6\"" in line:
                mode="cstatD6"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -D_7\"" in line:
                mode="cstatD7"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"cstat -D_8\"" in line:
                mode="cstatD8"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"ps -elfy_1\"" in line:
                mode="pselfy1"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"ps -elfy_2\"" in line:
                mode="pselfy2"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"ps -elfy_3\"" in line:
                mode="pselfy3"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=\"ps -elfy_4\"" in line:
                mode="pselfy4"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=ipcs" in line:
                mode="ipcs"
                print("starting "+mode)
                query="CREATE TABLE "+mode+" (line TEXT)"
                cursor.execute(query)
                db.commit()
                continue
            if "id=vmstat" in line:
                if osmode=="sunos" or osmode=="solsparc":
                    colnames=line.split("<pre>")[1].split()
                    colnames=list(map(lambda x: x.strip(), colnames))
                    numcols=len(colnames)
                    added=[]
                    query="CREATE TABLE vmstat("
                    insertquery="INSERT INTO vmstat VALUES ("
                    for c in colnames:
                        t=c
                        if c in added:
                            t=c+"_1"
                            added.append(t)
                        else:
                            added.append(c)
                        query+="\""+t+"\" "+(pbdtypes.get(c) or "TEXT")+","
                        insertquery+="?,"
                    query=query[:-1]
                    insertquery=insertquery[:-1]
                    query+=")"
                    insertquery+=")"
                else:
                    # ugh :/
                    colnames=line.split("<pre>")[1].split()[2:]
                    numcols=len(colnames)+2
                    added=[]
                    query="CREATE TABLE vmstat(\"datetime\" TEXT,"
                    insertquery="INSERT INTO vmstat VALUES (?,"
                    for c in colnames:
                        t=c
                        if c in added:
                            t=c+"_1"
                            added.append(t)
                        else:
                            added.append(c)
                        query+="\""+t+"\" "+(pbdtypes.get(c) or "TEXT")+","
                        insertquery+="?,"
                    query=query[:-1]
                    insertquery=insertquery[:-1]
                    query+=")"
                    insertquery+=")"
                cursor.execute(query)
                db.commit()
                count=0
                mode="vmstat"
                print("starting "+mode)
                continue
            if "id=sar-u" in line:
                query=""
                count=0
                if "SunOS" in line:
                    osmode="sunos"
                    sardate=line.split()[-1]
                insertquery=""
                mode="sar-u"
                print("starting "+mode)
                continue
            if "id=iostat" in line:
                query=""
                count=0
                insertquery=""
                mode="iostat"
                print("starting "+mode)
                continue
            if "id=sar-d" in line:
                query=""
                count=0
                insertquery=""
                mode="sar-d"
                print("starting "+mode)
                continue
            if "beg_mgstat" in line:
                query=""
                insertquery=""
                mode="mgstat"
                print("starting "+mode)
                continue
            if "id=perfmon" in line:
                query=""
                insertquery=""
                mode="perfmon"
                print("starting "+mode)
                continue
            #actual parsing things
            if mode=="sar-d":
                if "Linux" in line:
                    continue
                if "Average" in line:
                    continue
                if "SunOS" in line:
                    osmode="sunos"
                    sardate=line.split()[-1]
                    continue
                if ("tps" in line or "device" in line) and query=="":
                    cols=list(map(lambda x: x.strip(), line.split()))
                    numcols=len(cols)
                    query="CREATE TABLE sard(datetime TEXT,"
                    insertquery="INSERT INTO sard VALUES (?,"
                    skiprows=2
                    if osmode=="sunos":
                        skiprows=1
                    for c in cols[skiprows:]:
                        query+="\""+c+"\" "+(pbdtypes.get(c) or "TEXT")+","
                        insertquery+="?,"
                    query=query[:-1]
                    insertquery=insertquery[:-1]
                    query+=")"
                    insertquery+=")"
                    cursor.execute(query)
                    db.commit()
                    continue
                cols=line.split()
                if osmode=="sunos":
                    if len(cols)==numcols:
                        cols=[(sardate+" "+cols[0])]+cols[1:]
                        sartime=cols[0]
                    else:
                        cols=[(sardate+" "+sartime)]+cols
                else:
                    currentdate=cols[0]+" "+cols[1]
                    cols=[currentdate]+cols[2:]
                colcache.append(cols)
                colcachenum+=1
                if colcachenum==10000:
                    cursor.executemany(insertquery,colcache)
                    colcache=[]
                    colcachenum=0
                count+=1
                if (count%10000==0):
                    db.commit()
                    print(str(count)+".",end='',flush=True)
            if mode=="iostat":
                if "Linux" in line:
                    continue
                if len(line.split())==3:
                    currentdate=line.strip()
                    continue
                if "avg-cpu" in line:
                    skipline=1
                    continue
                if "Device" in line and query=="":
                    cols=list(map(lambda x: x.strip(), line.split()))
                    query="CREATE TABLE iostat(\"datetime\" TEXT,"
                    insertquery="INSERT INTO iostat VALUES (?,"
                    for c in cols:
                        query+="\""+c.replace(":","")+"\" "+(pbdtypes.get(c.replace(":","")) or "TEXT")+","
                        insertquery+="?,"
                    query=query[:-1]
                    insertquery=insertquery[:-1]
                    query+=")"
                    insertquery+=")"
                    cursor.execute(query)
                    db.commit()
                    continue
                elif "Device" in line:
                    continue
                cols=line.split()
                cols=[currentdate.strip()]+cols
                db.execute(insertquery,cols)
                count+=1
                if (count%10000==0):
                    db.commit()
                    print(str(count)+".",end='',flush=True)
            if mode=="vmstat":
                if "end_vmstat" in line:
                    continue
                cols=line.split()
                if len(cols)!=numcols:
                    continue
                if not (osmode=="solsparc" or osmode=="sunos"):
                    cols=[(cols[0]+" "+cols[1])]+cols[2:]
                cursor.execute(insertquery,cols)
                count+=1
                if (count%10000==0):
                    db.commit()
                    print(str(count)+".",end='',flush=True)
            if mode=="perfmon":
                if "end_win_perfmon" in line:
                    continue
                if query=="":
                    cols=line.split(",")
                    cols=list(map(lambda x: x[1:-1].replace("\"",""), cols))
                    query="CREATE TABLE perfmon(datetime TEXT,"
                    insertquery="INSERT INTO perfmon VALUES (?,"
                    for c in cols[1:]:
                        query+="\""+c+"\" REAL,"
                        insertquery+="?,"
                    query=query[:-1]
                    insertquery=insertquery[:-1]
                    query+=")"
                    insertquery+=")"
                    cursor.execute(query)
                    db.commit()
                    continue
                cols=list(map(lambda x: x[1:-1], line.split(",")))
                cols=list(map(lambda x: 0.0 if x==" " else x,cols))
                cursor.execute(insertquery,cols)
                count+=1
                if (count%10000==0):
                    db.commit()
                    print(str(count)+".",end='',flush=True)
            if mode=="mgstat":
                if "MGSTAT" in line:
                    continue
                if "Date" in line:
                    cols=list(map(lambda x: x.strip(), line.split(",")))
                    query="CREATE TABLE mgstat(\"datetime\" TEXT,"
                    insertquery="INSERT INTO mgstat VALUES (?,"
                    for c in cols[2:]:
                        query+="\""+c+"\" "+(pbdtypes.get(c) or "TEXT")+","
                        insertquery+="?,"
                    query=query[:-1]
                    insertquery=insertquery[:-1]
                    query+=")"
                    insertquery+=")"
                    cursor.execute(query)
                    db.commit()
                    continue
                cols=list(map(lambda x: x.strip(), line.split(",")))
                cols=[(cols[0]+" "+cols[1])]+cols[2:]
                cursor.execute(insertquery,cols)
                count+=1
                if (count%10000==0):
                    db.commit()
                    print(str(count)+".",end='',flush=True)
            if mode=="sar-u":
                if "Linux" in line:
                    sardate=line.split()[3]
                    continue
                if "Average" in line:
                    continue
                if "%usr" in line and osmode=="sunos":
                    print("creating ins")
                    cols=list(map(lambda x: x.strip(), line.split()[1:]))
                    numcols=len(cols)+1
                    query="CREATE TABLE \"sar-u\"(\"datetime\" TEXT,"
                    insertquery="INSERT INTO \"sar-u\" VALUES (?,"
                    for c in cols:
                        query+="\""+c+"\" "+(pbdtypes.get(c) or "TEXT")+","
                        insertquery+="?,"
                    query=query[:-1]
                    insertquery=insertquery[:-1]
                    query+=")"
                    insertquery+=")"
                    cursor.execute(query)
                    db.commit()
                    continue
                if "CPU" in line:
                    cols=list(map(lambda x: x.strip(), line.split()[2:]))
                    query="CREATE TABLE \"sar-u\"(\"datetime\" TEXT,"
                    insertquery="INSERT INTO \"sar-u\" VALUES (?,"
                    for c in cols:
                        query+="\""+c+"\" "+(pbdtypes.get(c) or "TEXT")+","
                        insertquery+="?,"
                    query=query[:-1]
                    insertquery=insertquery[:-1]
                    query+=")"
                    insertquery+=")"
                    cursor.execute(query)
                    db.commit()
                    continue
                cols=list(map(lambda x: x.strip(), line.split()))
                if osmode=="sunos":
                    cols=[(sardate+" "+cols[0])]+cols[1:]
                else:
                    cols=[(sardate+" "+cols[0]+" "+cols[1])]+cols[2:]
                cursor.execute(insertquery,cols)
                count+=1
                if (count%10000==0):
                    db.commit()
                    print(str(count)+".",end='',flush=True)


            generic_items=["license","ifconfig","sysctl-a","df-m","mount","cpffile","fdisk-l","ss1",
            "ss2","ss3","ss4","linuxinfo","ipcs","cpu","cstatc11","cstatc12","cstatc13","cstatc14",
            "pselfy1","pselfy2","pselfy3","pselfy4","cstatD1","cstatD2","cstatD3","cstatD4","cstatD5",
            "cstatD6","cstatD7","cstatD8","windowsinfo","tasklist"]
            if mode in generic_items:
                query="insert into \""+mode+"\" values(?)"
                cursor.execute(query,[line])
        db.commit()

    return
