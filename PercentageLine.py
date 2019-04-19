import pandas as pd
import numpy as np

import plotly
import plotly.graph_objs as go
import plotly.offline as offline

'''
Read every year data from csv file and select the certain reservoir data.
從水庫百分比資料(percentage-20XX.csv)獲取資料，並以每七天為單位計算平均百分比，
最後將百分比趨勢以折線圖呈現。
'''
def get_percentage(year, reservoir_name):

    percentage_path = "./DATA_Percentage/"
    year_data = []

    for yr in year:

        past_data = []
        file_name = percentage_path + "percentage-" + str(yr) + ".csv"
        df = pd.read_csv(file_name)
        df.index = list(df["Unnamed: 0"])

        # # # scan for each day to get every week data # # #

        day = 1  # count for week days
        while(day < df.shape[0]):
            week_day, sum_data, total_day = 0, 0, 0

            ## every 7 days, average values ##
            while(week_day != 7 and day < df.shape[0]):
                data = df.iloc[day][reservoir_name]  # date data

                if(type(data) == str):  # value is valid(ex: "XX.xx%")
                    data = data.replace("%", "")
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
    return year_data

'''
根據year_data畫成許多年可相比的折線圖(單一水庫)
'''
def plot_line_graph(year_data):

    layout = []
    # # create line for every year # #
    for yr in year:
        trace = go.Scatter(
            x = np.arange(1, len(year_data[yr - 2003])),  # number of weeks
            y = year_data[yr - 2003],  # year data
            mode = 'lines',
            name = str(yr)  # year name
        )
        layout.append(trace)

    offline.plot(layout, filename = "Line Plot.html")  # output: HTML file

# # # main # # #
year = np.arange(2003,2019)  # assign year range
reservoir_name = "曾文水庫"  # assign reservoir
year_data = get_percentage(year, reservoir_name)
plot_line_graph(year_data)

