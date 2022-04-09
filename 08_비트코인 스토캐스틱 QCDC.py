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

slowk, slowd = talib.STOCH(high_prices, low_prices, close_prices, fastk_period=14, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

SlowK = slowk[-1]
SlowD = slowd[-1]

SlowK3 = slowk[-3]
SlowD3 = slowd[-3]


if SlowK >= SlowD:
    stoch_state = "GC"
else:
    stoch_state = "DC"

S_KTI = ((SlowK - SlowK3) / SlowK3 + 100)
S_DTI = ((SlowD - SlowD3) / SlowD3 + 100)

if S_DTI > 0 and S_KTI > 0:
    stoch_ti_state = "TI_UP"
elif S_KTI < 0 and S_DTI < 0:
    stoch_ti_state = "TI_DW"
else:
    stoch_ti_state = "TI_NONE"

print("Slowk : {:,.2f}\n".format(SlowK))
print("SlowD : {:,.2f}\n".format(SlowD))
print("stoch_state : {}\n".format(stoch_state))
print("S_KTI : {:,.2f}\n".format(S_KTI))
print("S_DTI : {:,.2f}\n".format(S_DTI))
print("stoch_ti_state : {}\n".format(stoch_ti_state))


if stoch_state == "GC" and stoch_ti_state == "TI_UP":
    print("1차 매수")
elif stoch_state == "DC" and stoch_ti_state == "TI_DW":
    print("1차 매도")
else:
    print("매매 대기")