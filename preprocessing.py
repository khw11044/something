
import numpy as np



# 퍼센트 테이블로 바꾸기
def make_percent_table(df):
    df['highest_per'] = round(((df.high - df.open)/df.open)*100,2)
    df['lowest_per'] = round(((df.low - df.open)/df.open)*100,2)
    df['close_per'] = round(((df.close - df.open)/df.open)*100,2)
    df['positive'] = df['close_per'] > 0
    # df['close_per'].plot(figsize=(5,5), kind='bar', color=df.positive.map({True: 'r', False: 'blue'}))
    

# 어제 고가, 어제 저가, 어제 종가, 어제 거래량   
# 비트코인, BTC

def extraction_feature(coin_table):
    high_per_list = list(coin_table["highest_per"])
    low_per_list = list(coin_table["lowest_per"])
    close_per_list = list(coin_table["close_per"])
    positive_list = list(coin_table['positive'])

    print("high_per_list",high_per_list)
    print("low_per_list",low_per_list)
    print('positive_list',positive_list)


    # 양봉 종가 평균
    positive_close_per_list = list([close_per_list[i] for i,k in enumerate(positive_list) if k is True])
    positive_close_per_list = np.array(positive_close_per_list)
    positive_close_per_list_mean = round(np.mean(positive_close_per_list),3)
    print('양봉 종가 평균(b) :',positive_close_per_list_mean)

    # 양봉 고가 평균
    positive_hight_per_list = list([high_per_list[i] for i,k in enumerate(positive_list) if k is True])
    positive_hight_per_list = np.array(positive_hight_per_list)
    positive_hight_per_list_mean = round(np.mean(positive_hight_per_list),3)
    print('양봉 고가 평균(g) :',positive_hight_per_list_mean)

    # 양봉 이상치 종가 평균
    positive_hightest_close_per_list = list([i for i in positive_close_per_list if i > positive_close_per_list_mean])
    positive_hightest_close_per_list = np.array(positive_hightest_close_per_list)
    positive_hightest_close_per_list_mean = round(np.mean(positive_hightest_close_per_list),3)
    print('양봉 이상치 종가 평균(y) :', positive_hightest_close_per_list_mean)

    # 양봉 이상치 고가 평균
    positive_hightest_high_per_list = list([i for i in positive_close_per_list if i > positive_hight_per_list_mean])
    positive_hightest_high_per_list = np.array(positive_hightest_high_per_list)
    positive_hightest_high_per_list_mean = round(np.mean(positive_hightest_high_per_list),3)
    print('양봉 이상치 고가 평균(k) :', positive_hightest_high_per_list_mean)

    # 양봉 종가 평균, 양봉 고가 평균, 양봉 이상치 종가 평균, 양봉 이상치 고가 평균
    positive_feature = [positive_close_per_list_mean, positive_hight_per_list_mean, positive_hightest_close_per_list_mean, positive_hightest_high_per_list_mean]


    # 음봉 종가 평균 
    negative_close_per_list = list([close_per_list[i] for i,k in enumerate(positive_list) if k is not True])
    negative_close_per_list = np.array(negative_close_per_list)
    negative_close_per_list_mean = round(np.mean(negative_close_per_list),3)
    print("음봉 종가 평균(r) :", negative_close_per_list_mean)

    # 음봉 저가 평균
    negative_low_per_list = list([low_per_list[i] for i,k in enumerate(low_per_list) if k is not True])
    negative_low_per_list = np.array(negative_low_per_list)
    negative_low_per_list_mean = round(np.mean(negative_low_per_list),3)
    print('음봉 저가 평균(g) :',negative_low_per_list_mean)


    # 음봉 이상치 종가 평균
    negative_lowest_close_per_list = list([i for i in negative_close_per_list if i < negative_close_per_list_mean])
    negative_lowest_close_per_list = np.array(negative_lowest_close_per_list)
    negative_lowest_close_per_list_mean = round(np.mean(negative_lowest_close_per_list),3)
    print("음봉 이상치 종가 평균(y) :", negative_lowest_close_per_list_mean)

    # 음봉 이상치 저가 평균
    negative_lowest_low_per_list = list([i for i in negative_close_per_list if i < negative_low_per_list_mean])
    negative_lowest_low_per_list = np.array(negative_lowest_low_per_list)
    negative_lowest_low_per_list_mean = round(np.mean(negative_lowest_low_per_list),3)
    print('음봉 이상치 저가 평균(k) :',negative_lowest_low_per_list_mean)

    # 음봉 종가 평균, 음봉 저가 평균, 음봉 이상치 종가 평균, 음봉 이상치 저가 평균
    negative_feature = [negative_close_per_list_mean,negative_low_per_list_mean,negative_lowest_close_per_list_mean,negative_lowest_low_per_list_mean]
    return positive_feature, negative_feature