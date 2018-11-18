#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 15:47:31 2018

@author: brettwang
"""

import seaborn as sns
import numpy as np
import pandas as pd

freqDict = {'D':365, 'H':365*24}
f = "D"
ts_num = 6 # number of time series
moving_window = 24
col = [str(i) for i in range(1,ts_num+1)]
rs = np.random.RandomState(freqDict[f])
values = rs.randn(freqDict[f],ts_num).cumsum(axis=0)
dates = pd.date_range("1 1 2017", periods=freqDict[f], freq = f)
#dates = pd.date_range(start='1/1/2017', end='12/31/2017', freq =f)
data = pd.DataFrame(values, dates, columns=col)
data = data.rolling(moving_window).mean() #moving average, smooth

sns.set_style('whitegrid') #sns.set_style('whitegrid') 
sns.set_palette('hls')
sns.set_context('notebook')
sns.lineplot(data=data, linewidth=2)

