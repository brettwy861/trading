#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 17:32:41 2018

@author: brettwang
Daily Open + Volume plot for one cryptocurrency during specific date range
dependency:
    beautifulsoup
    pandas
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
#import seaborn as sns
import matplotlib.pyplot as plt
import sys

def getHistoricalData(coin,t_start,t_end):
    #t_start = '20170101'
    #t_end = '20171231'
    #coin = 'waves'
    t_start = str(t_start)
    t_end = str(t_end)
    url = "https://coinmarketcap.com/currencies/"+coin+"/historical-data/?start="+t_start+"&end="+t_end
    content = requests.get(url).content
    soup = BeautifulSoup(content,'html.parser')
    table = soup.find('table', {'class': 'table'})
    data = [[td.text.strip() for td in tr.findChildren('td')] 
            for tr in table.findChildren('tr')]
    
    df = pd.DataFrame(data)
    df.drop(df.index[0], inplace=True) # first row is empty , previously header
    df[0] =  pd.to_datetime(df[0]) # first col is date in format "Nov 15, 2018"
    for i in range(1,len(df.columns)):
        # remove , and -
        df[i] = pd.to_numeric(df[i].str.replace(",","").str.replace("-","")) 
    
    df.columns = ['Date','Open','High','Low','Close','Volume','Market Cap']
    df.set_index('Date',inplace=True)
    df.sort_index(inplace=True)
    return df

def plotOpenWithVolume(df,windowSize):
#new df with only open and volume columns
    newFrame = pd.concat([df['Open'], df['Volume']], axis=1)
    newFrame = newFrame.rolling(windowSize).mean()
    # Daily Open + Volume plot for one cryptocurrency during specific date range
    ax = newFrame.plot(x=newFrame.index, y="Open", legend=False, color="b",logy=False)
    ax2 = ax.twinx()
    newFrame.plot(x=newFrame.index, y="Volume", ax=ax2, legend=False, color="r",logy=False)
    ax.figure.legend(loc=9)
    ax.set_xlabel('Dates')
    ax.set_ylabel('Price to USD', color='b')
    ax2.set_ylabel('24-Hour Volume', color='r')
    plt.show()
    
def plotMultiTs(df,windowSize):#support one ts or df made of two ts
    if type(df) == pd.core.frame.DataFrame and len(df.columns)>1:
        newFrame = df.rolling(windowSize).mean()
        # Daily Open + Volume plot for one cryptocurrency during specific date range
        ax = newFrame.plot(x=newFrame.index, y=newFrame.columns[0], legend=False, color="b",logy=False)
        ax2 = ax.twinx()
        newFrame.plot(x=newFrame.index, y=newFrame.columns[1], ax=ax2, legend=False, color="r",logy=False)
        ax.figure.legend(loc=9)
        ax.set_xlabel('Dates')
        ax.set_ylabel('Price(USD) of '+ newFrame.columns[0], color='b')
        ax2.set_ylabel('Price(USD) of '+ newFrame.columns[1], color='r')
        plt.show()
    elif type(df) == pd.core.series.Series:
        newTs = df.rolling(windowSize).mean()
        ax = newTs.plot(x=newTs.index, y=newTs.data, legend=False, color="b",logy=False)
        ax.figure.legend(loc=9)
        ax.set_xlabel('Dates')
        ax.set_ylabel('Price(USD) of '+ newTs.name, color='b')
        plt.show()
        
def main(argv):
    if len(sys.argv)!=5:
        print("Please follow the format: python thisscript.py 'ethereum' '20170101' '20171231' 5")
    else:
        coin = sys.argv[1]
        t_start = sys.argv[2]
        t_end = sys.argv[3]
        windowSize = sys.argv[4]
        df = getHistoricalData(coin,t_start,t_end)
        plotOpenWithVolume(df,windowSize)

if __name__ == "__main__":
   main(sys.argv[1:])