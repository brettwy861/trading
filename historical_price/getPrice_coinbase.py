#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 21:28:28 2018

@author: brettwang
"""

import time
import re
import json
#import urllib2 as urlGet for py2
import urllib.request as urlGet # for py3
    

def unixTimeConversion(t):
    if type(t) == int and len(str(t))>10:
        t = int(str(t)[0:10])
    elif type(t) == str and len(t)>10:
        t = int(t[0:10])
    else:
        t = int(t)
    return timeConversion(time.ctime(t))

def timeConversion(t):
    tmp = re.split('\s+', t)
    if len(tmp[2])==1:
        tmp[2]='0'+tmp[2]
    hms = tmp[3].split(':') 
    month = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04',
             'May':'05','Jun':'06','Jul':'07','Aug':'08',
            'Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    return tmp[4]+month[tmp[1]]+tmp[2]+hms[0]+hms[1]#+hms[2]
 
def getBTCprice(t):
    if int(timeConversion(time.ctime()))-t<10000:
        print('data from recent 24 hours not available, retrieving current pricing... ')
        return float(json.load(urlGet.urlopen('https://api.coinbase.com/v2/prices/spot?currency=USD'))['data']['amount'])
    else:
        d=priceDict.get(str(t))
        if d != None:
            print(t)
            return d
        else:
            print('not found')
            return getBTCprice(t-1)
    
with open('price_coinbase_sorted.json','r') as f:
    priceDict  = json.load(f)


