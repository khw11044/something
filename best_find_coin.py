import pyupbit
import numpy as np
import time
from function import get_ma,get_current_price


def get_ror(coin,k,day_count):
    time.sleep(0.05)
    df = pyupbit.get_ohlcv(coin, count=day_count)
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)


    # 시가에 사서 변동성 돌파때 팜
    df['ror'] = np.where(df['high'] > df['target'],     # 조건문, 고가가 목표매도가 보다 높으면 즉 한번은 목표매도가를 넘었었다. 
                         df['target'] / df['open'],    # 구매, 시가때 구매하고 목표가때 팜
                         df['close']/ df['open'])                             # 아니면 종가때 팜 


    ror = df['ror'].cumprod()[-2]
    return ror



def finding_best_k(coin,day_count):
    print(coin)
    best_value = 0
    best_k=0

    for k in np.arange(0.1, 1.0, 0.1):              # 5일,10일,15일,20일
        ror = get_ror(coin,k,day_count)
        # print("%.1f %f" % (k, ror))
        if ror > best_value :
            best_value = ror
            best_k = k
        print("%.1f, %f" % ( k, ror))
    print("최적값 : %.1f, %f" % ( best_k, best_value))
    return round(best_k,2),round(best_value,5)

#k = finding_best_k(coin,day_count)

#print(k)

def get_target_price(coin,k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(coin, interval="day", count=2)   # 무조건 2이어야함
    time.sleep(0.05)

    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    start_price = df.iloc[-1]['open']
    return target_price,start_price

# 모든 코인 조회

def investigate_all_coin():
    coin_lists = dict()
    day_count = 14
    coins = pyupbit.get_tickers(fiat="KRW")
    for coin in coins:
        print("coin",coin)
        best_k,best_value =finding_best_k(coin,day_count)
        target_price,start_price = get_target_price(coin,best_k)
        if get_ma(coin,5) > start_price :
            print('하락장임')
            continue
        print("coin",coin)
        print("최적값",best_k,best_value)
        print("수익률",round((100*(target_price - start_price)/start_price),4))
        coin_lists[coin] = [best_value,round(target_price,-1),start_price]
        print('-------------------------')
        print()

    print(coin_lists)
    top_3_coins = sorted(coin_lists.items(), key=lambda x : x[1],reverse=True)[:3]
    return top_3_coins


# if __name__ == "__main__":
#     coin_lists = investigate_all_coin()

#     top_10 = sorted(coin_lists.items(), key=lambda x : x[1],reverse=True)[:10]

#     print("top_10",top_10)
#     for coin in top_10:
#         coin_name = coin[0]
#         target_price = coin[1][1]
#         current_price = pyupbit.get_orderbook(tickers=coin_name)[0]["orderbook_units"][0]["ask_price"]
#         highest_price =  pyupbit.get_ohlcv(coin, interval="day", count=1).iloc[0]['high']
#         print(coin_name)
#         print(target_price,current_price,highest_price)