# 臺灣水庫歷年資料視覺化 Reservoir Data Visiualization
[成果說明 PPT](https://drive.google.com/drive/folders/196guVduKk8WaOCXxMpmbkQN3FJhBzKoh?usp=sharing)  
[Plotly 圖表呈現](https://swboezezb8hx4zw2kranbq-on.drv.tw/Website/reservoir_representation.html)  

## 網頁爬蟲  
透過 `crawler_function.py` 和 `write_file.py` 兩個檔案，可以將水庫資料網站上的每天資料爬蟲下來，寫成 csv 檔，讓以後讀取資料較為方便。  
> 主程式為 : `grab_data.py` ，更多詳細說明在 : [HaackMD筆記](https://hackmd.io/s/r14Ut5bFE)  


### crawler_function.py  
**FUNCTION :**
- `find_value(name, web)`  
Search for a certain value (ex: *__VIEWSTATE*)  
在 web 內容裡找到特定的 value 值  

- `table_data_management(table, reservoir_dict_list, total_reservoir, index)`  
Manage DataFrame, get values from assigned columns, and return them.  
處理DataFrame type的資料，並從 index list 當中獲得要存取的欄位，加到reservoir_dict_list當中 
(由不同欄位資料的dictionary組成的list type)，並回傳。

- `reservoir_data_search(date, reservoir_dict_list, total_reservoir, index)`  
Get *__EVENTTARGET* 's and *__VIEWSTATE* 's value by using `find_value` function, and request to website using POST.  
先用 GET 的方式存取到兩個參數的值，用 POST 方式放入參數向網頁抓取資料。  

### write_file.py  
**FUNCTION :**
- `write_csv_file(reservoir_dict_list, length, date_index, year)`  
Write DataFrame to csv file.  
寫檔。  

## 資料視覺化  
把歷年的水庫水位資料從網站上取得後，有別於政府開放資料只提供即時資料，利用這份 project 可以透過將資料視覺化的過程，顯示單個或多個水庫在一段期間當中的水位變化，以及是否擁有季節性的水位規律。  

### fun_get_value.py
內有取得單日、每 n 日、每月、每年的 function 定義，可供 main 程式碼呼叫。  

**FUNCTION :**
- `a_day_value(path, file_name, date, reservoir, string)`  
Get one day's value with all type data from all reservoirs. ( if data is percentage : sting="percentage" )  
獲得單日資料，如果是百分比資料，則用 string = "percentage" 去掉 "%"  

- `n_days_value(path, filename, year, reservoir_name, days, string)`  
Read data and select every n(=days) days as a data point.  
讀入資料以每 n 天的平均值當作新的資料點，通常用於看整年每 n 天 (n < 31) 的資料趨勢  

- `month_value(path, filename, year, reservoir, string)`  
Get average month's value of assigned years.  
(if value is 5 times larger than average of past, print it out and skip adding it)  
分別讀取每年每個月的進水量平均資料，如果該月平均水量大於過去平均值 (判定為離群值) 5 倍，則不進行統計。  

- `year_value(path, file, reservoir_name, year_list, compute, string)`  
total or average waterflow of each year  
依據每年的總/平均水量計算

- `add_row_column(num, upper_bound)`  
Add number (normal situation) or return to 1 (number is up to upper_bound)  

- `period_list(days, year)`  
Use days to compute date points of every period.  
根據 days (日期間隔) 和 year (年份)，得到每段期間的日期點，作為作圖的 x 軸參考。  

### fun_ploting.py  
畫出長條圖、折線圖或多圖呈現的 function 定義，可供 main 程式碼呼叫。  

**FUNCTION :**
- `bar_plot(x, y, name, title, xaxis, yaxis, file_name)` 長條圖  

- `line_plot(x, y, name, title, xaxis, yaxis, file_name)` 折線圖  

- `sub_plot(x, y, name, title, xaxis, yaxis, file_name, row, column)` 多圖呈現  


### main.py
有四個主要程式碼區快的展現，分別為：

1. **單日**的水庫有效蓄水量與總容量的長條圖比較  
2. 單個水庫多年的**每 n 天**平均蓄水量折線圖比較
3. 多個水庫的平均**月**進水量折線圖(在同一張圖) & 長條圖(多圖)比較  
4. 單個水庫**整年**進水總量與出水總量的多圖(長條圖)呈現  

#### Block 1 單日 sample 成果  
[網頁呈現 website view - Plotly](https://swboezezb8hx4zw2kranbq-on.drv.tw/Reservoir/Bar%20Plot-1.html)
![image](https://github.com/hsiaoping-zhang/Reservoir_DataVisiualization/blob/master/example_graph%20%E5%9C%96%E8%A1%A8/bar_plot(a%20day).png)

根據指定日期比較單日資料之間的差異(ex: 現在蓄水量 / 有效總蓄水量)

#### Block 2 每 n 日 sample 成果  
[網頁呈現 website view - Plotly](https://swboezezb8hx4zw2kranbq-on.drv.tw/Reservoir/Line%20Plot-1.html)
![image](https://github.com/hsiaoping-zhang/Reservoir_DataVisiualization/blob/master/example_graph%20%E5%9C%96%E8%A1%A8/line_plot(n%20days).png)
曾文水庫多年的每 10 天平均蓄水量折線圖比較  

#### Block 3 每個月 sample 成果  
[網頁呈現 website view - Plotly](https://swboezezb8hx4zw2kranbq-on.drv.tw/Reservoir/Line%20Plot-2.html)
![image](https://github.com/hsiaoping-zhang/Reservoir_DataVisiualization/blob/master/example_graph%20%E5%9C%96%E8%A1%A8/line_plot(month).png)  
多個水庫的平均月進水量折線圖**在同一張圖**比較  

##### 每個月的 subplot 圖成果  
[網頁呈現 website view - Plotly](https://swboezezb8hx4zw2kranbq-on.drv.tw/Reservoir/SubPlot-1.html)
![image](https://github.com/hsiaoping-zhang/Reservoir_DataVisiualization/blob/master/example_graph%20%E5%9C%96%E8%A1%A8/subplots(month).png)  
多個水庫的平均月進水量長條圖**多圖**比較  

#### Block 4 每年 sample 成果  
[網頁呈現 website view - Plotly](https://swboezezb8hx4zw2kranbq-on.drv.tw/Reservoir/Subplot-2.html)
![image](https://github.com/hsiaoping-zhang/Reservoir_DataVisiualization/blob/master/example_graph%20%E5%9C%96%E8%A1%A8/subplots(year).png)
曾文水庫整年進水總量與出水總量的兩圖(長條圖)呈現  
