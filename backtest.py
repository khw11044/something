import pyupbit
import numpy as np
import time


def get_ma(ticker,look_day):
    """15,7일 등 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=look_day)
    ma15 = round(df['close'].rolling(look_day).mean().iloc[-1],3)
    return ma15



def get_ror(coin,k,ma):
    time.sleep(0.1)
    df = pyupbit.get_ohlcv(coin, count=14)
    df['range'] = (df['high'] - df['low']) * k
    df['ma'] = ma
    df['target'] = df['open'] + df['range'].shift(1)


    df['target'] = np.where(df['target'] > df['ma'],     # 조건문 고가가 목표매수가 보다 높으면
                            df['target'],    # 구매
                            df['high'] + 100) 
    

    df['ror'] = np.where(df['high'] > df['target'],     # 조건문 고가가 목표매수가 보다 높으면
                         df['close'] / df['target'],    # 구매
                         1)                             # 아니면 구매안하니깐 유지 


    ror = df['ror'].cumprod()[-2]
    return ror


coin = "KRW-BTC"

ma_list = [5,10,15,20]

best_value = 0
best_k=0
best_ma = 0

for m in ma_list:
    print('평균선 :',m)
    ma = get_ma(coin,m)
    for k in np.arange(0.1, 1.0, 0.1):
        ror = get_ror(coin,k,ma)
        print("%.1f %f" % (k, ror))
        if ror > best_value :
            best_value = ror
            best_k = k
            best_ma = ma 

print(best_k,best_ma,best_value)