import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup

import re
from io import StringIO
'''
這個函式會找特定的 value ，如「__VIEWSTATE」等
'''
def find_value(name, web):
    reg = 'name="' + name + '".+value="(.*)" />'
    pattern = re.compile(reg)
    result  = pattern.findall(web.text)
    try:
        return result[0]
    except:
        return ""

'''
處理DataFrame type的資料，並從index list當中獲得要存取的欄位，
加到reservoir_dict_list當中(由不同欄位資料的dictionary組成的list type)，並回傳
'''
def table_data_management(table, reservoir_dict_list, total_reservoir, index):
    table.index = table[0]  # set column 1 values to be index
    
    for num in range(len(index)):  # scan for each value we want to get(capacity, percentage...)
        for item in total_reservoir:
            value = table.at[item, index[num]]  # access value by reservoir name and column number
            
            try:
                value = float(value)  # try to convert value from string type to float

            except BaseException:  # exception: "--" or "XX.xx%"
            
                if("%" in value):  # percentage case
                    value = float(value.replace("%", ""))  # remove char %
                else:
                    value = "NULL"  # nan case
                    
            if(item in list(reservoir_dict_list[num].keys())):  # dict[item] has been created
                reservoir_dict_list[num][item].append(value)
            else:  # dict[item] has not been created
                reservoir_dict_list[num][item] = [] # creat a list container
                reservoir_dict_list[num][item].append(value)
                
    return reservoir_dict_list

'''
因為這個網頁進行爬蟲時，需要 __EVENTTARGET 和 __VIEWSTATE 兩個參數才能順利獲得查詢資料，
而兩個參數會隨每天而有所不同，因此必須先用 GET 的方式存取到兩個參數的值，
接著建立參數們，放入剛剛抓取到的驗證碼及查詢時間格式，
用 POST 方式向網頁抓取資料，最後藉著得到的網頁資訊進行資料的提取。
'''
def reservoir_data_search(date, reservoir_dict_list, total_reservoir, index):
    # open browser
    ses = requests.Session()

    # enter the website
    d = ses.get('http://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx')
    
    # parameter list
    load_list = [find_value("__EVENTTARGET", d), find_value("__VIEWSTATE", d)]
    if(date[2] == "1"):  # just take a look at schedule
        print("yy/mm/dd:", date)
    
    # website request needs POST parameter
    payload = {
        "__EVENTTARGET": load_list[0],
        "__VIEWSTATE": load_list[1],
        'ctl00$cphMain$cboSearch': "所有水庫",
        'ctl00$cphMain$ucDate$cboYear': date[0],
        'ctl00$cphMain$ucDate$cboMonth': date[1],
        'ctl00$cphMain$ucDate$cboDay': date[2],

    }
    # request to website using POST
    res = requests.post("http://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx", data = payload)
    # manage table data
    reservoir_dict_list = table_data_management(pd.read_html(res.text)[0], reservoir_dict_list, total_reservoir, index)
    
    return reservoir_dict_list