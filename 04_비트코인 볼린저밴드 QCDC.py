# 02_비트코인 시세조회

import requests

import talib
import numpy as np
from pandas import Series
# 터미널에서 pip install talib .. 이런식으로 설치. 

url = "https://api.upbit.com/v1/candles/minutes/30"

querystring = {"market":"KRW-BTC","count":"200"}

headers = {"Accept": "application/json"}

response = requests.request("GET", url, headers=headers, params=querystring)

# print(response.text)

btc_price = response.json()

print(btc_price[0])
print('market : ',btc_price[0]['market'])
print('candle_date_time_kst : ', btc_price[0]['candle_date_time_kst'])
print('opening_price : ', btc_price[0]['opening_price'])
print('high_price : ', btc_price[0]['high_price'])
print('low_price : ', btc_price[0]['low_price'])
print('trade_price : ', btc_price[0]['trade_price'])
print('candle_acc_trade_price : ', btc_price[0]['candle_acc_trade_price'])
print('candle_acc_trade_volume : ',btc_price[0]['candle_acc_trade_volume'])

open_prices = []
close_prices = []
high_prices = []
low_prices = []

for p in btc_price:
    open_prices.append(p['opening_price'])
    close_prices.append(p['trade_price'])
    high_prices.append(p['high_price'])
    low_prices.append(p['low_price'])
open_prices.reverse() #reverse 역방향으로 재배열 
close_prices.reverse()
high_prices.reverse()
low_prices.reverse()

# print('open_prices : {}\n'.format(open_prices))
# print('close_prices : {}\n'.format(close_prices))
# print('high_prices : {}\n'.format(high_prices))
# print('low_prices : {}\n'.format(low_prices))
print()
print('open_prices : {:,.2f}\n'.format(open_prices[-1]))
print('close_prices : {:,.2f}\n'.format(close_prices[-1]))
print('high_prices : {:,.2f}\n'.format(high_prices[-1]))
print('low_prices : {:,.2f}\n'.format(low_prices[-1]))

high_prices = np.array(high_prices, dtype='f8')
low_prices = np.array(low_prices, dtype='f8')
open_prices = np.array(open_prices, dtype='f8')
close_prices = np.array(close_prices, dtype='f8')

#볼린저밴드 점수 불러오기
upperband, middleband, lowerband = talib.BBANDS(close_prices, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
print("upperband : ", upperband[-1])
print()
print("middleBand : ", middleband[-1])
print()
print("lowerband : ", lowerband[-1])

bband_high = upperband[-1]
bband_midd = middleband[-1]
bband_low = lowerband[-1]

now_price = close_prices[-1]

if  now_price <= bband_low:
    print("가격이 하향돌파")
    print("분할매수 하세요")
elif bband_low < now_price < bband_midd:
    print("가격이 하단에 위치")
elif bband_midd <= now_price < bband_high:
    print("가격이 상단에 위치")
elif now_price >= bband_high:
    print("가격이 상단 상향돌파")
    print("분할 매도 하세요")
else:
    print("예외발생.")


bband_profit = bband_high - bband_low

print("bband_profit : ", bband_profit)