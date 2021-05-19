import numpy as np


# from pyupbit.exchange_api import Upbit
# from best_find_k import finding_best_k
# from preprocessing import make_percent_table, extraction_feature
from function import get_balance,get_current_price, sec
from slack import post_message



upbit = sec()


def buy_time(current_price, open_price, negative_feature, coin_name, buy_price_recode, target_price, ma15,positive_feature, my_price,jonbu_recode):
    krw = get_balance("KRW")
    if len(buy_price_recode) < 3:                                                                   # 하루에 3번 살 기회가 있음 
        if 'sudden_buy' not in buy_price_recode:  
            if current_price < open_price * (100 + negative_feature[-1])/100:
                if krw > my_price:                                          
                    buy_result = upbit.buy_market_order(coin_name, my_price*0.9995)       
                    if 'error' not in buy_result:
                        print("1급락장으로 코인 구매 {}".format(coin_name))
                        print(buy_result)   
                        buy_price_recode["sudden_buy"] = [current_price, my_price*0.9995/current_price]   # [급락장일때 산 가격, 산 코인수]
                        post_message("#coin", coin_name +': 1.급락장 코인 매수' +buy_price_recode["sudden_buy"])
                    else : 
                        print('buy_result')

        if 'sudden_mean_buy' not in buy_price_recode:  
            # 급락,저가 평균일때 삼
            if current_price < open_price * (100 + np.mean(negative_feature[-2] + negative_feature[-1]))/100:
                if krw > my_price:                                          
                    buy_result = upbit.buy_market_order(coin_name, my_price*0.9995)     
                    if 'error' not in buy_result:  
                        print("2급락장,저가 평균으로 코인 구매 {}".format(coin_name))
                        print(buy_result)   
                        buy_price_recode["sudden_mean_buy"] = [current_price, my_price*0.9995/current_price]
                        post_message("#coin", coin_name +': 2.급락 평균 코인 매수' +buy_price_recode["sudden_mean_buy"])
                    else:
                        print(buy_result)


        # 변동성 돌파전략으로 구매 (변동성이 감지되면 구매함) 
        if 'breaking_volatility' not in buy_price_recode:   
            if target_price < current_price: #and ma15 < current_price:   # 현재 가격이 목표가 이상이 되면 또한 현재 가격이 평균이동성 이상이면                             
                if krw > my_price:                                  
                    buy_result = upbit.buy_market_order(coin_name, my_price*0.9995)   
                    if 'error' not in buy_result:
                        print("3구매 코인 {} : {}".format(coin_name,my_price*0.9995 / current_price))
                        print(buy_result)   
                        buy_price_recode["breaking_volatility"] = [current_price, my_price*0.9995 / current_price]
                        print(buy_price_recode)
                        post_message("#coin", coin_name +': 3.변동성 돌파전략으로 매수' +buy_price_recode["breaking_volatility"])
                    else :
                        print(buy_result)
  

    print(coin_name,buy_price_recode)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------- 매도 -----------------------------------------------------------------------
    
    if len(buy_price_recode) != 0:
        if 'sudden_buy' in buy_price_recode:
            if current_price > buy_price_recode['sudden_buy'][0] * 1.02:     
                my_coin = buy_price_recode['sudden_buy'][-1]
                sell_result = upbit.sell_market_order(coin_name,my_coin*0.9995)
                if 'error' not in sell_result:
                    post_message("#coin", coin_name +': 급락 타이밍 매도(2%)' + buy_price_recode['sudden_buy'])
                    print('급락때 산거 매도')
                    del(buy_price_recode['sudden_buy'])

        elif 'sudden_mean_buy' in buy_price_recode:
            if current_price > buy_price_recode['sudden_mean_buy'][0] * 1.01:    
                my_coin = buy_price_recode['sudden_mean_buy'][-1]
                sell_result = upbit.sell_market_order(coin_name,my_coin*0.9995)
                if 'error' not in sell_result:
                    post_message("#coin", coin_name +': 급락 평균 타이밍 매도(1%)' + buy_price_recode['sudden_mean_buy'])
                    print('급락때 산거 매도 ')
                    del(buy_price_recode['sudden_mean_buy'])
  
        else :
            if open_price > ma15 : # 상승장
                if current_price > buy_price_recode['breaking_volatility'][0] * (100 + positive_feature[-2])/100:    
                    my_coin = buy_price_recode['breaking_volatility'][-1]
                    sell_result = upbit.sell_market_order(coin_name,my_coin*0.9995)
                    if 'error' not in sell_result:
                        post_message("#coin", coin_name +': 변동성에 사서 급등 매도')
                        print('급등으로 매도')
                        del(buy_price_recode['breaking_volatility'])
            else : # 하락장 
                if current_price > buy_price_recode['breaking_volatility'][0] * 1.01:    
                    my_coin = buy_price_recode['breaking_volatility'][-1]
                    sell_result = upbit.sell_market_order(coin_name,my_coin*0.9995)
                    if 'error' not in sell_result:
                        post_message("#coin", coin_name +': 하락장이여서 변동성에 사서 1% 이득')
                        print('하락장이여서 변동성에 사서 1% 이득')
                        del(buy_price_recode['breaking_volatility'])

    if len(jonbu_recode) != 0:
        if current_price > jonbu_recode["jonbu"][0] * 1.02:
            my_coin = jonbu_recode["jonbu"][1]
            sell_result = upbit.sell_market_order(coin_name,my_coin*0.9995)
            post_message("#coin", coin_name +': 존버탈출' + jonbu_recode["jonbu"])
            print('존버 탈출')
            del(jonbu_recode["jonbu"])


    return buy_price_recode,jonbu_recode



