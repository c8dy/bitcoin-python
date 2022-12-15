# 02_비트코인 시세조회

import requests

import talib
import numpy as np
from pandas import Series

# 터미널에서 pip install talib .. 이런식으로 설치. 

import schedule
import time


def Candles15():
    url = "https://api.upbit.com/v1/candles/minutes/30"

    querystring = {"market":"KRW-BTC","count":"200"}

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)

    btc_price = response.json()

    # print(btc_price[0])
    # print('market : ',btc_price[0]['market'])
    # print('candle_date_time_kst : ', btc_price[0]['candle_date_time_kst'])
    # print('opening_price : ', btc_price[0]['opening_price'])
    # print('high_price : ', btc_price[0]['high_price'])
    # print('low_price : ', btc_price[0]['low_price'])
    # print('trade_price : ', btc_price[0]['trade_price'])
    # print('candle_acc_trade_price : ', btc_price[0]['candle_acc_trade_price'])
    # print('candle_acc_trade_volume : ',btc_price[0]['candle_acc_trade_volume'])

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

    # print()
    # print('open_prices : {:,.2f}\n'.format(open_prices[-1]))
    # print('close_prices : {:,.2f}\n'.format(close_prices[-1]))
    # print('high_prices : {:,.2f}\n'.format(high_prices[-1]))
    # print('low_prices : {:,.2f}\n'.format(low_prices[-1]))

    high_prices = np.array(high_prices, dtype='f8')
    low_prices = np.array(low_prices, dtype='f8')
    open_prices = np.array(open_prices, dtype='f8')
    close_prices = np.array(close_prices, dtype='f8')

    return high_prices, low_prices, open_prices, close_prices

def MA():
    high_prices, low_prices, open_prices, close_prices = Candles15()
    ma_1st = talib.SMA(close_prices, timeperiod=5)
    ma_2nd = talib.SMA(close_prices, timeperiod=10)
    ma_3rd = talib.SMA(close_prices, timeperiod=20)
    ma_4th = talib.SMA(close_prices, timeperiod=60)
    ma_5th = talib.SMA(close_prices, timeperiod=120)


    # print('첫번째 이동평균선 : {:,.1f}'.format(ma_1st[-1]))
    # print('두번째 이동평균선 : {:,.1f}'.format(ma_2nd[-1]))
    # print('세번째 이동평균선 : {:,.1f}'.format(ma_3rd[-1]))
    # print('네번째 이동평균선 : {:,.1f}'.format(ma_4th[-1]))
    # print('다섯째 이동평균선 : {:,.1f}'.format(ma_5th[-1]))

    now_price = close_prices[-1]
    MA1 = ma_1st[-1]
    MA2 = ma_2nd[-1]
    MA3 = ma_3rd[-1]
    MA4 = ma_4th[-1]
    MA5 = ma_5th[-1]

    if now_price > MA1 and now_price > MA2 and now_price > MA3 and now_price > MA4 and now_price > MA5:
        if MA1 > MA2 and MA1 > MA3 and MA2 > MA3:
            # print("골드크로스, 1차 매수하세요.")
            ma_bns = "B1"
            if MA1 > MA4 and MA1 > MA5:
                # print("2차 골든크로스, 추가매수 할 수 있고,  수익 구간입니다. 수익매도를 할 수 있습니다.")
                ma_bns = "B2"
        else:
            # print("매수 대기중")
            ma_bns = "None"
    elif now_price < MA1 and now_price < MA2 and now_price < MA3 and now_price < MA4 and now_price < MA5:
        if MA1 < MA2 and MA1 < MA3 and MA2 < MA3:
            # print("데드크로스, 1차 매도하세요.")
            ma_bns = "S1"
            if MA1 < MA4 and MA1 < MA5:
                # print("2차 데드크로스, 추가매도 할 수 있고,  손절을 대비하세요.")
                ma_bns = "S2"
            else:
                # print("매도 대기중")
                ma_bns = "None"
    else:
        # print("현제 추세 전환 중입니다.")
        ma_bns = "None"
    return ma_bns, now_price


def BBand():
    high_prices, low_prices, open_prices, close_prices = Candles15()
    upperband, middleband, lowerband = talib.BBANDS(close_prices, timeperiod=5, nbdevup=2, nbdevdn=2, matype=0)
    # print("upperband : ", upperband[-1])
    # print()
    # print("middleBand : ", middleband[-1])
    # print()
    # print("lowerband : ", lowerband[-1])

    bband_high = upperband[-1]
    bband_midd = middleband[-1]
    bband_low = lowerband[-1]

    now_price = close_prices[-1]

    if  now_price <= bband_low:
        # print("가격이 하향돌파")
        # print("분할매수 하세요")
        bb_bns = "B1"
    elif bband_low < now_price < bband_midd:
        # print("가격이 하단에 위치")
        bb_bns = "DW"
    elif bband_midd <= now_price < bband_high:
        # print("가격이 상단에 위치")
        bb_bns = "UP"
    elif now_price >= bband_high:
        # print("가격이 상단 상향돌파")
        # print("분할 매도 하세요")
        bb_bns = "S1"
    else:
        # print("예외발생.")
        bb_bns = "None"
    return bb_bns


    # bband_profit = bband_high - bband_low
    
    # print("bband_profit : ", bband_profit)
    # print("------------------")


