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

ma_1st = talib.SMA(close_prices, timeperiod=5)
ma_2nd = talib.SMA(close_prices, timeperiod=10)
ma_3rd = talib.SMA(close_prices, timeperiod=20)
ma_4th = talib.SMA(close_prices, timeperiod=60)
ma_5th = talib.SMA(close_prices, timeperiod=120)


print('첫번째 이동평균선 : {:,.1f}'.format(ma_1st[-1]))
print('두번째 이동평균선 : {:,.1f}'.format(ma_2nd[-1]))
print('세번째 이동평균선 : {:,.1f}'.format(ma_3rd[-1]))
print('네번째 이동평균선 : {:,.1f}'.format(ma_4th[-1]))
print('다섯째 이동평균선 : {:,.1f}'.format(ma_5th[-1]))

now_price = close_prices[-1]
MA1 = ma_1st[-1]
MA2 = ma_2nd[-1]
MA3 = ma_3rd[-1]
MA4 = ma_4th[-1]
MA5 = ma_5th[-1]

if now_price > MA1 and now_price > MA2 and now_price > MA3 and now_price > MA4 and now_price > MA5:
    if MA1 > MA2 and MA1 > MA3 and MA2 > MA3:
        print("골드크로스, 1차 매수하세요.")
        if MA1 > MA4 and MA3 > MA5:
            print("2차 골든크로스, 추가매수 할 수 있고,  수익 구간입니다. 수익매도를 할 수 있습니다.")
elif now_price < MA1 and now_price < MA2 and now_price < MA3 and now_price < MA4 and now_price < MA5:
    if MA1 < MA2 and MA1 < MA3 and MA2 < MA3:
        print("데드크로스, 1차 매도하세요.")
        if MA1 < MA4 and MA3 < MA5:
            print("2차 데드크로스, 추가매도 할 수 있고,  손절을 대비하세요.")
else:
    print("현제 추세 전환 중입니다.")