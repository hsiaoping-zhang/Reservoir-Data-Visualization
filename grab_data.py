import plotly
import plotly.graph_objs as go
import plotly.offline as offline

import numpy as np
import pandas as pd
import csv
import os

import crawler_function
import write_file

'''
透過從2003年到現在日期建立，可以向網頁求得各別每天的資料。

parameter: 
1) year_list: 透過這個年份的賦值，可以指定查詢的年份
2) date_index: 如果日期並不是連續，則可以調整這個 list

'''
url = "http://fhy.wra.gov.tw/ReservoirPage_2011/Statistics.aspx"  # 
table = pd.read_html(url)

total_reservoir = list(table[0][0][4:-1])
total_reservoir.remove("集集攔河堰")  # can not grab from the website
total_reservoir.remove('高屏溪攔河堰')  # can not grab from the website

table = table[0]
#print(table[table[0] == '鯉魚潭水庫'])

table.index = table[0]


year_list = np.arange(2019,2020)
sum_day = 31
sub_day = [0, -3, 0, -1, 0, -1, 0, 0, -1, 0, -1, 0]  # sum_day + sub_day = month's days

for year in range(len(year_list)):
    current_capacity, out, current_water = {}, {}, {}
    reservoir_dict_list = [current_capacity, out, current_water]  # data contains several columns' value
    date_index = []  # index for DataFrame
    
    for month in range(1,13):
        total = sum_day + sub_day[month-1]

        if(year_list[year] % 4 == 0 and month == 2):  # leap year
            total = total + 1

        for date in range(1, total + 1):

            date_index.append(str(year_list[year]) + "-" +  str(month) + "-" + str(date))
            date_list = [str(year_list[year]), str(month), str(date)]
            index_list = [4, 10]  # columns number which we want to get
            reservoir_dict_list = crawler_function.reservoir_data_search(date_list, reservoir_dict_list, total_reservoir, index_list)  #開始parse資料

            if(month == 4 and date == 17):
                break
        if(month == 4 and date == 17):
            break
    print("finish:", year_list[year])  # finish a year
    write_file.write_csv_file(reservoir_dict_list, len(index_list), date_index, year_list[year])  # write to csv file

#offline.plot(data)