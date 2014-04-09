#!/usr/bin/python

"""dtop.py: Download the missing dtop zip files"""

import os
from hkex import Hkex
from datetime import date, timedelta


def getLatestDate(market, folder):
    """Get the list of files, and determine the latest date
    Keyword arguments:
    market -- stockOption / indexFuture
    folder -- the storage folder    
    """
    
    if market == 'stockOption':
        m = 'DTOP_O_'
    elif market == 'indexFuture':
        m = 'DTOP_F_'
    
    dateList = []
    # get file list from directory
    for f in os.listdir(folder):
        if m in f:
            # crop the date from filename
            row = f.replace(m,'').replace('.zip','')
            dateList.append(date(int(row[:4]), int(row[4:6]), int(row[6:])))

            
    latest = dateList[0]
    for x in range(1,len(dateList)):
        if dateList[x] > latest:
            latest = dateList[x]
    
    return latest

folder = './storage'
today = date.today()

downloader = Hkex()
downloader.fetchDtop('stockOption', getLatestDate('stockOption',folder), today)
downloader.fetchDtop('indexFuture', getLatestDate('indexFuture',folder), today)

