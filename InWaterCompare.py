import pandas as pd
import numpy as np

import plotly
import plotly.graph_objs as go
import plotly.offline as offline
'''
get reservoirs' assigned by reservoir, year list average inflow value
if value larger than average of past, print it out and skip adding it
分別讀取每年每個月的進水量平均資料，如果該月平均水量大於過去平均值(離群值)5倍，
則不進行統計。
'''
def average_year_value(path, item, year, reservoir):
    data = []
    sum_day = 31
    sub_day = [0, -3, 0, -1, 0, -1, 0, 0, -1, 0, -1, 0]  # sum_day + sub_day = month's days
    for i in range(len(reservoir)):
        data.append([])  # create list for each reservoir

    for yr in year:  # scan for each year

        file_name = path + item + str(yr) + ".csv"
        df = pd.read_csv(file_name)
        df.index = list(df["Unnamed: 0"])

        #df[df == 0] = np.nan
        df[df == -999.9] = np.nan  # ignore wrong data

        for num in range(len(reservoir)):  # scan for each reservoir
            days, count = 0, 0

            while(count < 12):
                next_days = days + sum_day + sub_day[count]
                value = df[reservoir[num]][days: next_days].mean()

                if(np.isnan(value)):
                    True
                elif(len(data[num]) < count + 1):  # has not been created month element
                    data[num].append(value)
                else:
                    if(value / 5 > data[num][count] and year.index(yr) > 3 and data[num][count] > 100):
                        print(reservoir[num], ":", yr, "/", count, "|", value, " | ", data[num][count],  " | ", int(value / data[num][count]), " times")

                    else:
                        data[num][count] += value
                        data[num][count] /= 2  # get average
                days = next_days
                count += 1  # month count

    return data

# # # main # # #
path = "./DATA_InWater/"
item = "In-Daily-"
year = list(np.arange(2003,2019))  # assign year list
reservoir_list = ["曾文水庫", "石門水庫", "翡翠水庫", "南化水庫", "日月潭水庫"]  # assign reservoirs

data = average_year_value(path, item , year, reservoir_list)  # get average data
layout = []
# create multiple plot and concat
for i in range(len(data)):
    trace = go.Scatter(x = np.arange(1,13), y = data[i], mode = "lines", name = reservoir_list[i])
    layout.append(trace)

offline.plot(layout, filename = "Bar Plot - In Water.html")  # output: HTML file
		