def sell_time(coin_name, buy_price_recode,my_price,jonbu_recode):                         # {'sudden_buy': [100, 49.975], 'sudden_mean_buy': [100, 49.975], 'breaking_volatility': [100, 49.975]}
    current_price = get_current_price(coin_name)
    my_coin = buy_price_recode["breaking_volatility"][-1]
    now_my_coin_price = my_coin * current_price     # 내가 산 코인 수 * 현재 가격
    print("bought_coin",my_coin)
    print("now_my_coin_price",now_my_coin_price)
    post_message("#coin", buy_price_recode)
    
    if now_my_coin_price > my_price * 1.01:   # 10000원 이상이되면 즉 이득이 되면 팜
        sell_result = upbit.sell_market_order(coin_name, my_coin*0.9995)      # 구매한 코인개수 그대로 팔기 
        if 'error' not in sell_result:
            post_message("#coin", coin_name +': 변동성 돌파전략 매도' +buy_price_recode["breaking_volatility"])
            del(buy_price_recode["breaking_volatility"])
            print('10,000원에 사서 {}원에 팜'.format(now_my_coin_price))
    
    else : 
        if 'jonbu' not in jonbu_recode:
            jonbu_recode["jonbu"] = buy_price_recode["breaking_volatility"]
            del(buy_price_recode["breaking_volatility"])
            post_message("#coin", coin_name +':존버')
        else:                       # 샀을때 가격[0]과 코인 개수[1] 
            b = jonbu_recode["jonbu"][1] + buy_price_recode["breaking_volatility"][1]
            a = (jonbu_recode["jonbu"][0] * jonbu_recode["jonbu"][1] + buy_price_recode["breaking_volatility"][0] * buy_price_recode["breaking_volatility"][1]) / (b)    
            jonbu_recode["jonbu"] = [a,b]       # [(코인 가격1 * 개수1 + 코인 가격2 * 개수2) / 개수1 + 개수2 , 
            del(buy_price_recode["breaking_volatility"])
            post_message("#coin", coin_name +':존버')




def buy_start_sell(coin_name,my_price,target_price,current_price):
    krw = get_balance("KRW")
    if krw > my_price:
        print("target_price",target_price)
        buy_result = upbit.buy_market_order(coin_name, my_price*0.9995) 
        if 'error' not in buy_result:  
            if target_price < current_price * 1.01 and target_price > current_price * 1.09 :    # 목표 매도가가 산시점에서 1%보다 작고 9% 크면
                target_price = round(int(current_price * 1.02),-1)                             # 2%에서 먹고 팔자  
            print("시작할때 사서 변동성일때 팔자 {} target {}".format(coin_name,str(target_price)))
            print(buy_result)  
            post_message("#coin", coin_name +': 시작할때 사서 변동성일때 팔자' + str(target_price))
            coin_num = upbit.get_balance(coin_name)
            print(current_price, target_price,coin_num)
            sell_limit_order = upbit.sell_limit_order(coin_name, target_price, coin_num*0.9995) # 매도가 걸기 
            print(sell_limit_order)
        else:
            print(buy_result)
            print('buy_start_sell에서 error 걸림')


def sell_fail(coin_name):
    uuid = upbit.get_order(coin_name)[0]["uuid"]    # 예약 매도 걸어둔거 실패하면
    upbit.cancel_order(uuid)                        # 거래 취소 
    coin_num = upbit.get_balance(coin_name)
    upbit.sell_market_order(coin_name, coin_num*0.9995) 

