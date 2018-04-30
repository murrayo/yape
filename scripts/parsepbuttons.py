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
              "us":"INTEGER","sy":"INTEGER","id":"INTEGER","wa":"INTEGER","st":"INTEGER"}
    mode="" #hold current parsing mode
    cursor = db.cursor()
    count=0
    with open(file, encoding="latin-1") as f:
        insertquery=""
        for line in f:
            #determine parsing states
            if "Topofpage" in line and mode!="":
                print("end of "+mode)
                query=""
                insertquery=""
                mode=""
                #no continues in here, because sometimes the topofpage is in the same line as the start of a
                #new section
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
            if "id=fidsk-l" in line:
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
                # ugh :/
                colnames=line.split("<pre>")[1].split()[2:]
                query="CREATE TABLE vmstat(\"datetime\" TEXT,"
                insertquery="INSERT INTO vmstat VALUES (?,"
                for c in colnames:
                    query+="\""+c+"\" "+(pbdtypes.get(c) or "TEXT")+","
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
            #actual parsing things
            if mode=="sar-d":
                if "Linux" in line:
                    continue
                if "Average" in line:
                    continue
                if "tps" in line and query=="":
                    cols=list(map(lambda x: x.strip(), line.split()))
                    query="CREATE TABLE sard(\"time\" TEXT,"
                    insertquery="INSERT INTO sard VALUES (?,"
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
                cols=line.split()
                currentdate=cols[0]+" "+cols[1]
                cols=[currentdate]+cols[2:]
                db.execute(insertquery,cols)
                count+=1
                if (count%10000==0):
                    db.commit()
                    print(count)
            if mode=="vmstat":
                if "end_vmstat" in line:
                    continue
                cols=line.split()
                if len(cols)==0:
                    continue
                cols=[(cols[0]+" "+cols[1])]+cols[2:]
                db.execute(insertquery,cols)
                count+=1
                if (count%10000==0):
                    db.commit()
                    print(count)
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
                db.execute(insertquery,cols)
                count+=1
                if (count%10000==0):
                    db.commit()
                    print(count)
            if mode=="sar-u":
                if "Linux" in line:
                    sardate=line.split()[3]
                    continue
                if "Average" in line:
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
                cols=[(sardate+" "+cols[0]+" "+cols[1])]+cols[2:]
                db.execute(insertquery,cols)
                count+=1
                if (count%10000==0):
                    db.commit()
                    print(count)


            generic_items=["license","ifconfig","sysctl-a","df-m","mount","cpffile","fdisk-l","ss1",
            "ss2","ss3","ss4","linuxinfo","ipcs","cpu","cstatc11","cstatc12","cstatc13","cstatc14",
            "pselfy1","pselfy2","pselfy3","pselfy4"]
            if mode in generic_items:
                query="insert into \""+mode+"\" values(?)"
                db.execute(query,[line])
        db.commit()
    return
