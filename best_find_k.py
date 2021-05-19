import pyupbit
import numpy as np
import time
from function import get_ma


def get_ror(coin,k,ma,day_count):
    time.sleep(0.06)
    df = pyupbit.get_ohlcv(coin, count=day_count)
    df['range'] = (df['high'] - df['low']) * k
    df['ma'] = ma
    df['target'] = df['open'] + df['range'].shift(1)


    df['target'] = np.where(df['target'] > df['ma'],     # 조건문, 목표 매수가가 평균값보다 높으면 
                            df['target'],                 # 그대로 
                            df['high'] + 100)               # 아니면 
    

    df['ror'] = np.where(df['close'] > df['target'],     # 조건문 고가가 목표매수가 보다 높으면
                         df['close'] / df['target'],    # 구매
                         1)                             # 아니면 구매안하니깐 유지 


    ror = df['ror'].cumprod()[-2]
    return ror



def finding_best_k(coin,day_count):
    print(coin)
    best_value = 0
    best_k=0
    ma_list = [5,10,15,20]
    best_ma_list = 0
    best_ma = 0

    for m in ma_list:
        print('평균선 :',m)
        for k in np.arange(0.1, 1.0, 0.1):
            ma = get_ma(coin,m)                 # 5일,10일,15일,20일
            ror = get_ror(coin,k,ma,day_count)
            # print("%.1f %f" % (k, ror))
            if ror > best_value :
                best_value = ror
                best_k = k
                best_ma = ma 
                best_ma_list = m
            print("%d, %.1f, %f" % (m, k, ror))
    print("최적값 : %d, %.1f, %f" % (best_ma_list, best_k, best_value))
    print(best_ma)
    return round(best_k,2), best_ma

#k = finding_best_k(coin,day_count)

#print(k)

def get_target_price(coin,day_count):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(coin, interval="day", count=2)

    k = finding_best_k(coin,day_count)

    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price


# coin = "KRW-BTC"
# finding_best_k(coin)