import numpy as np
import pandas as pd
import csv

import plotly
import plotly.graph_objs as go
import plotly.offline as offline
from plotly import tools  # for subplot

from fun_get_value import add_row_column

'''
Bar Graph 長條圖

- parameter:
x(list): list of x value
y(list): list of y value
name(list[str]): each data's name
title(str): graph's title
xaxis(str): name of x-axis
yaxis(str): name of y-axis
file_name(str): file name
'''
def bar_plot(x, y, name, title, xaxis, yaxis, file_name):
    data = []
    for i in range(len(name)):
        trace = go.Bar(x = x[i], y = y[i], name = name[i])
        data.append(trace)

    layout = go.Layout(title = title, xaxis = dict(title = xaxis), yaxis = dict(title = yaxis))
    fig = go.Figure(data = data, layout = layout)
    offline.plot(fig, filename = file_name + ".html")  # output: HTML file


'''
Line Graph 折線圖

- parameter:
x(list): list of x value
y(list): list of y value
name(list[str]): each data's name
title(str): graph's title
xaxis(str): name of x-axis
yaxis(str): name of y-axis
file_name(str): file name
'''
def line_plot(x, y, name, title, xaxis, yaxis, file_name):
    data = []
    # create multiple plot and concat
    for i in range(len(name)):
        trace = go.Scatter(x = x[i], y = y[i], mode = "lines", name = name[i])
        data.append(trace)

    layout = go.Layout(title = title, xaxis = dict(title = xaxis), yaxis = dict(title = yaxis))
    fig = go.Figure(data = data, layout = layout)
    offline.plot(fig, filename = file_name + ".html")  # output: HTML file

'''
Subplots 多圖呈現(長條圖)
根據送進來的資料，依照順序(由左到右、由上到下)輸出多圖，可供不同水庫間的資料比較。

- parameter:
x(list): list of x value
y(list): list of y value
name(list[str]): each data's name
title(str): graph's title
xaxis(list[str]): list of name of x-axis
yaxis(list[str]): list of name of y-axis
file_name(str): file name
row(int): number of subplot rows
column(int): number of subplot columns
'''
def sub_plot(x, y, name, title, xaxis, yaxis, file_name, row, column):
    
    fig = tools.make_subplots(rows = row, cols = column, subplot_titles = name)
    i, j = 1, 1
    for num in range(len(name)):
        tmp = go.Bar(x = x, y = y[num], name = name[num])  # a subplot
        fig.append_trace(tmp, i, j)
        fig['layout']['xaxis' + str(column*(i-1)+j)].update(title = xaxis[num])  # x-axis title
        fig['layout']['yaxis' + str(column*(i-1)+j)].update(title = yaxis[num])  # y-axis title
        # control subplot i and j position # 
        if(j == column):
            i, j = add_row_column(i, row), add_row_column(j, column)
        else:
            j = add_row_column(j, column)

    fig['layout'].update(title = title)
    offline.plot(fig, filename = file_name + ".html")


