# 02_비트코인 시세조회

from fileinput import close
from sre_compile import MAXCODE
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


rsi = talib.RSI(close_prices, timeperiod=14)

RSI = rsi[-1]
RSI3 = rsi[-3]

if RSI <= 25:
    rsi_state = "DW"
elif 25 < RSI < 75:
    rsi_state = "MD"
elif RSI >= 75:
    rsi_state = "UP"
else:
    rsi_state = "NONE"

RSI_TI = ((RSI - RSI3) / RSI3 + 100)

if RSI_TI > 0:
    rsi_ti_state = "TI_UP"
else:
    rsi_ti_state = "TI_DW"

print("RSI : {:.2f}\n".format(RSI))
print("RSI3 : {:.2f}\n".format(RSI3))
print("rsi_state : {}\n".format(rsi_state))
print("RSI_TI : {:.2f}\n".format(RSI_TI))
print("rsi_ti_state : {}\n".format(rsi_ti_state))


if rsi_state == "MD" and rsi_ti_state == "TI_UP":
    print("1차 매수")
elif rsi_state == "MD" and rsi_ti_state == "TI_DW":
    print("1차 매도")
else:
    print("매매 대기")