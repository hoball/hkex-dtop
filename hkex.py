#!/usr/bin/python
"""hkex.py: The class where downloading occurs"""

from ConfigParser import ConfigParser
from calendar import Calendar
from datetime import date, timedelta
import os, urllib2

class Hkex:
    def __init__(self):
        config = ConfigParser()
        config.read("config.ini")
        
        self.indexFutureUrl = config.get('dtop','index_future_url')
        self.stockOptionUrl = config.get('dtop','stock_option_url')
        
    
    def fetchDtop(self, market, start, end):
        # create a list of url to download
        
        # calculation must be in datetime.date object
        if isinstance(start, str):
            start = date(int(start[6:]), int(start[3:5]), int(start[:2]))
        
        if isinstance(end, str):
            end = date(int(end[6:]), int(end[3:5]), int(end[:2]))
        
        delta = timedelta(days=1)
        dateList = []
        
        x = start
        while (end - x >= end - end) :
            dateList.append(x)
            x = x + delta
            
        for x in range(len(dateList)): # monday=0, sunday=6
            if dateList[x].weekday() in range(5):
                dateFormat = str(dateList[x]).replace('-','')
                if market == 'all':
                    url = self.indexFutureUrl.replace('[date]',dateFormat)
                    self.save(url, 'DTOP_F_' + dateFormat + '.zip')
                   
                    url = self.stockOptionUrl.replace('[date]',dateFormat)
                    self.save(url, 'DTOP_O_' + dateFormat + '.zip')
                    
                elif market == 'indexFuture':
                    url = self.indexFutureUrl.replace('[date]',dateFormat)
                    self.save(url, 'DTOP_F_' + dateFormat + '.zip')
                    
                elif market == 'stockOption':
                    url = self.stockOptionUrl.replace('[date]',dateFormat)
                    self.save(url, 'DTOP_O_' + dateFormat + '.zip')
        
    
    def save(self,url, dtopFile):
        if os.path.exists('./storage/' + dtopFile):
            print "File exists. Skipping: ", dtopFile
            return
            
        print "Downloading ...",url
        
        try:
            response = urllib2.urlopen(url)
            data = response.read()
        
        except urllib2.HTTPError, e:
            if e.code == 404:
                print "Error: ", e.code, " - URL does not exist!"
            else:
                raise
        except urllib2.URLError, e:
            print "Failed to reach the server. Reason: ", e.reason
        
        else:
            try:
                zipFile = open('./storage/' + dtopFile,'wb')
                zipFile.write(data)
                zipFile.close()
            except IOError:
                print "...Cannot save the file ", dtopFile
            else:
                print "...Finished saving", dtopFile
        
        return

