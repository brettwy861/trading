#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 21 17:17:01 2018

@author: brettwang
Retrieving exchanges listed on coinmarketcap and save the json 
"""

import re
import urllib.request
import json
from time import sleep

urlbase = 'https://coinmarketcap.com'
url = 'https://coinmarketcap.com/exchanges/volume/24-hour/all'
html = urllib.request.urlopen(url).read()
exchangeId = re.findall('<tr id="(.*?)">', str(html))
exchanges = re.findall('alt="(.*?)">', str(html))
exchangeNames = exchanges[0:-4]

#get all url of exchanges in coinmarketcap
exchangeShortURL = re.findall('<a class="link-secondary" href="/exchanges(.*?)">', str(html)) 
exchangeURLs = []
for item in exchangeShortURL:
    exchangeURLs.append(urlbase+'/exchanges'+item)
    
# name, url
newList = []
for i in range(len(exchangeId)):
    newList.append([exchangeNames[i], exchangeURLs[i]])

website_re = 'title="Website"></span> <a href="(.*?)" target="_blank">'
fees_re = 'title="Fees"></span> <a href="(.*?)" target="_blank" rel="noopener">Fees'
chat_re = 'title="Chat"></span> <a href="(.*?)" target="_blank" rel="noopener">Chat'
twitter_re= 'title="Twitter"></span> <a href="(.*?)" target="_blank">'
blog_re = 'title="Blog"></span> <a href="(.*?)"" target="_blank" rel="noopener">Blog'

exchangeJson = []

for item in newList:
    print('fetching exchange '+item[0])
    sleep(2)
    newdict = {}
    html = urllib.request.urlopen(item[1]).read()
    newdict['name'] = item[0]
    newdict['website'] = re.findall(website_re, str(html)) 
    newdict['fees'] = re.findall(fees_re, str(html))
    newdict['chat'] = re.findall(chat_re, str(html))
    newdict['twitter'] = re.findall(twitter_re, str(html))
    newdict['blog'] = re.findall(blog_re, str(html))
    exchangeJson.append(newdict)

with open('exchange.json', 'w') as file:
    json.dump(exchangeJson, file, indent=2)
    file.close()
