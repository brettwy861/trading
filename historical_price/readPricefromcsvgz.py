#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 00:48:24 2018

@author: brettwang
"""

import pandas as pd
import time
import re
import json
import urllib.request as urlGet 

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

urlGet.urlretrieve('http://api.bitcoincharts.com/v1/csv/coinbaseUSD.csv.gz',filename = 'coinbaseUSD.csv.gz')
time.sleep(3)
data = pd.read_csv('coinbaseUSD.csv.gz', compression='gzip', error_bad_lines=False)

firstrow = list(data.keys())
timestamp = list(data[firstrow[0]])
priceUSD = list(data[firstrow[1]])
volume = list(data[firstrow[2]])

dic={}
vol={}
#convert timestamp unix to date time string
for idx,item in enumerate(timestamp):
    timestamp[idx]=unixTimeConversion(item)

#init the dict
dic = dict().fromkeys(timestamp,0)
vol = dict().fromkeys(timestamp,0)

#get all traded usd for every minute
for idx,dateTime in enumerate(timestamp):
    dic[dateTime]+=(priceUSD[idx]*volume[idx]) 
    vol[dateTime]+=volume[idx]

#get average BTC price for every minute
for dateTime in dic.keys():
    dic[dateTime]=round(dic[dateTime]/vol[dateTime],2) # dic[t] = sum_{i}(pi*vi) / sum(v)
        

fp = open('price_coinbase_sorted.json', 'w')
json.dump(dic, fp, sort_keys=True, indent=2)
fp.close()

# 20141218155657 20150107202402   
# 20151231235957 20160101000001
# 20161231235943 20170101000001
# 20171231235959 20180101000003
