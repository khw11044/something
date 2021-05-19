import time
import numpy as np
import pyupbit
import datetime

# from pyupbit.exchange_api import Upbit
from best_find_k import finding_best_k
from best_find_coin import investigate_all_coin
from preprocessing import make_percent_table, extraction_feature
from function import get_target_price,get_start_time,get_current_price, sec, total_my_assets
from timing import buy_time,sell_time,buy_start_sell,sell_fail
from slack import post_message

upbit = sec()


with open("coin.txt") as f:
    lines = f.readlines()
    coin_name1 = lines[0].strip()
    coin_name2 = lines[1].strip()
    coin_name3 = lines[2].strip()
    coin_name4 = lines[3].strip()

my_price = 5100
day_count = 14



ma_list = [5,10,15,20]

parameter_update_count = 0




# 자동매매 시작
print()
print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')
print("autotrade start")
post_message("#coin","autotrade start")
print('++++++++++++++++++++++++++++++++++++++++++++++++++++++')

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time(coin_name1)
        end_time = start_time + datetime.timedelta(days=1)
        print("parameter_update_count :",parameter_update_count)

# -------------------------------------------------------------------------------------

        if start_time < now < end_time - datetime.timedelta(seconds=30):
            if parameter_update_count == 0:
                parameter_update_count = 1
                post_message("#coin","today start")
                start_assets = total_my_assets()
                # k값과 이동평균 업데이트
                k1,best_ma1 = finding_best_k(coin_name1,day_count)                  # 0.1부터 0.9까지 지난 day_count동안 백테스팅한 결과 k
                k2,best_ma2 = finding_best_k(coin_name2,day_count)                  # 0.1부터 0.9까지 지난 day_count동안 백테스팅한 결과 k
                k3,best_ma3 = finding_best_k(coin_name3,day_count)                  # 0.1부터 0.9까지 지난 day_count동안 백테스팅한 결과 k
                k4,best_ma4 = finding_best_k(coin_name4,day_count)                  # 0.1부터 0.9까지 지난 day_count동안 백테스팅한 결과 k

                
                # coin1
                coin_table1 = pyupbit.get_ohlcv(coin_name1, interval="day", count=day_count)
                # 퍼센트표를 구함
                make_percent_table(coin_table1)
                # 종가평균, 고가평균,저가평균등등을 구함
                positive_feature1, negative_feature1 = extraction_feature(coin_table1)
                # 변동성돌파의 목표매수가, 시작가
                target_price1, open_price1 = get_target_price(coin_name1, k1)
                print(target_price1, open_price1)
                buy_price_recode1 = dict()
                jonbu_recode1 = dict()
                
                print('---------------------')

                # coin2
                coin_table2 = pyupbit.get_ohlcv(coin_name2, interval="day", count=day_count)
                make_percent_table(coin_table2)
                positive_feature2, negative_feature2 = extraction_feature(coin_table2)
                target_price2, open_price2 = get_target_price(coin_name2, k2)
                print(target_price2, open_price2)
                buy_price_recode2 = dict()
                jonbu_recode2 = dict()
                
                print('---------------------')

                # coin3
                coin_table3 = pyupbit.get_ohlcv(coin_name3, interval="day", count=day_count)
                make_percent_table(coin_table3)
                positive_feature3, negative_feature3 = extraction_feature(coin_table3)
                target_price3, open_price3 = get_target_price(coin_name3, k3)
                print(target_price3, open_price3)
                buy_price_recode3 = dict()
                jonbu_recode3 = dict()
                
                print('---------------------')

                # coin4
                coin_table4 = pyupbit.get_ohlcv(coin_name4, interval="day", count=day_count)
                make_percent_table(coin_table4)
                positive_feature4, negative_feature4 = extraction_feature(coin_table4)
                target_price4, open_price4 = get_target_price(coin_name4, k4)
                print(target_price4, open_price4)
                buy_price_recode4 = dict()
                jonbu_recode4 = dict()
                
                print('---------------------')

                top_10_coins = investigate_all_coin()
                print()
                print()
                print("선정된 코인 3개 :", top_10_coins)        # (코인 이름,[예상 수익률,목표 매도가, 현재가]

                coin_name5 = top_10_coins[0][0]
                target_price5, open_price5 = top_10_coins[0][-1][1:]
                current_price5 = get_current_price(coin_name5)
                buy_start_sell(coin_name5,my_price,target_price5,current_price5)    # 바로 사고 매도 예약 

                coin_name6 = top_10_coins[1][0]
                target_price6, open_price6 = top_10_coins[1][-1][1:]
                current_price6 = get_current_price(coin_name6)
                buy_start_sell(coin_name6,my_price,target_price6,current_price6)

                coin_name7 = top_10_coins[2][0]
                target_price7, open_price7 = top_10_coins[2][-1][1:]
                current_price7 = get_current_price(coin_name7)
                buy_start_sell(coin_name7,my_price,target_price7,current_price7)
                

                msg_coin_list = "오늘의 코인 :" + coin_name1 + coin_name2 + coin_name3 + coin_name4 + coin_name5 + coin_name6 + coin_name7 
                post_message("#coin", msg_coin_list)
                print()
                coin1_msg = "{}, target {}% 급등선 {}% 급락선 {}%".format(coin_name1,round(((target_price1-open_price1)/open_price1)*100,4),positive_feature1[-2],negative_feature1[-1])
                post_message("#coin", coin1_msg)
                coin2_msg = "{}, target {}% 급등선 {}% 급락선 {}%".format(coin_name2,round(((target_price2-open_price2)/open_price2)*100,4),positive_feature2[-2],negative_feature1[-1])
                post_message("#coin", coin2_msg)
                coin3_msg = "{}, target {}% 급등선 {}% 급락선 {}%".format(coin_name3,round(((target_price3-open_price3)/open_price3)*100,4),positive_feature3[-2],negative_feature1[-1])
                post_message("#coin", coin3_msg)
                coin4_msg = "{}, target {}% 급등선 {}% 급락선 {}%".format(coin_name4,round(((target_price4-open_price4)/open_price4)*100,4),positive_feature4[-2],negative_feature1[-1])
                post_message("#coin", coin4_msg)
                coin5_msg = "{}, target {}%".format(coin_name5,round(((target_price5-open_price5)/open_price5)*100,4))
                post_message("#coin", coin5_msg)
                coin6_msg = "{}, target {}%".format(coin_name6,round(((target_price6-open_price6)/open_price6)*100,4))
                post_message("#coin", coin6_msg)
                coin7_msg = "{}, target {}%".format(coin_name7,round(((target_price7-open_price7)/open_price7)*100,4))
                post_message("#coin", coin7_msg)

                
                
            
            # 현재 가격 
            current_price1 = get_current_price(coin_name1)
            current_price2 = get_current_price(coin_name2)
            current_price3 = get_current_price(coin_name3)
            current_price4 = get_current_price(coin_name4)

            

            print(target_price1, current_price1)
            print(target_price2, current_price2)
            print(target_price3, current_price3)
            print(target_price4, current_price4)


            print("{}, {}%, target {}% 급등선 {}% 급락선 {}%".format(coin_name1,round(((current_price1-open_price1)/open_price1)*100,4),round(((target_price1-open_price1)/open_price1)*100,4),positive_feature1[-2],negative_feature1[-1]))
            print("{}, {}%, target {}% 급등선 {}% 급락선 {}%".format(coin_name2,round(((current_price2-open_price2)/open_price2)*100,4),round(((target_price2-open_price2)/open_price2)*100,4),positive_feature2[-2],negative_feature2[-1]))
            print("{}, {}%, target {}% 급등선 {}% 급락선 {}%".format(coin_name3,round(((current_price3-open_price3)/open_price3)*100,4),round(((target_price3-open_price3)/open_price3)*100,4),positive_feature3[-2],negative_feature3[-1]))
            print("{}, {}%, target {}% 급등선 {}% 급락선 {}%".format(coin_name4,round(((current_price4-open_price4)/open_price4)*100,4),round(((target_price4-open_price4)/open_price4)*100,4),positive_feature4[-2],negative_feature4[-1]))

            
            print()
            print('------------------')
            
            buy_price_recode1,jonbu_recode1 = buy_time(current_price1, open_price1, negative_feature1, coin_name1, buy_price_recode1, target_price1, best_ma1, positive_feature1, my_price,jonbu_recode1)
            buy_price_recode2,jonbu_recode2 = buy_time(current_price2, open_price2, negative_feature2, coin_name2, buy_price_recode2, target_price2, best_ma2, positive_feature2, my_price,jonbu_recode2)
            buy_price_recode3,jonbu_recode3 = buy_time(current_price3, open_price3, negative_feature3, coin_name3, buy_price_recode3, target_price3, best_ma3, positive_feature3, my_price,jonbu_recode3)
            buy_price_recode4,jonbu_recode4 = buy_time(current_price4, open_price4, negative_feature4, coin_name4, buy_price_recode4, target_price4, best_ma4, positive_feature4, my_price,jonbu_recode4)

            print()
            print('---------다음---------')
        # ----------------------------------------- 변동성 돌파 전략 매도 --------------------------------------------------------------
        else:   # 종가 시간때에 
            current_assets = total_my_assets()
            msg = "시작 자산:{}원, 지금 자산:{}원, 수익률:{}%".format(start_assets ,current_assets,100*(current_assets - start_assets) / start_assets)
            post_message("#coin",msg)

            # 변동성 돌파전략으로 매수한것만 팜
            sell_time(coin_name1, buy_price_recode1,my_price,jonbu_recode1)
            sell_time(coin_name2, buy_price_recode2,my_price,jonbu_recode2)
            sell_time(coin_name3, buy_price_recode3,my_price,jonbu_recode3)
            sell_time(coin_name4, buy_price_recode4,my_price,jonbu_recode4)
          
            # 선정한 5개의 코인 시가에 사서 변동성지점에 매도하는것이 실패했다면 종가때 다 팜
            # sell_fail(coin_name5)
            # sell_fail(coin_name6)
            # sell_fail(coin_name7)

            parameter_update_count = 0
                
            
            
        time.sleep(1)
    except Exception as e:
        print(e)
        post_message("#coin", "try error" + str(e))
        time.sleep(1)