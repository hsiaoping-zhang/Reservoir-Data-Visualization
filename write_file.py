import pandas as pd
import numpy as np
import csv
'''
從 dict_list 當中一個個提取欄位的 dictionary，並寫成 csv 檔

parameter:
1) name: 可以自己安排寫檔的名稱

'''
def write_csv_file(dict_list, length, date_index, year):
    name = ["In-Daily"]

    for index in range(length):
        final = {}
        for i in reservoir_dict_list[index]:  # check for total data length
            if(len(reservoir_dict_list[index][i]) == len(reservoir_dict_list[index]['石門水庫'])):
                final[i] = reservoir_dict_list[index][i]
        df = pd.DataFrame(final, index = date_index)
        file = name[index] + "-" + str(year) +".csv"  # file name
        df.to_csv(file, encoding="utf_8_sig")  # maintain Chinese word(or they might become garbled)