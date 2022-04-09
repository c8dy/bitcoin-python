# 02_비트코인 시세조회

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

cci = talib.CCI(high_prices, low_prices, close_prices, timeperiod=20)

CCI = cci[-1]
CCI3 = cci[-3]

if CCI < -100:
    cci_state = "DW"
elif -100 <= CCI < 0:
    cci_state = "MD_DW"
elif 0 <= CCI < 100:
    cci_state = "MD_UP"
else:
    cci_state = "NONE"

#CCI 기울기
CCI_TI = ((CCI - CCI3) / CCI3+100)


if CCI_TI > 0:
    cci_ti_state = "TI_UP"
else:
    cci_ti_state = "TI_DW"

print("CCI : {:.2f}\n".format(CCI))
print("CCI3 : {:.2f}\n".format(CCI3))
print("cci_state : {}\n".format(cci_state))
print("CCI_TI : {:.2f}\n".format(CCI_TI))
print("cci_ti_state : {}\n".format(cci_state))

if cci_state == "MD_DW" and cci_ti_state == "TI_UP":
    print("1차 매수")
elif cci_state == "MD_UP" and cci_ti_state == "TI_UP":
    print("2차 매수")
elif cci_state == "MD_UP" and cci_ti_state == "TI_DW":
    print("1차 매도")
elif cci_state == "MD_DW" and cci_ti_state == "TI_DW":
    print("2차 매도")
else:
    print("매매 대기")