def MACD():
    high_prices, low_prices, open_prices, close_prices = Candles15()
    macd, macd_signal, macd_hist=talib.MACD(close_prices, fastperiod=12,slowperiod=26,signalperiod=9)
    MACD = macd[-1]
    MACDSIG = macd_signal[-1]

    if MACD >= MACDSIG:
        # macdstate = "GC= [만약에, 수익중이면 매도대기]\n= [만약에, 손실중이면 물타기]\n= [만약에, 매수전이면 매수]"
        macd_bns = "B1"
    elif MACD < MACDSIG:
        # macdstate = "DC= [만약에, 수익중이면 매도실시]\n= [만약에, 손실중이면 손절]\n= [만약에, 매수전이면 매수 불가]"
        macd_bns = "S1"
    else:
        # macdstate = "NONE"
        macd_bns = "None"
    return macd_bns
    # print("MACD : ", MACD)
    # print("MACDSIG : ", MACDSIG)
    # print("macdstate : ", macdstate)
    # print("--------------------")

def CCI():
    high_prices, low_prices, open_prices, close_prices = Candles15()
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

    # print("CCI : {:.2f}\n".format(CCI))
    # print("CCI3 : {:.2f}\n".format(CCI3))
    # print("cci_state : {}\n".format(cci_state))
    # print("CCI_TI : {:.2f}\n".format(CCI_TI))
    # print("cci_ti_state : {}\n".format(cci_state))

    if cci_state == "MD_DW" and cci_ti_state == "TI_UP":
        # print("1차 매수")
        cci_bns = "B1"
    elif cci_state == "MD_UP" and cci_ti_state == "TI_UP":
        # print("2차 매수")
        cci_bns = "B2"
    elif cci_state == "MD_UP" and cci_ti_state == "TI_DW":
        # print("1차 매도")
        cci_bns = "S1"
    elif cci_state == "MD_DW" and cci_ti_state == "TI_DW":
        # print("2차 매도")
        cci_bns = "S2"
    else:
        # print("매매 대기")
        cci_bns = "None"
    # print("--------------------")


def STOCH():
    high_prices, low_prices, open_prices, close_prices = Candles15()
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

    # print("Slowk : {:,.2f}\n".format(SlowK))
    # print("SlowD : {:,.2f}\n".format(SlowD))
    # print("stoch_state : {}\n".format(stoch_state))
    # print("S_KTI : {:,.2f}\n".format(S_KTI))
    # print("S_DTI : {:,.2f}\n".format(S_DTI))
    # print("stoch_ti_state : {}\n".format(stoch_ti_state))


    if stoch_state == "GC" and stoch_ti_state == "TI_UP":
        # print("1차 매수")
        stoch_bns = "B1"
    elif stoch_state == "DC" and stoch_ti_state == "TI_DW":
        # print("1차 매도")
        stoch_bns = "S1"
    else:
        # print("매매 대기")
        stoch_bns = "None"
    # print("--------------------")
    return stoch_bns

def RSI():
    high_prices, low_prices, open_prices, close_prices = Candles15()
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

    # print("RSI : {:.2f}\n".format(RSI))
    # print("RSI3 : {:.2f}\n".format(RSI3))
    # print("rsi_state : {}\n".format(rsi_state))
    # print("RSI_TI : {:.2f}\n".format(RSI_TI))
    # print("rsi_ti_state : {}\n".format(rsi_ti_state))


    if rsi_state == "MD" and rsi_ti_state == "TI_UP":
        # print("1차 매수")
        rsi_bns = "B1"
    elif rsi_state == "MD" and rsi_ti_state == "TI_DW":
        # print("1차 매도")
        rsi_bns = "S1"
    else:
        # print("매매 대기")
        rsi_bns = "None"
    # print("--------------------")
    return rsi_bns

def run():
    ma_bns, now_price = MA()
    bb_bns = BBand()
    macd_bns = MACD()
    cci_bns = CCI()
    stoch_bns = STOCH()
    rsi_bns = RSI()


    print("ma_bns : ", ma_bns)
    print("bb_bns : ", bb_bns)
    print("macd_bns : ", macd_bns)
    print("cci_bns : ", cci_bns)
    print("stoch_bns : ", stoch_bns)
    print("rsi_bns : ", rsi_bns)
    print("now_price : ", now_price)

    if ma_bns == 'S1' and bb_bns == 'S1' and macd_bns == 'S1' and cci_bns == 'S1' and stoch_bns == 'S1' and rsi_bns == 'S1':
        bns_stop = "S1"
    elif ma_bns == 'B1' and bb_bns == 'B1' and macd_bns == 'B1' and cci_bns == 'B1' and stoch_bns == 'B1' and rsi_bns == 'B1':
        bns_stop = "B1"
    else:
        bns_stop = "None"

    if bns_stop == "B1":
        print("분할 매수 실행")
    elif bns_stop == "S1":
        print("분할매도 로직 실행")
    else:
        print("매매 대기 상태")
        
    print("현제 가격 {:,.2f}".format(now_price))
    print("--------------------")
    print()

    print("bns_stop : ", bns_stop)

schedule.every(5).seconds.do(run)

t = 0
while True:
    schedule.run_pending()
    t += 1
    time.sleep(1)
    print(t, "초")
    if(t == 5):
        t = 0
    