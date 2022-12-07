# coding = utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

filepath = r"F:\Nighttime_Light\EX\Exper20210925\TX_google_MD.csv"
df = pd.read_csv(filepath)
date = df.columns.to_list()[2:]
# print((df[date[0]]+df[date[1]]+df[date[2]])/3)
n = 0
data = []
col = []
while (n <=len(date)-1):
    record = (df[date[n]] + df[date[n + 1]] + df[date[n + 2]] + df[date[n + 3]] + df[date[n + 4]] + df[date[n + 5]] + df[date[n + 6]]) / 7
    record = record.to_list()
    data.append(record)
    # print(date[n])
    col.append(date[n])
    n = n + 7
print(col)
data = pd.DataFrame(data).T
data.columns = col
print(data)
data.to_csv(r"F:\Nighttime_Light\EX\Exper20210925\weekly_TX_google_MD.csv")

# filepath = r"F:\Nighttime_Light\EX\Exper20210928\SS_weekly_Apple_md.csv"
# data = pd.read_csv(filepath)
# date = data.columns.to_list()[3:]
# print(date)
# df_1 = data[date[0]]
# df_2 = data[date[1]]
# df_3 = data[date[2]]
# df_4 = data[date[3]]
#
# n = 4
# ds =[]
# while n <= len(date) -1:
#     df = data[date[n]]
#     if n%4==0:
#         re = df-df_1
#     elif n%4 ==1:
#         re = df - df_2
#     elif n%4 ==2:
#         re = df - df_3
#     else:
#         re = df - df_4
#     ds.append(re.to_list())
#     n+=1
# DD = pd.DataFrame(ds).T
# DD.columns = date[4:]
# print(DD)
# DD.to_csv(r"F:\Nighttime_Light\EX\Exper20210928\S_weekly_apple_md.csv")