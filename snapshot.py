#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 14:28:50 2018

@author: brettwang
"""

import time
import os


def getGMTime():
    t=time.gmtime()
    year = str(t.tm_year)
    month = str(t.tm_mon)
    day = str(t.tm_mday)
    hour = str(t.tm_hour)
    minute = str(t.tm_min)
    second = str(t.tm_sec)
    if len(day) < 2:
        day = '0'+day
    if len(month) < 2:
        month = '0'+month
    if len(hour) < 2:
        hour = '0'+hour
    if len(minute) < 2:
        minute = '0'+minute
    if len(second) < 2:
        second = '0'+second
    return year+month+day+hour+minute    

while True:
    time.sleep(60)
    t=getGMTime()
    os.popen('cp /var/www/html/result.json /var/www/html/history/'+t+'.json')
