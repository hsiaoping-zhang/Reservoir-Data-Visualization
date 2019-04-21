import pandas as pd
import numpy as np

import plotly
import plotly.graph_objs as go
import plotly.offline as offline

'''
get one day's value with all type data from all reservoirs(if data is percentage : sting="percentage")
獲得單日資料，如果是百分比資料，則用string="percentage"去掉"%"

- parameter:
path(str): file folder
file_name(str): file name without year infomation(ex: "percentage-" or "In-Daily-")
date(str): assigned date(ex: "2019-4-7")
reservoir(bool): whether return reservoir list
string(str): data type in finding files("percentage", "floating_point")
'''
def a_day_value(path, file_name, date, reservoir, string):
    
    df = pd.read_csv(path + file_name)  # read file
    df.index = df["Unnamed: 0"]  # set date as DataFrame's index

    try:
        Capacity = list(df.loc[date][1:])  # get capacity / storage

    except BaseException:  # invalid date or other exception
        print("Error! Can not search the data.")
        return 0

    if(string == "percentage"):  # if data is percentage
        Capacity = percent_to_num(Capacity)
    
    if(reservoir):
        reservoir_list = list(df.columns[1:])  # df.columns[0] is column name
        return Capacity, reservoir_list

    return Capacity

'''
read data and select every n(=days) days as a data point
讀入資料以每 n 天的平均值當作新的資料點，通常用於看整年每 n 天(n < 31)的資料趨勢

- parameter:
path(str): file folder
filename(str): file name without year infomation(ex: "percentage-" or "In-Daily-")
year(list[int]): assigned years
reservoir_name(str): a reservoir name
days(int): date period
string(str): data type in finding files("percentage", "floating_point")
'''
def n_days_value(path, filename, year, reservoir_name, days, string):

    year_data = []
    period = period_list(days,2015)

    for yr in year:

        past_data = []
        file_name = path + filename + str(yr) + ".csv"
        df = pd.read_csv(file_name)
        df.index = list(df["Unnamed: 0"])

        # # # scan for each day to get every n days data # # #

        day = 1  # count for n days
        while(day < df.shape[0]):
            week_day, sum_data, total_day = 0, 0, 0

            # # every n(=days) days, average values # #
            isString = True
            while(week_day != days and day < df.shape[0]):
                data = df.iloc[day][reservoir_name]  # date data

                if(string == "percentage" and type(data) == str):  # value is valid(ex: "XX.xx%")
                    data = data.replace("%", "")

                elif(string != "percentage" and string != "floating_point"):
                    isString = False
                    print("string is a wrong assignment.")
                    return np.nan, np.nan
                # if data = nan, skip it
                sum_data += float(data)
                total_day += 1
                week_day += 1
                day += 1

            if(total_day):  # total legal days
                avg_data = sum_data / total_day
                past_data.append(avg_data)
            else:
                past_data.append("NULL")

        year_data.append(past_data)
    return year_data, period

'''
get average month's value of assigned years 
(if value is 5 times larger than average of past, print it out and skip adding it)
分別讀取每年每個月的進水量平均資料，如果該月平均水量大於過去平均值(判定為離群值)5倍，則不進行統計。

- parameter:
path(str): file folder
filename(str): file name without year infomation(ex: "percentage-" or "In-Daily-")
year(list[int]): list of assigned years
reservoir(list[str]): list of reservoirs' name
string(str): data type in finding files("percentage", "floating_point")
'''
def month_value(path, filename, year, reservoir, string):
    data = []
    sum_day = 31
    sub_day = [0, -3, 0, -1, 0, -1, 0, 0, -1, 0, -1, 0]  # sum_day + sub_day = month's days
    for i in range(len(reservoir)):
        data.append([])  # create list for each reservoir

    for yr in year:  # scan for each year

        file_name = path + filename + str(yr) + ".csv"
        df = pd.read_csv(file_name)
        df.index = list(df["Unnamed: 0"])

        df[df == -999.9] = np.nan  # ignore wrong data
        df[df == 0] = np.nan

        for num in range(len(reservoir)):  # scan for each reservoir
            days, count = 0, 0

            while(count < 12):
                next_days = days + sum_day + sub_day[count]

                if(string == "percentage"):
                    value = percent_to_num(df[reservoir[num]][days: next_days]).mean()
                else:
                    value = df[reservoir[num]][days: next_days].mean()

                if(np.isnan(value)):
                    True
                elif(len(data[num]) < count + 1):  # has not been created month element
                    data[num].append(value)
                else:
                    if(value / 5 > data[num][count] and year.index(yr) > 3 and data[num][count] > 100):
                        print(reservoir[num], ":", yr, "/", count + 1, "|", value, " | ", data[num][count],  " | ", int(value / data[num][count]), " times")

                    else:
                        data[num][count] += value
                        data[num][count] /= 2  # get average
                days = next_days
                count += 1  # month count

    return data


'''
total or average waterflow of each year
依據每年的總/平均水量計算

- parameter:
path(str): file folder
filename(str): file name without year infomation(ex: "percentage-" or "In-Daily-")
year(list[int]): list of assigned years
reservoir(str): list of reservoirs' name
string(str): data type in finding files("percentage", "floating_point")
'''
def year_value(path, file, reservoir_name, year_list, compute, string):   
    build, mean = False, []
    for year in range(len(year_list)):
        file_name = path  + file + str(year_list[year]) + ".csv"
        water = pd.read_csv(file_name)
        
        water[water == 0] = np.nan
        water[water == -999.9] = np.nan  # it might be a wrong data
        
        water2 = water[reservoir_name]

        if(string == "percentage"):
            water2 = pd.Series(percent_to_num(list(water2)))  # convert to list and return to series

        if(compute == "sum"):
            mean.append(water2.sum(0))  # y direction
        else:
            mean.append(water2.mean(0))

    return mean

def add_row_column(num, upper_bound):
    if(num == upper_bound):
        return 1
    else:
        return num + 1

'''
using days to compute date points of every period
根據 days(日期間隔) 和 year(年份)，得到每段期間的日期點，作為作圖的 x 軸參考。

- parameter:
days(int): period of counting days
year(int): assigned year
'''
def period_list(days, year):
    period = []
    month_day, current, month, sum_day = 31, 0, 1, 31
    sub_day = [0, -3, 0, -1, 0, -1, 0, 0, -1, 0, -1, 0]  # sum_day + sub_day = month's days
    flag = False
    while(1):
        current += days
        while(current > month_day):
            current -= month_day
            month += 1
            if(month > 12):  # over 365(/366)days
                flag = True
                break
            if(year % 4 == 0 and month == 2):
                month_day = 29
            else:
                month_day = 31 + sub_day[month - 1]
        if(flag):
            break
        date = str(month) + "/" + str(current)  # date format
        period.append(date)

    if(flag):  # remaining days
        period.append("12/31")

    return period

'''
remove char % from each data, if data is nan, ignore
移除掉每筆資料上的 % 

- parameter:
data(list[str]): list of data with "%"
'''
def percent_to_num(data):

    for num in range(len(data)):
        if(type(data[num]) == str):  # if data is nan, type(data) is float
            data[num] = float(data[num].replace("%", ""))
    return data