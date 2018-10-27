import requests
import datetime
import decimal
def fetch_all_currencies():
    url_currency = 'https://api.hitbtc.com/api/2/public/currency/'
    return requests.get(url_currency).json()
def fetch_currency(currency):
    url_currency = 'https://api.hitbtc.com/api/2/public/currency/'
    return requests.get(url_currency+currency).json()

def fetch_all_tickers():
    result = ''
    url_ticker = 'https://api.hitbtc.com/api/2/public/ticker/'
    for i in range(10):
        try:
            result = requests.get(url_ticker).json()
        except Exception as e:
            print('retry')
            continue
        else:
            break
    return result
    
def fetch_ticker(ticker):
    url = 'https://api.hitbtc.com/api/2/public/ticker/'
    return requests.get(url+ticker).json()
        tmp = symbol.split(' ')

def fetch_all_symbols():
    url_symbol = 'https://api.hitbtc.com/api/2/public/symbol/'
    return requests.get(url_symbol).json()

def fetch_symbol(symbol):
    url = 'https://api.hitbtc.com/api/2/public/symbol/'
    if '/' in symbol:
        tmp = symbol.split('/')
        symbol = tmp[0]+tmp[1]
    elif ' ' in symbol:
        tmp = symbol.split(' ')
        symbol = tmp[0]+tmp[1]
    return requests.get(url+symbol).json()

def fetch_orderbook(symbol, limit):
    url_orderbook = 'https://api.hitbtc.com/api/2/public/orderbook/'
    if type(limit) is str:
        limit = int(float(limit))
    else:
        limit = int(limit)
    if limit > 100:
        limit = '100'
    elif limit < 0:
        limit = '0'
    else:
        limit = str(limit)
    return requests.get(url_orderbook+symbol+'?limit='+limit).json()

def get_arbitrage_profit(token):
    Xa = fetch_ticker(token+'BTC')['ask']
    Yb = fetch_ticker(token+'ETH')['bid']
    Zb = fetch_ticker('ETHBTC')['bid']
    return float(decimal.Decimal(Yb)*decimal.Decimal(Zb)/decimal.Decimal(Xa))