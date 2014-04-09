#!/usr/bin/python
"""cli.py: command line version to test the script"""

from hkex import Hkex

sector = raw_input('Dwnload index(index) or stock option(stock) or "all"?')
start = raw_input('Start date (dd-mm-yyyy):')
end = raw_input('End date (dd-mm-yyyy):')

downloader = Hkex()

if sector == 'index':
    data = downloader.fetchDtop('indexFuture', start, end)
elif sector == 'stock':
    data = downloader.fetchDtop('stockOption', start, end)
elif sector == 'all':
    data = downloader.fetchDtop('all', start, end)
