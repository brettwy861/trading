"""
arbitrage_api.py need to be in the same directory  
"""
import decimal
import arbitrage_api as arb
import json
import os
import time
import base64

# get the time 24 hours ago
def get24hourAgo():
    t=time.gmtime(int(time.time())-3600*24)
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

# get all currency name in the exchange
def getAllID():
    currency = arb.fetch_all_currencies()
    tokens = [item['id'] for item in currency]
    tokens.sort()
    return tokens

#get all fee currency
def getFeecurrency():
    symbol = arb.fetch_all_symbols()
    feeCurrency = set([item['feeCurrency'] for item in symbol])
    return feeCurrency

#get pairs and quantityIncrement as well as ticksize.
#tri_only set to false, when all pairs needed. otherwise only pairs that can form triangle.
def getPairs(tri_only=True): 
    symbol = arb.fetch_all_symbols()
    precision = {}
    pairs = {}
    for item in symbol:
        if item['baseCurrency'] in pairs.keys():
            pairs[item['baseCurrency']].append(item['feeCurrency'])
        else:
            pairs[item['baseCurrency']]=[item['feeCurrency']]
        precision[item['baseCurrency']+item['feeCurrency']]={'quantityIncrement':item['quantityIncrement'],'tickSize':item['tickSize']}
    if tri_only == True:
        keyToRemove = [key for key, value in pairs.items() if len(value)==1]
        while keyToRemove != []:
            pairs.pop(keyToRemove.pop())
    return pairs, precision		

#compare fee currency priority, eg. USDT > BTC > ETH 
def compareFeecurrency(feeCurrency):
    d = getPairs(False)[0]
    feeDict ={}
    result = [[k,d[k]] for k,v in d.items() if k in feeCurrency]
    for item in result:
        feeDict[item[0]]=len(item[1])
    last = feeCurrency.difference(feeDict.keys()).pop()
    feeDict[last]=0
    feeDict['GUSD']=0
    feeDict['DAI']=0
    feeDict['EURS']=feeDict['USD']+1
    feeDict['EOS']=feeDict['ETH']+1
    return feeDict

# edge notation of all BTC-included Triangle
def getTriangles_v2(feeCurrency):
    pairs, precision = getPairs()
    feePriority = compareFeecurrency(feeCurrency)
    btcPriority = feePriority['BTC']
    Higher = [k for k,v in feePriority.items() if v > btcPriority]
    Lower = [k for k,v in feePriority.items() if v < btcPriority]
    tri = []
    for key,value in pairs.items():
        if (key != 'BTC') and ('BTC' in value):
            value.remove('BTC')
            for i in value:
                if i in Higher:
                    tri.append(key+'BTC-'+key+i+'-'+i+'BTC') # BCQ1-BCQ2-Q2Q1  key BTC + key i + i BTC
                elif i in Lower:
                    tri.append(key+i+'-'+key+'BTC-BTC'+i) # BCQ1-BCQ2-Q2Q1  key i + key BTC + BTC i
                else:
                    print('error')
                    return 0
    return tri, precision

#dirty data clean in hitbtc
def getPricePoints():
    allTickers = arb.fetch_all_tickers()
    dic = {}
    for item in allTickers:
        dic[item['symbol']]={}
        dic[item['symbol']]['ask']=item['ask']
        dic[item['symbol']]['bid']=item['bid']
    #dic['EBTCBTC']=dic['EBTCNEWBTC']
    #dic['EBTCETH']=dic['EBTCNEWETH']
    #dic['EBTCUSD']=dic['EBTCNEWUSD']
    dic['XRPUSD']=dic['XRPUSDT']
    dic['SBTCUSD']=dic['SBTCUSDT']
    dic['EMCUSD']=dic['EMCUSDT']
    dic['DRTUSD']=dic['DRTUSDT']
    dic['REPUSD']=dic['REPUSDT']
    dic['AVHUSD']=dic['AVHUSDT']
    #dic['CLOUTUSD']=dic['CLOUTUSDT']
    dic['EKOUSD']=dic['EKOUSDT']
    dic['BCPTUSD']=dic['BCPTUSDT']
    dic['FRECUSD']=dic['FRECUSDT']
    dic['XMCUSD']=dic['XMCUSDT']
    dic['BCHTUSD']=dic['BCCFTUSD']
    dic['BCHDAI']=dic['BCCFDAI']
    dic['BCHEURS']=dic['BCCFEURS']
    return dic

feeCurrency = getFeecurrency()
triangles_v2, precision = getTriangles_v2(feeCurrency)

# List all pairs that are in the triangle above, along with QuantityIncrement, tickSize
d = {}
for item in triangles_v2:
    a,b,c=item.split('-')
    d[item]={a:precision[a],b:precision[b],c:precision[c]}
    
# Maintain a json for the data above    
with open(os.path.join('/var/www/html/','precision.json'),'w') as f:
    json.dump(d, f, indent=2)

