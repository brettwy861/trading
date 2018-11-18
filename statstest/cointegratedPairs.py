import statsmodels.api as sm
#import statsmodels.formula.api as smf
#import seaborn as sns
import numpy as np
import pandas as pd
import historicalDataCMC as cmc

def find_cointegrated_pairs(dataframe):
    # DataFrame length
    n = dataframe.shape[1]
    # init matrix of p-values
    pvalue_matrix = np.ones((n, n))
    # col name
    keys = dataframe.keys()
    # init cointegrated pairs
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            # Two Time Series 
            ts1 = dataframe[keys[i]]
            ts2 = dataframe[keys[j]]
            # analyze coint
            result = sm.tsa.stattools.coint(ts1, ts2, trend='ctt',autolag='aic')
            # record p-value 
            pvalue = result[1]
            pvalue_matrix[i, j] = pvalue
            #if pvalue < 0.05:
            # record pairs and p-value
            pairs.append((keys[i], keys[j], pvalue))
    return pvalue_matrix, pairs

windowSize = 1
coinList = ['bitcoin','ethereum','litecoin','ripple','waves','stellar']
ts = {}
for c in coinList:
    ts[c] = cmc.getHistoricalData(c,20180101,20181115).Open
    ts[c] = ts[c].rolling(windowSize).mean()
df = pd.DataFrame(ts)
p_value, pairs = find_cointegrated_pairs(df)

pair_dict = {}
for item in pairs:
    pair_dict[item[0]+'-'+item[1]]=item[2]
pair_sorted = sorted(pair_dict.items(), key=lambda kv: kv[1])

# demo the smallest p-value and pairs, plot them on one graph
mostSignificantPair = pair_sorted[0][0].split('-')
leastSignificantPair = pair_sorted[-1][0].split('-')
MSPair = pd.concat([df[mostSignificantPair[0]],df[mostSignificantPair[1]]], axis=1)
LSPair = pd.concat([df[leastSignificantPair[0]],df[leastSignificantPair[1]]], axis=1)
cmc.plotMultiTs(MSPair,1)
cmc.plotMultiTs(LSPair,1)