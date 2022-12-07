# coding = utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import savgol_filter

# ## 数据表预处理
# filepath = r"H:\Region_Mobility_Report_CSVs\2021_US_Region_Mobility_Report.csv"
# dataset = pd.read_csv(filepath)
# data = pd.DataFrame(dataset)
# col = data.columns.tolist()
# col = col[2:4] + col[8:]
# df = []
# for i in range(data.shape[0]):
#     x = data.iloc[i]
#     if x['sub_region_1'] == "Texas":
#         df.append(x)
#     else:
#         pass
# df = pd.DataFrame(df, columns=col)
# df.fillna(0)
# df.to_csv(r"F:\Nighttime_Light\EX\Exper20210928\2021_Google_NY_MD.csv", index=False)
# print(df)
#
# ## 数据表重组
# file = r"F:\Nighttime_Light\EX\Exper20210928\2021_Google_NY_MD.csv"
# data = pd.read_csv(file)
# df = pd.DataFrame(data)
# df.fillna("A", inplace=True)
#
# ## 提取数据起止时间
# dtime = df["date"].tolist()
# new_dtime = []
# for g in range(len(dtime)):
#     da = dtime[g]
#     if da in new_dtime:
#         pass
#     else:
#         new_dtime.append(da)
#
# ## 获取数据所属County
# county_df = []
# for i in range(df.shape[0]):
#     x = df.iloc[i]
#     if x['sub_region_2'] == "A":
#         pass
#     else:
#         county_df.append(x)
# C_df = pd.DataFrame(county_df)
# county = C_df["sub_region_2"].tolist()
# new_county_list = []
# for j in range(len(county)):
#     a = county[j]
#     if a in new_county_list:
#         pass
#     else:
#         new_county_list.append(a)
#
# ## 按照场所分类
# FRAME = []
# for f in range(len(new_county_list)):
#     FRAME.append([])
# for e in range(len(new_county_list)):
#     for h in range(df.shape[0]):
#         record = df.iloc[h]
#         if record["sub_region_2"] == new_county_list[e]:
#             FRAME[e].append(record)
#         else:
#             pass
#     r = pd.DataFrame(FRAME[e])
#     outdir = r"F:\Nighttime_Light\EX\Exper20210928\TX_MD"
#     csvname = "2021_"+new_county_list[e] + ".csv"
#     out = os.path.join(outdir, csvname)
#     r.to_csv(out, index=False)
#     print(csvname + "输出完毕")

## 补充缺失值
file = r"F:\Nighttime_Light\EX\Exper20210925\CA_google_MD.csv"
df = pd.DataFrame(pd.read_csv(file))
col = df.columns.to_list()
df.fillna(0, inplace=True)
# print(data)

def weekly_mobility_index(x, y):
    n = 0
    z_list = []
    while n < len(x):
        a = x[n:n + 7]
        b = y[n:n + 7]
        z = np.trapz(b, a)
        z_list.append(z)
        n += 7
        # print(z)
    # plt.plot(np.arange(54), z_list, color="black")
    return z_list

S1 = []
for i in range(df.shape[0]):
    x = np.arange(len(col[2:])).tolist()
    y = df.iloc[i].to_list()[2:]
    s = weekly_mobility_index(x, y)
    S1.append(s)
# plt.show()

data_new = pd.DataFrame(S1)
clist = pd.DataFrame(pd.read_csv(file),columns=["County","date"])
df_new2 = pd.concat([clist.T,data_new.T])
new_col = ["County","date"]
i = 0
while i < len(col[2:]):
    col_n = col[2:][i]
    new_col.append(col_n)
    i +=7
df2 = df_new2.T
df2.columns = new_col

l = []
for m in range(df2.shape[0]):
    count = 0
    z_record = df2.iloc[m].to_list()[1:]
    for n in range(len(z_record)):
        if z_record[n] == 0:
            count += 1
        else:
            pass
    if count > len(z_record)/3:
        l.append(m)
    else:
        pass
df2 = df2.drop(labels=l,axis=0)
print(df2)
df2.to_csv(r"F:\Nighttime_Light\EX\Exper20210925\[new]CA_google_MD.csv",index = False)



# file = r"F:\Nighttime_Light\EX\小论文\移动数据\Google\County_count\class\grocery_and_pharmacy.csv"
# df = pd.DataFrame(pd.read_csv(file))
# print(df)
# df.fillna(0,inplace=True)
# plt.rcParams['font.sans-serif'] = ['SimHei']  # 步骤一（替换sans-serif字体）
# plt.rcParams['axes.unicode_minus'] = False  # 步骤二（解决坐标轴负数的负号显示问题）
# date = df.columns.to_list()[1:]
#
# for i in range(df.shape[0]):
#     x = df.iloc[i][1:].tolist()
#     plt.plot(date, x, color="grey")
#
# def sg_filter(L):
#     for i in range(len(L)):
#         pre_list = np.array(L)
#         np.set_printoptions(precision=8)
#         sg_result = savgol_filter(pre_list, 7, 3)
#         sg_result_list = sg_result.tolist()
#     return sg_result_list
#
#
# x_avg = []
# for j in range(0, len(date)):
#     xx = df[str(date[j])].tolist()
#     if xx is None:
#         avg = 0
#     else:
#         avg = np.sum(xx)
#     x_avg.append(avg)
# y = sg_filter(x_avg)
# print(y)
# # print(x_avg)
#
# # plt.ylabel("出行距离（以2020.01.13基准量")
# plt.xticks(range(0,len(date),7), rotation=45)
#
# plt.plot(date, y, color="red")
# # plt.title("Transit")
# plt.show()