# maintain the triangle qI and tS
with open(os.path.join('/var/www/html/','hitbtc-triangles-result.txt'),'w') as g:
    for k,v in d.items():
        tmp = k.split('-')
        g.write(tmp[0]+'-'+v[tmp[0]]['quantityIncrement']+'-'+v[tmp[0]]['tickSize']+'-'
                +tmp[1]+'-'+v[tmp[1]]['quantityIncrement']+'-'+v[tmp[1]]['tickSize']+'-'
                +tmp[2]+'-'+v[tmp[2]]['quantityIncrement']+'-'+v[tmp[2]]['tickSize']+'\n')

#convert from virtex to edge notation
def v2e(v):
    BC=v.split('-')[0]
    Q1=v.split('-')[1]
    Q2=v.split('-')[2]
    BCQ1 = BC+Q1
    BCQ2 = BC+Q2
    Q2Q1 = Q2+Q1
    e = BCQ1+'-'+BCQ2+'-'+Q2Q1
    return e

def findArbitrage_v2():
    while True:
        if 'result.json' in os.listdir('/var/www/html/'):#os.listdir(os.curdir):
            with open(os.path.join('/var/www/html/','result.json'),'r') as f: 
                dic = json.load(f)
            if len(list(dic.keys())[0])<16:
                dic2 = {}
                for k,v in dic.items():
                    dic2[v2e(k)]=v
                dic = dic2
        else:
            dic = dict.fromkeys(triangles_v2,0)
        pricePoints = getPricePoints()
        print('price got')
        for tri in triangles_v2:
            BCQ1 = tri.split('-')[0]
            BCQ2 = tri.split('-')[1]
            Q2Q1 = tri.split('-')[2]
            x=pricePoints.get(BCQ1)
            y=pricePoints.get(BCQ2)
            z=pricePoints.get(Q2Q1)
            if (x == None) or (y == None) or (z == None):
                continue
            Px=x.get('ask')
            Py=y.get('bid')
            Pz=z.get('bid')
            if (Px == None) or (Py == None) or (Pz == None):
                continue
            T = float(decimal.Decimal(Py)*decimal.Decimal(Pz)/decimal.Decimal(Px))
            if T>1.0031:
                if tri in dic.keys():
                    dic[tri]+=1
                else:
                    dic[tri]=1
                print('arbitrage spotted on '+tri)
        with open(os.path.join('/var/www/html/','result.json'),'w') as f:
            json.dump(dic, f, indent=2)
            f.close()
        # dictionary to bytes
        dic2byte = json.dumps(dic).encode('utf-8')
        encoded_byte = base64.standard_b64encode(dic2byte)
        with open(os.path.join('/var/www/html/','result_encoded.json'),'wb') as f:
            f.write(encoded_byte)
            
        sortedDic = sorted(dic.items(),key = lambda d:d[1],reverse=True)
        top10 = sortedDic[0:10]         
        with open(os.path.join('/var/www/html/','hitbtc-triangles-result-top.txt'),'w') as g:
            for item in top10:
                v = d[item[0]]
                tmp = item[0].split('-')
                g.write(tmp[0]+'-'+v[tmp[0]]['quantityIncrement']+'-'+v[tmp[0]]['tickSize']+'-'
                +tmp[1]+'-'+v[tmp[1]]['quantityIncrement']+'-'+v[tmp[1]]['tickSize']+'-'
                +tmp[2]+'-'+v[tmp[2]]['quantityIncrement']+'-'+v[tmp[2]]['tickSize']+'\n') 
        
        ####################### 24 hour top 10 ######################
        t0 = get24hourAgo()
        if t0+'.json' not in os.listdir('/var/www/html/history/'):
            print('the historical time not found')
            if int(t0[-2])==0:
                t1 = t0[0:-2]+str(int(t0[-2:])+1)
            else:
                t1 = t0[0:-2]+str(int(t0[-2:])-1)
            t0 = t1
        if t0+'.json' not in os.listdir('/var/www/html/history/'):
            a = os.listdir('/var/www/html/history/')
            a.sort()
            with open(os.path.join('/var/www/html/history/',a[-1]),'r') as f:
                dic0=json.load(f)
        else:
            with open(os.path.join('/var/www/html/history/',t0+'.json'),'r') as f:
                dic0=json.load(f)
        dic_24hr = dict().fromkeys(dic,0)
        for k,v in dic.items():
            if k in dic0.keys():
                dic_24hr[k]=dic[k]-dic0[k]
            else:
                dic_24hr[k]=dic[k]  
        sortedDic_24hr = sorted(dic_24hr.items(),key = lambda d:d[1],reverse=True)
        top10_24hr = sortedDic_24hr[0:10]      
        with open(os.path.join('/var/www/html/','hitbtc-triangles-24hr-result-top.txt'),'w') as g:
            for item in top10_24hr:
                v = d[item[0]]
                tmp = item[0].split('-')
                g.write(tmp[0]+'-'+v[tmp[0]]['quantityIncrement']+'-'+v[tmp[0]]['tickSize']+'-'
                +tmp[1]+'-'+v[tmp[1]]['quantityIncrement']+'-'+v[tmp[1]]['tickSize']+'-'
                +tmp[2]+'-'+v[tmp[2]]['quantityIncrement']+'-'+v[tmp[2]]['tickSize']+'\n') 
        print('json written')
        print(time.ctime())


findArbitrage_v2()
             