# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 14:55:01 2018

@author: Andreas Stöckl
"""
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

# FUNCTIONS
def loadArtikelPostillon(url):
    html = urllib.request.urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, 'html.parser')

    body = soup.find_all("div", class_="post-body-item")

    if body != []:
        body = body[0].get_text()
    else:
        return None

    return body

def getTextsafely(parent, element):
    text = parent.find(element)
    if text:
        return text.text
    return None

# MAIN CODE

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

import sqlite3

conn = sqlite3.connect('data/postillondata.sqlite')
cur = conn.cursor()

# only last month
url = "http://feeds.feedburner.com/blogspot/rkEL"
html = urllib.request.urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, 'xml')
teasers = soup.find_all("item")

for teaser in teasers:
    link = getTextsafely(teaser, 'link')
    category = getTextsafely(teaser, "category")
    title = getTextsafely(teaser, "title")
    date = getTextsafely(teaser, "pubDate")
    body = loadArtikelPostillon(link)
    cur.execute('''INSERT OR REPLACE INTO Links (url,Kategorie,Titel, Body, Datum, crawled) VALUES (?,?,?,?,?,?)''', (link,category,title,body,date,"1" ) )

conn.commit()
cur.close()
