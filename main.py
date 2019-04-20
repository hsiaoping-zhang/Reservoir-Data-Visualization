import pandas as pd
import numpy as np

import fun_get_value
import fun_ploting

'''
單日的水庫有效蓄水量與總容量的長條圖比較
'''
date = "2019-4-17"
current, reservoir_list = fun_get_value.a_day_value("./DATA_CurrentCapacity/", "Current-Capacity-2019.csv", date, True, "float_point")
total = fun_get_value.a_day_value("./DATA_SumCapacity/", "Sum-Capacity-2019.csv", date, False, "floating_point")

fun_ploting.bar_plot(

	x = [reservoir_list, reservoir_list], 
	y = [current, total], 
    name= ["現在有效蓄水量", "有效總容量"], 
    title = "水庫水量與總容積比較",
    xaxis = "水庫", 
    yaxis = "水量(萬立方公尺)", 
    file_name = "Bar Plot-1"

)


''' Block 1
單個水庫多年的每 n 天平均蓄水量折線圖比較
'''
year = np.arange(2003,2019)  # assign year range
reservoir_name = "曾文水庫"  # assign reservoir
length = len(year)
n = 10
title = "(折線圖) : " + reservoir_name + " 每 " + str(n) + " 天蓄水量比較"
year_data, period = fun_get_value.n_days_value("./DATA_CurrentCapacity/", "Current-Capacity-", year, reservoir_name, n, "floating_point")

fun_ploting.line_plot(

	x = [period] * length, 
	y = year_data, 
	title = title, 
	xaxis = '日期(月/日)', 
	yaxis = '蓄水量(萬立方公尺)', 
	name = year, 
	file_name = "Line Plot-1"

)

''' Block 2
多個水庫的平均月進水量折線圖(在同一張圖) & 長條圖(多圖)比較
'''
path = "./DATA_InWater/"
item = "In-Daily-"
year = list(np.arange(2003,2019))  # assign year list
reservoir_list = ["曾文水庫", "石門水庫", "翡翠水庫", "南化水庫", "日月潭水庫"]  # assign reservoirs

data = fun_get_value.month_value(path, item , year, reservoir_list, "floating_point")  # get average data

# line plot which all reservoirs in one graph
fun_ploting.line_plot(

	x = np.arange(1,13), 
	y = data, 
	name = reservoir_list, 
	title = "(折線圖) : 進水量(萬立方公尺)與月份比較", 
	xaxis = '時間(月)', 
	yaxis = '水量(萬立方公尺)', 
	file_name = "Line Plot-2"

)

row = int(len(reservoir_list) / 3 + 0.5)
column = int(len(reservoir_list) / row + 0.5)
title = '(折線圖) : 各水庫進水量(萬立方公尺)與月份比較'
length = len(data)

# bar subplot which each reservoir in a graph
fun_ploting.sub_plot(

	x = np.arange(1,13), 
	y = data, 
	name = reservoir_list,
	title = title, 
	xaxis = ['時間(月)']*length, 
	yaxis = ['水量(萬立方公尺)']*length, 
	row = row, 
	column = column,
	file_name = "SubPlot-1"

)

''' Block 3
單個水庫整年進水總量與出水總量的多圖(長條圖)呈現
'''
year_list = np.arange(2003,2019)
reservoir = "曾文水庫"
mean = fun_get_value.year_value("./DATA_InWater/", "In-Daily-", reservoir, year_list, "sum", "floating_point")
mean2 = fun_get_value.year_value("./DATA_OutWater/", "Out-Daily-", reservoir, year_list, "sum", "floating_point")
data = [mean, mean2]
length = len(data)
title = '(多圖比較) : ' + reservoir + ' 整年進 / 出水量(萬立方公尺) 呈現'

fun_ploting.sub_plot(

	x = year_list, 
	y = data, 
	name = ["進水量", "出水量"],
	title = title, 
	xaxis = ["年(西元)"] * length, 
	yaxis = ["水量(萬立方公尺)"] * length,
	row = 1, 
	column = 2,
	file_name = "Subplot-2"

)

