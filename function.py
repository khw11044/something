import pyupbit
import ast
from slack import post_message
import time

# 보안을 위해 코드에 바로 자신의 Key를 노출시키지 않기 위해

def sec():
    with open("upbit.txt") as f:
        lines = f.readlines()
        access_key = lines[0].strip()
        secret_key = lines[1].strip()
        upbit = pyupbit.Upbit(access_key, secret_key)
    
    return upbit

upbit = sec()

# -------------------------------------------함수 들 ---------------------------------------------

def get_target_price(coin,k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(coin, interval="day", count=2)   # 무조건 2이어야함
    time.sleep(0.06)

    target_price = round(int(df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k),-1)
    start_price = df.iloc[-1]['open']
    return target_price,start_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

# 상승장 일때만 매수, 하락장에서 매수해봐야 손해 
def get_ma(ticker,look_day):
    """15,7일 등 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=look_day)
    ma15 = round(df['close'].rolling(look_day).mean().iloc[-1],3)
    # print(ma15)
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


# 총 내 자산 조회
def total_my_assets():
    my_assets = 0
    # 개행해서 보기
    balances = upbit.get_balances()

    for balance in balances:
        if balance['currency'] == 'KRW':
            coin = 'KRW'
            my_assets += ast.literal_eval(balance['balance'])
        else:
            coin = 'KRW-' + balance['currency'] 
            now_price = get_current_price(coin)
            coin_assets = round(ast.literal_eval(balance['balance']) * now_price,2)
            my_assets += coin_assets
            earnings_rate = round(100 * (now_price - ast.literal_eval(balance['avg_buy_price'])) / now_price,2)

            msg = "코인:{}, 가격:{}원, 수익률:{}%".format(balance['currency'] ,coin_assets,earnings_rate)

            print(msg)
            post_message("#coin", msg)

    return round(my_assets,2)

