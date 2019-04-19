import numpy as np
import pandas as pd
import csv

import plotly
import plotly.graph_objs as go
import plotly.offline as offline

'''
Water Storage Compare
根據路徑及檔案名稱，可以讀取水庫資料以得知各水庫的蓄水量狀況。

** reservoir: 代表是否回傳水庫名稱list **
'''

def search_data(path, file_name, date, reservoir):
    
    df = pd.read_csv(path + file_name)  # read file
    df.index = df["Unnamed: 0"]  # set date as DataFrame's index

    try:
        Capacity = list(df.loc[date][1:])  # get capacity / storage

    except BaseException:  # invalid date or other exception
        print("Error! Can not search the data.")
        return 0
    
    if(reservoir):
        reservoir_list = list(df.columns[1:])  # df.columns[0] is column name
        return Capacity, reservoir_list

    return Capacity

date = "2019-4-17"

current, reservoir_list = search_data("./DATA_CurrentCapacity/", "Current-Capacity-2019.csv", date, True)
total = search_storage("./DATA_SumCapacity/", "Sum-Capacity-2019.csv", date, False)

# # graphing # #

trace1 = go.Bar(  # Bar Graph
    x = reservoir_list,  #reservoir name
    y = current,  # storage value list
    name = "Current Water Storage"  # data name
)

trace2 = go.Bar(
    x = reservoir_list,
    y = total,
    name = "Total Capacity"
)

data = [trace1, trace2]

offline.plot(data, filename = "Bar Plot.html")  # output: HTML file

