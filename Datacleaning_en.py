# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 18:09:08 2018

@author: Andreas Stöckl
"""

import sqlite3
import re
import pandas as pd

def bereinigePostillion(txt):
    if txt != None:
        txt = re.sub('\n\s*\n', '', txt)
        txt = re.sub('Shutterstock', '', txt)
        txt = re.sub('Pixabay', '', txt)
    return txt

def datumPostillion(txt):
    if txt != None:
        txt = txt.split("/")[0]
        txt = pd.to_datetime(txt)
        return str(txt)
    return None

conn = sqlite3.connect('data/postillondata_clean.sqlite')
cur = conn.cursor()

conn2 = sqlite3.connect('data/postillondata.sqlite')
cur2 = conn2.cursor()

sqlstr = 'SELECT url,Kategorie,Titel,Body,Datum FROM Links'
for row in cur2.execute(sqlstr):
    if row[1] != None:
        date = datumPostillion(row[4])
        if date is not None:
            cur.execute('''INSERT OR REPLACE INTO Artikel
                    (url,Kategorie,Titel,Body,Datum,Quelle,Fake) VALUES ( ?,?,?,?,?,?,? )''', (row[0],row[1],row[2],bereinigePostillion(row[3]),datumPostillion(row[4]),"Postillon",0 ) )
conn.commit()
cur2.close()
cur.close()
