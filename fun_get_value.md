# function 定義 ( fun_get_value.py )  
內有取得單日、每 n 日、每月、每年的 function 定義，當 py 檔裡 `import fun_get_value` 即可供程式碼呼叫。  
return 的型態都是 list 型別 (除了 `add_row_column` 和 `period_list`)，會根據有多少年或多少水庫的資料而長度有所變化。  

## **FUNCTION :**  

#### `a_day_value(path, file_name, date, reservoir, string)` :  

Get one day's value with all type data from all reservoirs. ( if data is percentage : sting="percentage" )  
獲得單日資料，如果是百分比資料，則用 string = "percentage" 去掉 "%"  

> parameter:  
path (str) : file folder  
file_name (str) : file name without year infomation(ex: "percentage-" or "In-Daily-")  
date (str) : assigned date(ex: "2019-4-7")  
reservoir (bool) : whether return reservoir list  
string (str) : data type in finding files("percentage", "floating_point")  
<hr>

#### `n_days_value(path, filename, year, reservoir_name, days, string)` :  

Read data and select every n(=days) days as a data point.  
讀入資料以每 n 天的平均值當作新的資料點，通常用於看整年每 n 天 (n < 31) 的資料趨勢  

> parameter:  
path (str) : file folder  
filename (str) : file name without year infomation(ex: "percentage-" or "In-Daily-")  
year (list[int]) : assigned years  
reservoir_name (str) : a reservoir name  
days (int) : date period  
string (str) : data type in finding files("percentage", "floating_point")  
<hr>

#### `month_value(path, filename, year, reservoir, string)` :  

Get average month's value of assigned years.  
(if value is 5 times larger than average of past, print it out and skip adding it)  
分別讀取每年每個月的進水量平均資料，如果該月平均水量大於過去平均值 (判定為離群值) 5 倍，則不進行統計。  

> parameter:  
path (str) : file folder  
filename (str) : file name without year infomation(ex: "percentage-" or "In-Daily-")  
year (list[int]) : list of assigned years  
reservoir (list[str]) : list of reservoirs' name  
string (str) : data type in finding files("percentage", "floating_point")  
<hr>


#### `year_value(path, file, reservoir_name, year_list, compute, string)` :  

total or average waterflow of each year
依據每年的總/平均水量計算

> parameter:  
path (str) : file folder  
filename (str) : file name without year infomation (ex: "percentage-" or "In-Daily-")  
year (list[int]) : list of assigned years  
reservoir (list[str]) : list of reservoirs' name  
string (str) : data type in finding files("percentage", "floating_point")  
<hr>


#### `add_row_column(num, upper_bound)` :  

Add number (normal situation) or return to 1 (number is up to upper_bound)  

> parameter:  
num (int) : number  
upper_bound (int) : the upper bound number  
<hr>


#### `period_list(days, year)` :  

Use days to compute date points of every period.  
根據 days (日期間隔) 和 year (年份)，得到每段期間的日期點，作為作圖的 x 軸參考。  

> parameter:  
days (int) : period of counting days  
year (int) : assigned year  
